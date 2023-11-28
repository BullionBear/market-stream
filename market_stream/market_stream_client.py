import asyncio
import grpc
from generated import market_stream_pb2
from generated import market_stream_pb2_grpc

from helper import get_logger

class MarketStreamClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.aio.insecure_channel(f'{host}:{port}')
        self.stub = market_stream_pb2_grpc.MarketStreamStub(self.channel)

        self.logger = get_logger(__name__)

    async def get_status(self):
        request = market_stream_pb2.Empty()
        response = await self.stub.GetStatus(request)
        return response.time

    async def subscribe(self, exchange, base, quote):
        request = market_stream_pb2.SubscriptionRequest(exchange=exchange, base=base, quote=quote)
        try:
            response = await self.stub.Subscribe(request)
            return response.status
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                self.logger.info(f"Error: {e.details()}")
            else:
                self.logger.info(f"Unexpected error: {e.code()}")


    async def unsubscribe(self, exchange, base, quote):
        request = market_stream_pb2.SubscriptionRequest(exchange=exchange, base=base, quote=quote)
        try:
            response = await self.stub.Unsubscribe(request)
            return response.status
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                self.logger.info(f"Error: {e.details()}")
            else:
                self.logger.info(f"Unexpected error: {e.code()}")

    async def close(self):
        await self.channel.close()


async def main():
    client = MarketStreamClient()
    response = await client.get_status()
    print(response)
    response = await client.subscribe('binancefuture', "BTC", "USDT")
    print(response)
    await client.close()

if __name__ == '__main__':
    asyncio.run(main())