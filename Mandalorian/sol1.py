#!/usr/bin/env python3
from pwn import *
from Crypto.Util.number import *
import decimal

remote = remote("edu-ctf.csie.org", 10192)

remote.sendlineafter('> ', '1')
exec(remote.recvline())  # c = ...................
exec(remote.recvline())  # e = ...................
exec(remote.recvline())  # n = ...................
k = n.bit_length()
decimal.getcontext().prec = k

p = decimal.Decimal(2 ** (260*3))
left = decimal.Decimal(0)
right = decimal.Decimal(n / p)
for i in range(260):
    remote.sendlineafter('> ', '2')
    p *= 2
    chosen_cipher = c * pow(p, e, n) % n
    remote.sendline(str(chosen_cipher))
    exec(remote.recvline())  # m = ..
    m = m % 2
    print(f"i: {i}, m: {m}")
    if (m == 0):
        right = (left + right) / 2
    elif (m == 1):
        left = (left + right) / 2
    print(long_to_bytes(right))
    if (right-left < 1):
        break

remote.interactive()
