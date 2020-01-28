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

# Solution 2
flag = ''
for i in range(260):
    remote.sendlineafter('> ', '2')
    p = decimal.Decimal(2 ** i)
    chosen_cipher = c * inverse(pow(p, e, n), n) % n
    remote.sendline(str(chosen_cipher))
    exec(remote.recvline())  # m = ..
    m %= 2
    tmp = 0
    for x in reversed(range(i)):
        tmp += inverse(2**(x+1), n) * int(flag[x])
    m -= tmp % n
    flag = str(m % 2) + flag
    print(flag)

flag = int(flag, 2)
print(long_to_bytes(flag))
remote.interactive()
