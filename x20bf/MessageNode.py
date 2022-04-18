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

import hashlib
import json
import sys
import time
from base64 import b64decode, b64encode

sys.path.insert(0, "../x20bf")
sys.path.insert(1, "../x20bf/depends/p2p")
sys.path.insert(2, "../x20bf/depends/p2p/p2pnetwork")
from x20bf.depends.p2p.p2pnetwork.node import Node


async def fetch(session, url):
    async with session.get(url) as response:
        try:
            height = await response.text()
            print(type(height))
            return height.strip('\'')
        # except aiohttp.ServerDisconnectedError:
        except:
            try:
                height = await blockcypher_height()
                return height
            except:
                pass
                return 1


async def mempool_height():
    async with aiohttp.ClientSession() as session:
        url = "https://mempool.space/api/blocks/tip/height"
        height = await fetch(session, url)
        return int(height.strip('\''))


def ripe_node_id(id):
    ripe_id = hashlib.new("ripemd160")
    ripe_id.update(bytes(id, "utf-8"))
    return ripe_id.hexdigest()


def node_callback(event, main_node, connected_node, data):
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
        blockcypher_height = repr(block_cypher.strip('\''))
        # f = open("BLOCK_TIME", "w")
        # f.write("" + blockcypher_height + "\n")
        # f.close()
        return int(blockcypher_height)
    except Exception:
        return 1
        pass


def btc_time():
    # TODO: ADD AS MANY SOURCES FOR btc_time() AS POSSIBLE!!!
    # mempool_loop = asyncio.new_event_loop()
    BTC_TIME = mempool_height()  # mempool_loop.run_until_complete(mempool_height())
    # assert int(BTC_TIME) >= int(blockcypher_height())
    return int(BTC_TIME)


def btc_unix_time_millis():
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
    return str(mempool_height()) + ":" + str(get_seconds())


def unix_time_millis():
    global unix_time_millis
    unix_time_millis = str(get_millis())
    return unix_time_millis


def unix_time_seconds():
    global unix_time_seconds
    unix_time_seconds = str(get_seconds())
    return unix_time_seconds


async def network_modulus():
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
    # :WEEBLE:WOBBLE: construction
    NETWORK_WEEBLE_WOBBLE = str(
        ":" + str(network_weeble()) + ":" + str(network_wobble()) + ":"
    )
    # f = open("NETWORK_WEEBLE_WOBBLE", "w")
    # f.write("" + str(network_weeble_wobble) + "\n")
    # f.close()
    return NETWORK_WEEBLE_WOBBLE


async def network_weeble():
    # (current_time - genesis time) yields time from bitcoin genesis block
    # dividing by number of blocks yields an average time per block
    # NETWORK_WEEBLE = int((get_millis() - genesis_time()) / mempool_height())
    # asyncio.create_task(mempool_height())
    height = await mempool_height()
    NETWORK_WEEBLE = int((get_nanos() - genesis_time()) / height)
    # f = open("NETWORK_WEEBLE", "w")
    # f.write("" + str(NETWORK_WEEBLE) + "\n")
    # f.close()
    return NETWORK_WEEBLE


async def network_wobble():
    # wobble is the remainder of the weeble_wobble calculation
    # source of deterministic entropy
    # NETWORK_WOBBLE = str(float((get_millis() - genesis_time()) / mempool_height() % 1)).strip(
    height = await mempool_height()
    network_wobble = str(float((get_nanos() - genesis_time()) / height % 1)).strip(
        "0."
    )
    f = open("NETWORK_WOBBLE", "w")
    f.write("" + str(network_wobble) + "\n")
    f.close()
    return network_wobble


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


def genesis_time():
    return 1231006505

def genesis_time_millis():
    return 1231006505*1000

def genesis_time_nanos():
    return 1231006505*1000*1000


