#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/ptrace.h>

#include "xzibit.h"
#include "x32_xor.h"

static void x32(void)
{
    char *x32_addr = NULL;
    char xor_val = 0;
    int prot = PROT_EXEC | PROT_READ | PROT_WRITE;
    int flags = MAP_PRIVATE | MAP_ANONYMOUS;
    x32_addr = mmap(NULL, g_x32_xor_sz, prot, flags, -1, 0);

    if (x32_addr == MAP_FAILED) {
        exit(1);
    }

    // Key is 0x40 @
    printf("Decryptor key: ");
    scanf("%c", &xor_val);
    for (unsigned int i = 0; i < g_x32_xor_sz; i++) {
        x32_addr[i] = ((char *)g_x32_xor)[i] ^ xor_val;
    }
    
    printf("Here is part of the flag: wctf{\n");
    printf("Now what?\n");
}

static void meme(void)
{
    FILE *fxzibit = NULL;
    printf("Naughty! I put a meme on your disk :)\n");

    if ((fxzibit = fopen("meme.webp", "wb+")) == NULL) {
        fprintf(stderr, "Whoops\n");
        return;
    }

    if (fwrite(g_xzibit, g_xzibit_sz, 1, fxzibit) != 1) {
        fprintf(stderr, "Whoops\n");
    }
    fclose(fxzibit);
}

int main(void)
{
    printf("Yo dawg I heard you like architectures, so we "
           "put architectures in your architectures!\n");

    if (ptrace(PTRACE_TRACEME, 0, 0 , 0) == -1) {
        meme();
    }
    else {
        x32();
    }
    return 0;
}