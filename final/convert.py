# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 20:06:57 2019

@author: user
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from difflib import SequenceMatcher

# return how similar of two string 
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

t_data = pd.read_csv("tabelog_info.csv", encoding = 'utf-8')
a_data = pd.read_csv("tripAdvisor_Kyoto_info_new.csv", encoding = 'utf-8')

t_name = t_data.iloc[:,1]
a_name = a_data.iloc[:,0]

#finding restaurant that both in Tabelog and TripAdvisor
pair = []
count = 0
ratio = 0
find = ''
for j in range(t_name.shape[0]):
    ratio = 0
    find = ''
    for i in range(a_name.shape[0]):
        r = similar(t_name[j],a_name[i])
        if r>ratio:
            ratio = r
            find = i
    if ratio > 0.9:
        #print(t_name[j])
        #print(find)
        k = [j,find]
        pair.append(k)
        count +=1
print('There are '+str(count)+' restaurant both in tabelog and tripadvisor')

#find restaurant that is overated or underated
overated = 0
underated = 0
out = []
over = []
under = []
for i in range(len(pair)):
    t_score = t_data.iloc[pair[i][0],2]
    a_score = a_data.iloc[pair[i][1],1]
    if a_score-t_score < 0.35:
        overated +=1
        out.append(i)
        over.append(i)
    elif a_score-t_score > 1:
        underated+=1
        out.append(i)
        under.append(i)
print('Overated count is '+str(overated))
print('Underated count is '+str(underated))
print('Total count is '+str(overated+underated))

#Anaylyze relationship between food category and overated&underated restaurant 
out_category = {}
for i in range(len(out)):
    num = out[i]
    category = t_data.iloc[pair[num][0],4]
    if category not in out_category:
        out_category[category] = 1
    else:
        out_category[category]+=1
plt.figure(0)
names = list(out_category.keys())
values = list(out_category.values())
plt.barh(range(len(out_category)),values,tick_label=names,linewidth = 0.4, color = 'c')
plt.show()

#Anaylyze relationship between location and overated&underated restaurant
out_location = {}
for i in range(len(out)):
    num = out[i]
    location = t_data.iloc[pair[num][0],3]
    if location not in out_location:
        out_location[location] = 1
    else:
        out_location[location]+=1
plt.figure(1)
names = list(out_location.keys())
values = list(out_location.values())
plt.barh(range(len(out_location)),values,tick_label=names,linewidth = 0.4, color = 'y')
plt.show()

#Anaylyze relationship between food category and overated restaurant 
out_category = {}
for i in range(len(over)):
    num = over[i]
    category = t_data.iloc[pair[num][0],4]
    if category not in out_category:
        out_category[category] = 1
    else:
        out_category[category]+=1
plt.figure(2)
names = list(out_category.keys())
values = list(out_category.values())
plt.barh(range(len(out_category)),values,tick_label=names,linewidth = 0.4, color = 'c')
plt.show()

#Anaylyze relationship between location and overated restaurant
out_location = {}
for i in range(len(over)):
    num = over[i]
    location = t_data.iloc[pair[num][0],3]
    if location not in out_location:
        out_location[location] = 1
    else:
        out_location[location]+=1
plt.figure(3)
names = list(out_location.keys())
values = list(out_location.values())
plt.barh(range(len(out_location)),values,tick_label=names,linewidth = 0.4, color = 'y')
plt.show()

#Anaylyze relationship between food category and underated restaurant 
out_category = {}
for i in range(len(under)):
    num = under[i]
    category = t_data.iloc[pair[num][0],4]
    if category not in out_category:
        out_category[category] = 1
    else:
        out_category[category]+=1
plt.figure(4)
names = list(out_category.keys())
values = list(out_category.values())
plt.barh(range(len(out_category)),values,tick_label=names,linewidth = 0.4, color = 'c')
plt.show()

#Anaylyze relationship between location and underated restaurant
out_location = {}
for i in range(len(under)):
    num = under[i]
    location = t_data.iloc[pair[num][0],3]
    if location not in out_location:
        out_location[location] = 1
    else:
        out_location[location]+=1
plt.figure(5)
names = list(out_location.keys())
values = list(out_location.values())
plt.barh(range(len(out_location)),values,tick_label=names,linewidth = 0.4, color = 'y')
plt.show()