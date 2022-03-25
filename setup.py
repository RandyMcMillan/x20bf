#!/usr/bin/env python
import os

from setuptools import find_packages, setup

# -*- coding: UTF-8 -*-

"""
Utility function to read the README.md file.
Used for the long_description.  It's nice, because now 1) we have a top level
README file and 2) it's easier to type in the README file than to put a raw
string in below ...
"""


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


here = os.path.abspath(os.path.dirname(__file__))

packages = find_packages(
    include=[
        "x20bf",
        "x20bf/gui",
        "depends/p2p",
        "depends/gnupg",
        "depends/fastapi",
        "depends/git/git",
        "depends/git/git/ext/gitdb/gitdb",
        "depends/git/git/ext/gitdb/gitdb/ext/smmap/smmap",
    ],
    exclude=["*.tests", "*.tests.*", "tests.*"],
)
print(packages)


setup(
    name="x20bf",
    version="0.0.1",
    author="randymcmillan, bitkarrot",
    author_email="randy.lee.mcmillan@gmail.com, me@bitkarrot.co",
    description=(
        str(
            "x20bf: An internet standards track protocol for"
            + "transporting, broadcasting and syndication of messages"
            + "ver common internet communications channels."
        )
    ),
    license="Apache License 2.0",
    keywords=["p2p", "decentralized", "gnupg", "node", "git", "bitcoin", "bitkarrot"],
    url="http://packages.python.org/x20bf",
    install_requires=[
        "pre_commit >= '2.1.0'",
        "aiohttp >= '3.7.4.post0'",
        "PyYAML >= '5.4.1'",
        "gnupg >= '2.3.1'",
        "asyncio >= '3.4.1'",
        "p2pnetwork >= '1.1.0'",
        "GitPython >= '3.1.27'",
    ],
    packages=[
        "x20bf",
        "x20bf/gui",
        "tests",
        "x20bf/depends/p2p/p2pnetwork",
        "x20bf/depends/gnupg",
        "x20bf/depends/fastapi/fastapi",
        "x20bf/depends/git/git",
        "x20bf/depends/git/git/ext/gitdb/gitdb",
        "x20bf/depends/git/git/ext/gitdb/gitdb/ext/smmap/smmap",
    ],
    py_modules=[],
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache License 2.0",
    ],
)
