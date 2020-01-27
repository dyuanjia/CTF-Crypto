# N-Time Pad

## Description:

> 你 484 通靈王

## Solution:

Classic many-time pad problem.

12 cipher texts are given and flag is the key. Since the first 5 characters `FLAG{` are known, try to decrypt the cipher text with this key first. The result is 12 partial plaintexts. Some of these plaintexts can be inferred further, e.g. `racke` can be inferred to be `racked`. Thus, I can XOR this extended plaintext with it cipher text again to get a longer key.

Repeat this process until the full flag is uncovered.

`FLAG{D0_u_know_One-Time-Pad's_md5_i5_37d52ab882a1397bec4e3e4eafba0f58??!!?!?}`
