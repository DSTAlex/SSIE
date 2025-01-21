# Dummy CDEV

## Objective

Create a dummy character device driver.
The driver must create one device in /dev.
The device shall print info in kernel message for each user space access (open, close, read, write),
it doesn't need to do something else.

## Definition of Done

1. Compilation OK (.ko generated)
2. Module loaded (with insmod)
3. One device created (/dev/dummy0) and register in sysfs (/sys/class/training)
4. Reading from device (cat /dev/dummy0) create kernel messages (in dmesg) for open, read, close
5. Writing to device (echo test > /dev/dummy0) create kernel messages (in dmesg) for open, write, close
6. Module unloaded (with rmmod)

## Hints

The dummy file_operations is already implemented.
You need to populate the init/exit function with the steps defined in .c. Please take care of errors.
Add necessary global variables (to share between init and exit).
