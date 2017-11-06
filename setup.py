from setuptools import setup

setup(
    name="irc-logger",
    version="1.0",
    scripts=["irc-loggerd.py"],
    install_requires=[
        'irc'
    ]
)