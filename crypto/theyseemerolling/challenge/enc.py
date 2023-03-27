
from Crypto.Util.strxor import strxor
from Crypto.Util.number import long_to_bytes
import os

key = os.urandom(8)

def encrypt_block(block):
  return strxor(key, block)

def encrypt(pt):
  ct = b''
  for i in range(0, len(pt), 4):
    index = long_to_bytes(i // 4)
    index = b'\x00' * (4 - len(index)) + index
    ct += encrypt_block(index + pt[i:i+4])
  return ct

if __name__ == '__main__':
  flag = open('flag', 'rb').read()
  flag += b'\x00' * (4 - len(flag) % 4)

  print(encrypt(flag).hex())
