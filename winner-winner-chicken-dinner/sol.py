# This is the equation solving part
# The connection part is not included

import os
import binascii

F = GF(2^65)
FF.<x> = GF(2^64, modulus=F.fetch_int(0x1fd07d87ee65cb055))

state = int(binascii.hexlify(os.urandom(8)), 16)
poly = 0xaa0d3a677e1be0bf

def gf_step():
    global init_state
    init_state = init_state * (x^43)
    ret = init_state.integer_representation()
    return (ret >> 63) & 1

def step():
    global state
    out = state & 1
    state >>= 1
    if out:
        state ^^= poly
    return out
    

def random():
    for _ in range(42):
        step()
    return step()


gf_state = int(''.join(reversed(bin(state)[2:])), 2)
gf_state = FF.fetch_int(gf_state)
while True:
    break
    gf_state = gf_state * (x^43)
    ret = gf_state.integer_representation()
    print (ret >> 63) & 1
    print random()
    raw_input('#')

with open('input', 'r') as f:
    seq = f.read()
seq = eval(seq)
print seq


now_state = 1
total = []
for i in range(64):
    now = []
    now_state *= (x^43)
    for i in range(64):
        now_bit = x^i
        now_bit = now_bit * now_state
        now_bit = now_bit.integer_representation()
        now_bit = (now_bit >> 63) & 1
        now.append(now_bit)
    total.append(now)

M = Matrix(FF, total).T
seq = Matrix(FF, seq)
ret = seq * (M^-1)
ret = ret[0]
print ret
init_state = 0
for i in range(64):
    init_state += ret[i]*x^i

for i in range(64):
    gf_step()

with open('output', 'w') as f:
    for i in range(100):
        f.write(str(gf_step()) + '\n')
