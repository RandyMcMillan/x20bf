import sys
sys.path.insert(0, "../x20bf")
sys.path.insert(1, "../x20bfi/depends/p2p")

import getopt as G
import sys as S

import x20bf.node_interface as ni


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


print("test.py")
print(S.version)
print(S.argv)
print(len(S.argv))
S.argv[0:] = "arg0"
S.argv[1:] = "arg1"
S.argv[2:] = "arg2"
S.argv[3:] = "arg3"
print(S.argv[0:])
print(S.argv[1:])
print(S.argv[2:])
print(S.argv[3:])
print(len(S.argv))
# B(S.argv[1:])
# B.main("['test.py', 'arg1', 'arg2', 'arg3']")

print(ni.version)
if __name__ == "__main__":
    main(S.argv[1:])
