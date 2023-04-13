#include <stdio.h>
#include <string.h>

char *flag = "wctf{Oh10_Stat3_1s_Smelly!}";

int main(void)
{
    char buff[256] = { 0 };
    printf("Just a baby reverse engineering challenge\n");
    printf("Ohio State University is the? ");
    fgets(buff, sizeof(buff), stdin);

    if (!strncmp(buff, "worst\n", sizeof(buff))) {
        printf("Correct! But the flag is elsewhere\n");
    } 
    else if (!strncmp(buff, "best\n", sizeof(buff))) {
        printf("wctf{Must_be_fr0m_OSU}\n");
    }
    else {
        printf("wctf{A_t0tally_fake_flag}\n");
    }
}