# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 15:53:08 2018

@author: hsu
"""
import argparse
import timeit

# construct c1 and database in [{},{},{}....] form
def construct_c1(data, min_support):
    database = []
    c1 = []
    freq_dic = {}
    for trans in data:
        trans = trans.replace('\n', "")
        trans = trans.split(" ")
        x = set() 
        for item in trans:
            x = x | {int(item)}      
            freq_dic[item] = freq_dic.get(item, 0) + 1
        database.append(x)    
    c1 = [[int(k)] for (k, v) in freq_dic.items() if v >= min_support]
    c1.sort()       #let set(c1) in ascending order
    for i in range(len(c1)):
        c1[i] = {c1[i][0]}
    return c1, database
 
# l_itemset join itself to get c+1_itemset
def joinset(itemset,n):
    ck = []
    for i in range(len(itemset)):        
        for j in range(i+1,len(itemset)):                      
            item1 = list(itemset[i])[:n-2]
            item2 = list(itemset[j])[:n-2]
            item1.sort()
            item2.sort()
            if item1 == item2:
                ck.append(itemset[i] | itemset[j])    
    return ck

#calculates the support for items in the C itemSet, scan data here, add new itemset to dictionary
def itemwithminsup(db, c_itemset, minsup, support_dict):
    L_itemset = []
    for i in range(len(c_itemset)):
        count = 0
        for j in range(len(db)):
            if c_itemset[i] <= db[j]:
                count+=1
            if count >= minsup:                
                key = tuple(c_itemset[i])
                support_dict[key] = count
        if count >= minsup:
            L_itemset.append(c_itemset[i])    
    return L_itemset
    
                            
#---------main-------------------------------------
start = timeit.default_timer()
parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="file")
parser.add_argument("minimun_support", help="minsupport")
parser.add_argument("output_file", help="file")
a = parser.parse_args()

# read file
f = open(a.input_file, "r")
db = []
for line in f:        
    db.append(line)
minsup = float(a.minimun_support)


freq_item = {}       #itemset dictionary, key : itemset, store in tuple, value : support (int)
sup = int(len(db)*minsup)
# generate c1 and l1
c1,database = construct_c1(db, sup) #database store data in a list of set form, ex : [{1},{2},{3},{1,2}......]
L1_itemset = itemwithminsup(database, c1, sup, freq_item)

L_itemset = L1_itemset
length = 2

while(L_itemset!=[]):

    C_itemset = joinset(L_itemset,length)                       
    L_itemset = itemwithminsup(database, C_itemset, sup, freq_item)      
    length += 1
#apriori finish
#write answer txt
with open(a.output_file,'w')as ff:
    for key, value in freq_item.items():
        item = []
        for i in range(len(key)):
            item.append(key[i])
        item.sort()
        for j in range(len(item)):
            ff.write(str(item[j])+' ')
        ff.write('('+str(value)+')'+'\n')
stop = timeit.default_timer()
print('minimun support = ', a.minimun_support)
print('Total Time: ', stop - start, 'sec' )  