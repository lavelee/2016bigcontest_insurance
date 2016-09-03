import MySQLdb
import datetime
import pickle
import numpy
import os
import pandas

a=numpy.matrix([0,0,0,0,0,0,0,0,1,1])
b=numpy.matrix([1,2,3,1,2,3,1,2,3,1])
c=numpy.matrix([1,2,3,4,1,2,3,4,1,2])
d=numpy.matrix([1,2,3,4,5,1,2,3,4,5])
e=numpy.matrix([1,2,3,4,5,6,7,8,9,10])
f=numpy.array(numpy.concatenate((a.T,b.T,c.T,d.T,e.T),1))
print(f)

def normalize(array): #-0.5~+0.5
    array=numpy.array(array,dtype='float32')
    for col_num in range(0,array.shape[1]):
        array[:,col_num]=(array[:,col_num]-array[:,col_num].min(0))/array[:,col_num].ptp(0)-0.5
    return array

print(normalize(f))

