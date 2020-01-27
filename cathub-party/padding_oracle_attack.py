import requests
import base64
import binascii
import io
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def s2B(ss):
    """
    Switch string and bytes.
    """
    if type(ss) == bytes:
        return ss
    return bytes([ord(c) for c in ss])


def B2s(bs):
    """
    Switch bytes and string.
    """
    if type(bs) == type(b''):
        return "".join(map(chr, bs))
    else:
        return bytes([ord(c) for c in bs])


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


def incrementByte(b):
    num = int.from_bytes(b, byteorder="little")
    return (num+1).to_bytes(1, byteorder="little")


'''
Base64 Original: 1lSDchhQ5l0SSSxLSX9ozsJtZnd4zCXDfrgkPqpJKwCknGnyFiCuFvb%2BL74P6ygKqXDRcyBwI6%2BSK3G%2BRbabxbwubLC1LjSnTqV9i%2BYLhzkPRWRnM96PQ1li5Sq5QZ22
Encoded: length = 128 (%2B = +; %2F = /)
Decoded: length = 96
Block Size      = 16
No. of Blocks   = 6
'''
plaintext = b""
blocksize = 16

url = "https://edu-ctf.csie.org:10190/party.php"
jar = requests.cookies.RequestsCookieJar()
jar.set('session', 'c050873e-3996-4606-874f-0fa337b13c23')
jar.set('rack.session', 'BAh7CEkiD3Nlc3Npb25faWQGOgZFVEkiRTFmOTA4MDVhMDM0YWFkMzA2ZjE5%0AMDBmOTM0Y2Q0YzQ4Nzk2MjE0YmM0YzczZTRjMjQxMGI0YmY4N2EyY2Y3ZmIG%0AOwBGSSIKZmxhc2gGOwBGewBJIgx1c2VyX2lkBjsARmkB3g%3D%3D%0A--79fc81cbd824fdb49f7f06a8ed589a8b73b2fba1')
jar.set('PHPSESSID', '3gu0675c0kos0glegdi7o75d04')

encoded_flag = "1lSDchhQ5l0SSSxLSX9ozsJtZnd4zCXDfrgkPqpJKwCknGnyFiCuFvb+L74P6ygKqXDRcyBwI6+SK3G+RbabxbwubLC1LjSnTqV9i+YLhzkPRWRnM96PQ1li5Sq5QZ22"
decoded_flag = base64.b64decode(encoded_flag)
cipher_length = len(decoded_flag)
last_idx = cipher_length
# TODO check if divisible
no_of_blocks = int(cipher_length / blocksize)

# TODO no IV
for block in range(no_of_blocks, 1, -1):
    print(f"Testing block {block}")
    last_idx -= blocksize

    fake = b""
    current_block = b""
    intermediates = []
    for padding in range(1, blocksize+1):
        original = decoded_flag[last_idx -
                                padding].to_bytes(1, byteorder='little')
        result = b''
        for i in range(256):
            left = decoded_flag[:last_idx-padding]
            right = decoded_flag[last_idx:last_idx+16]

            # test one byte
            b = i.to_bytes(1, byteorder='little')
            flag = left + b + fake + right

            # replace special character
            flag = base64.b64encode(flag)
            flag = B2s(flag)
            flag = flag.replace("+", "%2B")
            flag = flag.replace("/", "%2F")

            jar.set('FLAG', flag)
            response = requests.get(url, cookies=jar, verify=False)
            # print(response.text)

            if("Your flag seems strange" in response.text):
                result = b
                break
            elif("What the flag?!" in response.text):
                pass
            else:
                result = b
                print(f"Original: {i}")

        padding_number = padding.to_bytes(1, byteorder='little')
        intermediate = xor_string(result, padding_number)
        intermediates.append(intermediate)

        plain = xor_string(intermediate, original)
        print(f"\tByte {blocksize-padding}: {plain}")
        current_block = plain + current_block
        if(padding == blocksize):
            continue

        next_padding = (padding+1).to_bytes(1, byteorder='little')
        tmp = []
        for position in range(len(intermediates)):
            tmp.insert(0, xor_string(intermediates[position], next_padding))
        fake = b''.join(tmp)

    print(f"Block {block}: {current_block}\n")
    plaintext = current_block + plaintext

print(f"Plaintext: {plaintext}")

'''
GET /party.php HTTP/1.1
Host: edu-ctf.csie.org:10190
Connection: close
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36
Sec-Fetch-User: ?1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Referer: https://edu-ctf.csie.org:10190/user.php
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6,zh-TW;q=0.5
Cookie: session=c050873e-3996-4606-874f-0fa337b13c23; rack.session=BAh7CEkiD3Nlc3Npb25faWQGOgZFVEkiRTFmOTA4MDVhMDM0YWFkMzA2ZjE5%0AMDBmOTM0Y2Q0YzQ4Nzk2MjE0YmM0YzczZTRjMjQxMGI0YmY4N2EyY2Y3ZmIG%0AOwBGSSIKZmxhc2gGOwBGewBJIgx1c2VyX2lkBjsARmkB3g%3D%3D%0A--79fc81cbd824fdb49f7f06a8ed589a8b73b2fba1; PHPSESSID=3gu0675c0kos0glegdi7o75d04; FLAG=1lSDchhQ5l0SSSxLSX9ozsJtZnd4zCXDfrgkPqpJKwCknGnyFiCuFvb%2BL74P6ygKqXDRcyBwI6%2BSK3G%2BRbabxbwubLC1LjSnTqV9i%2BYLhzkPRWRnM96PQ1li5Sq5QZ22
cookie-installing-permission: required
dnt: 1
'''
