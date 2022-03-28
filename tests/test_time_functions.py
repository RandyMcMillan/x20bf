#!/usr/bin/env python3
import asyncio
import getopt as G
import sys as S

# from x20bf import time_functions
from time_functions import blockcypher_height
from time_functions import touch_time
from time_functions import btc_time
from time_functions import move_block_time
from time_functions import get_millis
from time_functions import get_seconds
from time_functions import mempool_height


touch = asyncio.new_event_loop()
touch.run_until_complete(touch_time(btc_time()))
print(move_block_time())
print(get_millis())
print(get_seconds())

bc_height = asyncio.new_event_loop()
print(bc_height.run_until_complete(blockcypher_height()))

mp_time = asyncio.new_event_loop()
print(mp_time.run_until_complete(mempool_height()))

# print(btc_unix_time_millis())
# print(btc_unix_time_seconds())
# print(unix_time_millis())
# print(unix_time_seconds())
# print(network_modulus())
# print(network_weeble_wobble())
# print(network_weeble())
# print(network_wobble())
# # print(mempool_height())
# loop.run_until_complete(mempool_height())


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
