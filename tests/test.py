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
from x20bf.TimeNode import (
    TimeNode,
    genesis_time,
    get_millis,
    get_nanos,
    get_seconds,
    mempool_height,
    network_weeble,
    network_wobble,
    node_callback,
    ripe_node_id
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


async def get_mempool_height():
    return mempool_height()


async def get_genesis_time():
    return genesis_time()


async def get_network_weeble():
    return network_weeble()


async def get_network_wobble():
    return network_wobble()


async def randsleep(caller=None) -> None:
    i = random.randint(0, 60)
    node_array.append(caller)
    node_shutdown_array = node_array
    if caller:
        print(f"{caller} sleeping for {i} seconds.")
        caller = TimeNode("127.0.0.1", 0, str(datetime.datetime.now()), callback=test_node_callback)
        node_port_array.append(caller.port)
        node_port_array.reverse()
        caller.start()
        await asyncio.sleep(3)
        if len(node_array) >= 10:
            caller.connect_with_node("127.0.0.1", node_port_array.pop())
            mempool_height = await get_mempool_height()
            genesis_time   = await get_genesis_time(),
            #  network_weeble = await get_network_weeble(),
            #  network_wobble = await get_network_wobble(),
            caller.send_to_nodes(
                {
                    "/": mempool_height,
                    "/genesis_time/": genesis_time,
                    #  "/weeble/": network_weeble,
                    #  "/wobble/": network_wobble,
                    "/nanos/": get_nanos(),
                }

            )
            await asyncio.sleep(random.randint(0, 10))


async def sender(name: int, q: asyncio.Queue) -> None:
    n = random.randint(0, 10)
    for _ in it.repeat(None, n):  # Synchronous loop for each single sender
        await randsleep(caller=f"Sender {name}")
        i = await makeitem()
        t = time.perf_counter()
        await q.put((i, t))
        print(f"Sender {name} added <{i}> to queue.")


async def receiver(name: int, q: asyncio.Queue) -> None:
    while True:
        await randsleep(caller=f"Receiver {name}")
        i, t = await q.get()
        now = time.perf_counter()
        print(f"Receiver {name} got element <{i}>"
              f" in {now-t:0.5f} seconds.")
        q.task_done()


async def main(nprod: int, ncon: int):
    q = asyncio.Queue()
    senders = [asyncio.create_task(sender(n, q)) for n in range(nprod)]
    receivers = [asyncio.create_task(receiver(n, q)) for n in range(ncon)]
    await asyncio.gather(*senders)
    await q.join()  # Implicitly awaits consumers, too
    for c in receivers:
        c.cancel()

if __name__ == "__main__":
    import argparse
    global node_array
    global node_port_array
    node_array = []
    node_shutdown_array = []
    node_port_array = []
    random.seed(444)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--nprod", type=int, default=5)
    parser.add_argument("-c", "--ncon", type=int, default=10)
    ns = parser.parse_args()
    start = time.perf_counter()

    asyncio.run(main(**ns.__dict__))

    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")
