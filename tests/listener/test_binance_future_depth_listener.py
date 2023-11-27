import unittest
import asyncio
from listener.binance_future_depth_listener import BinanceFutureDepthListener
import json


class TestBinanceFutureDepthListener(unittest.TestCase):
    def test_listen(self):
        async def test():
            listener = BinanceFutureDepthListener()

            # Define a callback function for incoming messages
            async def message_handler(message):
                print("Received message:", message)

            # Run the listener with the callback function
            listener_task = asyncio.create_task(listener.run(message_handler))

            # Send a subscription request
            await asyncio.sleep(1)  # Short delay to ensure the WebSocket connection is established
            await listener.subscribe("BTC", "USDT")

            # Example: Send another subscription request after some time
            await asyncio.sleep(5)
            await listener.subscribe("LTC", "USDT")

            # Example: Unsubscribe request after some time
            await asyncio.sleep(5)
            await listener.unsubscribe("LTC", "USDT")

            await asyncio.sleep(5)
            await listener.disconnect()

            # Wait for the listener task or timeout after 30 seconds
            try:
                await asyncio.wait_for(listener_task, 30)
            except asyncio.TimeoutError:
                print("Test timed out after 30 seconds")

        asyncio.run(test())


if __name__ == '__main__':
    unittest.main()
