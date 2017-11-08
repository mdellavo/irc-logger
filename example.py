import logging

from irclogger import IRCHandler, Channel

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = IRCHandler(Channel("abendigo"))

formatter = logging.Formatter('[%(asctime)s] (%(levelname)s) %(name)s: %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

log = logging.getLogger("irclogger-example")

for i in range(10):
    log.info("hello world - %s", i)
