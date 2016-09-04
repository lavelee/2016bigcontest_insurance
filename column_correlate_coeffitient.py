# -*- coding: utf-8 -*-
import numpy
def corrMatrix(dim2_array): #2차원배열 아니면 오류남.
	dim2_array=numpy.array(dim2_array)
	print(dim2_array.T)
	return numpy.corrcoef(dim2_array.T)

a=numpy.matrix([0,0,0,0,0,0,0,0,1,1])
b=numpy.matrix([1,2,3,1,2,3,1,2,3,1])
c=numpy.matrix([1,2,3,4,1,2,3,4,1,2])
d=numpy.matrix([1,2,3,4,5,1,2,3,4,5])
e=numpy.matrix([1,2,3,4,5,6,7,8,9,10])
f=numpy.array(numpy.concatenate((a.T,b.T,c.T,d.T,e.T),1))
print(f)

print(corrMatrix(f))