KDIR ?= /lib/modules/$(shell uname -r)/build
CROSS_TOOLS ?= arm-eabi-
ADDR ?= 0

.PHONY: all clean disasm locate

all:
	$(MAKE) -C $(KDIR) M=$(CURDIR) modules

clean:
	$(MAKE) -C $(KDIR) M=$(CURDIR) clean

disasm: all
	$(CROSS_TOOLS)objdump -drS hello.ko > hello.disasm

locate: all
	$(CROSS_TOOLS)addr2line -e hello.ko -j .init.text -f -i $(ADDR)
