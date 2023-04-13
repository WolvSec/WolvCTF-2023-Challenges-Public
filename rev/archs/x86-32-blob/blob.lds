ENTRY(_entry)
SECTIONS
{
    .text : {
        *(.entry*)
        *(.text*)
    }
    .data : {
        *(*.got*)
        *(*.rodata*)
        *(*.data*)
        *(*.bss*)
    }
    /DISCARD/ : { *(*) }
}
