from logging import Handler


class IRCHandler(Handler):

    def __init__(self, channel, *args, **kwargs):
        super(IRCHandler, self).__init__(*args, **kwargs)
        self.channel = channel

    def emit(self, record):
        self.channel.write(self.format(record))

