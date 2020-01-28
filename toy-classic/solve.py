#!/bin/env python3

import functools as fn
import numpy as np
import readline
import string
import random
import json
import hashlib

charset = string.ascii_lowercase + string.digits + ',. '
charset_idmap = {e: i for i, e in enumerate(charset)}

key_size = 80


def decrypt(ctx, key):
    N, key_size = len(charset), len(key)
    return ''.join(charset[(c - key[i % key_size]) % N] for i, c in enumerate(ctx))


print("""
It may converge to local optima
Run it several times until the plaintext is clear enough to be recovered manually
""")


def toPrintable(data):
    ul = ord('_')
    data = bytes(c if 32 <= c < 127 else ul for c in data)
    return data.decode('ascii')


# -- Loading Data -- #
with open('output.txt') as f:
    ctx = f.readline().strip()[4:]
    enc = bytes.fromhex(f.readline().strip()[6:])
# convert cipher text to its ID
ctx = [charset_idmap[c] for c in ctx]

with open('ngrams.json') as f:
    ngrams = json.load(f)


@fn.lru_cache(10000)
def get_trigram(x):
    x = ''.join(x)
    y = ngrams.get(x)
    if y is not None:
        return y
    ys = []
    a, b = ngrams.get(x[:2]), ngrams.get(x[2:])
    if a is not None and b is not None:
        ys.append(a+b)
    a, b = ngrams.get(x[:1]), ngrams.get(x[1:])
    if a is not None and b is not None:
        ys.append(a+b)
    if len(ys):
        return max(ys)
    if any(c not in ngrams for c in x):
        return -25
    return sum(map(ngrams.get, x))


@fn.lru_cache(10000)
def fitness(a):
    plain = decrypt(ctx, a)
    tgs = zip(plain, plain[1:], plain[2:])
    score = sum(get_trigram(tg) for tg in tgs)
    return score


def initialize(size):
    population = []
    for i in range(size):
        key = tuple(random.randrange(len(charset)) for _ in range(key_size))
        population.append(key)
    return population


def crossover(a, b, prob):
    r = list(a)
    for i in range(len(r)):
        if random.random() < prob:
            r[i] = b[i]
    return tuple(r)


def mutate(a):
    r = list(a)
    i = random.randrange(len(a))
    r[i] = random.randrange(len(charset))
    return tuple(r)


# real_key = tuple([28, 38, 1, 15, 1, 24, 34, 16, 18, 18, 5, 12, 19, 6, 21, 7, 29, 30, 22, 37, 37, 7, 22, 14, 31, 25, 11, 1, 28, 36, 27, 26, 20, 0, 35, 25, 25, 5, 23, 24, 35, 30, 38, 19, 28, 16, 36, 14, 11, 16, 6, 15, 17, 5, 9, 31, 32, 23, 23, 20, 13, 25, 11, 19, 18, 35, 3, 35, 30, 26, 21, 35, 8, 21, 25, 29, 18, 31, 18, 8])
# Unknown. Below is a shitty genetic algorithm
# Initialize Population
population_size = 1000
# Sort population by fitness score
key_population = initialize(population_size)
key_population = sorted(key_population, key=fitness, reverse=True)

i = 0
while(True):
    try:
        i += 1
        # Select to top elites
        elite_size = 100
        top_score = fitness(key_population[0])
        top_dec = decrypt(ctx, key_population[0])
        print(f"{i:4}: {top_score:.8f} {top_dec[:120]}")
        key_population = key_population[:elite_size]
        for k in range(population_size - elite_size):
            a = random.randrange(len(key_population))
            new_population = []
            # Crossover if less than 0.5
            if(random.random() < 0.5):
                b = random.randrange(len(key_population))
                prob = random.random()
                new_population.append(crossover(
                    key_population[a], key_population[b], prob))
            else:
                new_population.append(mutate(key_population[a]))
        key_population.extend(new_population)
        # Sort again
        key_population = sorted(key_population, key=fitness, reverse=True)
    except KeyboardInterrupt:
        break

key = list(key_population[0])
print(key)
# #Line 133
#         bests.extend(population[:200])
#     bests = run(bests)
# except KeyboardInterrupt:
#     pass
# key = list(bests[0])


# -- Manually Fix -- #
print('')
print('Manually Fix')
print('h / l: move backward / forward, j / k: decrease / increase key, q: quit')
off = 0
while True:
    score = fitness(tuple(key))
    plain = decrypt(ctx, key)
    print(key)
    print('Score: ', score)
    print(' ' * off + 'v')
    for i in range(0, len(plain), key_size):
        print(plain[i:i+key_size])
    print(' ' * off + '^')
    cmd = input('> ').encode('ascii')
    if cmd == b'h':
        off = max(off - 1, 0)
    elif cmd == b'l':
        off = min(off + 1, key_size - 1)
    elif cmd == b'j':
        key[off] = (key[off] - 1) % len(charset)
    elif cmd == b'k':
        key[off] = (key[off] + 1) % len(charset)
    elif cmd == b'q':
        break
    else:
        print('Incorrect input')

# -- Print Flag -- #
k = hashlib.sha512(''.join(charset[k] for k in key).encode('ascii')).digest()
dec = bytes(ci ^ ki for ci, ki in zip(enc, k))
print('dec = ', dec)


