import redis


class RedisPublisher:
    def __init__(self, host='localhost', port=6379):
        self.redis = redis.Redis(host=host, port=port)

    def publish(self, channel, message):
        self.redis.publish(channel, message)