The challenge provides only one file, `homework_help` which appears to be a x86-64 ELF binary. 
First, lets open up the binary in a disassembler and take a look at what's inside.

Show functions (using r2 as dissasmbler) 
```
[0x00000000]> fs symbols
[0x00000000]> f | grep "sym"

0x00001000 27 sym._init
0x00001180 22 sym.main
0x000011a0 38 sym._start
0x000011d0 41 sym.deregister_tm_clones
0x00001200 57 sym.register_tm_clones
0x00001240 57 sym.__do_global_dtors_aux
0x00001280 0 sym.frame_dummy
0x00001290 429 sym.__stack_chk_fail
0x00001440 67 sym.offer_help
0x00001490 302 sym.eval
0x000015c0 116 sym.ask
0x00001634 13 sym._fini
```

We can see some familiar symbols here like `main`, but also the functions `offer_help`, `eval` , and `ask`. Let's start from `main` and follow where it takes us.

`main`   disas
```
[0x00000000]> s sym.main
[0x00001180]> pdf

            ; DATA XREF from entry0 @ 0x11b8
            ;-- section..text:
            ;-- name:
┌ 22: int main (int argc, char **argv, char **envp);
│           0x00001180      f30f1efa       endbr64
│           0x00001184      4883ec08       sub rsp, 8
│           0x00001188      31c0           xor eax, eax
│           0x0000118a      e831040000     **call sym.ask**
│           0x0000118f      31c0           xor eax, eax
│           0x00001191      4883c408       add rsp, 8
└           0x00001195      c3             ret
```

All this is doing is calling `ask`, one of the functions we saw. We can use the same method as we did with `main` in order to seek to, and print `ask`. To keep this consise, I will not include the disassembly for these functions.

By continuing this process, we determine that `ask` just prompts the user for input and passes the results to `eval`.  `eval` is the most complex of the functions seen so far, but in general it appears to do the following: 
1. Do some operations on the input recived from `ask`.
2. If the result of the operations is not 3, then return.
3. If the result is 3 it prints "Thanks, I'll help you check the flag." and reads in the data to `FLAG`
4. Returns

What's strange is, After reading in the user supplied flag, `eval` returns to `ask`, which then immediatly return to main. Where is the flag check?

Check XREFs to `FLAG`
```
[0x00001490]> axt obj.FLAG

sym.__stack_chk_fail 0x13c1 [DATA] lea rcx, obj.FLAG
sym.offer_help 0x1477 [DATA] lea rdi, obj.FLAG
sym.eval 0x1593 [DATA] lea rdi, obj.FLAG
```

It's very weird that `__stack_chk_fail` would reference `FLAG`. 

