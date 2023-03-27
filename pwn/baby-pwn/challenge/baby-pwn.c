#include <stdio.h>
#include <string.h>

void print_flag(void)
{
    printf("wctf{W3lc0me_t0_C0stc0_I_L0v3_Y0u!}\n");
}

void vuln(void)
{
    volatile int a = 0xdeadbeef;
    char buff[32] = { 0 };
    printf("Gimme some input: ");
    fgets(buff, 48, stdin);

    if (a != 0xdeadbeef) {
        print_flag();
    }
}


int main(void)
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    vuln();
    return 0;
}
