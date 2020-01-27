# Cathub Party

## Description:

> Cathub threw a party, let's enjoy!

## Solution:

Padding Oracle Attack.

Target: block cipher

- Cipher Block Chaining (CBC)
- PKCS#7 Padding

The encrypted flag in the cookie is also base64 encoded, so I need to decode it first into raw encrypted bytes. After some trial and error, I found out that the block size is 16. Since the encrypted bytes have a length of 96, there are 6 blocks in total.

The first block will not be decrypted because I don't have the IV. The oracle will return a `"Your flag seems strange"` message if the padding is valid but the flag is not the same as the original. It will return a `"What the flag?!"` message if the padding is invalid.

Starting from the second last block, I brute force the last byte until I get an valid padding. This means that the decrypted byte is `\x01`. I can then xor it with the guessed encrypted byte to get an intermediate value. Then, I xor the intermediate value with the original encrypted byte to get the plaintext.

Using this method of brute forcing until I get an valid padding byte by byte, I obtained the flag. The flag starts at the second block, so I didn't need to decrypt the first block.

Code has room for improvements.

`FLAG{EE0DF17A410C90F86E88471346B6DA77E8C878200B37E60C53E9A56913211465}`
