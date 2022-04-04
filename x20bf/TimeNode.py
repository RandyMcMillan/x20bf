import sys
import hashlib
sys.path.insert(0, "../x20bf")
sys.path.insert(1, "../x20bf/depends/p2p")
sys.path.insert(2, "../x20bf/depends/p2p/p2pnetwork")
from x20bf.depends.p2p.p2pnetwork.node import Node


def ripe_node_id(id):
    ripe_id = hashlib.new("ripemd160")
    ripe_id.update(bytes(id, "utf-8"))
    return str(ripe_id.hexdigest())


class TimeNode(Node):

    # Python class constructor
    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(TimeNode, self).__init__(host, port, id, callback, max_connections)
        print("TimeNode: Started")
        self.ripe_id = ripe_node_id

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
