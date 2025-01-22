make
if [[ $? == 0 ]]
then
    insmod pcifacto.ko
    dmesg | tail
fi