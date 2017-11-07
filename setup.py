from setuptools import setup

setup(
    name="irc-logger",
    version="1.0",
    description="",
    url="http://github.com/mdellavo/irc-logger",
    author="Marc DellaVolpe",
    author_email="marc.dellavolpe@gmail.com",
    license="MIT",
    scripts=[
        "bin/irc-loggerd"
    ],
    install_requires=[
        "irc"
    ],
    packages=["irclogger"],
    zip_safe=False
)