```
[0x00001490]> s sym.__stack_chk_fail 
[0x00001290]> pdf

┌ 420: void sym.__stack_chk_fail ();
│           ; var int64_t var_ch @ rsp+0xc
│           ; var int64_t var_10h @ rsp+0x10
│           ; var int64_t var_14h @ rsp+0x14
│           ; var int64_t var_18h @ rsp+0x18
│           ; var int64_t var_20h @ rsp+0x20
│           ; var int64_t var_28h @ rsp+0x28
│           ; var int64_t var_30h @ rsp+0x30
│           ; var int64_t var_38h @ rsp+0x38
│           ; var int64_t var_40h @ rsp+0x40
│           ; var int64_t var_48h @ rsp+0x48
│           ; var int64_t var_50h @ rsp+0x50
│           ; var int64_t var_58h @ rsp+0x58
│           ; var int64_t var_60h @ rsp+0x60
│           ; var int64_t var_68h @ rsp+0x68
│           ; var int64_t var_70h @ rsp+0x70
│           ; var int64_t var_78h @ rsp+0x78
│           ; var int64_t var_80h @ rsp+0x80
│           ; var int64_t var_88h @ rsp+0x88
│           ; var jmpbuf env @ rsp+0x90
│           ; var int64_t var_158h @ rsp+0x158
│           0x00001290      f30f1efa       endbr64
│           0x00001294      4881ec680100.  sub rsp, 0x168
│           0x0000129b      64488b042528.  mov rax, qword fs:[0x28]
│           0x000012a4      488984245801.  mov qword [var_158h], rax
│           0x000012ac      31c0           xor eax, eax
│           0x000012ae      488dbc249000.  lea rdi, [env]              ; jmpbuf env
│           0x000012b6      48b817000000.  movabs rax, 0x1200000017
│           0x000012c0      c74424141400.  mov dword [var_14h], 0x14   ; [0x14:4]=1
│           0x000012c8      4889442418     mov qword [var_18h], rax
│           0x000012cd      48b81d000000.  movabs rax, 0x500000001d
│           0x000012d7      4889442420     mov qword [var_20h], rax
│           0x000012dc      48b846000000.  movabs rax, 0x5d00000046
│           0x000012e6      4889442428     mov qword [var_28h], rax
│           0x000012eb      48b842000000.  movabs rax, 0x4100000042
│           0x000012f5      4889442430     mov qword [var_30h], rax
│           0x000012fa      48b86c000000.  movabs rax, 0x330000006c
│           0x00001304      4889442438     mov qword [var_38h], rax
│           0x00001309      48b85d000000.  movabs rax, 0x5a0000005d
│           0x00001313      4889442440     mov qword [var_40h], rax
│           0x00001318      48b80e000000.  movabs rax, 0x3a0000000e
│           0x00001322      4889442448     mov qword [var_48h], rax
│           0x00001327      48b86a000000.  movabs rax, 0x410000006a
│           0x00001331      4889442450     mov qword [var_50h], rax
│           0x00001336      48b840000000.  movabs rax, 0x5700000040
│           0x00001340      4889442458     mov qword [var_58h], rax
│           0x00001345      48b808000000.  movabs rax, 0x3400000008
│           0x0000134f      4889442460     mov qword [var_60h], rax
│           0x00001354      48b83c000000.  movabs rax, 0xb0000003c
│           0x0000135e      4889442468     mov qword [var_68h], rax
│           0x00001363      48b803000000.  movabs rax, 0x3400000003
│           0x0000136d      4889442470     mov qword [var_70h], rax
│           0x00001372      48b828000000.  movabs rax, 0x4600000028
│           0x0000137c      4889442478     mov qword [var_78h], rax
│           0x00001381      48b85f000000.  movabs rax, 0x530000005f
│           0x0000138b      488984248000.  mov qword [var_80h], rax
│           0x00001393      48b810000000.  movabs rax, 0x5000000010
│           0x0000139d      488984248800.  mov qword [var_88h], rax
│           0x000013a5      c744240c3600.  mov dword [var_ch], 0x36
│           0x000013ad      e86efdffff     **call sym.imp._setjmp** : int setjmp(jmpbuf env)
│           0x000013b2      f30f1efa       endbr64
│           0x000013b6      85c0           test eax, eax
│       ┌─< 0x000013b8      755e           jne 0x1418
│       │   0x000013ba      31c0           xor eax, eax
│       │   0x000013bc      ba41000000     mov edx, 0x41               ; 'A'
│       │   0x000013c1      488d0d782c00.  lea rcx, obj.FLAG           ; 0x4040
│      ┌──< 0x000013c8      eb0a           jmp 0x13d4
..
│      ││   ; CODE XREF from sym.__stack_chk_fail @ 0x13ec
│     ┌───> 0x000013d0      8b548410       mov edx, dword [rsp + rax*4 + 0x10]
│     ╎││   ; CODE XREF from sym.__stack_chk_fail @ 0x13c8
│     ╎└──> 0x000013d4      3154240c       xor dword [var_ch], edx
│     ╎ │   0x000013d8      0fbe1401       movsx edx, byte [rcx + rax]
│     ╎ │   0x000013dc      8b74240c       mov esi, dword [var_ch]
│     ╎ │   0x000013e0      39f2           cmp edx, esi
│     ╎┌──< 0x000013e2      7542           jne 0x1426
│     ╎││   0x000013e4      4883c001       add rax, 1
│     ╎││   0x000013e8      4883f820       cmp rax, 0x20               ; "@"
│     └───< 0x000013ec      75e2           jne 0x13d0
│      ││   0x000013ee      488d3d0f0c00.  lea rdi, str.Well_Done.     ; 0x2004 ; "Well Done." ; const char *s
│      ││   0x000013f5      e8e6fcffff     **call sym.imp.puts**       ; int puts(const char *s)
│      ││   ; CODE XREF from sym.__stack_chk_fail @ 0x1424
│     ┌───> 0x000013fa      488b84245801.  mov rax, qword [var_158h]
│     ╎││   0x00001402      64482b042528.  sub rax, qword fs:[0x28]
│    ┌────< 0x0000140b      752b           jne 0x1438
│    │╎││   0x0000140d      4881c4680100.  add rsp, 0x168
│    │╎││   0x00001414      c3             ret
..
│    │╎││   ; CODE XREF from sym.__stack_chk_fail @ 0x13b8
│    │╎│└─> 0x00001418      488d3df00b00.  lea rdi, str.Nope.          ; 0x200f ; "Nope." ; const char *s
│    │╎│    0x0000141f      e8bcfcffff     **call sym.imp.puts**       ; int puts(const char *s)
│    │└───< 0x00001424      ebd4           jmp 0x13fa
│    │ │    ; CODE XREF from sym.__stack_chk_fail @ 0x13e2
│    │ └──> 0x00001426      488dbc249000.  lea rdi, [env]
│    │      0x0000142e      be01000000     mov esi, 1
│    │      0x00001433      e828fdffff     **call sym.imp.__longjmp_chk**
│    │      ; CODE XREF from sym.__stack_chk_fail @ 0x140b
└    └────> 0x00001438      e853feffff     **call sym.__stack_chk_fail**   ; void __stack_chk_fail(void)
```


This looks like the flag check. PWN players may have recognized the `gets` call in `ask` that is vulnerable to a buffer overflow. If an overflow occurs, then the stack canary will be overwritten and `__stack_chk_fail` will get called right before `ask` would normally return (after `eval`). Normally `__stack_chk_fail` would segfault the program, but here it has been overwritten to check the flag first.   Let's reverse this check for the flag.

This function starts by initializing an integer array, then loops at `0x13d0` 32 times, iterating over the int array. Each element in the array is xored with the value in `var_ch` and this result is saved back to `var_ch`. We can extract the array and the initial value of `var_ch` to generate the flag. Be careful of endianess when extracting the array.

Python solver
```
data = bytearray([0x41, 0x14, 0x17, 0x12, 0x1d, 0x50, 0x46, 0x5d,
                  0x42, 0x41, 0x6c, 0x33, 0x5d, 0x5a, 0x0e, 0x3a, 
                  0x6a, 0x41, 0x40, 0x57, 0x08, 0x34, 0x3c, 0x0b, 
                  0x03, 0x34, 0x28, 0x46, 0x5f, 0x53, 0x10, 0x50])
  
c = 0x36          # var_ch
for b in data:
    c = b ^ c
    print(chr(c), end='')
print()
```

```
$ python3 solve.py 

wctf{+m0r3_l1ke_5t4ck_chk_w1n=-}
```
