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
    # print("get_mempool_height()")
    return await mempool_height()


async def get_genesis_time():
    # print("get_genesis_time()")
    return genesis_time


async def get_network_weeble():
    # print("get_network_weeble()")
    return await network_weeble()


async def get_network_wobble():
    # print("get_network_wobble()")
    return await network_wobble()


async def randsleep(mph, n_weeble, n_wobble, caller=None) -> None:
    i = random.randint(0, 10)
    node_array.append(caller)
    node_shutdown_array.append(caller)
    if caller:
        print(f"{caller} sleeping for {i} seconds.")
        node = TimeNode("127.0.0.1", 0, str(datetime.datetime.now()), callback=test_node_callback)
        node_shutdown_array.append(node)
        node_port_array.append(node.port)
        node_port_array.reverse()
        node.start()
        await asyncio.sleep(i)
        if len(node_array) >= 10:
            node.connect_with_node("127.0.0.1", node_port_array.pop())
            # mempool_height = await get_mempool_height()
            print(type(mph))
            print(mph)
            print(type(n_weeble))
            print(n_weeble)
            genesis_time = await get_genesis_time(),
            print(type(genesis_time))
            print(genesis_time)
            node.send_to_nodes(
                {
                    "/": mph,
                    "/node.port/": node.port,
                    "/genesis_time/": genesis_time,
                    "/weeble/": n_weeble,
                    "/wobble/": n_wobble,
                    "/nanos/": get_nanos(),
                }

            )
            # caller.stop()
            # await asyncio.sleep(random.randint(0, i))
    for caller in node_shutdown_array:
        try:
            # caller.stop()
            # print("caller.stop()")
            print(caller)
            print(len(node_shutdown_array))
        except Exception as er:
            print(er)


async def sender(name: int, q: asyncio.Queue) -> None:
    n = random.randint(1, 3)
    for _ in it.repeat(None, n):  # Synchronous loop for each single sender
        mempool_heights = [asyncio.create_task(get_mempool_height())]
        network_weebles = [asyncio.create_task(get_network_weeble())]
        network_wobbles = [asyncio.create_task(get_network_wobble())]
        await asyncio.gather(*mempool_heights)
        await asyncio.gather(*network_weebles)
        await asyncio.gather(*network_wobbles)
        await q.join()  # Implicitly awaits recievers, too
        for height in mempool_heights:
            for weeble in network_weebles:
                for wobble in network_wobbles:
                    print(height)
                    print(weeble)
                    print(wobble)
                    await randsleep(height, weeble, wobble, caller=f"Sender {name}")
                    # i = await makeitem()
                    # t = time.perf_counter()
                    # await q.put((i, t))
                    # print(f"Sender {name} added <{i}> to queue <{t}>.")
                    wobble.cancel()
                    weeble.cancel()
                    height.cancel()
                    try:
                        q.get_nowait()
                    except asyncio.QueueEmpty:
                        pass
                        # print(q.qsize())


async def receiver(name: int, q: asyncio.Queue) -> None:
    while True:
        mempool_heights = [asyncio.create_task(get_mempool_height())]
        network_weebles = [asyncio.create_task(get_network_weeble())]
        network_wobbles = [asyncio.create_task(get_network_wobble())]
        await asyncio.gather(*mempool_heights)
        await asyncio.gather(*network_weebles)
        await asyncio.gather(*network_wobbles)
        await q.join()  # Implicitly awaits recievers, too
        for height in mempool_heights:
            for weeble in network_weebles:
                for wobble in network_wobbles:
                    await randsleep(height, weeble, wobble, caller=f"Reciever {name}")
                    i, t = await q.get()
                    now = time.perf_counter()
                    print(f"Receiver {name} got element <{i}>" f" in {now-t:0.5f} seconds.")
                    wobble.cancel()
                    weeble.cancel()
                    height.cancel()
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

    asyncio.run(main(**ns.__dict__))

    for node in node_shutdown_array:
        try:
            print("node.stop()")
            print(len(node_shutdown_array))
            node.stop()
        except Exception as er:
            print(er)

    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")
