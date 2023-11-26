import asyncio
import websockets
import json

class MarketListener:
    def __init__(self, uri):
        self.uri = uri
        self.queue = asyncio.Queue()
        self.connected = False

    async def _listen(self, ws, callback, *args, **kwargs):
        # Listen for messages and invoke the callback
        self.connected = True
        try:
            while True:
                message = await ws.recv()
                callback(message, *args, **kwargs)
        finally:
            self.connected = False

    async def _send(self, ws):
        # Continuously check and send messages from the queue
        while self.connected:
            message = await self.queue.get()
            await ws.send(message)

    async def send(self, request):
        # Put a request in the queue to be sent
        await self.queue.put(json.dumps(request))

    async def run(self, callback, *args, **kwargs):
        async with websockets.connect(self.uri) as ws:
            # Start the WebSocket connection and message sending tasks
            websocket_task = asyncio.create_task(self._listen(ws, callback, *args, **kwargs))
            send_task = asyncio.create_task(self._send(ws))

            # Wait for both tasks to complete
            await asyncio.gather(websocket_task, send_task)

# Example usage
async def main():
    listener = MarketListener("wss://fstream.binance.com/ws")

    # Define a callback function for incoming messages
    def process_message(message):
        print("Received message:", message)

    # Run the listener with the callback function
    asyncio.create_task(listener.run(process_message))

    # Send a subscription request
    await asyncio.sleep(1)  # Short delay to ensure the WebSocket connection is established
    await listener.send({
        "method": "SUBSCRIBE",
        "params": ["btcusdt@depth5@100ms"],
        "id": 1
    })

    # Example: Send another subscription request after some time
    await asyncio.sleep(5)
    await listener.send({
        "method": "SUBSCRIBE",
        "params": ["ltcusdt@depth5@100ms"],
        "id": 2
    })

    # Keep the program running to maintain the WebSocket connection
    while True:
        await asyncio.sleep(3600)  # Sleep for an hour at a time

if __name__ == "__main__":
    asyncio.run(main())
