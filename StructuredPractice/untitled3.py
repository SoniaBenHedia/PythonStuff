# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 15:42:17 2020

@author: sbenhedia
"""

import csv as csv

with open ('test.csv', 'w') as file:
    writer=csv.writer(file, delimiter=",")
    writer.writerow(["m","m"])