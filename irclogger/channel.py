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
        try:
            os.remove(self.path)
        except OSError:
            pass

    def open(self, mode='r', blocking=True):
        flag = 0
        if mode == 'r':
            flag |= os.O_RDONLY
        elif mode == 'w':
            flag |= os.O_WRONLY
        if not blocking:
            flag |= os.O_NONBLOCK
        fd = os.open(self.path, flag)
        return os.fdopen(fd, mode)

    def write(self, line):
        with self.open("w") as f:
            f.write(line.encode("utf-8") + "\n")
