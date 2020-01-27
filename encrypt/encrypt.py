from sympy import *
import random
import string


def op1(p, s):
    return sum([i * j for i, j in zip(s, p)]) % 256


def op2(m, k):
    return bytes([i ^ j for i, j in zip(m, k)])


def op3(m, p):
    return bytes([m[p[i]] for i in range(len(m))])


def op4(m, s):
    return bytes([s[x] for x in m])


'''
Linear Feedback Shift Register
'''


def stage0(m):
    random.seed('oalieno')
    p = [int(random.random() * 256) for i in range(16)]
    # [239, 194, 15, 76, 81, 87, 59, 247, 160, 19, 227, 201, 119, 125, 116, 166]
    s = [int(random.random() * 256) for i in range(16)]
    # [33, 27, 174, 156, 244, 29, 254, 247, 61, 1, 41, 132, 82, 49, 173, 170]
    c = b''
    for x in m:              # each element in the flag
        k = op1(p, s)
        c += bytes([x ^ k])  # element x is xor-ed with k
        # first element is discarded and last is appended with k
        s = s[1:] + [k]
    # for i in range(16):
     #   print(f'{m[i]} {c[i]}')
    return c


'''
Substitution Permutation Network
'''


def stage1(m):
    random.seed('oalieno')
    k = [int(random.random() * 256) for i in range(16)]
    p = [i for i in range(16)]
    random.shuffle(p)
    s = [i for i in range(256)]
    random.shuffle(s)

    c = m
    for i in range(16):
        c = op2(c, k)
        c = op3(c, p)
        c = op4(c, s)
    return c


def encrypt(m, key):
    stage = [stage0, stage1]
    # print("Key: " + str(key))  # converted to number

    for i in map(int, f'{key:08b}'):  # key is formatted to binary of length 8
        m = stage[i](m)
    return m


def check_char(l):
    global correct
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`|~"
    for ch in chars:
        l[j] = ch
        f = "".join(l)
        for k in keys:
            c = encrypt(f.encode(), k)
            cnt = 0
            for i in range(16):
                if(cipher[i] == c[i]):
                    cnt += 1
            if(cnt != correct):
                print(ch)
                correct += 1
                return f


if __name__ == '__main__':
    cipher = open('cipher', 'rb').read()
    flag = open('flag', 'rb').read()
    assert(len(flag) == 16)
    #key = open('key', 'rb').read()
    #assert(E ** (I * pi) + len(key) == 0)

    keys = [79, 115, 121, 124, 103]

    # flags = open('flags', 'r')
    f = "FLAG{q6B3K.t~*V}"
    correct = 11
    for j in range(10, 15):
        l = list(f)
        f = check_char(l)
        # print(f'{k}: {cnt}')

    check = "FLAG{q6B3KviyaM}"
    output = encrypt(check.encode(), 79)
    count = 0
    for i in range(16):
        if(cipher[i] == output[i]):
            count += 1
    print(count)

    # iterating keys
    # for k in range(256):
    #     c = encrypt(flag, k)
    #     cnt = 0
    #     for i in range(16):
    #         if(cipher[i] == c[i]):
    #             cnt += 1
    #     print(f'{k}: {cnt}')

    #open('cipher2', 'wb').write(encrypt(flag, int.from_bytes(key, 'little')))

    #cipher2 = open('cipher2', 'rb').read()
    # for i in range(16):
    #print(f'{cipher[i]} {cipher2[i]}')
