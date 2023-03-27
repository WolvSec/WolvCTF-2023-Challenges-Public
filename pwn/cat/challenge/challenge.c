
#include <stdlib.h>
#include <stdio.h>

void win() {
  puts("Told you C was dangerous :P");
  system("/bin/sh");
}

int main() {
  setvbuf(stdin, NULL, 0, 0);
  setvbuf(stdout, NULL, 0, 0);

  puts("Welcome to the C Analysis Tool (cat). Enter your C code below, and it will print out which lines are dangerous!\n");
  fflush(stdout);
  char buffer[128];

  gets(buffer);
  puts(buffer);
}
