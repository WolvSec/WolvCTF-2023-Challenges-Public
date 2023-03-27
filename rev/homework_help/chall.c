#include <setjmp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define   FLAG_SIZE  33
const int BUF_SIZE = 8;
char FLAG[FLAG_SIZE];

void __stack_chk_fail() {
	jmp_buf jbuf;
	int offsets[] = {65, 20, 23, 18, 29,  80, 70, 93, 66, 65, 108,
	         	 51, 93, 90, 14, 58, 106, 65, 64, 87,  8,  52, 
			 60, 11,  3, 52, 40,  70, 95, 83, 16, 80};
	int check = 54;
	if(!setjmp(jbuf)) {
		for(int i = 0; i < 32; i++) {
			check = offsets[i] ^ check;
			if(FLAG[i] != check) {
				longjmp(jbuf, 1);
			}
		} 
		puts("Well Done.");
		return;
	}
	puts("Nope.");
	return;
}

void offer_help() {
	puts("Thanks, I'll help you check the flag");
	printf("Flag: ");
	if(fgets(FLAG, FLAG_SIZE, stdin) != NULL){
		return;
	}
} 

int eval(char *buf) {			
	char good_chr[] = "0123456789+\n";
	char *delim = strtok(buf, "+");
	int sum = 0;

	if(strspn(buf, good_chr) != strlen(buf)) {
		puts("Uh, the answer wouldn't look like that");
		return 0.0;
	}

	while(delim) {
		sum += atoi(delim);
		delim = strtok(NULL, "+");
	}

	if (sum != 3) {
		puts("That really dosn't look right, I'll keep trying");
	} else {
		puts("Thanks, I'll help you check the flag");
		printf("Flag: ");
		fgets(FLAG, FLAG_SIZE, stdin);
	}
	return sum;
}

__attribute__((stack_protect)) int ask() {
	char buf[BUF_SIZE];
	puts("Bro can you help me with my homework?");
	puts("What is the largest number of circles with a diameter of 0.7 that will fit completely inside a 2 x 1 rectangle without overlapping?");
	printf("Answer: ");
	gets(buf);
	return eval(buf);
}



int main() {
	int answer = ask();
	return 0;
}


