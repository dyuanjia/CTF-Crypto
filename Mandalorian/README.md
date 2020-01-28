# Mandalorian

## Description:

> I fixed the type, can you solve it?

## Solution:

### Solution 1: binary search

n is a 1024 bit number, so I need 1024 iterations to get the precise flag. However, as can be seen from the source code, each connection only has 261 iterations. Minus 1 for getting `c`, `e`, `n`, only 260 iterations left.

I ran it against the server anyway, and the outputs are all 0. In fact, I changed the starting power and ran it 2 more times, the outputs are still all 0. This means that the flag $$\epsilon$$ $$[0, \frac{n}{2^{780}})$$.

Setting the left and right boundaries accordingly, and the starting power to be $$2^{781}$$, I ran the binary search again until the boundaries converge. The resultant right boundary is then the flag.

### Solution 2: bit by bit

Starting from the LSB, deduce the flag bit by bit until it's fully recovered.

`FLAG{Youg0tTH3Fl4GIHavesPoKEN}`
