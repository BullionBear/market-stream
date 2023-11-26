import redis
import threading

from helper import get_logger


class RedisSubscriber:
    def __init__(self, host='localhost', port=6379):
        self.redis = redis.Redis(host=host, port=port)
        self.pubsub = self.redis.pubsub()
        self.callback = dict()

        self.logger = get_logger(__name__)

    def subscribe(self, channel, callback, *args, **kwargs):
        self.callback.update({channel: lambda message: callback(message, *args, **kwargs)})
        self.pubsub.subscribe(channel)

    def unsubscribe(self, channel):
        self.pubsub.unsubscribe(channel)
        self.callback.pop(channel)

    def listen(self):
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                channel = message['channel'].decode('utf-8')
                message = message['data'].decode('utf-8')
                self.callback[channel](message)

    def start_listening(self):
        thread = threading.Thread(target=self.listen)
        thread.start()
