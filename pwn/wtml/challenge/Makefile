CC=gcc
CFLAGS=-I. -fno-stack-protector -Wno-format-security -Wl,-z,norelro
EXECUTABLE=challenge

all: $(EXECUTABLE)

$(EXECUTABLE): challenge.c
	$(CC) $(CFLAGS) -o $(EXECUTABLE) challenge.c

clean:
	$(RM) $(EXECUTABLE)
