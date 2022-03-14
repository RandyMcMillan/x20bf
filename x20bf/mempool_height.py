#!/usr/bin/env python3
import asyncio
import configparser
import os

import aiohttp

from logger import logger

# get the path to config.ini
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")

# check if the path is to a valid file
if not os.path.isfile(config_path):
    print("BadConfigError")  # not a standard python exception

config = configparser.ConfigParser()
config.read(config_path)
# config.read("configs.ini")
config.sections()
config.get("DEFAULTS", "", fallback=False)


MEMPOOL_LOGGER = True


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def mempool_height():
    async with aiohttp.ClientSession() as session:
        url = "https://mempool.space/api/blocks/tip/height"
        height = await fetch(session, url)
        if MEMPOOL_LOGGER:
            logger.info(height)
        return height


loop = asyncio.new_event_loop()
# loop = asyncio.get_event_loop()
loop.run_until_complete(mempool_height())
