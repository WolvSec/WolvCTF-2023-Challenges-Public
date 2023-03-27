# Squirrel Feeding

### Idea

Hash map data is stored on the stack

Overflowing the last bucket allows you to increment/decrement the return address

Calculate offset between normal return address and `print` function. Use that as the weight on the overflowing entry. Arguments will already be set up from an existing function call.

### Binary Security

```
Canary                        : ✘ 
NX                            : ✓ 
PIE                           : ✓ 
Fortify                       : ✘ 
RelRO                         : Full
```