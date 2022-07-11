obj-m := P1F2.o

all:
	$(MAKE) -C /lib/modules/$(shell uname -r)/build M=$(shell pwd) modules

clean:
	$(MAKE) -C /lib/modules/$(shell uname -r)/build M=$(shell pwd) clean
install:
	insmod P1F2.ko
delete:
	rmmod P1F2.ko
