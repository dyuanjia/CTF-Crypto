# winner winner chicken dinner

## Description:

> Winner, winner, chicken dinner! There it is. Thank you. God, I love this town. I love this game. And, Jim, I might even love you.

## Solution:

The key point of this question is to rewrite the step function into a multiply operation in $$GF(2^{128})$$ such that the whole system becomes linear, then we can solve it with some matrix multplication.

After changing into $$GF(2^{128})$$, the `random()` function changes into $$state*x^{43}$$, and we can calculate the result bit by bit. For example, if the first state is $$11_2$$, the output of `random()` will be eqivalent to the output of the sum of `random()` with initial states $$10_2$$ and $$01_2$$.

By collecting 64 output from the RNG, we can establish 64 equations. Then we only have 64 variables (the initial state is 64 bits long). Simply solve it with some linear algebra to break the PRNG.

`FLAG{w3_W4nT_fA_d4_CaI!!!fA_d4_CaI!!!fA_d4_CaI!!!}`
