#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    printf("You got to the end! Congrats!\n");
    printf("Flag part: ann0y1ng?!}\n");
    
    return 0;
}