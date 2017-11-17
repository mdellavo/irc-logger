import time
import threading
from logging import Handler
from Queue import Queue, Full

from .channel import Channel


def ensure_written(channel, msg):
    while True:
        try:
            return channel.write(msg)
        except OSError:
            time.sleep(1)


def channel_writer(channel, queue):
    while True:
        msg = queue.get()
        ensure_written(channel, msg)


class IRCHandler(Handler):
    def __init__(self, channel, max_size=0, **kwargs):
        super(IRCHandler, self).__init__(**kwargs)
        if isinstance(channel, basestring):
            channel = Channel(channel)
        self.channel = channel
        self.queue = Queue(maxsize=max_size)

        self.thread = threading.Thread(target=channel_writer, args=(self.channel, self.queue))
        self.thread.start()

    def emit(self, record):
        try:
            self.queue.put_nowait(self.format(record))
        except Full:
            pass
