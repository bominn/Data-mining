# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 19:58:34 2019

@author: user
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

a_data = pd.read_csv("tripAdvisor_Kyoto_info_new.csv", encoding = 'utf-8')
#Average and Std for TripAdvisor data
a_average_rating = a_data.iloc[:,1].sum()/a_data.shape[0]
s = 0
for i in range(a_data.shape[0]):
    sub = a_average_rating - a_data.iloc[i,1]
    s = s+sub*sub
math.sqrt(s)
s = s/a_data.shape[0]
print('TripAdvisor Average = '+str(a_average_rating))
print('TripAdvisor Std = '+str(s))

#distribution of the rating
rating_count = {}
rate = a_data.iloc[:,1]
for i in range(rate.shape[0]):
    if rate[i] not in rating_count:
        rating_count[rate[i]] = 1
    else:
        rating_count[rate[i]]+=1
names = list(rating_count.keys())
values = list(rating_count.values())
plt.figure(0)
plt.bar(range(len(rating_count)),values,tick_label=names)

#
q = a_data[a_data['Excellent'].notnull()]
print(q.shape)
excellent = q.iloc[:,9]
e = excellent.values
for i in range(e.shape[0]):
    e[i] = e[i].replace("%","")
    e[i] = int(e[i])

excellent_count = {}
excellent_count['90~99'] = 0
excellent_count['80~89'] = 0
excellent_count['70~79'] = 0
excellent_count['60~69'] = 0
excellent_count['50~59'] = 0
excellent_count['40~49'] = 0
excellent_count['30~39'] = 0
excellent_count['20~29'] = 0
excellent_count['<20'] = 0
for i in range(len(e)):
    if e[i]/10 >= 9:
        excellent_count['90~99']+=1
    elif e[i]/10 >=8:
        excellent_count['80~89']+=1
    elif e[i]/10 >=7:
        excellent_count['70~79']+=1
    elif e[i]/10 >=6:
        excellent_count['60~69']+=1
    elif e[i]/10 >=5:
        excellent_count['50~59']+=1
    elif e[i]/10 >=4:
        excellent_count['40~49']+=1
    elif e[i]/10 >=3:
        excellent_count['30~39']+=1
    elif e[i]/10 >=2:
        excellent_count['20~29']+=1
    else:
        excellent_count['<20']+=1
plt.figure(1)
name = list(excellent_count.keys())
value = list(excellent_count.values())
plt.bar(range(len(excellent_count)),value,tick_label=name)