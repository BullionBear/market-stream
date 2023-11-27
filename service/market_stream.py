import grpc
import asyncio
from datetime import datetime
from concurrent import futures

from generated import market_stream_pb2
from generated import market_stream_pb2_grpc
from publisher import RedisPublisher
from listener import BinanceFutureDepthListener


class MarketStream(market_stream_pb2_grpc.MarketStreamServicer):

    def __init__(self):
        pass

    async def GetStatus(self, request, context):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return market_stream_pb2.ServerTimeReply(time=current_time)

async def serve():
    server = grpc.aio.server()
    market_stream_pb2_grpc.add_MarketStreamServicer_to_server(MarketStream(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())