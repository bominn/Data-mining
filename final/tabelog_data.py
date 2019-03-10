# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 19:45:30 2019

@author: user
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

data = pd.read_csv("tabelog_info.csv", encoding = 'utf-8')
tokyo_data = pd.read_csv("tabelog_tokyo_info.csv", encoding = 'utf-8')

#Average rating and Standard deviation 
rating = data.iloc[:,2]
average_rate = rating.sum()/rating.shape[0]
print('Average = '+str(average_rate))
s = 0
for i in range(rating.shape[0]):
    r = average_rate - rating[i]
    s = s+r*r
math.sqrt(s)
std = s/rating.shape[0]
print('Std = '+str(std))

#Clustering by food category
food = data.loc[:,'FoodCategory']
food_count = {}
for i in range(food.shape[0]):
    if food[i] not in food_count:
        food_count[food[i]] = 1
    else:
        food_count[food[i]]+=1

#if number of restaurant < 10，classify to others
new = {'others': 0}
for key,value in food_count.items():
    if value <=10:
        new['others']+=value
    else:
        new[key] = value
        
#draw pie chart (food category)      
label = [key for key,value in new.items()]
size =  [value for key,value in new.items()]
plt.pie(size , labels = label,autopct='%1.1f%%',labeldistance =1.2  ,pctdistance=0.75,radius = 1.5)     

# Average rating for different food category
y = []
x = []
for key,value in new.items():
    if key == 'others':
        continue
    else:
        category = data['FoodCategory'] == key
        y.append(key)
        see = data[category]
        see_rating = see.iloc[:,2].sum()/see.shape[0]
        x.append(see_rating)
        #print(key+' average rating is '+str(see_rating))
        
#draw barh chart (different food category rating)
plt.figure(figsize=(10,5))
plt.barh(y,x,height = 0.5,linewidth = 0.4, color = 'c')
plt.axvline(3.66, color="red")
plt.text(3.66,-1 ,'average')
plt.show()

#Clustering by location
location = data.loc[:,'NearstStation']
location_count = {}
for i in range(location.shape[0]):
    if location[i] not in location_count:
        location_count[location[i]] = 1
    else:
        location_count[location[i]]+=1
 #if number of restaurant < 15，classify to others       
L_location = {'others': 0}
for key,value in location_count.items():
    if value <=15:
        L_location['others']+=value
    else:
        L_location[key] = value
#draw pie chart(location)
label = [key for key,value in L_location.items()]
size =  [value for key,value in L_location.items()]
plt.pie(size , labels = label,autopct='%1.1f%%',labeldistance =1.2  ,pctdistance=0.8,radius = 1.5)

# Average rating for different location
y = []
x = []
for key,value in L_location.items():
    if key == 'others':
        continue
    else:
        category = data['NearstStation'] == key
        y.append(key)
        see = data[category]
        see_rating = see.iloc[:,2].sum()/see.shape[0]
        x.append(see_rating)
        #print(key+' average rating is '+str(see_rating))

#draw barh chart(different location rating)       
plt.figure(figsize=(10,5))
plt.barh(y,x,height = 0.5,linewidth = 0.4, color = 'y')
plt.axvline(3.66, color="red")
plt.text(3.66,-1 ,'average')
plt.show()
 
#Compare to Tokyo restaurant
to_rating = tokyo_data.iloc[:,2]
to_rate = to_rating.sum()/to_rating.shape[0]
print('Tokyo average rating is '+str(to_rate))
s = 0
for i in range(to_rating.shape[0]):
    r = to_rate - to_rating[i]
    s = s+r*r
math.sqrt(s)
s = s/to_rating.shape[0]
print('Tokyo Std is '+str(s))