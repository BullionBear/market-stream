import unittest
import asyncio
from concurrent import futures
import grpc
from grpc_testing import server_from_dictionary, strict_real_time

from generated import greeter_pb2
from generated import greeter_pb2_grpc

from service.greeter import GreeterServicer

class GreeterTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Create a test server
        self.server = grpc.aio.server()
        greeter_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), self.server)

        # Start the server
        self.server_port = self.server.add_insecure_port('localhost:0')
        await self.server.start()

        # Create a channel to the server
        self.channel = grpc.aio.insecure_channel('localhost:' + str(self.server_port))

    async def asyncTearDown(self):
        await self.server.stop(None)

    async def test_greeter_service(self):
        # Create a stub (client)
        stub = greeter_pb2_grpc.GreeterStub(self.channel)

        # Send a request and wait for the response
        response = await stub.SayHello(greeter_pb2.HelloRequest(name='Test User'))

        # Check the response
        self.assertEqual(response.message, 'Hello, Test User')

if __name__ == '__main__':
    unittest.main()