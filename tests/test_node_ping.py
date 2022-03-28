#######################################################################################################################
# Author: Maurice Snoeren                                                                                             #
# Version: 0.1 beta (use at your own risk)                                                                            #
#                                                                                                                     #
# This example show how to create your own peer 2 peer network using the callback. So, you do not need to implement   #
# a new class. However, it is adviced to implement your own class rather than use the callback. Callback will get you #
# a big and large method implementation.                                                                              #
#######################################################################################################################

import sys
import time

sys.path.insert(0, "../x20bf")
sys.path.insert(1, "../x20bf/depends/p2p")

# import x20bf.depends.p2p.p2pnetwork.node as node
# from x20bf.depends.p2p.p2pnetwork.node import Node
# from p2pnetwork.node import Node
# from p2p.node import Node
from x20bf.depends.p2p.p2pnetwork.node import Node

import ping as p
from time_functions import btc_time


# The big callback method that gets all the events that happen inside the p2p network.
# Implement here your own application logic. The event holds the event that occurred within
# the network. The main_node contains the node that is handling the connection with and from
# other nodes. An event is most probably triggered by the connected_node! If there is data
# it is represented by the data variable.
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

    except Exception as e:
        print(e)


# Just for test we spin off multiple nodes, however it is more likely that these nodes are running
# on computers on the Internet! Otherwise we do not have any peer2peer application.
node_1 = Node("127.0.0.1", 8001, callback=node_callback)
node_2 = Node("127.0.0.1", 8002, callback=node_callback)
node_3 = Node("127.0.0.1", 8003, callback=node_callback)


print(btc_time())
time.sleep(1)
# node_1.debug = True
# node_2.debug = True
# node_3.debug = True
node_1.start()
node_2.start()
node_3.start()
time.sleep(1)

node_1.connect_with_node("127.0.0.1", 8002)
node_2.connect_with_node("127.0.0.1", 8003)
node_3.connect_with_node("127.0.0.1", 8001)

time.sleep(2)

node_1.send_to_nodes("message: hoi from node 1")
node_1.send_to_nodes(str(p.btc_time()))
node_1.send_to_nodes(str(btc_time()))

time.sleep(5)

node_1.stop()
node_2.stop()
node_3.stop()

print("end")
