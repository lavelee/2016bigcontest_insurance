# -*- coding: utf-8 -*-
#코드내에 한글로 된 경로가 있을때 위 인코딩줄 빼면 세이브가 안되어 실행되지 않는다. 

import MySQLdb
import datetime
import pickle
import numpy
import os
import pandas

#서버접속 설정과 한글사용위한 인코딩 설정
mydb=MySQLdb.connect(host='localhost',user='root', passwd='tjdgus123', db='insurance_nullfix')
cur=mydb.cursor()
mydb.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')

ifdummy=0

#query . 끝에 Y/N 은 제외했다 나중에 붙임.
sql_cucntt="""Select
  cntt.CUST_ROLE,
  cntt.IRKD_CODE_DTAL,
  cntt.IRKD_CODE_ITEM,
  cntt.GOOD_CLSF_CDNM,
  cntt.CNTT_YM,
  cntt.CLLT_FP_PRNO,
  cntt.REAL_PAYM_TERM,
  cntt.SALE_CHNL_CODE,
  cntt.CNTT_STAT_CODE,
  cntt.EXPR_YM,
  cntt.EXTN_YM,
  cntt.LAPS_YM,
  cntt.PAYM_CYCL_CODE,
  cntt.MAIN_INSR_AMT,
  cntt.SUM_ORIG_PREM,
  cntt.RECP_PUBL,
  cntt.CNTT_RECP,
  cntt.MNTH_INCM_AMT,
  cntt.DISTANCE,
  cust.SEX,
  cust.AGE,
  cust.RESI_COST,
  cust.RESI_TYPE_CODE,
  cust.FP_CAREER,
  cust.CUST_RGST,
  cust.CTPR,
  cust.OCCP_GRP1,
  cust.OCCP_GRP2,
  cust.TOTALPREM,
  cust.MINCRDT,
  cust.MAXCRDT,
  cust.WEDD_YN,
  cust.MATE_OCCP_GRP1,
  cust.MATE_OCCP_GRP2,
  cust.CHLD_CNT,
  cust.LTBN_CHLD_AGE,
  cust.MAX_PAYM_YM,
  cust.MAX_PRM,
  cust.CUST_INCM,
  cust.RCBASE_HSHD_INCM,
  cust.JPBASE_HSHD_INCM
From
  cntt Left Join
  cust
    On cntt.CUST_ID = cust.CUST_ID
Where
  cust.SIU_CUST_YN ="""


sql_cuclaim="""Select
  claim.ACCI_OCCP_GRP1,
  claim.ACCI_OCCP_GRP2,
  claim.CHANG_FP_YN,
  claim.RECP_DATE,
  claim.ORIG_RESN_DATE,
  claim.RESN_DATE,
  claim.CRNT_PROG_DVSN,
  claim.ACCI_DVSN,
  claim.CAUS_CODE,
  claim.CAUS_CODE_DTAL,
  claim.DMND_RESN_CODE,
  claim.DMND_RSCD_SQNO,
  claim.HOSP_OTPA_STDT,
  claim.HOSP_OTPA_ENDT,
  claim.RESL_CD1,
  claim.VLID_HOSP_OTDA,
  claim.HOUSE_HOSP_DIST,
  claim.HOSP_CODE,
  claim.ACCI_HOSP_ADDR,
  claim.HOSP_SPEC_DVSN,
  claim.CHME_LICE_NO,
  claim.PAYM_DATE,
  claim.DMND_AMT,
  claim.PAYM_AMT,
  claim.PMMI_DLNG_YN,
  claim.SELF_CHAM,
  claim.NON_PAY,
  claim.TAMT_SFCA,
  claim.PATT_CHRG_TOTA,
  claim.DSCT_AMT,
  claim.COUNT_TRMT_ITEM,
  claim.DCAF_CMPS_XCPA,
  claim.NON_PAY_RATIO,
  claim.HEED_HOSP_YN,
  cust.SEX,
  cust.AGE,
  cust.RESI_COST,
  cust.RESI_TYPE_CODE,
  cust.FP_CAREER,
  cust.CUST_RGST,
  cust.CTPR,
  cust.OCCP_GRP1,
  cust.OCCP_GRP2,
  cust.TOTALPREM,
  cust.MINCRDT,
  cust.MAXCRDT,
  cust.WEDD_YN,
  cust.MATE_OCCP_GRP1,
  cust.MATE_OCCP_GRP2,
  cust.CHLD_CNT,
  cust.LTBN_CHLD_AGE,
  cust.MAX_PAYM_YM,
  cust.MAX_PRM,
  cust.CUST_INCM,
  cust.RCBASE_HSHD_INCM,
  cust.JPBASE_HSHD_INCM
From
  claim Left Join
  cust
    On claim.CUST_ID = cust.CUST_ID
Where
  cust.SIU_CUST_YN = """

