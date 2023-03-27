from pwn import *

context(arch='mips', os='linux', endian='big', word_size=32)

# Establish the target process to patch
target = elf.ELF('main')

# map ffffffffffff9028 to -0x2760($gp), 0x100abaa0

# ptmalloc_init
target.asm(target.symbols['ptmalloc_init'] + 0x9c, 'nop')

target.asm(target.symbols['__libc_malloc'] + 0x4c, 'move $s0, $zero')

# target.asm(target.symbols['__libc_malloc'] + 0x58, 'nop')

# patch 0x1000d0d4
target.asm(target.symbols['arena_get2.isra.5'] + 0x35c, 'nop')

# patch 0x100155a4
target.asm(target.symbols['__ctype_init'] + 0x14, 'nop')

# patch 0x100155b4
target.asm(target.symbols['__ctype_init'] + 0x20, 'nop')

# patch 0x100155c0
target.asm(target.symbols['__ctype_init'] + 0x24, 'nop')

# patch 0x100155cc
# target.p32(target.symbols['__ctype_init'] + 0x30, 0x6786d8a0)

target.asm(target.symbols['__ctype_init'] + 0x30, 'nop')

target.asm(target.symbols['__ctype_init'] + 0x3c, 'nop')

target.asm(target.symbols['__ctype_init'] + 0x4c, 'nop')

target.asm(target.symbols['__ctype_init'] + 0x54, 'nop')

target.asm(target.symbols['__ctype_init'] + 0x5c, 'nop')

target.asm(target.symbols['__ctype_init'] + 100, 'nop')

target.asm(target.symbols['__ctype_init'] + 108, 'nop')

# patch 0x100155dc
target.asm(target.symbols['__ctype_init'] + 0x2c, 'nop')

# patch 0x100155e4
target.asm(target.symbols['__ctype_init'] + 0x50, 'nop')

# patch 0x100155ec
target.asm(target.symbols['__ctype_init'] + 0x38, 'nop')

# patch 0x100155f4
target.asm(target.symbols['__ctype_init'] + 0x60, 'nop')

# patch 0x100155fc
target.asm(target.symbols['__ctype_init'] + 0x44, 'nop')

# patch 0x10004c94
target.p32(target.symbols['__libc_start_main'] + 0x1a4, 0x679ad8a0)

target.asm(target.symbols['arena_get2.isra.5'] + 876, 'nop')

target.save('main_patched')
