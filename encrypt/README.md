# encrypt

## Description:

> The flag is encrypted :P

## Solution:

Looking at the source code, there's a flag with length 16, and a key with length 1.

Knowing that the first 5 `FLAG{` and the last character `}`, I generated some random flags. For each of these flags, I encrypt them using each of the printable characters(key), and compare the output with the given cipher. I noticed that for keys 79, 103, 115, 121, 124, most of the flags gave a output with 6 similar characters as the given cipher, but a few of them gave 7. Since at least 6 character are correct, for flags giving 7 similarities has another correct character at a correct position.

Therefore, for each of the positions 5 to 14, I bruteforce all printable characters and see which one gives a output with more similarities.