def columnNames(sql,initial="select",end="from"): #컬럼네임 리스팅 좌우 단어 받아서 컬럼네임 배열로 출력. 
    sql=sql.upper()
    initial=initial.upper()
    end=end.upper()
    column_names=sql[sql.find(initial)+len(initial)+1 : sql.find(end)] #select 이후 띄어쓰기 하나 때문에 +1
    column_names=column_names.replace(" ","").split(",")
    #print (column_names)
    #print len(column_names)
    return column_names

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
                data=timestampToDays(data) #datetime 타입일 경우 float 로 바로 변환안되니 다른함수로 숫자로 바꿔오자. txt 타입은 쿼리에서부터 이미 제거해서 가지고 들어왔음. 
                #print 'date conversion applied' #data와 array[i][j] 로 이중접근 중이므로 최대한 data로 처리
            #print '\n\nbefore',array,type(array[i][j]) #float 바꾸기 전
            array[i][j]=numpy.float32(data)
            #array[i][j]=float(data) #원래 데이터는 이거였는데, 파이썬의 folat는 float64가 기본이라서 나중에 텐서플로에서 오류남. 텐서플로는 float32만을 사용하기 때문. 
            #print '\nafter',array,type(array[i][j]) #float 바꾼 후
            j=j+1
        i=i+1
        #print '\n printing data_type \n',data_type #첫줄에서 만든 데이터 타입
    return array

def normalize(array): #-0.5~+0.5
    array=numpy.array(array,dtype='float32')
    for col_num in range(0,array.shape[1]):
        array[:,col_num]=(array[:,col_num]-array[:,col_num].min(0))/array[:,col_num].ptp(0)-0.5
    return array

def randomize(labels,dataset):
    permutation = numpy.random.permutation(labels.shape[0])
    shuffled_dataset=dataset[permutation,:]
    shuffled_labels = labels[permutation]
    return shuffled_labels, shuffled_dataset

def dataDivide(labels,dataset,test_ratio=0.2): #일정비율로 테스트와 트레인셋을 나눔
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
        print data['test_cuclaim_label'][10]
        print data['test_cuclaim_data'][10]

def autoCategoricalIndex(array,n_category_limit=100): #numpy array 받음
    #유니크 자료수가 100개 미만이면 categorical 로 분류해 [true, false, false,.... ] 로 만들어 내보낸다.
    return numpy.array(unqCount(array)<n_category_limit)

def unqCount(array):
    unq_count=[]
    for i in range(0,array.shape[1]):
        unq_count.append(len(numpy.unique(array[:,i])))
    #print(unq_count)
    return unq_count

def showCategoricalLimit(array,total_variable_limit=0.01): #기본값으로 데이터 개수의 1% 까지 변수확장 허용
    #데이터 라인수에 따라 학습가능한 변수 수가 달라진다. 데이터가 많으면 변수 수를 늘려도 된다. 카테고리 자동분류에 도움. 
    unq_array=numpy.array(unqCount(array))
    unq_sorted=numpy.sort(unq_array)

    if total_variable_limit >1: #리밋에 0~1 값은 비율로 판단해 계산하고 1 넘는값은 몇개로 지정했다고 생각함. 
        limit=total_variable_limit
        print '\nvariable limit : ',total_variable_limit
    else:
        limit=total_variable_limit*array.shape[0]
        print '\nvariable limit ratio : ',total_variable_limit*100,'%   ',total_variable_limit*array.shape[0]

    n_total_variables=array.shape[1]
    if limit < n_total_variables:
        raise NameError('받은 배열의 컬럼이 limit 개수보다 많아서 더미화를 진행할 수 없습니다')

    for i in range(0,unq_sorted.shape[0]):
        n_total_variables += unq_sorted[i]-1 #해당 변수를 dummylize 해서 추가된 변수개수를 포함하면 총 변수개수는 몇개가 되는가.
        if n_total_variables > limit: #총 데이터 라인수*지정비율 보다 변수 수가 많아질때
            #print '\n now total variables calculated : ', n_total_variables 
            print 'unique items vector : ',unq_array
            #print 'unique items sorted vector : ',unq_sorted
            print 'you can dummylize ',i,'columns counted from smallest'
            print 'dummylize 할 수 있는 컬럼중 가장 항목수가 많은 컬럼의 항목수 : ',unq_sorted[i-1]
            #print 'Variable# sum expected after dummylize : ', n_total_variables-unq_sorted[i]
            return unq_sorted[i-1]+1 #가능한 가장 큰 값에 +1 함. 


