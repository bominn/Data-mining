# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 02:14:14 2018

@author: hsu
"""
import argparse
import timeit
import numpy as np
# construct bitvector
def init_bitvector(data):
    num = 0
    for line in data:
        line = line.replace('\n','')
        line = line.split(' ')
        for i in range(len(line)):
            line[i] = int(line[i])
        temp = max(line)                   
        if temp > num:
            num = temp           
    bitvector = np.zeros(((len(data),num+1)))
    for i in range(len(data)):
        data[i] = data[i].replace('\n','')
        item = data[i].split(' ')
        for num in item:
            bitvector[i][int(num)] = 1
    return bitvector
#recursion to get frequent
def re(bitvector, min_support, matrix ,frequent, name,freq_items):
    new_matrix = []
    new_freq = frequent.copy()
    n = []
    for item in frequent:               
        find = bitvector[:,item]
        k = np.multiply(matrix ,find)     
        support= np.sum(k)     
        if support >= min_support:
            new = name.copy()
            new = new | {item}
            new_matrix.append(k)
            n.append(new)
            freq_items[frozenset(new)] = int(support)
        else :
            new_freq.remove(item)
    
    if new_freq != []:
            
        for i in range(1,len(new_freq)):
            re(bitvector, min_support, new_matrix[i-1], new_freq[i:], n[i-1], freq_items)    
    
    return freq_items
# run eclat algorithm
def eclat_2(bitvector, min_support, freq_items):
    fr = []
    for i in range(0,len(bitvector[1])):      
        support = np.sum(bitvector[:,i])       
        if support >= min_support:
            x = {i}
            freq_items[frozenset(x)] = int(support)
            fr.append(i)    
    fz = fr.copy()
    for item in fr:
        name = {item}
        fz.remove(item)
        matrix = bitvector[:,item]      
        freq_items = re(bitvector, min_support,matrix,fz,name,freq_items)
       
    return freq_items      

#----------------main----------------------------------
start = timeit.default_timer()

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="file")
parser.add_argument("minimun_support", help="minsupport")
parser.add_argument("output_file", help="file")
a = parser.parse_args()

#read file
f = open(a.input_file, "r")
db = []
for line in f:    
    db.append(line)
bitvector = init_bitvector(db)
minsup = float(a.minimun_support)
temp = {}
out = eclat_2(bitvector,len(db)*minsup,temp)

#write answer txt
with open(a.output_file,'w')as f:
    for k,v in out.items():
        k = list(map(int,k))
        k.sort()
        for i in range(len(k)):            
            f.write(str(k[i])+' ')
        f.write('('+str(v)+')'+'\n')
stop = timeit.default_timer()
print('minimun support = ', a.minimun_support)
print('total Time: ', stop - start)  



