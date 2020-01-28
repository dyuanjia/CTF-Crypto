# RSACTR

## Description:

> NIL

## Solution:

This challenge is CTR block cipher mode using RSA.

First you can use option 3 to encrypt 0 and recover nonce. Then use option 2 to get encrypted flag `c`. Once you get nonce and encrypted flag, you can write out an equation `(c - flag) ^ 3 = nonce`. Then, simply use coppersmith method to get the small root `flag`.

`FLAG{dIdyousolVEITWIthCoppERsmith}`
