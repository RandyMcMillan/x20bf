import sys

# import time
# import getpass

sys.path.append(".")

from p2psecure.blockchain import Blockchain

bc = Blockchain()

block = bc.process_block({"data": "MAurice Snoeren"}, "transaction")
bc.add_block(block)

print(bc.get_block(1))

print(bc.get_block(3))

print(bc.get_block(6))
