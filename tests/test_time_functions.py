#!/usr/bin/env python3
import asyncio
import getopt as G
import sys as S

from time_functions import (blockcypher_height, btc_time, btc_unix_time_millis,
                            btc_unix_time_seconds, get_millis, get_seconds,
                            mempool_height, move_block_time, network_modulus,
                            network_weeble, network_weeble_wobble,
                            network_wobble, touch_time, unix_time_millis,
                            unix_time_seconds)

loop = asyncio.new_event_loop()
loop.run_until_complete(touch_time(btc_time()))
# print(touch_time(btc_time()))
print(move_block_time())
print(get_millis())
print(get_seconds())
print(blockcypher_height())
print(btc_time())
print(btc_unix_time_millis())
print(btc_unix_time_seconds())
print(unix_time_millis())
print(unix_time_seconds())
print(network_modulus())
print(network_weeble_wobble())
print(network_weeble())
print(network_wobble())
# print(mempool_height())
loop.run_until_complete(mempool_height())


def main(argv):
    inputfile = ""
    outputfile = ""
    try:
        opts, args = G.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except G.GetoptError:
        print("test.py -i <inputfile> -o <outputfile>")
        S.exit(2)
        for opt, arg in opts:
            if opt == "-h":
                print("test.py -i <inputfile> -o <outputfile>")
                S.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = arg
            elif opt in ("-o", "--ofile"):
                outputfile = arg
        print('Input file is "', inputfile)
        print('Output file is "', outputfile)


if __name__ == "__main__":
    main(S.argv[1:])
