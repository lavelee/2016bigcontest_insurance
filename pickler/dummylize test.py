# -*- coding: utf-8 -*-
import MySQLdb
import datetime
import pickle
import numpy
import os
import pandas

column_names = numpy.array('a,b,c,d,e'.split(","))

def autoCategoricalIndex(array,n_category_limit=100): #numpy array 받음
    #유니크 자료수가 100개 미만이면 categorical 로 분류해 [true, false, false,.... ] 로 만들어 내보낸다.
    return unqCount(array)<n_category_limit

def unqCount(array):
    unq_count=[]
    for i in range(0,array.shape[1]):
        unq_count.append(len(numpy.unique(array[:,i])))
    #print(unq_count)
    return unq_count

def showCategoricalLimit(array,total_variable_limit=0.01): #기본값으로 데이터 개수의 1% 까지 변수확장 허용
    #데이터 라인수에 따라 학습가능한 변수 수가 달라진다. 데이터가 많으면 변수 수를 늘려도 된다. 카테고리 자동분류에 도움. 
    unq_array=numpy.array(unqCount(array))
    numpy.sort(unq_array)
    n_total_variables=0
    for i in range(0,unq_array.shape[0]):
        n_total_variables += unq_array[i]-1 #해당 변수를 dummylize 해서 추가된 변수개수를 포함하면 총 변수개수는 몇개가 되는가.
        if n_total_variables > total_variable_limit*array.shape[0]: #총 데이터 라인수*지정비율 보다 변수 수가 많아질때
            print 'unique items vector : ',unq_array
            print 'variable limit ratio : ',total_variable_limit*100,'%'
            print 'you can dummylize ',i,'columns counted from smallest'
            print 'dummylize 할 수 있는 컬럼중 가장 항목수가 많은 컬럼의 항목수 : ',unq_array[i-1]
            print 'Variable# sum expected after dummylize : ', n_total_variables-unq_array[i]
            return unq_array[i-1]+1 #가능한 가장 큰 값에 +1 함. 


def dummylize(array,cat_index):
    global column_names
    print '\nbefore dummylize, ',array.shape[1],' columns. ' 
    print 'got index 5 columns',cat_index.shape[0]
    i=0 # numpy 배열은 enumerate 사용불가라서 어쩔수없이.. 
    for cat_yn in cat_index:
        if cat_yn :
            #print(pandas.get_dummies(array[:,i]))
            dummy_array=pandas.get_dummies(array[:,i]) # dummy array 를 만들어서
            array=numpy.concatenate((array,numpy.array(dummy_array,dtype='float32')-0.5),1) #기존 배열에 추가
            #-0.5는 전체데이터를 -0.5~+0.5 했는데 dummy는 0,1 나와서 빼준거. 나중에 normalize 하면 500메가 넘게 나옴. normalize 안하거나 빼서만들면 75메가.
            for item in dummy_array.columns: #pandas 가 만든 더미배열의 컬럼 각각에 대해
                column_names=numpy.append(column_names,column_names[i]+'_'+str(item)) #컬럼네임 배열에 _ 붙여 추가하기
        i+=1
    i=0
    for cat_yn in reversed(cat_index):
        position = len(cat_index)-i-1
        if cat_yn :
            #print position
            array=numpy.delete(array,position,1) #뒤에서부터 더미로 바꾼 원본 컬럼 삭제. 앞에서부터 하면 i 가 달라져서 안됨 
            column_names=numpy.delete(column_names,position,0) #컬럼네임도 똑같이 삭제
        i+=1
    print 'after dummylyze, ',array.shape[1],' columns.'
    return column_names, array


a=numpy.matrix([0,0,0,0,0,0,0,0,1,1])
b=numpy.matrix([1,2,3,1,2,3,1,2,3,1])
c=numpy.matrix([1,2,3,4,1,2,3,4,1,2])
d=numpy.matrix([1,2,3,4,5,1,2,3,4,5])
e=numpy.matrix([1,2,3,4,5,6,7,8,9,10])
f=numpy.array(numpy.concatenate((a.T,b.T,c.T,d.T,e.T),1))
print(f)
a,b=dummylize(f,autoCategoricalIndex(f,showCategoricalLimit(f,0.5)))
print a
print b

