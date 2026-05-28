CLANG ?= clang-16
ARCH := $(subst x86_64,amd64,$(shell uname -m))

BPF_CFLAGS := -O2 -g -target bpf -D__TARGET_ARCH_$(ARCH)

all: process_exec.o network_tracker.o

%.o: %.c
	$(CLANG) $(BPF_CFLAGS) -c $< -o $@

clean:
	rm -f *.o
