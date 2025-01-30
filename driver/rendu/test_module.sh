#!/bin/bash

function facto  {
    fact=1
    num=$(($1))
    while [[ $num -gt 1 ]]
    do
        fact=$((fact * num))  #fact = fact * num
        num=$((num - 1))      #num = num - 1
    done
    return $fact
}

make

if [[ $? == 0 ]]
then
    insmod pcifacto.ko
    for i in $(seq 0 10)
    do
        echo -n "test:$i "
        echo -n $i > /dev/edu-fact0
        facto $i
        expected=$fact
        got=$(tr -d '\0' < /dev/edu-fact0)
        if [[ $expected == $got ]]
        then
            echo 'OK'
        else
            echo "got:$got expect:$expected"
        fi
        
    done
    rmmod pcifacto
fi
