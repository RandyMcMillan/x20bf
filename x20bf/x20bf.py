#######################################################################################################################
# Author: Maurice Snoeren                                                                                             #
# Version: 0.1 beta (use at your own risk)                                                                            #
#                                                                                                                     #
# This example show how to derive a own Node class (MyOwnPeer2PeerNode) from p2pnet.Node to implement your own Node   #
# implementation. See the MyOwnPeer2PeerNode.py for all the details. In that class all your own application specific  #
# details are coded.                                                                                                  #
#######################################################################################################################
import time
import sys
from TimeNode import TimeNode

sys.path.insert(0, "../x20bf")
sys.path.insert(1, "../x20bf/depends/p2p")
sys.path.insert(2, "../x20bf/depends/p2p/p2pnetwork")

# import x20bf.depends.p2p.p2pnetwork.node as node
# from x20bf.depends.p2p.p2pnetwork.node import Node


time_node_1 = TimeNode("127.0.0.1", 8383)
time_node_2 = TimeNode("127.0.0.1", 8384)

node_1 = TimeNode("127.0.0.1", 8001)
node_2 = TimeNode("127.0.0.1", 8002)
node_3 = TimeNode("127.0.0.1", 8003)

time.sleep(1)

time_node_1.start()
time_node_2.start()
node_1.start()
node_2.start()
node_3.start()

time.sleep(1)

node_1.connect_with_node("127.0.0.1", 8002)
node_2.connect_with_node("127.0.0.1", 8003)
node_3.connect_with_node("127.0.0.1", 8002)
time_node_1.connect_with_node("127.0.0.1", 8384)
time_node_2.connect_with_node("127.0.0.1", 8383)

time.sleep(2)

node_1.send_to_nodes({"name": "Maurice", "number": 11})

time.sleep(5)

node_1.stop()
node_2.stop()
node_3.stop()
time_node_1.stop()
time_node_2.stop()
print("end test")
