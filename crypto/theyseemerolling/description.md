# they see me rollin (my own crypto)

This challenge provides an introduction to utilizing a crib! The cipher is
designed to encrypt four bytes at a time, which are combined with a "counter".
This string is XORed with a secret key, and then output. Here, due to the setup,
we are able to utilize the knowledge that the first four characters are `wctf`
to immediately find the secret key! We know that the first eight bytes are
`wctf\x00\x00\x00\x00` XORed with the key, so by reversing the XOR, we can find
the key and decrypt all subsequent blocks.
