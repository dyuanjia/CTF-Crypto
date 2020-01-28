from spn import SPN, int2bits
from operator import attrgetter
from pprint import pprint
from path import Path
import functools as fn
import numpy as np
import os
import math
import itertools
import random
import heapq
import copy
import ast
import hashlib


def self_XOR(bits, mapping):
    assert (len(bits) == len(mapping))
    out = 0
    for b, m in zip(bits, mapping):
        if (int(m, 2)):
            out ^= int(b, 2)
    return out


def print_table(table, title):
    print(title)
    print('===' + '='*len(table)*6)
    print('   ' + ''.join(f'{hex(i):>6}' for i in range(len(table))))
    for x in range(len(table)):
        print(f'{hex(x):>3}', end='')
        print(''.join(f'{str(int(n)):>6}' for n in table[x]))
    print()


def idx2input(v, sbits, nbits):
    u = np.zeros(nbits, dtype=np.int)
    for b in v:
        u[b] = 1
    u = u.reshape((-1, sbits))
    return {block: ''.join(ui.astype(str))
            for block, ui in enumerate(u) if np.count_nonzero(ui)}


def key2int(keys, idx, sbits, nbits):
    out = np.zeros(nbits, dtype=np.int)
    for i, k in zip(idx, keys):
        for offset in range(sbits):
            out[i*sbits+offset] = k[offset]
    return int(''.join(out.astype(str)), 2)


# -- Loading Data -- #
random.seed(24)
nblock = 16
nround = 4
key = os.urandom(8)

with open('output.txt') as f:
    sbox = ast.literal_eval(f.readline().split('=')[1].strip())
    pbox = ast.literal_eval(f.readline().split('=')[1].strip())
    lines = f.read().splitlines()
    enc = bytes.fromhex(lines.pop()[6:])

cipher = SPN(sbits=4, nblock=nblock, nround=nround)
cipher.set_boxes(sbox, pbox)

sbits, nbits = cipher.sbits, cipher.nbits
N = 1 << sbits

data = []
# x is 64 bits
for x, y in zip(lines[::2], lines[1::2]):
    x = bytes.fromhex(x[4:])
    y = bytes.fromhex(y[4:])
    data.append((x, y))

x_test = data[0][0]
y_test = data[0][1]

# 338518602
for i in range(2**64):
    try:
        # if(i % 10000000000 == 0):
        #     print(f"Iter: {i}")
        # key = i.to_bytes((64 + 7) // 8, "little")
        key = os.urandom(8)
        cipher.set_key(key)
        yy = cipher.encrypt(x_test)

        if(yy == y_test):
            print(f"Success at {i}")
            print(yy)
            print(y_test)
            print(key)
            break
    except KeyboardInterrupt:
        print(f"Interrupted at {i}")
        break
