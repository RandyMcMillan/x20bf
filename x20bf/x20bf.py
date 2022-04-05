#######################################################################################################################
# Author: Maurice Snoeren                                                                                             #
# Version: 0.1 beta (use at your own risk)                                                                            #
#                                                                                                                     #
# This example show how to derive a own Node class (MyOwnPeer2PeerNode) from p2pnet.Node to implement your own Node   #
# implementation. See the MyOwnPeer2PeerNode.py for all the details. In that class all your own application specific  #
# details are coded.                                                                                                  #
#######################################################################################################################
import time
import datetime
import sys
import asyncio
from TimeNode import TimeNode, network_weeble, network_wobble
from TimeNode import mempool_height
from TimeNode import ripe_node_id
from TimeNode import node_callback
from TimeNode import get_nanos, get_millis, get_seconds, genesis_time


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
                "Event/{}/{}/{}/{}".format(
                    event, main_node.id, connected_node.id, data
                )
            )

    except Exception as e:
        print(e)


# test find_free_port in TimeNode.py
node_0 = TimeNode("127.0.0.1", 0, str(datetime.datetime.now()), callback=test_node_callback)
node_1 = TimeNode("127.0.0.1", 8001, str(datetime.datetime.now()), callback=test_node_callback)
node_2 = TimeNode("127.0.0.1", 8002, str(datetime.datetime.now()), callback=test_node_callback)
node_3 = TimeNode("127.0.0.1", 8003, str(datetime.datetime.now()), callback=test_node_callback)

time_node_1 = TimeNode("127.0.0.1", 8383, str(get_millis()), callback=test_node_callback)
time_node_2 = TimeNode("127.0.0.1", 8384, str(get_millis()), callback=test_node_callback)

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

loop = asyncio.new_event_loop()


time_node_1.send_to_nodes({"/":
                           loop.run_until_complete(mempool_height()),
                           "/genesis_time/":
                           genesis_time(),
                           "/weeble/":
                           network_weeble(),
                           "/wobble/":
                           network_wobble(),
                           "/nanos/":
                           get_nanos()}
                          )
time_node_1.send_to_nodes({"/millis/": get_millis(),
                           "/seconds/": get_seconds()}
                          )

time_node_2.send_to_nodes({"/":
                           loop.run_until_complete(mempool_height()),
                           "/genesis_time/":
                           genesis_time(),
                           "/weeble/":
                           network_weeble(),
                           "/wobble/":
                           network_wobble(),
                           "/nanos/":
                           get_nanos()}
                          )
time_node_2.send_to_nodes({"/millis/":
                           get_millis(),
                           "/seconds/":
                           get_seconds()}
                          )

node_1.send_to_nodes({"/":
                      loop.run_until_complete(mempool_height()),
                      "/genesis_time/":
                      genesis_time(),
                      "/nanos/":
                      get_nanos()}
                     )
node_1.send_to_nodes({"/millis/":
                      get_millis(),
                      "/seconds/":
                      get_seconds(),
                      "/weeble/":
                      network_weeble(),
                      "/wobble/":
                      network_wobble()}
                     )

node_2.send_to_nodes({"/":
                      loop.run_until_complete(mempool_height()),
                      "/genesis_time/":
                      genesis_time(),
                      "/nanos/":
                      get_nanos()}
                     )
node_2.send_to_nodes({"/millis/":
                      get_millis(),
                      "/seconds/":
                      get_seconds(),
                      "/weeble/":
                      network_weeble(),
                      "/wobble/":
                      network_wobble()}
                     )

node_3.send_to_nodes({"/":
                      loop.run_until_complete(mempool_height()),
                      "/genesis_time/":
                      genesis_time(),
                      "/nanos/":
                      get_nanos()}
                     )
node_3.send_to_nodes({"/millis/":
                      get_millis(),
                      "/seconds/":
                      get_seconds(),
                      "/weeble/":
                      network_weeble(),
                      "/wobble/":
                      network_wobble()}
                     )

time.sleep(5)

node_1.stop()
node_2.stop()
node_3.stop()
time_node_1.stop()
time_node_2.stop()
print("end test")
