SOURCES = NoisyParityDemo.c MultiClassTsetlinMachine.c TsetlinMachine.c tm_random.c
HEADERS = MultiClassTsetlinMachine.h TsetlinMachine.h

CC ?= gcc
CFLAGS_COMMON = -Wall -O3 -ffast-math -march=native -flto

NoisyParityDemo: $(SOURCES) $(HEADERS)
	$(CC) $(CFLAGS_COMMON) -o NoisyParityDemo $(SOURCES)

clean:
	rm -f NoisyParityDemo
