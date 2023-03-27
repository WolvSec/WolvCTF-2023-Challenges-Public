CC=gcc
CFLAGS=-I. -fno-stack-protector -no-pie -g
EXECUTABLE=challenge

all: $(EXECUTABLE)

$(EXECUTABLE): challenge.c
	$(CC) $(CFLAGS) -o $(EXECUTABLE) challenge.c

clean:
	$(RM) $(EXECUTABLE)
