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

    def open(self, mode="r"):
        return open(self.path, mode=mode)

    def write(self, line):
        with self.open("w") as f:
            f.write(line.encode("utf-8") + "\n")
