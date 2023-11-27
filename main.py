import asyncio

from listener import MarketListener, BinanceFutureDepthListener
from publisher import RedisPublisher

from helper import get_logger


class 

async def test():
    listener = BinanceFutureDepthListener()

    # Define a callback function for incoming messages
    def message_handler(message):
        print("Received message:", message)

    # Run the listener with the callback function
    asyncio.create_task(listener.run(message_handler))

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



if __name__ == "__main__":
    asyncio.run(test())



