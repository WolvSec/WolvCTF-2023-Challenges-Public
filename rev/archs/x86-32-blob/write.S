    .equ SYS_WRITE, 4
    .global write
    .text
write:
    mov     4(%esp), %ebx
    mov     8(%esp), %ecx
    mov     12(%esp), %edx
    mov     $SYS_WRITE, %eax
    push    %ecx
    push    %edx
    push    %ebp
    mov     %esp, %ebp
    sysenter
