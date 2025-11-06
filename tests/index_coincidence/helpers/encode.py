import random
import sys

"""
Obfuscate the given file by generating a random XOR key with length from 2 up
to 300. The output filename is based on the original name, but includes the key
length.
"""
filename = sys.argv[1]
with open(filename, "rb") as f:
    data = bytearray(f.read())

width = random.randint(2, 300)
key = [random.randint(0, 255) for i in range(width)]

for i in range(len(data)):
    data[i] ^= key[i % len(key)]

outname = "%s_%03d.enc" % (filename, width)
with open(outname, "wb") as f:
    f.write(data)
