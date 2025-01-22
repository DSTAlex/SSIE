KDIR= /lib/modules/$(shell uname -r)/build
PWD := $(shell pwd)

obj-m += preparedev.o
obj-m += preparedrv.o

all:
	make -C $(KDIR) M=$(PWD) modules

install:
	$(MAKE) -C $(KDIR) M=$(PWD) modules_install

clean: 
	make -C $(KDIR) M=$(PWD) clean
