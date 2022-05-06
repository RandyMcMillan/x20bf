#!/usr/bin/env python3
# test.py
import sys
import time
import datetime
import asyncio
import itertools as it
import os
import random

sys.path.insert(0, "../x20bf")
sys.path.insert(1, "../x20bf/depends/p2p")
sys.path.insert(2, "../x20bf/depends/p2p/p2pnetwork")

# from x20bf.depends.p2p.p2pnetwork.node import Node
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


async def makeitem(size: int = 5) -> str:
    return os.urandom(size).hex()


async def run(caller=None) -> None:
    i = random.randint(0, 10)
    node_array.append(caller)
    node_shutdown_array.append(caller)
    if caller:
        print(f"{caller} sleeping for {i} seconds.")
        node = MessageNode("127.0.0.1", 0, str(datetime.datetime.now()), callback=test_node_callback)
        node_shutdown_array.append(node)
        node_port_array.append(node.port)
        node_port_array.reverse()
        node.start()
        await asyncio.sleep(i)
        if len(node_array) >= 10:
            node.connect_with_node("127.0.0.1", node_port_array.pop())
            node.send_to_nodes(
                {
                    node.port
                }

            )
    for caller in node_shutdown_array:
        try:
            print(caller)
            print(len(node_shutdown_array))
        except Exception as er:
            print(er)


async def sender(name: int, q: asyncio.Queue) -> None:
    n = random.randint(1, 3)
    for _ in it.repeat(None, n):  # Synchronous loop for each single sender
        run_node = [asyncio.create_task(run())]
        await asyncio.gather(*run_node)
        await q.join()  # Implicitly awaits recievers, too
        for node in run_node:
            await run(caller=f"Sender {name}")
            try:
                q.get_nowait()
            except asyncio.QueueEmpty:
                pass


async def receiver(name: int, q: asyncio.Queue) -> None:
    while True:
        run_node = [asyncio.create_task(run())]
        await q.join()  # Implicitly awaits recievers, too
        for node in run_node:
            await run(caller=f"Reciever {name}")
            i, t = await q.get()
            now = time.perf_counter()
            print(f"Receiver {name} got element <{i}>" f" in {now-t:0.5f} seconds.")
            q.task_done()
        for task in q:
            task.cancel()


async def main(nsend: int, nrecv: int):
    q = asyncio.Queue()
    senders = [asyncio.create_task(sender(n, q)) for n in range(nsend)]
    receivers = [asyncio.create_task(receiver(n, q)) for n in range(nrecv)]
    await asyncio.gather(*senders)
    # await asyncio.gather(*receivers)
    await q.join()  # Implicitly awaits recievers, too
    for c in receivers:
        c.cancel()

if __name__ == "__main__":
    import argparse
    global node
    # default local node port 8383
    # TODO: there will be a mix of service nodes and burst nodes
    # The burst nodes will select a random port
    # The service nodes will use prescribed ports tbd
    node = MessageNode("127.0.0.1", 8383, str(datetime.datetime.now()), callback=test_node_callback)
    global node_array
    global node_port_array
    global node_shutdown_array
    node_array = []
    node_shutdown_array = []
    node_port_array = []
    random.seed(444)
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--nsend", type=int, default=15)
    parser.add_argument("-r", "--nrecv", type=int, default=15)
    ns = parser.parse_args()
    start = time.perf_counter()

    time.sleep(1)

    running = True
    while running:
        print("Commands: run, message, ping, discovery, status, connect, debug, stop")
        s = input("Please type a command:")

        if s == "stop":
            running = False

        elif s == "run":
            asyncio.run(main(**ns.__dict__))

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

    for node in node_shutdown_array:
        try:
            print("node.stop()")
            print(len(node_shutdown_array))
            node.stop()
        except Exception as er:
            print(er)

    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")
