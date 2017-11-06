#!/usr/bin/env python

import os
import sys
import ssl
import logging
import argparse
from threading import Thread

from irc.connection import Factory
from irc.client import SimpleIRCClient, ServerConnectionError, NickMask

log = logging.getLogger("irc-logger")

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


def handle_client(bot, f):
    while True:
        line = f.read().strip()
        if not line:
            break
        bot.say(line)


def channel_reader(bot):
    while True:
        with bot.log_channel.open() as f:
            handle_client(bot, f)


class Bot(SimpleIRCClient):
    def __init__(self, server, channel, name):
        super(Bot, self).__init__()
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
            thread.start()

    def on_disconnect(self, _, event):
        log.info('disconnected from %s', self.server)
        self.log_channel.remove()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('server', help="server to connect to")
    parser.add_argument('channel', help="channel to join")
    parser.add_argument('name', help="name of channel/fifo")
    parser.add_argument('-p', '--port', default=9999, type=int)
    return parser.parse_args()


def main():
    args = get_args()

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] (%(levelname)s) %(name)s: %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    bot = Bot(args.server, args.channel, args.name)

    try:
        ssl_factory = Factory(wrapper=ssl.wrap_socket)
        bot.connect(
            args.server,
            args.port,
            args.name,
            connect_factory=ssl_factory
        )
    except ServerConnectionError as x:
        print(x)
        sys.exit(1)

    try:
        bot.start()
    except KeyboardInterrupt:
        bot.reactor.disconnect_all()


if __name__ == '__main__':
    main()

