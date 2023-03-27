
prefix = 'wctf{'
numbers = [ord(c) for c in prefix]
end = ord('}')

import time
import random

starttime = time.time()

for seed in range(23068672 + 2**31, 2**32):
  if seed % 0x100000 == 0:
    print(f'{seed} seeds searched in {time.time() - starttime} seconds')

  random.seed(seed)
  correct = True
  for i in range(len(numbers)):
    if random.randint(97, 126) != numbers[i]:
      correct = False
  if correct:
    print('seed = ', seed)
    print(prefix, end='')
    generated = []
    for _ in range(32):
      c = random.randint(97, 126)
      generated.append(c)
      if c == end:
        print(''.join(chr(x) for x in generated))
        break
