import time
import datetime
import logging

from irclogger import IRCHandler, Channel

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = IRCHandler(Channel("abendigo"))

formatter = logging.Formatter('[%(asctime)s] (%(levelname)s) %(name)s: %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

log = logging.getLogger("irclogger-example")

for i in range(5):
    log.info("%s - hello world - the time is now %s", i, datetime.datetime.now().strftime("%c"))
    time.sleep(.5)

logging.shutdown()  # make sure we shutdown
