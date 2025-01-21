# Generic PCI driver for QEMU pci-testdev

## Objective

Create a driver that probe/remove the qemu PCI test device.
Read all available tests in BAR 0+1.

## Definition of Done

1. Compilation OK (.ko generated)
2. Module loaded (with insmod)
3. pci device probed: print info of current device and all available tests in BAR 0+1
4. Module unloaded (with rmmod)
5. pci device removed: print info of current device

## Hints

- change all ???
