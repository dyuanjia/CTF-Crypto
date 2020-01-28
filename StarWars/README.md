# StarWars

## Description:

> factor n with pollard p - 1

## Solution:

The vulnerability here is the function `fantasticPrime()`, which returns a prime number too small to be suitable for use in RSA.

This can be broken with Pollard's algorithm.

`FLAG{ArEUr3ADyfORst4rw4Rs9}`
