# 64r2
Octeon Rev
## What You Need
https://github.com/HighW4y2H3ll/OCTEON-im8724-SDK/archive/refs/tags/lfs-mirror.tar.gz  
`git submodule update --init`
## Building
Run `scuba build`
## Solving
Patch the binary with `solv.py` and then run it with upstream `qemu-mips64 -cpu Octeon68XX`
