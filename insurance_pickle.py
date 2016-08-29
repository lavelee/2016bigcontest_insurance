# -*- coding: utf-8 -*-
#코드내에 한글로 된 경로가 있을때 위 인코딩줄 빼면 세이브가 안되어 실행되지 않는다. 

import MySQLdb
import datetime
import pickle
import numpy
import os

#서버접속 설정과 한글사용위한 인코딩 설정
mydb=MySQLdb.connect(host='localhost',user='root', passwd='tjdgus123', db='insurance_nullfix')
cur=mydb.cursor()
mydb.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')

#query . 끝에 Y/N 은 제외했다 나중에 붙임.
sql_cucntt="SELECT CUST_ROLE, IRKD_CODE_DTAL, IRKD_CODE_ITEM, GOOD_CLSF_CDNM, CNTT_YM, CLLT_FP_PRNO, REAL_PAYM_TERM, SALE_CHNL_CODE, CNTT_STAT_CODE, EXPR_YM, EXTN_YM, LAPS_YM, PAYM_CYCL_CODE, MAIN_INSR_AMT, SUM_ORIG_PREM, RECP_PUBL, CNTT_RECP, MNTH_INCM_AMT, DISTANCE, SEX, AGE, RESI_COST, RESI_TYPE_CODE, FP_CAREER, CUST_RGST, CTPR, OCCP_GRP1, OCCP_GRP2, TOTALPREM, MINCRDT, MAXCRDT, WEDD_YN, MATE_OCCP_GRP1, MATE_OCCP_GRP2, CHLD_CNT, LTBN_CHLD_AGE, MAX_PAYM_YM, MAX_PRM, CUST_INCM, RCBASE_HSHD_INCM, JPBASE_HSHD_INCM FROM cntt LEFT JOIN cust ON cntt.CUST_ID=cust.CUST_ID WHERE cust.SIU_CUST_YN="
sql_cuclaim="SELECT ACCI_OCCP_GRP1, ACCI_OCCP_GRP2, CHANG_FP_YN, RECP_DATE, ORIG_RESN_DATE, RESN_DATE, CRNT_PROG_DVSN, ACCI_DVSN, CAUS_CODE, CAUS_CODE_DTAL, DMND_RESN_CODE, DMND_RSCD_SQNO, HOSP_OTPA_STDT, HOSP_OTPA_ENDT, RESL_CD1, VLID_HOSP_OTDA, HOUSE_HOSP_DIST, HOSP_CODE, ACCI_HOSP_ADDR, HOSP_SPEC_DVSN, CHME_LICE_NO, PAYM_DATE, DMND_AMT, PAYM_AMT, PMMI_DLNG_YN, SELF_CHAM, NON_PAY, TAMT_SFCA, PATT_CHRG_TOTA, DSCT_AMT, COUNT_TRMT_ITEM, DCAF_CMPS_XCPA, NON_PAY_RATIO, HEED_HOSP_YN, SEX, AGE, RESI_COST, RESI_TYPE_CODE, FP_CAREER, CUST_RGST, CTPR, OCCP_GRP1, OCCP_GRP2, TOTALPREM, MINCRDT, MAXCRDT, WEDD_YN, MATE_OCCP_GRP1, MATE_OCCP_GRP2, CHLD_CNT, LTBN_CHLD_AGE, MAX_PAYM_YM, MAX_PRM, CUST_INCM, RCBASE_HSHD_INCM, JPBASE_HSHD_INCM from claim left join cust on claim.CUST_ID=cust.CUST_ID where cust.SIU_CUST_YN="




def getdata(target,yn):
    yn=str(yn) #숫자로 넘어온거 문자로 바꿔서 더할수있게
    if target=="cucntt":
        sql=sql_cucntt+yn
    elif target=="cuclaim":
        sql=sql_cuclaim+yn
    #sql=sql+' limit 2' #테스트용 10개만 뽑아볼때쓰는 코드
    #print sql #쿼리 만들어진거 확인
    cur.execute(sql)
    return [list(a) for a in cur.fetchall()] #왜 tuple 로 받아오지? list로 못받아오나? list() 쓰면되는군

def timestampToDays(timestamp, bottom=datetime.date(1995,1,1)):
    return (timestamp-bottom).total_seconds()/3600/24

def allFloat(array):
    i=0
    data_type=[]
    for lines in array:
        j=0
        for data in lines:
            if i==0: #첫행으로 data type 구분하고 이거사용해서 if분기해 float로 전체변경. 
                data_type.append(type(data))
            if str(data_type[j])=="<type 'datetime.date'>":
                data=timestampToDays(data) #datetime 타입일 경우 float 로 바로 변환안되니 다른함수로 숫자로 바꿔오자
                #print 'date conversion applied' #data와 array[i][j] 로 이중접근 중이므로 최대한 data로 처리
            #print '\n\nbefore',array,type(array[i][j]) #float 바꾸기 전
            array[i][j]=float(data)
            #print '\nafter',array,type(array[i][j]) #float 바꾼 후
            j=j+1
        i=i+1
        #print '\n printing data_type \n',data_type #첫줄에서 만든 데이터 타입
    return array

