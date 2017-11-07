import os

FIFO_PATH = os.path.join("/", "tmp", "{name}.fifo")


class Channel(object):
    def __init__(self, name):
        self.name = name
        self.path = FIFO_PATH.format(name=self.name)

    def create(self):
        self.remove()
        os.mkfifo(self.path)

    def remove(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def open(self):
        return open(self.path)
