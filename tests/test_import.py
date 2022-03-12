#!/usr/bin/env python3
S = __import__("sys")
B = __import__("0x20bf")
print("test_import.py")
print(str("LINE:4 1") + str(0x20BF))
print(str("LINE 5 2") + str("B"))
print("venv working...")
print(S.version)
B.main(S.argv[1:])
