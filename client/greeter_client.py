import asyncio
import grpc
from generated import greeter_pb2
from generated import greeter_pb2_grpc


class GreeterClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.aio.insecure_channel(f'{host}:{port}')

    async def say_hello(self, name):
        stub = greeter_pb2_grpc.GreeterStub(self.channel)
        request = greeter_pb2.HelloRequest(name=name)
        response = await stub.SayHello(request)
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