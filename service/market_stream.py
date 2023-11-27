import grpc
import asyncio
import json
from datetime import datetime
from concurrent import futures

from generated import market_stream_pb2
from generated import market_stream_pb2_grpc
from publisher import RedisPublisher
from listener import BinanceFutureDepthListener


class MarketStream(market_stream_pb2_grpc.MarketStreamServicer):

    def __init__(self, publisher):
        self.listeners = {
            "binancefuture": BinanceFutureDepthListener()
        }
        self.publisher: RedisPublisher = publisher

    async def GetStatus(self, request, context):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return market_stream_pb2.ServerTimeReply(time=current_time)

    async def Subscribe(self, request, context):
        if request.exchange not in self.listener:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f'{request.exchange} is not implemented')
            return market_stream_pb2.ServerTimeReply()
        listener = self.listeners[request.exchange]
        asyncio.create_task(listener.run(self.message_handler))

    async def run(self):
        for ex, listener in self.listeners.items():
            asyncio.create_task(listener.run(lambda msg: self.message_handler(ex, msg)))

    def message_handler(self, exchange, message):
        if exchange == "binancefuture":
            self.binancefuture_handler(message)
        else:
            raise ValueError(f"{exchange} not implemented yet")

    def binancefuture_handler(self, message):
        if "id" in message:
            return
        data = {
            "id": message["E"],
            "ts": message["T"],
            "s": message["s"],
            "u": message["u"],
            "pu": message["pu"],
            "b": [[float(p), float(v)] for p, v in message["b"]],
            "a": [[float(p), float(v)] for p, v in message["a"]]
        }
        self.publisher.publish(f"binancefuture@{data['s']}@perp", data)


async def serve(redis_host, redis_port):
    server = grpc.aio.server()
    publisher = RedisPublisher(redis_host, redis_port)
    market_stream = MarketStream(publisher)
    asyncio.create_task(market_stream.run())
    market_stream_pb2_grpc.add_MarketStreamServicer_to_server(market_stream, server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    with open('./config.json') as jfile:
        config = json.load(jfile)
    asyncio.run(serve(config["redis_host"], config["redis_port"]))