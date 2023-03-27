
from Crypto.Util.strxor import strxor

def decrypt_block(block, key):
  pt = strxor(block, key)
  return pt[4:]

if __name__ == '__main__':
  ct = bytes.fromhex(open('output.txt', 'r').read())

  crib = b'\x00\x00\x00\x00wctf'
  key = strxor(crib, ct[0:8])
  for i in range(0, len(ct), 8):
    print(decrypt_block(ct[i:i+8], key).decode(), end='')

