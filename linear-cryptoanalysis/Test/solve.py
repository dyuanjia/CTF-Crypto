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


key1 = b'\xdbe\xc5\x16\xea\xdb\xaa\x8b'
key2 = b'>\nX\x8a\xf8CY\xd8'
key3 = b'\nd\xe8\xe0\x8f\xc1\x8eA'
key4 = b's\x14\xfa\x13\xae\xe1*?'
key5 = b'n\x95B\xc9d\xea\x9fI'

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

# -- Build Linear Approximation Table -- #
input_sum = output_sum = list(cipher.sbox.keys())
table = np.zeros((nblock, nblock))
for i, input_mapping in enumerate(input_sum):
    for o, output_mapping in enumerate(output_sum):
        for s_in, s_out in cipher.sbox.items():
            table[i][o] += (self_XOR(s_in, input_mapping) ==
                            self_XOR(s_out, output_mapping))

# print_table(table, 'Linear Approximation Table')
bias_table = table - (1 << (sbits-1))
print_table(bias_table, 'Bias Table')
# print(int2bits(int.from_bytes(key5, "little"), nbits))


# -- Construct Linear Approximations for the Complete Cipher -- #
best_paths = []
plaintexts = list(cipher.sbox.keys())
for bit_idx in range(0, nbits, sbits):
    paths = []
    for u1 in plaintexts:
        p = [bit_idx+offset for offset, b in enumerate(u1) if (int(b, 2))]

        # round 1: substitution
        v = sbox[u1]
        complete_bias = bias_table[int(u1, 2)][int(v, 2)]
        # permutation
        v1 = [pbox[b]
              for b, vi in zip(range(bit_idx, bit_idx+sbits), v) if (int(vi, 2))]
        v1.sort()
        u2 = idx2input(v1, sbits, nbits)

        # round 2: substitution
        v2 = []
        for block, ui in u2.items():
            u2[block] = sbox[ui]
            complete_bias *= bias_table[int(ui, 2)
                                        ][int(u2[block], 2)] / N
            complete_bias *= 2
            # permutation
            v2.extend([pbox[sbits*block + offset]
                       for offset, vi in enumerate(u2[block]) if (int(vi, 2))])
        v2.sort()
        u3 = idx2input(v2, sbits, nbits)

        # round 3: substitution
        v3 = []
        for block, ui in u3.items():
            u3[block] = sbox[ui]
            complete_bias *= bias_table[int(ui, 2)
                                        ][int(u3[block], 2)] / N
            complete_bias *= 2
            # permutation
            v3.extend([pbox[sbits*block + offset]
                       for offset, vi in enumerate(u3[block]) if (int(vi, 2))])
        v3.sort()
        u4 = idx2input(v3, sbits, nbits)

        pa = Path(complete_bias, p, u4)
        paths.append(pa)

    paths.sort(key=attrgetter('abs_bias'), reverse=True)
    round_best_paths = [pa for pa in paths if (
        pa.bias == paths[0].bias and pa.bias != 0)]
    best_paths.extend(round_best_paths)

best_paths.sort(key=attrgetter('abs_bias'), reverse=True)
for pa in best_paths:
    print(pa)
exit()

counts = np.load('round5_7_10.npy')
counts -= 500
counts = np.abs(counts)
counts /= 1000
max_idx = np.argmax(counts)
print(counts[max_idx])
print(int2bits(max_idx, 12))
# counts = np.sort(counts)
for i in range(len(counts)):
    if(counts[i] > 0.05):
        print(i)
        print(counts[i])
        print(int2bits(i, 12))
exit()
# -- Start Attack -- #
# last round key
candidate = best_paths[1]
n = len(candidate.u)
print(candidate)
counts = np.zeros(1 << (sbits*n))
for k in range(1 << (sbits*n)):
    keys = [int2bits(k, sbits*n)[i:i+sbits] for i in range(0, sbits*n, sbits)]
    idx = list(candidate.u.keys())
    test_key = key2int(keys, idx, sbits, nbits)

    # all known plaintext pairs
    for x, y in data:
        xx = int.from_bytes(x, "little")
        yy = int.from_bytes(y, "little")

        result = 0
        # plaintext bits needed
        for p in candidate.p:
            result ^= int(int2bits(xx, nbits)[p], 2)

        # xor the last round key
        v4 = int2bits(test_key ^ yy, nbits)
        # convert into 4bit array
        v4 = [v4[i:i+sbits] for i in range(0, nbits, sbits)]
        # reverse sbox
        u4 = [cipher.isbox[vi] for vi in v4]
        u4 = ''.join(u4)
        for i in candidate.u_idx:
            result ^= int(u4[i], 2)

        if (result == 0):
            counts[k] += 1

print(counts)
np.save("round5_7_10.npy", counts)
exit()
# block: 0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15
# k1:
# k2:
# k3:
# k4:                          1000      0100      1110                          1101
# k5: 1111 1000 0100 0111 1100 1111 1111 0011 0011 0001 0011 1000 1001 1001 .... 1011

rkeys = []
# -- Print Flag -- #
rkeyi = ''.join(hex(c)[2:] for c in rkeys)
rkeyi = bytes.fromhex(rkeyi)[::-1]
k = hashlib.sha512(rkeyi).digest()
dec = bytes(ci ^ ki for ci, ki in zip(enc, k))
print('dec = ', dec)

# FLAG{