def dummylize(array,cat_index,sql,dummylize=1):
    if dummylize==0:
        cat_index=numpy.zeros(cat_index.shape[0])
    column_names=columnNames(sql) #더미화된 결과 컬럼이름 받기위해 sql 을 받아오기로 함. 
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
    #print(column_names)
    print 'after dummylyze, ',array.shape[1],' columns.'
    return column_names, array

    

try:
    #자료 가져와서, 변수타입 float로 바꾸고, numpy 배열로 업그레이드하고 -0.5~+0.5 normalize 까지 한방에! getdata만 바꿔주면됨.
    cucntt_y=numpy.array(allFloat(getdata("cucntt",1)),dtype="float32")
    #print'cucntt_y volume : ',cucntt_y.shape
    cucntt_n=numpy.array(allFloat(getdata("cucntt",0)),dtype="float32")
    #print'cucntt_n volume : ',cucntt_n.shape
    cuclaim_y=numpy.array(allFloat(getdata("cuclaim",1)),dtype="float32")
    #print'cuclaim_y volume : ',cuclaim_y.shape
    cuclaim_n=numpy.array(allFloat(getdata("cuclaim",0)),dtype="float32")
    #print'cuclaim_n volume : ',cuclaim_n.shape



    #dummy화                 
    cucntt =numpy.concatenate((cucntt_y,cucntt_n),0)#더미화 위해 잠시 테이블 합침
    cuclaim=numpy.concatenate((cuclaim_y,cuclaim_n),0) #왜 나눠서 가져왔냐면, classification index 만들기 위해서임
    #아래는 자동으로 카테고리 컬럼이 뭔지 생성. 
    afterdummy_variables_limit=100  #고유항목수 N개(N>1) , N의 비율로(0~1값) dummy 화 할지 결정. 
                                                #더미화로 추가될 컬럼수를 의미(항목 몇개이하~가 아님).   더미화 안된 컬럼+더미화 컬럼은 이 숫자보다 클수 있음.  
    cucntt_cat_tf_index=autoCategoricalIndex(cucntt,showCategoricalLimit(cucntt,afterdummy_variables_limit)) #자동변수 . 아니면 수동으로
    cuclaim_cat_tf_index=autoCategoricalIndex(cuclaim,showCategoricalLimit(cuclaim,afterdummy_variables_limit))
    cucntt_cnames, cucntt  =dummylize(cucntt , cucntt_cat_tf_index , sql_cucntt,ifdummy) #더미화 실행, 안하려면 이 줄 삭제가 아니라 옵션에 ,0 넣기
    cuclaim_cnames, cuclaim=dummylize(cuclaim, cuclaim_cat_tf_index, sql_cuclaim,ifdummy)
    cucntt=normalize(cucntt) #합친김에 normalize
    cuclaim=normalize(cuclaim)
    print 'cucntt shape : ',cucntt.shape
    print 'cuclaim shape : ',cuclaim.shape
    cucntt_y=cucntt[:cucntt_y.shape[0]] #합쳤던 테이블 분리
    cucntt_n=cucntt[cucntt_y.shape[0]:]
    cuclaim_y=cuclaim[:cuclaim_y.shape[0]]
    cuclaim_n=cuclaim[cuclaim_n.shape[0]:]
    del cucntt, cuclaim #메모리를 위해. 


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
        'train_cuclaim_data' : train_cuclaim_data,
        'cucntt_column_names' : cucntt_cnames,
        'cuclaim_column_names' : cuclaim_cnames
        }
    pickle.dump(save,f,pickle.HIGHEST_PROTOCOL)
    f.close()
    print '\npicklize finished.  filename :',pickle_name,' Size : ',os.stat(pickle_name).st_size/1024/1024,'MByte'

    pickletest(pickle_name)

finally:
    print("closing")
    cur.close()
    mydb.close()
