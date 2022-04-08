import asyncio

# from logger import logger
import hashlib
import socket

# import os
# import shutil
import sys
import time
from contextlib import closing
from decimal import getcontext
from math import floor as floor

import aiohttp
import blockcypher
import mpmath

sys.path.insert(0, "../x20bf")
sys.path.insert(1, "../x20bf/depends/p2p")
sys.path.insert(2, "../x20bf/depends/p2p/p2pnetwork")
from x20bf.depends.p2p.p2pnetwork.node import Node


async def fetch(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except aiohttp.client_exceptions.ServerDisconnectedError:
        pass


async def mempool_height():
    async with aiohttp.ClientSession() as session:
        url = "https://mempool.space/api/blocks/tip/height"
        height = await fetch(session, url)
        return height


def ripe_node_id(id):
    print(ripe_node_id.__name__)
    ripe_id = hashlib.new("ripemd160")
    ripe_id.update(bytes(id, "utf-8"))
    return ripe_id.hexdigest()


def node_callback(event, main_node, connected_node, data):
    print(node_callback.__name__)
    try:
        if (
            event != "node_request_to_stop"
        ):  # node_request_to_stop does not have any connected_node, while it is the main_node that is stopping!
            print(
                "Event: {} from main node {}: connected node {}: {}".format(
                    event, main_node.id, connected_node.id, data
                )
            )
        ripe_id = hashlib.new("ripemd160")
        ripe_id.update(bytes(id, "utf-8"))
        return ripe_id.hexdigest()

    except Exception as e:
        print(e)
        return e  # probably bad TODO: handle this much better


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
    print(btc_time.__name__)
    # TODO: ADD AS MANY SOURCES FOR btc_time() AS POSSIBLE!!!
    # mempool_loop = asyncio.new_event_loop()
    BTC_TIME = mempool_height()  # mempool_loop.run_until_complete(mempool_height())
    # assert int(BTC_TIME) >= int(blockcypher_height())
    return int(BTC_TIME)


def btc_unix_time_millis():
    print(btc_unix_time_millis.__name__)
    global SESSION_ID
    SESSION_ID = str(mempool_height()) + ":" + str(get_millis())
    f = open("SESSION_ID", "w")
    f.write("" + SESSION_ID + "\n")
    f.close()
    f = open("SESSION_ID.lock", "w")
    f.write("" + SESSION_ID + "\n")
    f.close()
    return SESSION_ID


def btc_unix_time_seconds():
    print(btc_unix_time_seconds.__name__)
    return str(mempool_height()) + ":" + str(get_seconds())


def unix_time_millis():
    global unix_time_millis
    print(unix_time_millis.__name__)
    unix_time_millis = str(get_millis())
    return unix_time_millis


def unix_time_seconds():
    global unix_time_seconds
    print(unix_time_seconds.__name__)
    unix_time_seconds = str(get_seconds())
    return unix_time_seconds


async def network_modulus():
    print(network_modulus.__name__)
    # internal time stamping mechanism
    # rolling deterministic time field:
    # (current_time - genesis time) yields time from bitcoin genesis block
    # we use the current block height to calculate a modulus
    # source of deterministic entropy
    # get_millis() is known to the GPGS and GPGR
    # GENESIS_TIME is well known
    # mempool_height() block height message was contructed is known to GPGR and GPGS
    # TODO: add functions to reconstruct :WEEBLE:WOBBLE: based on these values
    # NETWORK_MODULUS = (get_millis() - genesis_time()) % mempool_height()
    NETWORK_MODULUS = (get_nanos() - genesis_time()) % mempool_height()
    f = open("NETWORK_MODULUS", "w")
    f.write("" + str(NETWORK_MODULUS) + "\n")
    f.close()
    return NETWORK_MODULUS


async def network_weeble_wobble():
    print(network_weeble_wobble.__name__)
    # :WEEBLE:WOBBLE: construction
    NETWORK_WEEBLE_WOBBLE = str(
        ":" + str(network_weeble()) + ":" + str(network_wobble()) + ":"
    )
    # f = open("NETWORK_WEEBLE_WOBBLE", "w")
    # f.write("" + str(network_weeble_wobble) + "\n")
    # f.close()
    return NETWORK_WEEBLE_WOBBLE


async def network_weeble():
    print(network_weeble.__name__)
    # (current_time - genesis time) yields time from bitcoin genesis block
    # dividing by number of blocks yields an average time per block
    # NETWORK_WEEBLE = int((get_millis() - genesis_time()) / mempool_height())
    # asyncio.create_task(mempool_height())
    height = await mempool_height()
    print(type(height))
    print(type(get_nanos()))
    print(type(genesis_time()))
    NETWORK_WEEBLE = int((get_nanos() - genesis_time()) / int(height))
    # f = open("NETWORK_WEEBLE", "w")
    # f.write("" + str(NETWORK_WEEBLE) + "\n")
    # f.close()
    return NETWORK_WEEBLE


async def network_wobble():
    print(network_wobble.__name__)
    # wobble is the remainder of the weeble_wobble calculation
    # source of deterministic entropy
    # NETWORK_WOBBLE = str(float((get_millis() - genesis_time()) / mempool_height() % 1)).strip(
    height = await mempool_height()
    print(type(height))
    print(type(get_nanos()))
    print(type(genesis_time()))
    NETWORK_WOBBLE = str(float((get_nanos() - genesis_time()) / int(height) % 1)).strip(
        "0."
    )
    f = open("NETWORK_WOBBLE", "w")
    f.write("" + str(NETWORK_WOBBLE) + "\n")
    f.close()
    return int(NETWORK_WOBBLE)


def get_nanos():
    print(get_nanos.__name__)
    getcontext().prec = 50
    mpmath.mp.dps = 50
    global nanos
    # capture float nanosecond time
    # other wise it will be rounded to millis seconds + 000 zeros
    nanos = float(time.time_ns())
    # test_nanos_percision(nanos)
    # test_millis_percision(nanos)
    print(type(nanos))
    return int(mpmath.mpf(nanos))


def get_millis():
    print(get_millis.__name__)
    global millis
    millis = int(floor(get_nanos() / 1000))
    # test_nanos_percision(millis)
    # test_millis_percision(millis)
    print(get_millis.__name__)
    print(type(millis))
    return millis


def get_seconds():
    print(get_seconds.__name__)
    global seconds
    seconds = int(round(time.time()))
    print(get_seconds.__name__)
    print(type(seconds))
    return seconds


def genesis_time():
    print(genesis_time.__name__)
    return int(1231006505)


def find_free_port():
    print(find_free_port.__name__)
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


class TimeNode(Node):

    # Python class constructor
    def __init__(self, host, port=None, id=None, callback=None, max_connections=0):
        if port == 0:
            port = find_free_port()
        super(TimeNode, self).__init__(host, port, id, callback, max_connections)
        self.port = port
        self.genesis = genesis_time()
        self.ripe_id = ripe_node_id
        self.loop = asyncio.new_event_loop()
        print("TimeNode:" + str(self.ripe_id(id)) + " Started")

    # all the methods below are called when things happen in the network.
    # implement your network node behavior to create the required functionality.

    def outbound_node_connected(self, node):
        print(
            "outbound_node_connected ("
            + self.ripe_id(self.id)
            + "): "
            + self.ripe_id(node.id)
        )

    def inbound_node_connected(self, node):
        print(
            "inbound_node_connected: ("
            + self.ripe_id(self.id)
            + "): "
            + self.ripe_id(node.id)
        )

    def inbound_node_disconnected(self, node):
        print(
            "inbound_node_disconnected: ("
            + self.ripe_id(self.id)
            + "): "
            + self.ripe_id(node.id)
        )

    def outbound_node_disconnected(self, node):
        print(
            "outbound_node_disconnected: ("
            + self.ripe_id(self.id)
            + "): "
            + self.ripe_id(node.id)
        )

    def node_message(self, node, data):
        print(
            "node_message ("
            + self.ripe_id(self.id)
            + ") from "
            + self.ripe_id(node.id)
            + ": "
            + str(data)
        )

    def node_disconnect_with_outbound_node(self, node):
        print(
            "node wants to disconnect with oher outbound node: ("
            + self.ripe_id(self.id)
            + "): "
            + self.ripe_id(node.id)
        )

    def node_request_to_stop(self):
        print("node is requested to stop (" + self.ripe_id(self.id) + "): ")