def normalize(array): #-0.5~+0.5
    return (array - array.min(0))/array.ptp(0)-0.5

def randomize(labels,dataset):
    permutation = numpy.random.permutation(labels.shape[0])
    shuffled_dataset=dataset[permutation,:]
    shuffled_labels = labels[permutation]
    return shuffled_labels, shuffled_dataset

def dataDivide(labels,dataset,test_ratio=0.2):
    divide_position=int(labels.shape[0]*test_ratio)
    #print 'divide_position : ',divide_position
    test_labels = labels[:divide_position]
    test_dataset= dataset[:divide_position]
    train_labels = labels[divide_position:]
    train_dataset = dataset[divide_position:]
    return test_labels, test_dataset, train_labels, train_dataset

def pickletest(pickle_name):
    with open(pickle_name,'rb') as g:
        data=pickle.load(g)
        print data['test_cuclaim_label'][10], data['test_cuclaim_data'][10]

try:
    #자료 가져와서, 변수타입 float로 바꾸고, numpy 배열로 업그레이드하고 -0.5~+0.5 normalize 까지 한방에! getdata만 바꿔주면됨.
    cucntt_y=normalize(numpy.array(allFloat(getdata("cucntt",1))))
    #print'cucntt_y volume : ',cucntt_y.shape
    cucntt_n=normalize(numpy.array(allFloat(getdata("cucntt",0))))
    #print'cucntt_n volume : ',cucntt_n.shape
    cuclaim_y=normalize(numpy.array(allFloat(getdata("cuclaim",1))))
    #print'cuclaim_y volume : ',cuclaim_y.shape
    cuclaim_n=normalize(numpy.array(allFloat(getdata("cuclaim",0))))
    #print'cuclaim_n volume : ',cuclaim_n.shape

    #라벨링한뒤에 class들 합치기
    cucntt_label=numpy.concatenate((numpy.zeros(cucntt_y.shape[0])+1,numpy.zeros(cucntt_n.shape[0])),axis=0)
    cucntt_data=numpy.concatenate((cucntt_y,cucntt_n),axis=0)
    #print'cucntt label, data : ',cucntt_label.shape, cucntt_data.shape
    cuclaim_label=numpy.concatenate((numpy.zeros(cuclaim_y.shape[0])+1,numpy.zeros(cuclaim_n.shape[0])),axis=0)
    cuclaim_data=numpy.concatenate((cuclaim_y,cuclaim_n),axis=0)
    #print'cuclaim label, data : ',cuclaim_label.shape, cuclaim_data.shape

    #위치 섞기
    cucntt_label, cucntt_data=randomize(cucntt_label,cucntt_data)
    cuclaim_label,cuclaim_data=randomize(cuclaim_label,cuclaim_data,)
    #print(cuclaim_label)

    #test / train set 분리
    test_cucntt_label, test_cucntt_data, train_cucntt_label, train_cucntt_data = dataDivide(cucntt_label,cucntt_data)
    #print'test_cucntt_label , train_cucntt_label shape : ',test_cucntt_label.shape,train_cucntt_label.shape
    test_cuclaim_label, test_cuclaim_data, train_cuclaim_label, train_cuclaim_data = dataDivide(cuclaim_label,cuclaim_data)
    #print'test_cuclaim_label , train_cuclaim_label shape : ',test_cuclaim_label.shape,train_cuclaim_label.shape


    #picklelize
    pickle_name='cucntt_cuclaim_null_randomfix.pickle'
    f = open(pickle_name,'wb')
    save={
        'test_cucntt_label' : test_cucntt_label,
        'test_cucntt_data' : test_cucntt_data,
        'train_cucntt_label' : train_cucntt_label,
        'train_cucntt_data' : train_cucntt_data,
        'test_cuclaim_label' : test_cuclaim_label,
        'test_cuclaim_data' : test_cuclaim_data,
        'train_cuclaim_label' : train_cuclaim_label,
        'train_cuclaim_data' : train_cuclaim_data
        }
    pickle.dump(save,f,pickle.HIGHEST_PROTOCOL)
    f.close()
    print 'picklize finished.   Size : ',os.stat(pickle_name).st_size/1024/1024,'MByte'

    #pickletest(pickle_name)

finally:
    print("closing")
    cur.close()
    mydb.close()
