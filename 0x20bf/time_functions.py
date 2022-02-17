#!/usr/bin/env python3
import asyncio
import os
import shutil
import time

import aiohttp
import blockcypher

from logger import logger

genesis_time = 1231006505


async def touch_time(time):
    f = open(os.getcwd() + "/BLOCK_TIME", "w")
    f.write("" + str(time) + "\n")
    f.close()


def move_block_time():
    try:
        shutil.move(os.getcwd() + "/BLOCK_TIME", os.getcwd() + "/OLD_BLOCK_TIME")
    except Exception:
        logger.info("moveblock_time() failed!")
        touch_time()
        pass


def get_millis():
    global millis
    millis = int(round(time.time() * 1000))
    return millis


def get_seconds():
    global seconds
    seconds = int(round(time.time()))
    return seconds


def blockcypher_height():
    try:
        # block_cypher = blockcypher.get_latest_blockcypher_height(coin_symbol='btc')
        block_cypher = blockcypher.get_latest_blockcypher_height()
        blockcypher_height = repr(block_cypher)
        f = open("BLOCK_TIME", "w")
        f.write("" + blockcypher_height + "\n")
        f.close()
        return int(blockcypher_height)
    except Exception:
        return 0
        pass


def btc_time():
    # TODO: ADD AS MANY SOURCES FOR btc_time() AS POSSIBLE!!!
    mempool_loop = asyncio.new_event_loop()
    BTC_TIME = mempool_loop.run_until_complete(mempool_height())
    # assert int(BTC_TIME) >= int(blockcypher_height())
    return int(BTC_TIME)


def btc_unix_time_millis():
    global SESSION_ID
    SESSION_ID = str(btc_time()) + ":" + str(get_millis())
    f = open("SESSION_ID", "w")
    f.write("" + SESSION_ID + "\n")
    f.close()
    f = open("SESSION_ID.lock", "w")
    f.write("" + SESSION_ID + "\n")
    f.close()
    return SESSION_ID


def BTC_UNIX_TIME_SECONDS():
    return str(btc_time()) + ":" + str(get_seconds())


def unix_time_millis():
    global unix_time_millis
    unix_time_millis = str(get_millis())
    return unix_time_millis


def UNIX_TIME_SECONDS():
    global unix_time_seconds
    unix_time_seconds = str(get_seconds())
    return unix_time_seconds


def NETWORK_MODULUS():
    # internal time stamping mechanism
    # rolling deterministic time field:
    # (current_time - genesis time) yields time from bitcoin genesis block
    # we use the current block height to calculate a modulus
    # source of deterministic entropy
    # get_millis() is known to the GPGS and GPGR
    # GENESIS_TIME is well known
    # btc_time() block height message was contructed is known to GPGR and GPGS
    # TODO: add functions to reconstruct :WEEBLE:WOBBLE: based on these values
    NETWORK_MODULUS = (get_millis() - genesis_time) % btc_time()
    f = open("NETWORK_MODULUS", "w")
    f.write("" + str(NETWORK_MODULUS) + "\n")
    f.close()
    return NETWORK_MODULUS


def NETWORK_WEEBLE_WOBBLE():
    # :WEEBLE:WOBBLE: construction
    NETWORK_WEEBLE_WOBBLE = str(
        ":" + str(NETWORK_WEEBLE()) + ":" + str(NETWORK_WOBBLE()) + ":"
    )
    f = open("NETWORK_WEEBLE_WOBBLE", "w")
    f.write("" + str(NETWORK_WEEBLE_WOBBLE) + "\n")
    f.close()
    return NETWORK_WEEBLE_WOBBLE


def NETWORK_WEEBLE():
    # (current_time - genesis time) yields time from bitcoin genesis block
    # dividing by number of blocks yields an average time per block
    NETWORK_WEEBLE = int((get_millis() - genesis_time) / btc_time())
    f = open("NETWORK_WEEBLE", "w")
    f.write("" + str(NETWORK_WEEBLE) + "\n")
    f.close()
    return NETWORK_WEEBLE


def NETWORK_WOBBLE():
    # wobble is the remainder of the weeble_wobble calculation
    # source of deterministic entropy
    NETWORK_WOBBLE = str(float((get_millis() - genesis_time) / btc_time() % 1)).strip(
        "0."
    )
    f = open("NETWORK_WOBBLE", "w")
    f.write("" + str(NETWORK_WOBBLE) + "\n")
    f.close()
    return int(NETWORK_WOBBLE)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def mempool_height():
    async with aiohttp.ClientSession() as session:
        url = "https://mempool.space/api/blocks/tip/height"
        height = await fetch(session, url)
        return height


loop = asyncio.new_event_loop()
# loop = asyncio.get_event_loop()
loop.run_until_complete(mempool_height())
loop.run_until_complete(touch_time(btc_time()))

logger.info(":NETWORK_MODULUS:" + str(NETWORK_MODULUS()) + ":")
logger.info(":NETWORK_WEEBLE:" + str(NETWORK_WEEBLE()) + ":")
logger.info(":NETWORK_WOBBLE:" + str(NETWORK_WOBBLE()) + ":")
logger.info(":NETWORK_WEEBLE_WOBBLE" + str(NETWORK_WEEBLE_WOBBLE()))
