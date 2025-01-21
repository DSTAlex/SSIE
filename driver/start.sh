#!/bin/bash


# login tainee
IMG=$(dirname $0)/kernel_training.qcow2
QEMU=qemu-system-x86_64

$QEMU -m 4096 -smp 2 \
    -nic user,model=virtio-net-pci,hostfwd=tcp::2222-:22 \
    -device pci-testdev \
    -hda $IMG $@