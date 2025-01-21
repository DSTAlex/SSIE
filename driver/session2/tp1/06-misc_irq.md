# Keyboard grabber

## Objective

Create a character device driver who write the keyboard event.
The keyboard IRQ is always number 1 (see /proc/interrupts for i8042).
Use the misc class subsytem to ease the cdev creation.

## Definition of Done

1. Compilation OK (.ko generated)
2. Module loaded (with insmod)
3. 1 misc device created (/dev/kbd_grab) and register in sysfs (/sys/class/misc)
4. Reading from device (cat /dev/kbd_grab) show nothing until a key is pressed/released
5. Close the read with Ctrl+C
6. Module unloaded (with rmmod)

## Hints

- See misc_register to create the device / misc_unregister to release it
- See the wait_queue (declaration, got_char, read) ~= std::condition_variable
- in misc_irq_init:
  - init the workqueue
  - register the top half irq_handler on IRQ1
- in top half (irq_handler) call the bottom half through the workqueu

