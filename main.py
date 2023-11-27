import asyncio

from listener import MarketListener, BinanceFutureDepthListener
from publisher import RedisPublisher

from helper import get_logger


class MarketStream:
    def __init__(self, publisher):
        self.publisher: RedisPublisher = publisher
        self.depth_streams: dict[str, MarketListener] = {
            "binancefuture": BinanceFutureDepthListener()
        }

        self.logger = get_logger(__name__)

    @classmethod
    async def async_init(cls, publisher):
        self = cls(publisher)
        return self

    async def subscribe(self, exchange, base, quote):
        await self.depth_streams[exchange].subscribe(base, quote)
        self.logger.info(f"Subscribe {base + quote} in {exchange}")
        if exchange == 'binancefuture':
            return f"{exchange}@{(base + quote).lower()}@perp"
        else:
            raise ValueError(f'{exchange} is not implemented')

    async def run(self):
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
        self.logger.debug(f'{data=}')
        channel = f"{data['ex']}@{data['s'].lower()}@{data['ins']}"
        self.publisher.publish(channel, data)

async def main():
    publisher = RedisPublisher()
    market_stream = MarketStream(publisher)
    await market_stream.run()
    await asyncio.sleep(5)
    await market_stream.subscribe('binancefuture', 'BTC', 'USDT')
    # await market_stream.run()


if __name__ == "__main__":
    asyncio.run(main())



