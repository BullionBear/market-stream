import asyncio
import websockets
import json

from helper import get_logger


class MarketListener:
    def __init__(self, uri):
        self.uri = uri
        self.queue = asyncio.Queue()
        self.connected = False
        self.ws = None
        self.logger = get_logger(__name__)

    async def _listen(self, ws, callback, *args, **kwargs):
        self.connected = True
        try:
            while self.connected:
                message = await ws.recv()
                message = json.loads(message)
                await callback(message, *args, **kwargs)
        except websockets.exceptions.ConnectionClosed:
            self.logger.warning("Websocket connection closed")
        finally:
            self.connected = False

    async def _send(self, ws):
        while self.connected:
            message = await self.queue.get()
            self.logger.info(f"Receive and send {message}")
            if message is None:
                break
            await ws.send(message)

    async def _heartbeat(self, ws):
        while self.connected:
            try:
                await ws.ping()
                self.logger.debug("Ping!")
                await asyncio.sleep(30)  # Send a ping every 30 seconds
            except websockets.exceptions.ConnectionClosed:
                break

    async def send(self, request):
        self.logger.info(f"Put {request} to queue")
        await self.queue.put(json.dumps(request))

    async def run(self, callback, *args, **kwargs):
        async with websockets.connect(self.uri) as ws:
            self.ws = ws
            websocket_task = asyncio.create_task(self._listen(ws, callback, *args, **kwargs))
            send_task = asyncio.create_task(self._send(ws))
            heartbeat_task = asyncio.create_task(self._heartbeat(ws))
            await asyncio.gather(websocket_task, send_task, heartbeat_task)

    async def disconnect(self):
        if self.connected:
            self.logger.info(f"Disconnecting Websocket")
            self.connected = False
            await self.ws.close()
            await self.queue.put(None)  # Signal the send task to stop

    async def is_connected(self):
        return self.connected

    async def subscribe(self, base, quote):
        pass

    async def unsubscribe(self, base, quote):
        pass
