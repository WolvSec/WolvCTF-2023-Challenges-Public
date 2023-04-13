#include <elf.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/mman.h>

#include "sad.h"
#include "x32_xor_blob.h"

static inline void flag_part(void)
{
    char xor_val = 0;
    printf("Decryptor key: ");
    scanf("%c", &xor_val);
    for (unsigned int i = 0; i < g_x32_xor_blob_sz; i++) {
        ((char *)g_x32_xor_blob)[i] ^= xor_val;
    }

    void (*blob)(void) = (void (*)(void)) g_x32_xor_blob;
    blob();
}

static void arm64(void)
{
    Elf32_Ehdr hdr;
    off_t arm64_off, arm64_sz;
    FILE *fexe = NULL;
    FILE *farm64 = NULL;
    size_t nread;
    char buff[1024];

    fexe = fopen("/proc/self/exe", "rb");
    if (fexe == NULL) {
        goto exit;
    }

    if (fread(&hdr, sizeof(hdr), 1, fexe) != 1) {
        goto exit;
    }
    arm64_off = hdr.e_shoff;
    arm64_off += (hdr.e_shnum * hdr.e_shentsize);

    if (fseek(fexe, 0, SEEK_END)) {
        goto exit;
    }

    if ((arm64_sz = ftell(fexe)) == -1) {
        goto exit;
    }
    arm64_sz -= arm64_off;

    if (arm64_sz <= 0) {
        goto exit;
    }

    if (fseek(fexe, arm64_off, SEEK_SET)) {
        goto exit;
    }

    farm64 = fopen("pimp-my.ride", "wb+");
    if (farm64 == NULL) {
        goto exit;
    }

    while ((nread = fread(buff, 1, 1024, fexe)) > 0) {
        if (fwrite(buff, nread, 1, farm64) != 1) {
            goto exit;
        }
        arm64_sz -= nread;
    }

    if (arm64_sz) {
        goto exit;
    }

    if (chmod("pimp-my.ride", S_IRUSR | S_IWUSR | S_IXUSR)) {
        goto exit;
    }

exit:
    if (fexe != NULL) {
        fclose(fexe);
    }

    if (farm64 != NULL) {
        fclose(farm64);
    }
}


static inline long my_ptrace(void)
{
   long ret;
    __asm__ volatile(
        "mov $0, %%ebx\n"
        "mov $0, %%ecx\n"
        "mov $0, %%edx\n"
        "mov $0, %%esi\n"
        "mov $26, %%eax\n"
        "int $128\n"
        "mov %%eax, %0" 
        : "=r"(ret) 
        : 
        : "ebx", "ecx", "edx", "esi", "eax"
    );

    return ret;
}

static void meme(void)
{
    FILE *fsad = NULL;
    printf("I am disappointed :(\n");

    if ((fsad = fopen("meme.pdf", "wb+")) == NULL) {
        fprintf(stderr, "Whoops\n");
        return;
    }

    if (fwrite(g_sad, g_sad_sz, 1, fsad) != 1) {
        fprintf(stderr, "Whoops\n");
    }
    fclose(fsad);
}

int main(void)
{
    printf("Dang did you pull me out of that other guy?\n");
    printf("But anyways, welcome to x86!\n");

    if (my_ptrace() == -1) {
        meme();
    }
    else {
        flag_part();
        arm64();
    }
    return 0;
}