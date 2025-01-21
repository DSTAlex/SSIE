# Echo CDEV with ioctl

## Objective

Create a character device driver who echo write data when read again.
The maximum size of message to be echoed shall be parametrized.
The echo buffer shall be resettable by an ioctl.
The echo mode can be changed (force upper, lower, or don't change case).

## Definition of Done

1. Compilation OK (.ko generated)
2. Module loaded (with insmod)
3. One device created (/dev/echo0) and register in sysfs (/sys/class/training)
4. Reading from device (cat /dev/echo0) return nothing
5. Writing to device (echo test > /dev/echo0)
6. Reading from device (cat /dev/echo0) return previous writted data (test)
7. Send ioctl reset command
8. Reading from deivce (cat /dev/echo0) return nothing
9. Module unloaded (with rmmod)

## Hints

Reuse the driver created in PW2.
- see the header file with IOCTL definition
- add the unlocked_ioctl function and register it in file_operations
- on ioctl function, switch on cmd
  - if reset, memset the buffer to 0
  - if set_mode, update current mode from arg
  - if get_mode, store current mode to arg (put_user)
- the mode output is already implemented on read function
- the cdev_echo_ctl program send the defined ioctl