def find_free_port():
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
        self.discovery_messages = {}
        self.rsa_key = None

    def node_message(self, connected_node, message):
        """node_message is overridden to provide open text communication with
        hashing for message integrity. The message is sent by using a dict data structure.
        The NodeConnection class already converts this back to a dict structure in this method.
        The check is performed by check_message, see the documentation there. When the message is valid, it will be
        processed. The field '_type' determines the packet type. Currently the following packets are implemented:
          ping: The ping packet is send by a node to check the connection and latency.
          pong: The pong packet is the reply that is send based an a ping packet.
          discovery: The discovery packet is send to discover the connection list of a connecting node.
          discovery_answer: The answer of a node to a discovery packet that holds its list of connecting nodes."""
        # try:
        print("node_message from " + connected_node.id + ": " + str(message))

        if self.check_message(message):
            if "_type" in message:
                if message["_type"] == "ping":
                    self.received_ping(connected_node, message)

                elif message["_type"] == "pong":
                    self.received_pong(connected_node, message)

                elif message["_type"] == "discovery":
                    self.received_discovery(connected_node, message)

                elif message["_type"] == "discovery_answer":
                    self.received_discovery_answer(connected_node, message)

                else:
                    self.debug_print(
                        "node_message: message type unknown: "
                        + connected_node.id
                        + ": "
                        + str(message)
                    )

        else:
            print("Received message is corrupted and cannot be processed!")





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

    def node_message(self, connected_node, message):
        """node_message is overridden to provide secure communication using hashing and signing. The message has been
        send by using a dict data structure. The NodeConnection class already converts this back to a dict structure
        in this method.
        The check is performed by check_message, see the documentation there. When the message is valid, it will be
        processed. The field '_type' determines the packet type. Currently the following packets are implemented:
          ping: The ping packet is send by a node to check the connection and latency.
          pong: The pong packet is the reply that is send based an a ping packet.
          discovery: The discovery packet is send to discover the connection list of a connecting node.
          discovery_answer: The answer of a node to a discovery packet that holds its list of connecting nodes."""
        # try:
        print("node_message from " + connected_node.id + ": " + str(message))

        if self.check_message(message):
            if "_type" in message:
                if message["_type"] == "ping":
                    self.received_ping(connected_node, message)

                elif message["_type"] == "pong":
                    self.received_pong(connected_node, message)

                elif message["_type"] == "discovery":
                    self.received_discovery(connected_node, message)

                elif message["_type"] == "discovery_answer":
                    self.received_discovery_answer(connected_node, message)

                else:
                    self.debug_print(
                        "node_message: message type unknown: "
                        + connected_node.id
                        + ": "
                        + str(message)
                    )

        else:
            print("Received message is corrupted and cannot be processed!")

    def create_message(self, data):
        """This method creates the message based on the Python dict data variable to be sent to other nodes. Some data
        is added to the data, like the id, timestamp, message is and hash of the message. In order to check the
        message validity when a node receives it, the message is hashed and signed. The method returns a string
        of the data in JSON format, so it can be send immediatly to the node. The public key is also part of the
        communication packet."""
        for el in [
            "_id",
            "_timestamp",
            "_message_id",
            "_hash",
            "_signature",
            "_public_key",
        ]:  # Clean up the data, to make sure we calculatie the right things!
            if el in data:
                del data[el]

        try:
            data["_mcs"] = self.message_count_send
            data["_mcr"] = self.message_count_recv
            data["_id"] = self.id
            data["_timestamp"] = time.time()
            data["_message_id"] = self.get_hash(data)

            self.debug_print("Message creation:")
            self.debug_print(
                "Message hash based on: " + self.get_data_uniq_string(data)
            )

            data["_hash"] = self.get_hash(data)

            self.debug_print(
                "Message signature based on: " + self.get_data_uniq_string(data)
            )

            data["_signature"] = self.sign_data(data)
            data["_public_key"] = self.get_public_key().decode("utf-8")

            self.debug_print("_hash: " + data["_hash"])
            self.debug_print("_signature: " + data["_signature"])
            self.debug_print("_public_key: " + data["_public_key"])

            return data

        except Exception as e:
            self.debug_print("SecureNode: Failed to create message " + str(e))

    def check_message(self, data):
        """When a message is received it is hashed and signed by the sending node. This method checks the hash
        and signature of the message. When the signature, data hash and message id is correct, the method
        returns True otherwise False.
        TODO: if a node is known, the public key should be stored, so this could not be changed by the
        node in the future. That is more safe. Maybe the public key should be exchanged prior."""
        self.debug_print("Incoming message information:")
        self.debug_print("_hash: " + data["_hash"])
        self.debug_print("_signature: " + data["_signature"])

        signature = data["_signature"]
        public_key = data["_public_key"]
        data_hash = data["_hash"]
        message_id = data["_message_id"]
        timestamp = data["_timestamp"]

        # 1. Check the signature!
        del data["_public_key"]
        del data["_signature"]
        checkSignature = self.verify_data(data, public_key, signature)

        # 2. Check the hash of the data
        del data["_hash"]
        checkDataHash = self.get_hash(data) == data_hash

        # 3. Check the message id
        del data["_message_id"]
        checkMessageId = self.get_hash(data) == message_id

        # 4. Restore the data
        data["_signature"] = signature
        data["_public_key"] = public_key
        data["_hash"] = data_hash
        data["_message_id"] = message_id
        data["_timestamp"] = timestamp

        self.debug_print("Checking incoming message:")
        self.debug_print(" signature : " + str(checkSignature))
        self.debug_print(" data hash : " + str(checkDataHash))
        self.debug_print(" message id: " + str(checkMessageId))

        return checkSignature and checkDataHash and checkMessageId

    def send_message(self, message):
        """This method sends a string to all the nodes in the format {"message": message}. It uses also
        the create_message method in order to hash and sign the message as well."""
        self.send_to_nodes(
            self.create_message({"_type": "message", "message": message})
        )

    #######################################################
    # Hashing of Python variables methods                 #
    #######################################################

    def get_data_uniq_string(self, data):
        """This function makes sure that a complex dict variable (consisting of other dicts and lists,
        is converted to a unique string that can be hashed. Every data object that contains the same
        values, should result into the dame unique string."""
        return json.dumps(data, sort_keys=True)

    def get_hash(self, data):
        """Returns the hased version of the data dict. The dict can contain lists and dicts, but it must
        be based as dict."""
        try:
            h = hashlib.sha512()
            message = self.get_data_uniq_string(data)

            self.debug_print("Hashing the data:")
            self.debug_print("Message: " + message)

            h.update(message.encode("utf-8"))

            self.debug_print("Hash of the message: " + h.hexdigest())

            return h.hexdigest()

        except Exception as e:
            print("Failed to hash the message: " + str(e))

    def send_discovery(self):
        """Send the discovery packet to all the connected nodes.
        TODO: Improve discovery information that is send back by the nodes."""
        self.send_to_nodes(
            self.create_message(
                {"_type": "discovery", "id": self.id, "timestamp": time.time()}
            )
        )

    def send_discovery_answer(self, node, data):
        """Send the discovery_answer packet to a specific node (mostly were we received a discovery packet
        from). This packet contains a list of all the nodes with which we have a connection with."""
        nodes = []
        for n in self.nodes_inbound:
            nodes.append(
                {
                    "id": n.id,
                    "ip": n.host,
                    "port": n.main_node.port,
                    "connection": "inbound",
                }
            )
        for n in self.nodes_outbound:
            nodes.append(
                {"id": n.id, "ip": n.host, "port": n.port, "connection": "outbound"}
            )

        node.send(
            self.create_message(
                {
                    "id": data["id"],
                    "_type": "discovery_answer",
                    "timestamp": data["timestamp"],
                    "nodes": nodes,
                }
            )
        )

    def received_discovery(self, node, data):
        """This method processes the discovery packet and send back a discover_anwser_message with the details
        and relay it to the other hosts, when I got the answers from them  send it through. This means i
        need to administer these messages as well to relay it back."""
        if data["id"] in self.discovery_messages:
            self.debug_print(
                "discovery_message: message already received, so not sending it"
            )

        else:
            self.debug_print("discovery_message: process message")
            self.discovery_messages[data["id"]] = node
            self.send_discovery_answer(node, data)
            self.send_to_nodes(
                self.create_message(
                    {
                        "_type": "discovery",
                        "id": data["id"],
                        "timestamp": data["timestamp"],
                    }
                ),
                [node],
            )

    def received_discovery_answer(self, node, data):
        """This method processes the discovery_answer packet. In the case it is not mine, the packet is relayed
        to the correct node. Nothing is done with this information.
        TODO: A method to process this information should be invoked."""
        if data["id"] in self.discovery_messages:  # needs to be relayed
            self.send_discovery_answer(self.discovery_messages[data["id"]], data)

        else:
            if data["id"] == self.id:
                self.debug_print(
                    "discovery_message_answer: This is for me!: "
                    + str(data)
                    + ":"
                    + str(time.time() - data["timestamp"])
                )

            else:
                self.debug_print("unknwon state!")

    def node_disconnect_with_outbound_node(self, node):
        print(
            "node wants to disconnect with oher outbound node: ("
            + self.ripe_id(self.id)
            + "): "
            + self.ripe_id(node.id)
        )

    def node_request_to_stop(self):
        print("node is requested to stop (" + self.ripe_id(self.id) + "): ")
