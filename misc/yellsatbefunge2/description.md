# yellsatbefunge2

Ok... so maybe making the walls out of bridges wasn't a good idea. 
Now the program halts if you run into a wall. Surely you can't get out now!

We've fixed the wall issue! Well... sort of. Not really.

Remember the bridges from yellsatbefunge1? We can utilize those to skip past the
halt instruction! We'll move the program counter over to a similar place, but
while doing so, we'll also write a bridge into the wall (since the wall is two
instructions "thick"). Thus, we'll overwrite the wall to be `@#`, and when we
execute this, the bridge will skip the halt!
