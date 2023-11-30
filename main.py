import os
import asyncio

from service import serve

if __name__ == '__main__':
    asyncio.run(serve(os.getenv("REDIS_HOST", "localhost"),
                      os.getenv("REDIS_PORT", 6379)))
