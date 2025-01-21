KDIR= /lib/modules/$(shell uname -r)/build
#KDIR= <target-linux-src-path>
PWD := $(shell pwd)

USER_PROG= misc_mmap_test

obj-m := misc_mmap.o

all: $(USER_PROG)
	$(MAKE) -C $(KDIR) M=$(PWD)

install:
	$(MAKE) -C $(KDIR) M=$(PWD) modules_install

clean:
	rm -f $(USER_PROG)
	$(MAKE) -C $(KDIR) M=$(PWD) clean
