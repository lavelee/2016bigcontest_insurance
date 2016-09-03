# -*- coding: utf-8 -*-
import pickle
import xlwt
import numpy
import os

#피클의 모든 item을 가져옵니다. 태그 하나당 시트 하나가 만들어집니다.
#trained_w12b12_cucntt.pickle
#trained_w12b12_cuclaim.pickle

pickle_name = 'trained_w12b12_cuclaim.pickle'

#엑셀이름
excel_name=pickle_name[:pickle_name.find(".pickle")]+'.xls'

def pickleread(pickle_name):
    with open(pickle_name,'rb') as f:
        data=pickle.load(f)
        return data

def sheetmake(data):
    global pickle_name,excel_name
    book = xlwt.Workbook()
    for dictitle , dictdata in data.items():
        dictdata=numpy.matrix(dictdata) #1차원 배열 있으면 shape 차원 하나라 오류나서.
        sheet=book.add_sheet(dictitle)
        for n_row in range(0,dictdata.shape[0]):
            for n_col in range(0,dictdata.shape[1]):
                value=numpy.asscalar(dictdata[n_row,n_col])
                sheet.row(n_row).write(n_col,value)
        print 'making sheet : ',dictitle
    book.save(excel_name)
    print 'finished, file saved : ',excel_name


if os.path.isfile(excel_name): #이미 파일이 있으면 삭제함 #엑셀파일이 열려있으면 삭제도 못하고 오류남. 
	os.remove(excel_name)
	print('target excel file exists. continue after deleting')
sheetmake(pickleread(pickle_name))





