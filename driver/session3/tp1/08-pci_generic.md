# Generic PCI driver for QEMU pci-testdev

## Objective

Create a driver that probe/remove the qemu PCI test device.

## Definition of Done

1. Compilation OK (.ko generated)
2. Module loaded (with insmod)
3. pci device probed: print info of current device
4. Module unloaded (with rmmod)
5. pci device removed: print info of current device

## Hints

- see current implementation:
  - pci_device_id table
  - probe/remove
  - init/exit
- update vid:pid retrieved from lspci

