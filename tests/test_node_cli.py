import getpass
import sys
import datetime
import time

sys.path.insert(0, "../x20bf")
sys.path.insert(1, "../x20bf/depends/p2p")
sys.path.insert(2, "../x20bf/depends/p2p/p2pnetwork")
sys.path.append(".")


from x20bf.MessageNode import (
    MessageNode
)


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


if len(sys.argv) > 1:
    port = int(sys.argv[1])

if len(sys.argv) > 2:
    host = sys.argv[1]
    port = int(sys.argv[2])

# Start the Node
node = MessageNode("127.0.0.1", 0, str(datetime.datetime.now()), callback=test_node_callback)
node.start()
node.debug = False
time.sleep(1)

running = True
while running:
    print("Commands: message, ping, discovery, status, connect, debug, stop")
    s = input("Please type a command:")

    if s == "stop":
        running = False

    elif s == "message":
        node.send_message(input("Message to send:"))

    elif s == "ping":
        node.send_ping()

    elif s == "discovery":
        node.send_discovery()

    elif s == "status":
        node.print_connections()

    elif s == "debug":
        node.debug = not node.debug

    elif s == "connect":
        host = input("host: ")
        port = int(input("port: "))
        node.connect_with_node(host, port)

    else:
        print("Command not understood '" + s + "'")

node.stop()
