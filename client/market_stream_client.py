import asyncio
import grpc
from generated import market_stream_pb2
from generated import market_stream_pb2_grpc


class MarketStreamClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.aio.insecure_channel(f'{host}:{port}')

    async def get_status(self):
        stub = market_stream_pb2_grpc.MarketStreamStub(self.channel)
        request = market_stream_pb2.Empty()
        response = await stub.GetStatus(request)
        return response.time

    async def close(self):
        await self.channel.close()


async def main():
    client = MarketStreamClient()
    response = await client.get_status()
    print(response)
    await client.close()

if __name__ == '__main__':
    asyncio.run(main())