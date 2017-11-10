import ssl
import logging
from threading import Thread

from irc.client import NickMask
from irc.connection import Factory
from irc.bot import SingleServerIRCBot, ExponentialBackoff

from irclogger.channel import Channel

log = logging.getLogger("irc-logger")

RECONNECT_TIMEOUT = 10


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


class Bot(SingleServerIRCBot):
    def __init__(self, host, port, channel, name):
        if channel[0] != '#':
            channel = "#" + channel

        super(Bot, self).__init__([(host, port)], name, name,
                                  recon=ExponentialBackoff(min_interval=RECONNECT_TIMEOUT, max_interval=2*RECONNECT_TIMEOUT),
                                  connect_factory=Factory(wrapper=ssl.wrap_socket))
        self.name = name
        self.channel = channel
        self.log_channel = Channel(self.name)

    @property
    def server_host(self):
        return self.server_list[0].host

    @property
    def server_port(self):
        return self.server_list[0].server_port

    def say(self, fmt, *args, **kwargs):
        self.connection.privmsg(self.channel, fmt.format(*args, **kwargs))

    def on_welcome(self, _, event):
        log.info('connected to %s, joining %s...', self.server_host, self.channel)
        self.connection.join(self.channel)

    def on_join(self, _, event):
        nm = NickMask(event.source)
        if nm.nick == self.name:
            log.info('joined %s', self.channel)
            self.log_channel.create()
            thread = Thread(target=channel_reader, args=(self,))
            thread.setDaemon(True)
            thread.start()

    def on_disconnect(self, _, event):
        log.info('disconnected from %s', self.server_host)
        self.log_channel.remove()
