import sys
import argparse
import logging

from irclogger import Bot


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

    bot = Bot(args.server_host, args.server_port, args.channel, args.name)

    try:
        bot.start()
    except KeyboardInterrupt:
        bot.die()
