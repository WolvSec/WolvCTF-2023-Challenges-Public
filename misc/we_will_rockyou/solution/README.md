This challenge is just an intro to zip password craking; there are a few tools, but I like fcrackzip. The key here is using the common rockyou.txt. The entire attack takes about a minute or so to complete.
```shell
fcrackzip -b  -D -p rockyou.txt -u we_will_rock_you.zip 
```

This results in a password of "michigan4ever" and the flag is within the password-protected folder.

```julia
wctf{m1cH1g4n_4_3v3R}
```
