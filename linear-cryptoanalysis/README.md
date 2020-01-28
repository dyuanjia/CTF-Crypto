# Linear Cryptoanalysis

## Description:

> Uniform cost search

## Solution:

**NOT SOLVED**

First, I build the linear approximation table, and calculated their bias. Then, I search for paths that will give the highest bias. The general rule is: the fewer active S-boxes, the larger the magnitude of the overall linear expression bias. So when I search for paths, I only use 1 sbox in the first round.

The cipher is in blocks of 4 bits, with a total of 16 blocks. Thus, I calculated the bias for all 16 possible paths for each block, and kept those with high bias.

NL represent the number of known plaintexts required, it is reasonable to approximate NL by $$N_L \approx \frac{1}{\epsilon^2}$$. Since 1000 plaintexts were provided, $$\epsilon \approx \frac{1}{10}$$, therefore the bias of a path should be larger than 0.1.

After finding the paths, I started to extract the key bits. For all possible values of the target partial subkey, the corresponding ciphertext bits are exclusive-ORed with the bits of the target partial subkey and the result is run backwards through the corresponding S-boxes. This is done for all known plaintext/ciphertext samples and a count is kept for each value of the target partial subkey. The count for a particular target partial subkey value is incremented when the linear expression holds true for the bits into the last round’s S-boxes and the known plaintext bits. I stored the resultant counts for later access without the need to calculate them again.

The target partial subkey value which has the count which differs the greatest from half the number of plaintext/ciphertext samples is assumed to represent the correct values of the target partial subkey bits.

However, when I extracted partial key bits from several paths, those partial key bits for the same block are different for different paths, and I'm not sure which is the correct one, so I'm stuck here.

_Possible path forward_: encrypt a test flag with my own key and see if I can find a way to choose the correct key bits.
