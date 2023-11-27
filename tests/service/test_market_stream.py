import asyncio
import unittest
from concurrent import futures
from datetime import datetime
import grpc
from grpc_testing import server_from_dictionary, strict_real_time
from generated import market_stream_pb2
from generated import market_stream_pb2_grpc

# Import your service
from service.market_stream import MarketStream


class MarketStreamTest(unittest.TestCase):

    def setUp(self):
        self.servicers = {
            market_stream_pb2.DESCRIPTOR.services_by_name['MarketStream']: MarketStream()
        }
        self.server = server_from_dictionary(self.servicers, strict_real_time())

    def tearDown(self):
        pass

    def test_get_status(self):
        method_descriptor = market_stream_pb2.DESCRIPTOR.services_by_name['MarketStream'].methods_by_name[
            'GetStatus']
        call = self.server.invoke_unary_unary(
            method_descriptor,
            (),
            market_stream_pb2.Empty(),
            None
        )

        response = asyncio.get_event_loop().run_until_complete(call)
        self.assertIsNotNone(response.time, "Time should not be None")
        # Additional assertions can be added here

if __name__ == '__main__':
    unittest.main()



if __name__ == '__main__':
    unittest.main()
