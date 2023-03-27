#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.number import *
from Crypto.Util.strxor import strxor
from pwn import *
import argparse

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('remote', type=str, default=None)

  args = parser.parse_args()

  c = remote(*args.remote.split(':'))

  # Read in s ^ a mod n
  line = c.recvline().strip().decode()
  if line.startswith('== proof-of-work'):
    line = c.recvline().strip().decode()
  
  s_a_mod_n = int(line)

  # Send b = 1
  c.recv()
  c.sendline(b'1')

  # Read in the encrypted flag
  result = c.recvline().strip().decode()

  # Decrypt
  key = long_to_bytes(s_a_mod_n)
  dec = strxor(bytes.fromhex(result), key)
  print(dec.decode().strip())
