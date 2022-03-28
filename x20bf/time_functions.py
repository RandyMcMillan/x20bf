#!/usr/bin/env python3
import asyncio
import os
import shutil
import time
from math import floor as floor
import mpmath
from decimal import getcontext

import aiohttp
import blockcypher

from x20bf.logger import logger

genesis_time = 1231006505


def test_nanos_percision(nanos):
    getcontext().prec = 50
    mpmath.mp.dps = 50
    print("nanos = " + str(nanos))
    print(" mpmath.mpf(nanos): {0}".format(mpmath.mpf(nanos)))
    print(" mpmath.sqrt(nanos): {0}".format(mpmath.sqrt(nanos)))
    print("What is returned from thee get_nanos() function...")
    print(" int(mpmath.mpf(nanos)): {0}".format(int(mpmath.mpf(nanos))))


def test_millis_percision(nanos):
    getcontext().prec = 50
    mpmath.mp.dps = 50
    print("nanos = " + str(nanos))
    print(" mpmath.mpf(nanos): {0}".format(mpmath.mpf(nanos)))
    print(" mpmath.sqrt(nanos): {0}".format(mpmath.sqrt(nanos)))
    print("What is returned from thee get_millis() function...")
    print(" int(mpmath.mpf(nanos)): {0}".format(int(mpmath.mpf(nanos))))


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


def get_nanos():
    getcontext().prec = 50
    mpmath.mp.dps = 50
    global nanos
    # capture float nanosecond time
    # other wise it will be rounded to millis seconds + 000 zeros
    nanos = float(time.time_ns())
    # test_nanos_percision(nanos)
    # test_millis_percision(nanos)
    return int(mpmath.mpf(nanos))


def get_millis():
    global millis
    millis = int(floor(get_nanos() / 1000))
    # test_nanos_percision(millis)
    # test_millis_percision(millis)
    return millis


def get_seconds():
    global seconds
    seconds = int(round(time.time()))
    return seconds


async def blockcypher_height():
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


def btc_unix_time_seconds():
    return str(btc_time()) + ":" + str(get_seconds())


def unix_time_millis():
    global unix_time_millis
    unix_time_millis = str(get_millis())
    return unix_time_millis


def unix_time_seconds():
    global unix_time_seconds
    unix_time_seconds = str(get_seconds())
    return unix_time_seconds


def network_modulus():
    # internal time stamping mechanism
    # rolling deterministic time field:
    # (current_time - genesis time) yields time from bitcoin genesis block
    # we use the current block height to calculate a modulus
    # source of deterministic entropy
    # get_millis() is known to the GPGS and GPGR
    # GENESIS_TIME is well known
    # btc_time() block height message was contructed is known to GPGR and GPGS
    # TODO: add functions to reconstruct :WEEBLE:WOBBLE: based on these values
    # NETWORK_MODULUS = (get_millis() - genesis_time) % btc_time()
    NETWORK_MODULUS = (get_nanos() - genesis_time) % btc_time()
    f = open("NETWORK_MODULUS", "w")
    f.write("" + str(NETWORK_MODULUS) + "\n")
    f.close()
    return NETWORK_MODULUS


def network_weeble_wobble():
    # :WEEBLE:WOBBLE: construction
    NETWORK_WEEBLE_WOBBLE = str(
        ":" + str(network_weeble()) + ":" + str(network_wobble()) + ":"
    )
    f = open("NETWORK_WEEBLE_WOBBLE", "w")
    f.write("" + str(network_weeble_wobble) + "\n")
    f.close()
    return NETWORK_WEEBLE_WOBBLE


def network_weeble():
    # (current_time - genesis time) yields time from bitcoin genesis block
    # dividing by number of blocks yields an average time per block
    # NETWORK_WEEBLE = int((get_millis() - genesis_time) / btc_time())
    NETWORK_WEEBLE = int((get_nanos() - genesis_time) / btc_time())
    f = open("NETWORK_WEEBLE", "w")
    f.write("" + str(NETWORK_WEEBLE) + "\n")
    f.close()
    return NETWORK_WEEBLE


def network_wobble():
    # wobble is the remainder of the weeble_wobble calculation
    # source of deterministic entropy
    # NETWORK_WOBBLE = str(float((get_millis() - genesis_time) / btc_time() % 1)).strip(
    NETWORK_WOBBLE = str(float((get_nanos() - genesis_time) / btc_time() % 1)).strip(
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


def network_time_logger():
    logger.info(":NETWORK_MODULUS:" + str(network_modulus()) + ":")
    logger.info(":NETWORK_WEEBLE:" + str(network_weeble()) + ":")
    logger.info(":NETWORK_WOBBLE:" + str(network_wobble()) + ":")
    logger.info(":NETWORK_WEEBLE_WOBBLE" + str(network_weeble_wobble()))


loop = asyncio.new_event_loop()
# loop = asyncio.get_event_loop()
loop.run_until_complete(mempool_height())
loop.run_until_complete(blockcypher_height())
loop.run_until_complete(touch_time(btc_time()))
