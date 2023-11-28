import asyncio
import grpc
from generated import greeter_pb2
from generated import greeter_pb2_grpc


class GreeterClient:
    def __init__(self, host='localhost', port=50051):
        options = [
            ('grpc.keepalive_time_ms', 30000),  # Send keepalive ping every 30 seconds
            ('grpc.keepalive_timeout_ms', 10000),  # Wait 10 seconds for pong response
            ('grpc.keepalive_permit_without_calls', True),  # Allow keepalive pings when there are no calls
            ('grpc.http2.min_time_between_pings_ms', 10000),  # Minimum time between pings
            ('grpc.http2.max_pings_without_data', 0),  # Allow pings without data
            ('grpc.http2.min_ping_interval_without_data_ms', 5000)  # Minimum interval between pings without data
        ]
        self.channel = grpc.aio.insecure_channel(f'{host}:{port}', options=options)
        self.stub = greeter_pb2_grpc.GreeterStub(self.channel)

    async def say_hello(self, name):
        request = greeter_pb2.HelloRequest(name=name)
        response = await self.stub.SayHello(request)
        return response.message

    async def close(self):
        await self.channel.close()


async def main():
    client = GreeterClient()
    response = await client.say_hello("Alice")
    print(response)
    await client.close()

if __name__ == '__main__':
    asyncio.run(main())