# Train

## Description:

> NIL

## Solution:

This challenge is CBC block cipher mode using RSA.

The line `date, session, secret = plain.split(b'|')` may cause error if there is not enough `|`. The error message can be used to recover the flag just like padding oracle attack.

Unintended solution: the value of public exponent e is small, simply use coppersmith method can also recover the flag.

`FLAG{cBCNEVERGetSoLD}`
