import logging
from threading import Thread

from irc.client import SimpleIRCClient, NickMask

from irclogger.channel import Channel

log = logging.getLogger("irc-logger")


def handle_client(bot, f):
    while True:
        data = f.read()
        if not data:
            break
        lines = data.splitlines()
        for line in lines:
            bot.say(line)


def channel_reader(bot):
    while True:
        with bot.log_channel.open() as f:
            handle_client(bot, f)


class Bot(SimpleIRCClient):
    def __init__(self, server, channel, name):
        super(Bot, self).__init__()

        if channel[0] != '#':
            channel = "#" + channel

        self.server = server
        self.name = name
        self.channel = channel
        self.log_channel = Channel(self.name)

    def say(self, fmt, *args, **kwargs):
        self.connection.privmsg(self.channel, fmt.format(*args, **kwargs))

    def on_welcome(self, _, event):
        log.info('connected to %s, joining %s...', self.server, self.channel)
        self.connection.join(self.channel)

    def on_join(self, _, event):
        log.info('joined %s', self.channel)
        nm = NickMask(event.source)
        if nm.nick == self.name:
            self.log_channel.create()
            thread = Thread(target=channel_reader, args=(self,))
            thread.setDaemon(True)
            thread.start()

    def on_disconnect(self, _, event):
        log.info('disconnected from %s', self.server)
        self.log_channel.remove()

