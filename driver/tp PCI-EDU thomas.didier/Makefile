KDIR= /lib/modules/$(shell uname -r)/build
#KDIR= <target-linux-src-path>
PWD := $(shell pwd)

obj-m += edu_driver.o


all:
	$(MAKE) -C $(KDIR) M=$(PWD)

install:
	$(MAKE) -C $(KDIR) M=$(PWD) modules_install

clean: 
	$(MAKE) -C $(KDIR) M=$(PWD) clean
