# Dummy sample of platform device/driver

## Objective

Create a platform_device and the associated platform_driver.
The resources used in the device are hard-coded (old way).

## Definition of Done

1. Compilation OK (.ko generated)
2. Device module loaded (with insmod)
3. Welcome message in dmesg
[96268.352914] Welcome to sample Platform device !
4. Driver module loaded (with insmod)
5. Welcome message in dmesg
[96295.643336] Welcome to sample platform driver !
[96295.643455] ** sample_drv_probe **
[96295.643457] Memory Area 1
[96295.643461] Start= 100000,  End= 1fffff Size= 1048576
[96295.643462] Memory Area 2
[96295.643465] Start= 300000,  End= 3fffff Size= 1048576
[96295.643467] IRQ Number of device= 6
6- Load / unload the device or driver parts and see what happens 




