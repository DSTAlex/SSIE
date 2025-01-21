# mmap example

## Objective

Create a character device driver who allow a process to access it's internal buffer.

## Definition of Done

1. Compilation OK (.ko generated)
2. Module loaded (with insmod)
3. 1 misc device created (/dev/mydriver_misc_mmap) and register in sysfs (/sys/class/misc)
4. mmap from a user process to /dev/mydriver_misc_mmap
5. Reading from buffer return the kernel buffer content (lorem ipsum...)
6. Module unloaded (with rmmod)

## Hints

- See page reservation in misc_mmaptest_init
- See the misc_mmaptest_mmap syscall implementation

