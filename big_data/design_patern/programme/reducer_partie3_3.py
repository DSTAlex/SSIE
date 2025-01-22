#!/usr/bin/python3
import sys

actual_index = -1
actual_sum = 0

for line in sys.stdin:
    weekday, sum = line.split('\t')
    if actual_index != weekday:
        if actual_index != -1:
            print('{0}\t{1}'.format(actual_index, float(actual_sum)))
        actual_sum = 0
        actual_index = weekday
    actual_sum += float(sum)

print('{0}\t{1}'.format(actual_index, float(actual_sum)))