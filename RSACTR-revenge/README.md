# RSACTR-revenge

## Description:

> NIL

## Solution:

This challenge is the same as the challenge `RSACTR` except there is no option 3 to recover nonce. We can get three different encrypted flag:

```
(c1 - flag) ^ 3 = nonce
(c2 - flag) ^ 3 = nonce + 2020
(c3 - flag) ^ 3 = nonce + 4040
```

Elementary algebra can be used to eliminate the nonce variable:

```
(c2 - flag) ^ 3 - (c1 - flag) ^ 3 = 2020
(c3 - flag) ^ 3 - (c2 - flag) ^ 3 = 2020
```

These two equations have the same root `flag`, so they will have a common divisor. Simply do a gcd algorithm will reveal the flag. This trick is basically the same as Franklin-Reiter Related Message Attack.

`FLAG{GCdISSuchaGO0DalgOriTHM}`
