# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 02:14:14 2018

@author: hsu
"""
import argparse
import timeit
import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
mod = SourceModule(
"""
__global__ void multiply_them(int *dest, int *a, int *b, int *size)
{
  
  const int tid = threadIdx.x;
  const int bid = blockIdx.x;
  int i;
  
  for(i=bid*blockDim.x + tid; i<*size; i+=gridDim.x * blockDim.x){
    dest[i] = a[i] * b[i];
    
    __syncthreads();
  }
 
}
"""
)
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
    #bitvector = np.ascontiguousarray(bitvector)
    return bitvector
#recursion to get frequent
def re(bitvector, min_support, ma,frequent, name,freq_items):
    new_matrix = []
    new_freq = frequent.copy()
    n = []
    for item in frequent:               
        find = bitvector[:,item].astype(np.int32)   
        
        k = np.zeros_like(find)
        size = len(find)
        size = np.int32(size)                      
        multiply = mod.get_function("multiply_them")
        multiply(
                cuda.Out(k), cuda.In(ma), cuda.In(find), cuda.In(size), 
                block = (256,1,1),grid = (1,1))
        #k = np.multiply(ma,find) 
        
        support= np.sum(k)     
        if support >= min_support:
            #print(support)
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
        #print(item)
        name = {item}
        fz.remove(item)
        matrix = bitvector[:,item].astype(np.int32)      
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
#print(db)
bitvector = init_bitvector(db)
minsup = float(a.minimun_support)
temp = {}
#print(bitvector)

out = eclat_2(bitvector,len(db)*minsup,temp)
#print(len(out))
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


