from logger import logger
from time_functions import btc_time, unix_time_millis
import version as version
from p2pnetwork.node import Node


class NodeInterface(Node):

    # Python class constructor

    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(NodeInterface, self).__init__(
            host, port, id, callback, max_connections
        )
        self.version = version.version()
        self.start_time = str(":" + str(btc_time()) + ":" + str(unix_time_millis()) + ":")
        logger.info("x20bf v" + self.version + " General Purpose Messaging Protocol " + "https://0x20bf.org")
        logger.info(":START_TIME" + self.start_time)

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
