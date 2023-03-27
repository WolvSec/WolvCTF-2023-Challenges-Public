# yellsatbefunge3

Self-modifying code is annoying to deal with and can lead to vulnerabilties. Let's execute Read-Only Befunge.

So, we've eliminated the ability to write to the board at least. Well, if we
can't get out, we can just read the flag from outside! This is a bit trickier
since the solution involves writing Befunge from scratch. The general gist
involves finding the row and column needed, and then looping through each column
until we read off the board. Below is a relatively short solution!

```
v @@@@@@@@@@@@@@@@@@@@
v @@@@@@@@@@@@@@@@@@@@
v @@>1>1+:7g,v      @@ ok, now you REALLY can't get out now
>>>>^ ^      <      @@
v @@                @@
v @@@@@@@@@@@@@@@@@@@@
v @@@@@@@@@@@@@@@@@@@@
>"wctf{.r--r--r--_00p5}">,v
                        ^ <
```
