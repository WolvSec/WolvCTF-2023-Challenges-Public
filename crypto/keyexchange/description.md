# keyexchange

Diffie-Hellman key exchange is used in many cryptographic protocols to set up
a shared key between two parties. However, this only works if you choose good
values of `a` and `b`. In this case, we are allowed to control the value of `b`.
In Diffie-Hellman, the secret key is computed as `s^(ab) mod N`. Since we have 
access to `g^a mod N`, but not `N`, we can't regenerate the shared key exactly.
However, if we give the program `b = 1`, then we know the shared key will just
be the same value! Thus, we'll be able to find the decryption key.
