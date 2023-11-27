import unittest
import asyncio
from concurrent import futures
from datetime import datetime, timedelta
import grpc
from grpc_testing import server_from_dictionary, strict_real_time

from generated import market_stream_pb2
from generated import market_stream_pb2_grpc

# Import your service
from service.market_stream import MarketStream


class MarketStreamTest(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        # Create a test server
        self.server = grpc.aio.server()
        market_stream_pb2_grpc.add_MarketStreamServicer_to_server(MarketStream(), self.server)

        # Start the server
        self.server_port = self.server.add_insecure_port('localhost:0')
        await self.server.start()

        # Create a channel to the server
        self.channel = grpc.aio.insecure_channel('localhost:' + str(self.server_port))

    async def asyncTearDown(self):
        await self.server.stop(None)

    async def test_get_status(self):
        # Create a stub (client)
        stub = market_stream_pb2_grpc.MarketStreamStub(self.channel)

        # Send a request and wait for the response
        response = await stub.GetStatus(market_stream_pb2.Empty())

        # current time
        print(response.time)
        system_time = datetime.strptime(response.time, "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        # Check the response
        self.assertTrue(current_time - system_time < timedelta(seconds=1))


if __name__ == '__main__':
    unittest.main()
