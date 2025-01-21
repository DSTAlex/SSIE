KERNEL_SRC := /lib/modules/$(shell uname -r)/build
PWD  := $(shell pwd)

obj-m := misc_irq.o

all:
	make -C $(KERNEL_SRC) M=$(PWD) modules

install:
	make -C $(KERNEL_SRC) M=$(PWD) modules_install

clean:
	make -C $(KERNEL_SRC) M=$(PWD) clean
