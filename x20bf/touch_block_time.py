#!/usr/bin/env python3
import asyncio
import time

import blockcypher

from logger import logger
from mempool_height import mempool_height

LOGGER = True

millis = int(round(time.time() * 1000))
seconds = int(round(time.time()))

try:
    block_time = blockcypher.get_latest_block_height(coin_symbol="btc")
    block_height = repr(block_time)
    f = open("BLOCKCYPHER_HEIGHT", "w")
    f.write("" + block_height + "\n")
    f.close()
    if LOGGER:
        logger.info(block_time)
        logger.info(block_height)
except Exception:
    loop = asyncio.new_event_loop()
    block_height = loop.run_until_complete(mempool_height())
    if LOGGER:
        logger.info(str(block_height))
    f = open("MEMPOOL_SPACE_HEIGHT", "w")
    f.write("" + block_height + "\n")
    f.close()
    pass
# TODO: add more redundant block height checks
