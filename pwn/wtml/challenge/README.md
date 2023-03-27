# WTML

### Idea

End message with "</" and no null terminator since fread is used.

Replace the tag "\x00" with "\x01" which will make the replacer use v2.

v2 method is vulnerable with printf. Add %p in message to leak libc base. Use second printf to overwrite GOT with one gadget.

### Binary Security

```
Canary                        : ✘ 
NX                            : ✓ 
PIE                           : ✓ 
Fortify                       : ✘ 
RelRO                         : ✘ 
```
