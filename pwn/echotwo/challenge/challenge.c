#include <stdio.h>
#include <stdlib.h>


void echo() {
    printf("Welcome to Echo2\n");

    int num_bytes;
    int result = scanf("%d", &num_bytes);
    char buffer[256];
    fread(buffer, sizeof(char), num_bytes, stdin);
    printf("Echo2: %s\n",buffer);
}

int main() {
    // void *handle = dlopen("libc.so.6", RTLD_GLOBAL);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    echo();
    printf("Goodbye from Echo2\n");
    return 0;
}
