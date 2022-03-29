import asyncio
import getopt as G
import sys

sys.path.insert(0, "../x20bf")
sys.path.insert(1, "../x20bf/depends/p2p")

# from x20bf import time_functions
# import x20bf.time_functions
from x20bf.time_functions import blockcypher_height
from x20bf.time_functions import touch_time
from x20bf.time_functions import btc_time
from x20bf.time_functions import move_block_time
from x20bf.time_functions import get_millis
from x20bf.time_functions import get_seconds
from x20bf.time_functions import mempool_height


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
        sys.exit(2)
        for opt, arg in opts:
            if opt == "-h":
                print("test.py -i <inputfile> -o <outputfile>")
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = arg
            elif opt in ("-o", "--ofile"):
                outputfile = arg
        print('Input file is "', inputfile)
        print('Output file is "', outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
