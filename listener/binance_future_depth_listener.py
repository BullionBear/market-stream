import random

from helper import get_logger
from listener.market_listener import MarketListener


class BinanceFutureDepthListener(MarketListener):
    def __init__(self):
        super().__init__("wss://fstream.binance.com/ws")
        self.channel = set()
        self.logger = get_logger(__name__)

        self._requests = dict()

    async def subscribe(self, base, quote):
        symbol = (base + quote).lower()
        request_id = random.randint(1, 2 ** 32)
        request = {
            "method": "SUBSCRIBE",
            "params": [f"{symbol}@depth5@100ms"],
            "id": request_id
        }
        self._requests[request_id] = request
        await super().send(request)

    async def unsubscribe(self, base, quote):
        symbol = (base + quote).lower()
        request_id = random.randint(1, 2 ** 32)
        request = {
            "method": "UNSUBSCRIBE",
            "params": [f"{symbol}@depth5@100ms"],
            "id": request_id
        }
        self._requests[request_id] = request
        await super().send(request)

    async def run(self, callback, *args, **kwargs):
        def wrapper(message,  *wrapper_args, **wrapper_kwargs):
            if self._helper(message):
                callback(message, *wrapper_args, **wrapper_kwargs)

        await super().run(wrapper, *args, **kwargs)

    def _helper(self, message):
        if "id" in message:
            request_id = message["id"]
            payload = self._requests[request_id]
            self.logger.info(f"Receive {payload=}")
            if payload["method"] == "SUBSCRIBE":
                self.channel.update(payload["params"])
                self.logger.info(f"Adding symbol {payload['params']}")
            elif payload["method"] == "UNSUBSCRIBE":
                self.channel.difference_update(payload["params"])
                self.logger.info(f"Removing symbol {payload['params']}")
            del self._requests[request_id]
            return False
        return True

