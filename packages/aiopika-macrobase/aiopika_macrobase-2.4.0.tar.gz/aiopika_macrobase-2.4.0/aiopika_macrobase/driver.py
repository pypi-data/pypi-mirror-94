import os
import asyncio
import logging.config

from signal import SIG_IGN, SIGINT, SIGTERM, Signals
from signal import signal as signal_func

from typing import List, Dict, Type, Callable, Awaitable

import sentry_sdk
from macrobase_driver.driver import MacrobaseDriver
from macrobase_driver.config import CommonConfig, AppConfig
from macrobase_driver.hook import HookHandler
from macrobase_driver.logging import get_logging_config

from .config import AiopikaDriverConfig
from .hook import AiopikaHookNames
from .result import AiopikaResult, AiopikaResultAction
from .method import Method
from .router import Router, HeaderMethodRouter
from .serializers import deserialize
from .exceptions import AiopikaException, DeserializeFailedException, ContentTypeNotSupportedException,\
    ResultDeliveryFailedException, MethodNotFoundException

import uvloop
from aio_pika import connect_robust, Connection, IncomingMessage, Channel, Queue

from structlog import get_logger

log = get_logger('macrobase.aiopika')


class AiopikaDriver(MacrobaseDriver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.name is None:
            self.name = 'Aiopika Driver'

        self._connection = None
        self._channel: Channel = None
        self._queue: Queue = None

        self._hooks: Dict[AiopikaHookNames, List[HookHandler]] = {}
        self._methods: Dict[str, Method] = {}

        self._router: Router = None
        self.router_cls: Type[Router] = HeaderMethodRouter

    @property
    def config(self) -> CommonConfig[AppConfig, AiopikaDriverConfig]:
        return self._config

    def add_hook(self, name: AiopikaHookNames, handler):
        if name not in self._hooks:
            self._hooks[name] = []

        self._hooks[name].append(HookHandler(self, handler))

    def add_method(self, method: Method):
        self._methods[method.identifier] = method

    def add_methods(self, methods: List[Method]):
        self._methods.update({method.identifier: method for method in methods})

    def _setup_sentry(self):
        if self.config.driver.sentry_dsn is None:
            return

        sentry_sdk.init(
            dsn=self.config.driver.sentry_dsn,
            environment=self.config.driver.sentry_env
        )

    async def process_message(self, message: IncomingMessage, *args, **kwargs):
        async with message.process(ignore_processed=self.config.driver.ignore_processed):
            await self._process_message(message)

    async def _process_message(self, message: IncomingMessage):
        method = ''
        try:
            method = self._router.get_method(message)
            log.info(f'<IncomingMessage correlation_id: {message.correlation_id} method: {method}> processing')

            result = await self._get_method_result(message, method)
        except MethodNotFoundException as e:
            log.error(f'<IncomingMessage correlation_id: {message.correlation_id} method: {method}> ignore unknown method')
            result = AiopikaResult(action=AiopikaResultAction.nack, requeue=self.config.driver.requeue_unknown)
            await self._process_result(message, result, ignore_reply=True)
            return
        except Exception as e:
            requeue = e.requeue if isinstance(e, AiopikaException) else self.config.driver.requeue_if_failed

            log.error(e)
            result = AiopikaResult(action=AiopikaResultAction.nack, requeue=requeue)
            await self._process_result(message, result, ignore_reply=True)
            return

        await self._process_result(message, result, ignore_reply=False)

    async def _get_method_result(self, message: IncomingMessage, method: Method):
        data = message.body

        try:
            if message.content_type is not None and len(message.content_type) != 0:
                data = deserialize(message.body, message.content_type)
        except ContentTypeNotSupportedException as e:
            pass

        return await method.handler(self, message, data=data, identifier=method.identifier)

    async def _process_result(self, message: IncomingMessage, result: AiopikaResult, ignore_reply: bool = False):
        if result.requeue:
            await asyncio.sleep(self.config.driver.requeue_delay)

        if result.action == AiopikaResultAction.ack:
            await message.ack(multiple=result.multiple)
        elif result.action == AiopikaResultAction.nack:
            await message.nack(multiple=result.multiple, requeue=result.requeue)
        elif result.action == AiopikaResultAction.reject:
            await message.reject(requeue=result.requeue)

        if ignore_reply:
            return

        if message.reply_to is not None and len(message.reply_to) != 0:
            try:
                result_message = result.get_response_message()

                await self._channel.default_exchange.publish(
                    result_message,
                    routing_key=message.reply_to
                )
            except Exception as e:
                raise ResultDeliveryFailedException

    async def _prepare(self):
        log.debug(f'Router <{self.router_cls.__name__}> initialize')
        self._router = self.router_cls(self._methods)

        self._logging_config = get_logging_config(self.config.app)
        logging.config.dictConfig(self._logging_config)

        await self._add_health_if_needed()

    async def _add_health_if_needed(self):
        if self.config.driver.health_endpoint:
            from .endpoint import HealthEndpoint
            self.add_method(Method(HealthEndpoint(self.context, self.config), 'health'))

    async def _consume(self) -> Connection:
        host            = self.config.driver.rabbitmq.host
        port            = self.config.driver.rabbitmq.port
        user            = self.config.driver.rabbitmq.user
        password        = self.config.driver.rabbitmq.password
        virtual_host    = self.config.driver.rabbitmq.vhost
        queue           = self.config.driver.queue.name

        log.info(f'<Aiopika worker: {os.getpid()}> Connect to {host}:{port}/{virtual_host} ({user}:******)')
        self._connection = await connect_robust(
            host=host,
            port=port,
            login=user,
            password=password,
            virtualhost=virtual_host,

            loop=self.loop
        )

        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=self.config.driver.prefetch_count)

        self._queue = await self._channel.declare_queue(
            queue,
            durable=self.config.driver.queue.durable,
            auto_delete=self.config.driver.queue.auto_delete
        )

        await self._queue.consume(self.process_message)

        return self._connection

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)

        log.debug(self.config.driver.logo)

        self.loop.run_until_complete(self._prepare())
        uvloop.install()

        pid = os.getpid()
        log.info(f'<Aiopika worker: {pid}> Starting worker')
        self._setup_sentry()

        await_func = self.loop.run_until_complete
        await_func(self._call_hooks(AiopikaHookNames.before_server_start.value))

        connection: Connection = None

        try:
            connection = await_func(self._consume())
            self.loop.run_forever()
        except BaseException as e:
            log.error(e)

            if self._connection is not None:
                await_func(connection.close())
        finally:
            if self._connection is not None:
                await_func(self._connection.close())
            log.info(f'<Aiopika worker: {pid}> Stopping worker')

            await_func(self._call_hooks(AiopikaHookNames.after_server_stop.value))
            self.loop.close()
