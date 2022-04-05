import asyncio
import os
import shutil
import sys
import time
from decimal import getcontext
from math import floor as floor

import aiohttp
import blockcypher
import mpmath
from logger import logger

sys.path.insert(0, "../x20bf")
sys.path.insert(1, "../x20bf/depends/p2p")
sys.path.insert(2, "../x20bf/depends/p2p/p2pnetwork")


from x20bf.depends.p2p.p2pnetwork.node import Node


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def mempool_height():
    async with aiohttp.ClientSession() as session:
        url = "https://mempool.space/api/blocks/tip/height"
        height = fetch(session, url)
        return height


loop = asyncio.new_event_loop()
# loop = asyncio.get_event_loop()
loop.run_until_complete(mempool_height())
loop.run_until_complete(blockcypher_height())
loop.run_until_complete(touch_time(btc_time()))


class Time(Node):

    # Python class constructor
    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(Time, self).__init__(host, port, id, callback, max_connections)
        self.genesis = 1231006505
        print("Time: Started")

    def unsignedToSigned(n, byte_count):
        return int.from_bytes(
            n.to_bytes(byte_count, "little", signed=False), "little", signed=True
        )

    def signedToUnsigned(n, byte_count):
        return int.from_bytes(
            n.to_bytes(byte_count, "little", signed=True), "little", signed=False
        )

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

    def move_block_time(self):
        try:
            shutil.move(os.getcwd() + "/BLOCK_TIME", os.getcwd() + "/OLD_BLOCK_TIME")
        except Exception:
            logger.info("moveblock_time() failed!")
            self.touch_time()
            pass

    def get_nanos(self):
        getcontext().prec = 50
        mpmath.mp.dps = 50
        global nanos
        # capture float nanosecond time
        # other wise it will be rounded to millis seconds + 000 zeros
        nanos = float(time.time_ns())
        # test_nanos_percision(nanos)
        # test_millis_percision(nanos)
        return int(mpmath.mpf(nanos))

    def get_millis(self):
        global millis
        self.millis = int(floor(self.get_nanos() / 1000))
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
        return str(BTC_TIME)

    def btc_unix_time_millis(self):
        global SESSION_ID
        SESSION_ID = str(self.btc_time()) + "/" + str(self.get_millis())
        f = open("SESSION_ID", "w")
        f.write("" + SESSION_ID + "\n")
        f.close()
        f = open("SESSION_ID.lock", "w")
        f.write("" + SESSION_ID + "\n")
        f.close()
        return SESSION_ID

    def btc_unix_time_seconds(self):
        return str(self.btc_time()) + "/" + str(self.get_seconds())

    def unix_time_millis(self):
        global unix_time_millis
        unix_time_millis = str(self.get_millis())
        return unix_time_millis

    def unix_time_seconds(self):
        global unix_time_seconds
        unix_time_seconds = str(self.get_seconds())
        return unix_time_seconds

    def network_modulus(self):
        # internal time stamping mechanism
        # rolling deterministic time field:
        # (current_time - genesis time) yields time from bitcoin genesis block
        # we use the current block height to calculate a modulus
        # source of deterministic entropy
        # get_millis() is known to the GPGS and GPGR
        # GENESIS_TIME is well known
        # btc_time() block height message was contructed is known to GPGR and GPGS
        # TODO/ add functions to reconstruct /WEEBLE/WOBBLE/ based on these values
        # NETWORK_MODULUS = (get_millis() - genesis_time) % btc_time()
        NETWORK_MODULUS = (self.get_nanos() - self.genesis_time) % self.btc_time()
        f = open("NETWORK_MODULUS", "w")
        f.write("" + str(NETWORK_MODULUS) + "\n")
        f.close()
        return NETWORK_MODULUS

    def network_weeble_wobble():
        # /WEEBLE/WOBBLE/ construction
        NETWORK_WEEBLE_WOBBLE = str(
            "/" + str(self.network_weeble()) + "/" + str(self.network_wobble()) + "/"
        )
        f = open("NETWORK_WEEBLE_WOBBLE", "w")
        f.write("" + str(NETWORK_WEEBLE_WOBBLE) + "\n")
        f.close()
        return NETWORK_WEEBLE_WOBBLE

    def network_weeble(self):
        # (current_time - genesis time) yields time from bitcoin genesis block
        # This is the Bitcoin network age.
        # dividing by number of blocks yields an average time per block
        # We think of the weeble as a minute hand (moving average 10 mins)
        # NETWORK_WEEBLE = int((get_millis() - genesis_time) / btc_time())
        NETWORK_WEEBLE = int((self.get_nanos() - self.genesis_time) / self.btc_time())
        f = open("NETWORK_WEEBLE", "w")
        f.write("" + str(NETWORK_WEEBLE) + "\n")
        f.close()
        return NETWORK_WEEBLE

    def network_wobble(self):
        # wobble is the remainder of the weeble_wobble calculation
        # We think of the wobble as the second hand (nanosecond hand)
        # source of deterministic entropy
        NETWORK_WOBBLE = str(
            float((self.get_nanos() - self.genesis_time) / self.btc_time() % 1)
        ).strip("0.")
        f = open("NETWORK_WOBBLE", "w")
        f.write("" + str(NETWORK_WOBBLE) + "\n")
        f.close()
        return int(NETWORK_WOBBLE)

    def network_time_logger(self):
        logger.info("/NETWORK_MODULUS/" + str(self.network_modulus()) + "/")
        logger.info("/NETWORK_WEEBLE/" + str(self.network_weeble()) + "/")
        logger.info("/NETWORK_WOBBLE/" + str(self.network_wobble()) + "/")
        logger.info("/NETWORK_WEEBLE_WOBBLE/" + str(self.network_weeble_wobble()) + "/")

    # all the methods below are called when things happen in the network.
    # implement your network node behavior to create the required functionality.

    def outbound_node_connected(self, node):
        print("outbound_node_connected (" + self.id + "): " + node.id)

    def inbound_node_connected(self, node):
        print("inbound_node_connected: (" + self.id + "): " + node.id)

    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: (" + self.id + "): " + node.id)

    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: (" + self.id + "): " + node.id)

    def node_message(self, node, data):
        print("node_message (" + self.id + ") from " + node.id + "/ " + str(data))

    def node_disconnect_with_outbound_node(self, node):
        print(
            "node wants to disconnect with oher outbound node: ("
            + self.id
            + "): "
            + node.id
        )

    def node_request_to_stop(self):
        print("node is requested to stop (" + self.id + "): ")
