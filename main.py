import grpc
import asyncio
from generated import market_stream_pb2
from generated import market_stream_pb2_grpc

async def get_status():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = market_stream_pb2_grpc.MarketStreamStub(channel)
        response = await stub.GetStatus(market_stream_pb2.Empty())
        print("Server time:", response.time)

if __name__ == '__main__':
    asyncio.run(get_status())