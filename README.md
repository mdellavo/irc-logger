# IRC Logger

Relays messages from FIFO to IRC channel

## Install

```
$ pip install git+git://github.com/mdellavo/irc-logger.git@master
```

## Usage 

```
usage: irc-loggerd.py [-h] [-p PORT] server channel name

positional arguments:
  server                server to connect to
  channel               channel to join
  name                  name of channel/fifo

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT
```

## Example

Start the logging service
```
$ ./irc-loggerd.py -p 6697 chat.freenode.net foo foo
```

Now write some data to the fifo while monitoring IRC
```
$ echo -n hello > /tmp/foo.fifo
```

## Python Logging
The `irclogger` package includes a handler `IRCHandler` for the `logging` package.  This allows python applications to log through the FIFO to IRC.

```python
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
```  

## Author

Marc DellaVolpe  (marc.dellavolpe@gmail.com)

## License
    The MIT License (MIT)

    Copyright (c) 2017 Marc DellaVolpe

    Permission is hereby granted, free of charge, to any person obtaining a copy of this
    software and associated documentation files (the "Software"), to deal in the Software
    without restriction, including without limitation the rights to use, copy, modify, merge,
    publish, distribute, sublicense, and/or sell copies of the Software, and to permit
    persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies
    or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
    INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
    PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
    FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
    OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.