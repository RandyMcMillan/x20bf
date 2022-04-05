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


async def randsleep(caller=None) -> None:
    i = random.randint(0, 60)
    node_array.append(caller)
    if caller:
        print(f"{caller} sleeping for {i} seconds.")
        caller = TimeNode("127.0.0.1", 0, str(datetime.datetime.now()), callback=test_node_callback)
        node_port_array.append(caller.port)
        node_port_array.reverse()
        caller.start()
        await asyncio.sleep(3)
        if len(node_array) <= 10:
            caller.connect_with_node("127.0.0.1", node_port_array.pop())
            await asyncio.sleep(random.randint(0, 60))


async def produce(name: int, q: asyncio.Queue) -> None:
    n = random.randint(0, 10)
    for _ in it.repeat(None, n):  # Synchronous loop for each single producer
        await randsleep(caller=f"Producer {name}")
        i = await makeitem()
        t = time.perf_counter()
        await q.put((i, t))
        print(f"Producer {name} added <{i}> to queue.")


async def consume(name: int, q: asyncio.Queue) -> None:
    while True:
        await randsleep(caller=f"Consumer {name}")
        i, t = await q.get()
        now = time.perf_counter()
        print(f"Consumer {name} got element <{i}>"
              f" in {now-t:0.5f} seconds.")
        q.task_done()


async def main(nprod: int, ncon: int):
    q = asyncio.Queue()
    producers = [asyncio.create_task(produce(n, q)) for n in range(nprod)]
    consumers = [asyncio.create_task(consume(n, q)) for n in range(ncon)]
    await asyncio.gather(*producers)
    await q.join()  # Implicitly awaits consumers, too
    for c in consumers:
        c.cancel()

if __name__ == "__main__":
    import argparse
    global node_array
    global node_port_array
    node_array = []
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
