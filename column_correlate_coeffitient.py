# -*- coding: utf-8 -*-
import numpy
import scipy.stats

def corrSpearman(dim2_array): #한방에 하니 메모리가 수십기가 필요. 메모리를 적게 쓰기위해 spearman 을 for로 구현. 
	dim2_array=numpy.array(dim2_array)
	n_col=dim2_array.shape[1]
	corrsp_result=numpy.zeros((n_col,n_col))
	corrsp_pvalue=numpy.zeros((n_col,n_col))
	print '\nspearman correlation coefficient calculation initialized. \nthis may take few minutes if array is big.'
	for col in range(0,n_col):
		print 'processing rows : ', col,'/',n_col #시간이 많이 걸리니까 진행도 표시. 
		for col2 in range(0,n_col):
			corrsp_result[col,col2] , corrsp_pvalue[col,col2] = scipy.stats.spearmanr(dim2_array[:,col],dim2_array[:,col2])
	print'spearman -finished.\n'
			#print n_col,n_col2,' spearmanr : ',scipy.stats.spearmanr(f[:,n_col],f[:,n_col2])
	#print corrsp_result
	#print corrsp_pvalue
	return corrsp_result, corrsp_pvalue

def corrPearson(dim2_array): #2차원배열 아니면 오류남.
	dim2_array=numpy.array(dim2_array)
	#print(dim2_array.T)
	result = numpy.corrcoef(dim2_array.T)
	return result #리턴 하나

a=numpy.matrix([0,0,0,0,0,0,0,0,1,1])
b=numpy.matrix([1,2,3,1,2,3,1,2,3,1])
c=numpy.matrix([1,2,3,4,1,2,3,4,1,2])
d=numpy.matrix([1,2,3,4,5,1,2,3,4,5])
e=numpy.matrix([1,2,3,4,5,6,7,8,9,10])
f=numpy.array(numpy.concatenate((a,b,c,d,e),0))
print(f)
print(f.T)

pearson_result=corrPearson(f)
spearman_result , spearman_pvalue = corrSpearman(f)

print'\npearson_result'
print(pearson_result)
print'\nspearman_result'
print(spearman_result)
print'\nspearman_pvalue'
print(spearman_pvalue)



