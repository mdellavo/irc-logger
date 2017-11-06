# IRC Logger

Relays messages from FIFO to IRC channel

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
$ ./irc-loggerd.py chat.freenode.net #foo foo
```

Now write some data to the fifo while monitoring IRC
```
$ echo -n hello > /tmp/foo.fifo
```

## Author

Marc DellaVolpe  (marc.dellavolpe@gmail.com)

## License
    The MIT License (MIT)

    Copyright (c) 2016 Marc DellaVolpe

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