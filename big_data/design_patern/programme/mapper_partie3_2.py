#!/usr/bin/python3
from datetime import datetime
import sys

week = [(0,0)] * 7

for line in sys.stdin:
    data = line.strip().split("\t")
    
    if len(data) == 6:
        date, hour, city, type_shop, money, type_pay = data
    
        day = datetime.strptime(date,"%Y-%m-%d").weekday()
        
        sum, number = week[day]
        week[day]= (sum + float(money), number+1)

for i in range(7):
    print("{0}\t{1}\t{2}".format(i, week[i][0], week[i][1]))
                                

