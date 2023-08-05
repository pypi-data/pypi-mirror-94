import asyncio
from .request import RPCResponse, RPCMessageType
from .exceptions import ResponseContentException

from ..driver import AiopikaDriver, IncomingMessage
from ..method import Method
from ..router import HeaderMethodRouter, IncomingRoutingFailedException
from ..result import AiopikaResult, AiopikaResultAction
from ..exceptions import PayloadTypeNotSupportedException, SerializeFailedException, ResultDeliveryFailedException, \
    MethodNotFoundException

from structlog import get_logger
log = get_logger('macrobase.aiopika_rpc')


class AiopikaRPCDriver(AiopikaDriver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'Aiopika RPC Driver'
        self.router_cls = HeaderMethodRouter

    async def _process_message(self, message: IncomingMessage):
        method = None

        try:
            method = self._router.get_method(message)
            result = await self._get_method_result(message, method)
            ignore_reply = False
        except MethodNotFoundException as e:
            log.debug(f'Ignore unknown method')
            result = AiopikaResult(action=AiopikaResultAction.nack, requeue=self.config.driver.requeue_unknown)
            ignore_reply = True
        except Exception as e:
            log.error(e)
            result = RPCResponse(payload=e, type=RPCMessageType.error).get_result(message.correlation_id, method.identifier if method is not None else '', message.expiration)
            ignore_reply = True

        await self._process_result(message, result, ignore_reply=ignore_reply)

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
                try:
                    result_message = result.get_response_message()
                except (PayloadTypeNotSupportedException, SerializeFailedException) as e:
                    result_message = result.get_response_message(
                        payload=ResponseContentException(),
                        type=RPCMessageType.error.value
                    )

                await self._channel.default_exchange.publish(
                    result_message,
                    routing_key=message.reply_to
                )
            except Exception as e:
                raise ResultDeliveryFailedException

    async def _add_health_if_needed(self):
        if self.config.driver.health_endpoint:
            from .endpoint import HealthEndpoint
            self.add_method(Method(HealthEndpoint(self.context, self.config), 'health'))
