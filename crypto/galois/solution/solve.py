from pwn import *
from Crypto.Util.number import *
from Crypto.Util.strxor import *
import argparse

def GF_mult(x, y):
    product = 0
    for i in range(127, -1, -1):
        product ^= x * ((y >> i) & 1)
        x = (x >> 1) ^ ((x & 1) * 0xE1000000000000000000000000000000)
    return product

def H_mult(H, val):
    product = 0
    for i in range(16):
        product ^= GF_mult(H, (val & 0xFF) << (8 * i))
        val >>= 8
    return product

def GHASH(H, A, C):
    C_len = len(C)
    A_padded = bytes_to_long(A + b'\x00' * (16 - len(A) % 16))
    if C_len % 16 != 0:
        C += b'\x00' * (16 - C_len % 16)

    tag = H_mult(H, A_padded)

    for i in range(0, len(C) // 16):
        tag ^= bytes_to_long(C[i*16:i*16+16])
        tag = H_mult(H, tag)

    tag ^= bytes_to_long((8*len(A)).to_bytes(8, 'big') + (8*C_len).to_bytes(8, 'big'))
    tag = H_mult(H, tag)

    return tag


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--remote', type=str, default=None)

    args = parser.parse_args()

    if args.debug:
        context.terminal = ['tmux', 'splitw', '-h']
        conn = gdb.debug(context.binary.path, '''
        set follow-fork-mode child
        break main
        continue
        ''')
    elif args.remote:
        ip, port = args.remote.split(':')
        conn = remote(ip, port)
    else:
        conn = process(['python3', '../release/server.py'])  # Actually start running the process

    AES_BLOCK_SIZE = 16
    message = b'heythisisasupersecretsupersecret'
    header = b"WolvCTFCertified"

    # first encryption
    conn.recvuntil(b'> ')
    conn.sendline(b'1')

    conn.recvuntil(b'> ')
    conn.sendline(b'F' * 32) # IV of Fs

    conn.recvuntil(b'> ')
    conn.sendline(b'0' * 64) # 3 blocks of 0s

    ct = conn.recvline(keepends = False)[5:]
    tag = conn.recvline(keepends = False)[6:]
    print("ct is", ct)
    print("tag is", tag)

    tag = bytes.fromhex(tag.decode("utf-8"))
    ct = bytes.fromhex(ct.decode("utf-8"))

    # second encryption
    conn.recvuntil(b'> ')
    conn.sendline(b'1')

    conn.recvuntil(b'> ')
    conn.sendline((b'0' * 31) + (b'1')) # IV of Fs

    conn.recvuntil(b'> ')
    conn.sendline(b'0' * 64) # 3 blocks of 0s

    ct2 = conn.recvline(keepends = False)[5:]
    tag = conn.recvline(keepends = False)[6:]
    print("ct is", ct)
    print("tag is", tag)

    tag = bytes.fromhex(tag.decode("utf-8"))
    ct2 = bytes.fromhex(ct2.decode("utf-8"))


    # ct  - first block is enc(0), second block is enc(1)
    # ct2 - first block is enc(2)
    # enc(0) is ct[0]
    # enc(1) is ct[1]
    # enc(2) is ct[2]

    temp_ct = ct[:AES_BLOCK_SIZE*2] + ct2[:AES_BLOCK_SIZE]

    numBlocks = 2
    submit_ct = b''
    for i in range(1, numBlocks + 1):
        submit_ct += strxor(
            temp_ct[i * AES_BLOCK_SIZE: (i+1) * AES_BLOCK_SIZE],
            message[(i-1) * AES_BLOCK_SIZE: i * AES_BLOCK_SIZE])
    hkey = temp_ct[:AES_BLOCK_SIZE]
    authTag = strxor(
        temp_ct[:AES_BLOCK_SIZE],
        long_to_bytes(GHASH(bytes_to_long(hkey), header, submit_ct))
    )

    # submission
    conn.recvuntil(b'> ')
    conn.sendline(b'2')

    conn.recvuntil(b'> ')
    conn.sendline(b'0' * 32) # IV of 0s

    conn.recvuntil(b'> ')
    conn.sendline(submit_ct.hex().encode()) # ct

    conn.recvuntil(b'> ')
    conn.sendline(authTag.hex().encode()) # tag of Fs

    print(conn.recvline(keepends=False))