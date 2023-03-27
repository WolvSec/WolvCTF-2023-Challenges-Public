# yellsatbefunge4

The last challenge! Now, we're only allowed a single write, and the walls have
expanded to be four tiles "thick". This means that we can't utilize a bridge to
skip over halts. This is where an interesting feature of Befunge can be used:
string mode. When Befunge runs into a `"` character, it will enter string mode
and start pushing all characters it encounters onto the stack until it runs into
another `"`. Thus, we can use this to bypass a wall of _any_ size!

```
v @@@@@@@@@@@@@@@@@@@@@@@@
v @@@@@@@@@@@@@@@@@@@@@@@@
v @@@@@@@@@@@@@@@@@@@@@@@@
v @@@@@@@@@@@@@@@@@@@@@@@@
v @@@@                @@@@ how many times have i said this now?
>>>>>>98+2*16pv       @@@@
v @@@@"       <       @@@@
v @@@@@@@@@@@@@@@@@@@@@@@@
v @@@@@@@@@@@@@@@@@@@@@@@@
v @@@@@@@@@@@@@@@@@@@@@@@@
v @@@@@@@@@@@@@@@@@@@@@@@@
>"wctf{string_mode?_xd}">,v
                        ^ <
```

Here, we'll write a `"` charater just past the wall and allow Befunge to skip
over all of the intermediate halt instructions.
