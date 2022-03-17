import asyncio

from p2pnetwork.node import Node

import logger as logger
import version as version
from time_functions import (blockcypher_height, btc_time, genesis_time,
                            get_millis, get_seconds, mempool_height)


class NodeInterface(Node):

    # Python class constructor

    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(NodeInterface, self).__init__(host, port, id, callback, max_connections)
        loop = asyncio.new_event_loop()
        self.logger = logger.logger()

        self.genesis_time = genesis_time
        self.btc_time = btc_time()
        self.get_millis = get_millis()
        self.get_seconds = get_seconds()
        self.mempool_height = loop.run_until_complete(mempool_height())
        self.blockcypher_height = loop.run_until_complete(blockcypher_height())
        self.version = version.version()
        self.start_time = str(":" + str(btc_time()) + ":" + str(get_millis()) + ":")
        self.logger.info(
            "x20bf v"
            + self.version
            + " General Purpose Messaging Protocol "
            + "https://0x20bf.org"
        )
        self.logger.info(":START_TIME" + self.start_time)

    # all the methods below are called when things happen in the network.
    # implement your network node behavior to create the required functionality.
    def network_lag(self):

        loop = asyncio.new_event_loop()

        # TODO: check time_functions - more sources needed
        # if delta > 0 - either service unavailable or lag
        if (
            abs(
                loop.run_until_complete(self.blockcypher_height())
                - loop.run_until_complete(self.mempool_height())
            )
        ) > 0:
            return abs(
                loop.run_until_complete(self.blockcypher_height())
                - loop.run_until_complete(self.mempool_height())
            )

        if (
            abs(
                loop.run_until_complete(self.mempool_height())
                - loop.run_until_complete(self.blockcypher_height())
            )
        ) > 0:
            return abs(
                loop.run_until_complete(self.mempool_height())
                - loop.run_until_complete(self.blockcypher_height())
            )

        return 0

    def outbound_node_connected(self, node):
        print("outbound_node_connected (" + self.id + "): " + node.id)

    def inbound_node_connected(self, node):
        print("inbound_node_connected: (" + self.id + "): " + node.id)

    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: (" + self.id + "): " + node.id)

    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: (" + self.id + "): " + node.id)

    def node_message(self, node, data):
        print("node_message (" + self.id + ") from " + node.id + ": " + str(data))

    def node_disconnect_with_outbound_node(self, node):
        print(
            "node wants to disconnect with oher outbound node: ("
            + self.id
            + "): "
            + node.id
        )

    def node_request_to_stop(self):
        print("node is requested to stop (" + self.id + "): ")
