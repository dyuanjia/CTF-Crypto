import binascii
import io


def n2s(n, byteorder='big'):
    """
    Number to string.
    """
    length = (len(hex(n))-1)//2
    return int(n).to_bytes(length=length, byteorder=byteorder)


def byte(x):
    s = io.BytesIO()
    s.write(bytearray((x,)))
    return s.getvalue()


def xor_string(s1, s2):
    """
    Exclusive OR (XOR) @s1, @s2 byte by byte
    return the xor result with minimun length of s1,s2
    """
    if type(s1) != type(s2):
        raise TypeError('Input must be the same type, both str or bytes.')
    if type(s1) == type(s2) == bytes:
        return b''.join([byte(a ^ b) for a, b in zip(s1, s2)])
    return ''.join([chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2)])


with open('N-Time Pad', 'r') as content_file:
    content = content_file.read()

ciphers = content.split()                                # string
ciphers = list(map(lambda x: n2s(int(x, 16)), ciphers))  # byte string

flag = b"FLAG{D0_u_know_One-Time-Pad's_md5_i5_37d52ab882a1397bec4e3e4eafba0f58??!!?!?}"
plain_text = list(map(lambda x: xor_string(x, flag), ciphers))
for i, text in enumerate(plain_text):
    print(f"{i}: {text}")

# Plaintext taken from wikipedia
print(xor_string(
    ciphers[1], b"racked, but requires the use of a one-time pre-shared key the same size as, o"))
