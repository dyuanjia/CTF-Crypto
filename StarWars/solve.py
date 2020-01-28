#!/usr/bin/env python3
from pwn import *
from Crypto.Util.number import *


def pollard(n):
    a = 2
    b = 2
    while True:
        a = pow(a, b, n)
        d = GCD(a-1, n)
        if 1 < d < n:
            return d
        b += 1


remote = remote("rayfish.zoolab.org", 20000)

remote.sendlineafter('> ', '1')
exec(remote.recvline())  # c = ...................
exec(remote.recvline())  # e = ...................
exec(remote.recvline())  # n = ...................

p = pollard(n)
q = n // p
d = inverse(e, (p-1) * (q-1))
m = pow(c, d, n)

print(long_to_bytes(m))

