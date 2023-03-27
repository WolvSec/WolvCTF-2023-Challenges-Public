CC=gcc
CFLAGS=-I. -fno-stack-protector
EXECUTABLE=challenge

all: $(EXECUTABLE)

$(EXECUTABLE): challenge.c
	$(CC) $(CFLAGS) -o $(EXECUTABLE) challenge.c

clean:
	$(RM) $(EXECUTABLE)
