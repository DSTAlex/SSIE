#!/usr/bin/python3
import sys

week = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

actual_index = -1
actual_sum = 0
actual_number = 0

for line in sys.stdin:
    index_week, sum, number = line.split('\t')
    if actual_index != index_week:
        if actual_index != -1:
            print('{0}\t{1}'.format(week[int(actual_index)], float(actual_sum)/float(actual_number)))
        actual_sum = 0
        actual_index = index_week
        actual_number = 0
    actual_number += int(number)
    actual_sum += float(sum)

print('{0}\t{1}'.format(week[int(actual_index)], float(actual_sum)/float(actual_number)))