import asyncio
import websockets
import json

class MarketListener:
    def __init__(self, uri):
        self.uri = uri
        self.queue = asyncio.Queue()
        self.connected = False
        self.ws = None  # WebSocket connection object

    async def _listen(self, ws, callback, *args, **kwargs):
        self.connected = True
        try:
            while self.connected:
                message = await ws.recv()
                callback(message, *args, **kwargs)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connected = False

    async def _send(self, ws):
        while self.connected:
            message = await self.queue.get()
            if message is None:  # None message as a signal to stop
                break
            await ws.send(message)

    async def send(self, request):
        await self.queue.put(json.dumps(request))

    async def run(self, callback, *args, **kwargs):
        async with websockets.connect(self.uri) as ws:
            self.ws = ws
            websocket_task = asyncio.create_task(self._listen(ws, callback, *args, **kwargs))
            send_task = asyncio.create_task(self._send(ws))
            await asyncio.gather(websocket_task, send_task)

    async def disconnect(self):
        if self.connected:
            self.connected = False
            await self.ws.close()
            await self.queue.put(None)  # Signal the send task to stop
