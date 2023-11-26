import asyncio

from listener import BinanceFutureDepthListener
from publisher import RedisPublisher

from helper import get_logger


class MarketStream:
    def __init__(self, publisher):
        self.publisher: RedisPublisher = publisher
        self.depth_streams = {
            "binancefuture": BinanceFutureDepthListener()
        }

        self.logger = get_logger(__name__)
        asyncio.run(self._run())

    def subscribe(self, exchange, symbol):
        self.depth_streams[exchange].subscribe(symbol)

    async def _run(self):
        tasks = []
        for exchange, stream in self.depth_streams.items():
            task = asyncio.create_task(stream.run(lambda message: self.callback(exchange, message)))
            tasks.append(task)
        await asyncio.gather(*tasks)

    def callback(self, exchange, message):
        if exchange == 'binancefuture':
            self._binancefuture_handler(message)
        else:
            raise ValueError(f"{exchange} is not implemented")

    def _binancefuture_handler(self, message):
        data = {
            "id": message["E"],
            "ts": message["T"],
            "ex": "binancefuture",
            "s": message["s"],
            "ins": "perp",
            "a": [[float(p), float(v)] for p, v in message["a"]],
            "b": [[float(p), float(v)] for p, v in message["b"]]
        }
        channel = f"{data['ex']}@{data['s']}@{data['ins']}"
        self.publisher.publish(channel, data)








