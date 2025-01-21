# Echo CDEV

## Objective

Create a character device driver who echo write data when read again.
The maximum size of message to be echoed shall be parametrized.

## Definition of Done

1. Compilation OK (.ko generated)
2. Module loaded (with insmod)
3. One device created (/dev/echo0) and register in sysfs (/sys/class/training)
4. Reading from device (cat /dev/echo0) return nothing
5. Writing to device (echo test > /dev/echo0)
6. Reading from device (cat /dev/echo0) return previous writted data (test)
7. Module unloaded (with rmmod)

## Hints

Reuse the driver created in PW1.
- add a module parameter for size of message buffer (module_param, MODULE_PARM_DESC)
- allocate buffer (kzalloc) on init 
- store the data in buffer (copy_from_user) on write, check for overflow!
- return the data from buffer (copy_to_user) on read, check for overflow!
- release (kfree) buffer on exit

