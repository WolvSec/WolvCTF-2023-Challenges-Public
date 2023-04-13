#include <elf.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>

#include "wtf.h"

static clock_t start;

static inline void meme(void)
{
    FILE *fmp4 = NULL;

    if ((fmp4 = fopen("pimp.mp4", "wb+")) == NULL) {
        fprintf(stderr, "Dang\n");
        return;
    }

    if (fwrite(g_wtf, g_wtf_sz, 1, fmp4) != 1) {
        fprintf(stderr, "Dang\n");
    }
    fclose(fmp4);
}


static inline void decrypt_mips32(void)
{
    // vigenere cipher key: MIPS32
    char pass[32] = { 0 };
    FILE *fmips32 = NULL;
    FILE *fdecoded = NULL;
    printf("What do you think the next ARCH is?: ");
    if ((clock() - start) > 10000) {
        meme();
        goto exit;
    }
    scanf("%31s", pass);

    fmips32 = fopen("west-coast", "rb");
    fdecoded = fopen("customs", "wb+");
    if (fmips32 == NULL || fdecoded == NULL) {
        goto exit;
    }

    size_t mod = strlen(pass);

    int cur_char = 20;
    int xor_char = 0;
    int count = 0;
    while ((cur_char = fgetc(fmips32)) != EOF) {
        xor_char = (int)(((unsigned char) cur_char) ^ pass[count % mod]);
        if (fputc(xor_char, fdecoded) !=  xor_char) {
            goto exit;
        }
        count++;
    } 

exit:
    if (fmips32 != NULL) {
        fclose(fmips32);
    }

    if (fdecoded != NULL) {
        fclose(fdecoded);
    }
}

static inline void mips32(void)
{
    Elf64_Ehdr hdr;
    off_t mips32_off, mips32_sz;
    FILE *fexe = NULL;
    FILE *fmips32 = NULL;
    size_t nread;
    char buff[1024];

    if ((clock() - start) > 10000) {
        meme();
        return;
    }
    fprintf(stderr, "I hope you are not using QEMU!\n");

    //FIX ME BEFORE RELEASE
    fexe = fopen("/proc/self/exe", "rb");
    if (fexe == NULL) {
        goto exit;
    }

    if (fread(&hdr, sizeof(hdr), 1, fexe) != 1) {
        goto exit;
    }
    mips32_off = hdr.e_shoff;
    mips32_off += (hdr.e_shnum * hdr.e_shentsize);

    if (fseek(fexe, 0, SEEK_END)) {
        goto exit;
    }

    if ((mips32_sz = ftell(fexe)) == -1) {
        goto exit;
    }
    mips32_sz -= mips32_off;

    if (mips32_sz <= 0) {
        goto exit;
    }

    if (fseek(fexe, mips32_off, SEEK_SET)) {
        goto exit;
    }

    fmips32 = fopen("west-coast", "wb+");
    if (fmips32 == NULL) {
        goto exit;
    }

    while ((nread = fread(buff, 1, 1024, fexe)) > 0) {
        if (fwrite(buff, nread, 1, fmips32) != 1) {
            goto exit;
        }
        mips32_sz -= nread;
    }

    if (mips32_sz) {
        goto exit;
    }

    if (chmod("west-coast", S_IRUSR | S_IWUSR | S_IXUSR)) {
        goto exit;
    }

exit:
    if (fexe != NULL) {
        fclose(fexe);
    }

    if (fmips32 != NULL) {
        fclose(fmips32);
    }
}




static inline void flag_part(void)
{
    // vigenere cipher key: ARM64
    char flag[11] = { 30, 38, 37, 2, 64, 30, 37, 121, 69, 107, 0 };
    char pass[32] = { 0 };
    printf("Decryptor pass: ");
    scanf("%31s", pass);
    start = clock();
    size_t mod = strlen(pass);
    for (int i = 0; i < 10; i++) {
        char xor = pass[i % mod];
        flag[i] ^= xor;
    }
    if ((clock() - start) > 10000) {
        meme();
        return;
    }
    
    printf("Another flag part: %s\n", flag);
}


int main(void)
{
    start = clock();
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    printf("What the f? How did you make it this far?\n");
    printf("I guess welcome to _ARM64_!\n");

    if ((clock() - start) > 10000) {
        meme();
    }
    else {
        flag_part();
        start = clock();
        mips32();
        start = clock();
        decrypt_mips32();
    }

    return 0;
}