#!/usr/bin/python3
from datetime import datetime
import sys


week = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

for line in sys.stdin:
    data = line.strip().split("\t")
    
    if len(data) == 6:
        date, hour, city, type_shop, money, type_pay = data
    
        day = datetime.strptime(date,"%Y-%m-%d").weekday()
        
        
        print("{0}\t{1}".format(week[date], money))
                                
