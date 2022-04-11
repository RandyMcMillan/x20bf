#######################################################################################################################
# Author: Maurice Snoeren                                                                                             #
# Version: 0.1 beta (use at your own risk)                                                                            #
#                                                                                                                     #
# This example show how to derive a own Node class (MyOwnPeer2PeerNode) from p2pnet.Node to implement your own Node   #
# implementation. See the MyOwnPeer2PeerNode.py for all the details. In that class all your own application specific  #
# details are coded.                                                                                                  #
#######################################################################################################################
import asyncio
import datetime
import sys
import time

from TimeNode import (
    TimeNode,
    genesis_time,
    get_millis,
    get_nanos,
    get_seconds,
    mempool_height,
    network_weeble,
    network_wobble,
    node_callback,
    ripe_node_id,
)

sys.path.insert(0, "../x20bf")
sys.path.insert(1, "../x20bf/depends/p2p")
sys.path.insert(2, "../x20bf/depends/p2p/p2pnetwork")

# import x20bf.depends.p2p.p2pnetwork.node as node
# from x20bf.depends.p2p.p2pnetwork.node import Node


def test_node_callback(event, main_node, connected_node, data):
    try:
        if (
            event != "node_request_to_stop"
        ):  # node_request_to_stop does not have any connected_node, while it is the main_node that is stopping!
            print(
                "Event/{}/{}/{}/{}".format(event, main_node.id, connected_node.id, data)
            )

    except Exception as e:
        print(e)


# test find_free_port in TimeNode.py
node_0 = TimeNode(
    "127.0.0.1", 0, str(datetime.datetime.now()), callback=test_node_callback
)
node_1 = TimeNode(
    "127.0.0.1", 8001, str(datetime.datetime.now()), callback=test_node_callback
)
node_2 = TimeNode(
    "127.0.0.1", 8002, str(datetime.datetime.now()), callback=test_node_callback
)
node_3 = TimeNode(
    "127.0.0.1", 8003, str(datetime.datetime.now()), callback=test_node_callback
)

time_node_1 = TimeNode(
    "127.0.0.1", 8383, str(get_millis()), callback=test_node_callback
)
time_node_2 = TimeNode(
    "127.0.0.1", 8384, str(get_millis()), callback=test_node_callback
)

time.sleep(1)

time_node_1.start()
time_node_2.start()
node_0.start()
node_1.start()
node_2.start()
node_3.start()

time.sleep(1)

node_0.connect_with_node("127.0.0.1", 8001)
node_1.connect_with_node("127.0.0.1", 8002)
node_2.connect_with_node("127.0.0.1", 8003)
node_3.connect_with_node("127.0.0.1", 8383)
time_node_1.connect_with_node("127.0.0.1", 8384)
time_node_2.connect_with_node("127.0.0.1", node_0.port)

time.sleep(2)

loop = asyncio.new_event_loop()


time_node_1.send_to_nodes(
    {
        "/genesis_time/": genesis_time(),
        "/nanos/": get_nanos(),
    }
)

time_node_2.send_to_nodes(
    {
        "/genesis_time/": genesis_time(),
        "/nanos/": get_nanos(),
    }
)

node_1.send_to_nodes(
    {
        "/genesis_time/": genesis_time(),
        "/nanos/": get_nanos(),
    }
)

node_2.send_to_nodes(
    {
        "/genesis_time/": genesis_time(),
        "/nanos/": get_nanos(),
    }
)

node_3.send_to_nodes(
    {
        "/genesis_time/": genesis_time(),
        "/nanos/": get_nanos(),
    }
)

time.sleep(5)

node_0.stop()
node_1.stop()
node_2.stop()
node_3.stop()
time_node_1.stop()
time_node_2.stop()
print("end test")
