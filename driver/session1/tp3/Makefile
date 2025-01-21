KERNEL_SRC := /lib/modules/$(shell uname -r)/build
PWD  := $(shell pwd)

USER_PRG = cdev_echo_ctl

obj-m := cdev_echo.o

all: $(USER_PRG)
	make -C $(KERNEL_SRC) M=$(PWD) modules

install:
	make -C $(KERNEL_SRC) M=$(PWD) modules_install

clean:
	rm $(USER_PRG)
	make -C $(KERNEL_SRC) M=$(PWD) clean
