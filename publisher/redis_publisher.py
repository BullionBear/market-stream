import redis
import aioredis


class RedisPublisher:
    def __init__(self, host='localhost', port=6379):
        self.redis = redis.Redis(host=host, port=port)

    def publish(self, channel: str, message: str):
        self.redis.publish(channel, message)


class AsyncRedisPublisher:
    def __init__(self, url='redis://localhost', port=6379):
        self.url = url
        self.port = port
        self.redis = None

    async def connect(self):
        url = f"redis://{self.url}:{self.port}"
        self.redis = await aioredis.from_url(url)

    async def publish(self, channel: str, message: str):
        if not self.redis:
            await self.connect()
        await self.redis.publish(channel, message)

    async def close(self):
        if self.redis:
            self.redis.close()
            await self.redis.wait_closed()