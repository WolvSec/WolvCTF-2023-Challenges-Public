#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tiny_aes.h"

#define CBC 1


static volatile uint8_t key_d[] = { 0x9b, 0x30, 0xe8, 0xe4, 0x96, 0x71, 0xbf, 0xa3, 0x3c, 0xf1, 0x97, 0x4e, 0xc0, 0x40, 0x70, 0x61 };
static volatile uint8_t flag_d[] = { 0x52, 0xbc, 0x27, 0xb6, 0xe6, 0x2f, 0xcb, 0x4d, 0x17, 0x68, 0x4f, 0x4f, 0xc8, 0xa0, 0x3b, 0x7d, 0x63, 0x18, 0x09, 0x59, 0xa7, 0x5f, 0xfe, 0x1b, 0x22, 0xa7, 0x4c, 0xbd, 0x9d, 0xcd, 0x05, 0xa7 };
static volatile uint8_t iv_d[]  = { 0x63, 0x2b, 0x5f, 0x35, 0xcd, 0x63, 0x01, 0xeb, 0x26, 0xa5, 0x8a, 0x62, 0x1c, 0x89, 0xb9, 0xe3 };


#pragma GCC push_options
#pragma GCC optimize ("O0")
void lfsr16_obfuscate(volatile uint8_t *s, int length, unsigned short seed) {
    int i, lsb;

    for (i=0; i<length; i++) {
        s[i] ^= seed & 0x00ff;
        lsb = seed & 1;
        seed >>= 1;
        if (lsb) seed ^= 0xB400u;
    }
}
#pragma GCC pop_options

static int do_cbc(uint8_t *flag)
{
    uint8_t *key = malloc(16);
    uint8_t *iv = malloc(16);
    int i = 0;
    int j = 0;
    for (j = 0; j < 16; j++) {
        flag[j + 16] = flag_d[j + 16];
    }
    for (i = 0; i < 16; i++) {
        key[i] = key_d[i];
        iv[i] = iv_d[i];
        flag[i] = flag_d[i];
    }
    // uint8_t out_flag[]  = { 'w',  'c',  't',  'f',  '{',  'W',  '3',  '1',  'l',  '_',  '1',  '_',  'g',  'u',  '3',  '5',
    //                         's',  '_',  '1',  't',  '_',  'w',  '4',  '5',  '_',  '4',  '3',  '5',  ':',  ')',  '}',  '\0',
    //                       };
    
    // struct AES_ctx enc_ctx;
    
    // AES_init_ctx_iv(&enc_ctx, key, iv);
    
    // AES_CBC_encrypt_buffer(&enc_ctx, out_flag, 32);

    // lfsr16_obfuscate(out_flag, 16, 0x8953);
    // lfsr16_obfuscate(out_flag + 16, 16, 0x9018);

    // i = 0;
    // for (i = 0; i < 32; i++) {
    //     printf("0x%02x, ", out_flag[i]);
    // }
    // printf("\n");

    struct AES_ctx dec_ctx;
    AES_init_ctx_iv(&dec_ctx, key, iv);
    
    AES_CBC_decrypt_buffer(&dec_ctx, flag, 32);
    free(key);
    free(iv);
    return 0;
}


int main(int argc) {
    
    printf("What are you doing here?\n");
    uint8_t *flag = malloc(32);
    int i = 0;
    for (i = 0; i < argc; ++i)
    {
        if (i % 2) {
            lfsr16_obfuscate(key_d, 16, 0x3856);
            lfsr16_obfuscate(iv_d, 16, 0x6378);
            lfsr16_obfuscate(flag_d, 16, 0x8953);
            lfsr16_obfuscate(flag_d + 16, 16, 0x9018);
        }
        do_cbc(flag);
    }
    printf("Well since you're here anyway have a flag:\n%s\n", flag);
    free(flag);
    return 0;
}
