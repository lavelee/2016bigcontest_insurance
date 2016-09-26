# -*- coding: utf-8 -*-
#코드내에 한글로 된 경로가 있을때 위 인코딩줄 빼면 세이브가 안되어 실행되지 않는다. 
#test/train 에 동일한 cust_id 가 섞이는 문제를 SQL 쿼리와 함께 해결함. 하지만 블럭을 나누는 그 한칸은 중복되는 상태. 

import MySQLdb
import datetime
import pickle
import numpy
import os, sys
import pandas

#서버접속 설정과 한글사용위한 인코딩 설정
mydb=MySQLdb.connect(host='localhost',user='root', passwd='tjdgus123', db='insurance_nullfix') #쿼리에 DB명 지정되어있으면 이거 바꿔도 적용 안됨.
cur=mydb.cursor()
mydb.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')

ifnormalize=1
afterdummy_variables_limit=0 #고유항목수 N개(N>1) , N의 비율로(0~1값) dummy 화 할지 결정. 
                                        #더미화로 추가될 컬럼수를 의미(항목 몇개이하~가 아님).   더미화 안된 컬럼+더미화 컬럼은 이 숫자보다 클수 있음.  
pickle_name='clcntt_randfix01.pickle' #만들어진 피클 이름. picklize 에서 쓴다. 
test_ratio=0.2 #데이터에서 테스트셋의 비율


#혹시 외부변수가 있다면 외부변수 우선 설정. 
try :
    dbname = sys.argv[1] #sql 파일의 경로포함 이름. 경로/nullfix01.sql 에서 .sql 떼고 경로/nullfix01
    ifoutdel = int(sys.argv[2]) #0 또는 1
    afterdummy_variables_limit = int(sys.argv[3]) #0, 100, 1000
    tryno = int(sys.argv[4]) #몇번째 제작중인 picklefile 인지 #0,1,2,3,4...
    #filename : (저장경로/)rand00 outdel0 dummy000 00.pickle
    pickle_name = dbname+' outdel'+str(ifoutdel)+' dummy'+str(afterdummy_variables_limit)+' '+str(tryno)+'.pickle'
except IndexError :
    pass



#query . 끝에 Y/N 은 제외했다 나중에 붙임.    cust_part.cust_id 는 디버그용이라 실제에선 뺌. 
sql_input=""" Select
   cust_part.AGE,
   cust_part.SEX,
   cust_part.RESI_COST,
   cust_part.RESI_TYPE_CODE,
   cust_part.FP_CAREER,
   cust_part.CUST_RGST,
   cust_part.CTPR,
   cust_part.OCCP_GRP1,
   cust_part.OCCP_GRP2,
   cust_part.TOTALPREM,
   cust_part.MINCRDT,
   cust_part.MAXCRDT,
   cust_part.WEDD_YN,
   cust_part.MATE_OCCP_GRP1,
   cust_part.MATE_OCCP_GRP2,
   cust_part.CHLD_CNT,
   cust_part.LTBN_CHLD_AGE,
   cust_part.MAX_PAYM_YM,
   cust_part.MAX_PRM,
   cust_part.CUST_INCM,
   cust_part.RCBASE_HSHD_INCM,
   cust_part.JPBASE_HSHD_INCM,
   insurance_nullfix.cntt.CNTT_YM,
   insurance_nullfix.cntt.CUST_ROLE,
   insurance_nullfix.cntt.IRKD_CODE_DTAL,
   insurance_nullfix.cntt.IRKD_CODE_ITEM,
   insurance_nullfix.cntt.GOOD_CLSF_CDNM,
   insurance_nullfix.cntt.CLLT_FP_PRNO,
   insurance_nullfix.cntt.REAL_PAYM_TERM,
   insurance_nullfix.cntt.SALE_CHNL_CODE,
   insurance_nullfix.cntt.CNTT_STAT_CODE,
   insurance_nullfix.cntt.EXPR_YM,
   insurance_nullfix.cntt.EXTN_YM,
   insurance_nullfix.cntt.LAPS_YM,
   insurance_nullfix.cntt.PAYM_CYCL_CODE,
   insurance_nullfix.cntt.MAIN_INSR_AMT,
   insurance_nullfix.cntt.SUM_ORIG_PREM,
   insurance_nullfix.cntt.RECP_PUBL,
   insurance_nullfix.cntt.CNTT_RECP,
   insurance_nullfix.cntt.MNTH_INCM_AMT,
   insurance_nullfix.cntt.DISTANCE,
   insurance_nullfix.claim.HOSP_CODE,
   insurance_nullfix.claim.ACCI_OCCP_GRP1,
   insurance_nullfix.claim.ACCI_OCCP_GRP2,
   insurance_nullfix.claim.CHANG_FP_YN,
   insurance_nullfix.claim.RECP_DATE,
   insurance_nullfix.claim.ORIG_RESN_DATE,
   insurance_nullfix.claim.RESN_DATE,
   insurance_nullfix.claim.CRNT_PROG_DVSN,
   insurance_nullfix.claim.ACCI_DVSN,
   insurance_nullfix.claim.CAUS_CODE,
   insurance_nullfix.claim.CAUS_CODE_DTAL,
   insurance_nullfix.claim.DMND_RESN_CODE,
   insurance_nullfix.claim.DMND_RSCD_SQNO,
   insurance_nullfix.claim.HOSP_OTPA_STDT,
   insurance_nullfix.claim.HOSP_OTPA_ENDT,
   insurance_nullfix.claim.RESL_CD1,
   insurance_nullfix.claim.HEED_HOSP_YN,
   insurance_nullfix.claim.NON_PAY_RATIO,
   insurance_nullfix.claim.DCAF_CMPS_XCPA,
   insurance_nullfix.claim.COUNT_TRMT_ITEM,
   insurance_nullfix.claim.DSCT_AMT,
   insurance_nullfix.claim.PATT_CHRG_TOTA,
   insurance_nullfix.claim.TAMT_SFCA,
   insurance_nullfix.claim.NON_PAY,
   insurance_nullfix.claim.SELF_CHAM,
   insurance_nullfix.claim.PMMI_DLNG_YN,
   insurance_nullfix.claim.PAYM_AMT,
   insurance_nullfix.claim.DMND_AMT,
   insurance_nullfix.claim.PAYM_DATE,
   insurance_nullfix.claim.CHME_LICE_NO,
   insurance_nullfix.claim.HOSP_SPEC_DVSN,
   insurance_nullfix.claim.ACCI_HOSP_ADDR,
   insurance_nullfix.claim.HOUSE_HOSP_DIST,
   insurance_nullfix.claim.VLID_HOSP_OTDA,
   fpinfo.INCB_DVSN,
   fpinfo.ETRS_YM,
   fpinfo.FIRE_YM,
   fpinfo.CLLT_FP_PRNO,
   fpinfo.BRCH_CODE,
   fpinfo.EDGB,
   fpinfo.BEFO_JOB
  From
    claim inner Join
          (Select cust.* From cust Where cust.SIU_CUST_YN = %s) as cust_part
      On cust_part.CUST_ID = claim.CUST_ID
    Left Join
    insurance_nullfix.cntt
      On insurance_nullfix.claim.POLY_NO = insurance_nullfix.cntt.POLY_NO And
      insurance_nullfix.cntt.CUST_ID = insurance_nullfix.claim.CUST_ID 
    Left join 
    insurance_nullfix.fpinfo
      On insurance_nullfix.cntt.CLLT_FP_PRNO = fpinfo.CLLT_FP_PRNO """

#제출용 데이터의 cust_id 목록. 
sql_custid_submit='''Select   cust_part.cust_id  From  claim inner Join
(Select cust.* From cust Where cust.SIU_CUST_YN = 2 ) as cust_part
On cust_part.CUST_ID = claim.CUST_ID'''

def columnNames(sql,initial="select",end="from"): #컬럼네임 리스팅 좌우 단어 받아서 컬럼네임 배열로 출력. 
    sql=sql.upper()
    initial=initial.upper()
    end=end.upper()
    column_names=sql[sql.find(initial)+len(initial)+1 : sql.find(end)] #select 이후 띄어쓰기 하나 때문에 +1
    column_names=column_names.replace(" ","").split(",")
    #print (column_names)
    #print len(column_names)
    return column_names

def getdata(yn):
    # yn=str(yn) #원래는 텍스트+텍스트라 str 변환이었지만 %d 에 대입위해 숫자로 들어온거 냅둠.
    sql=sql_input%yn
    #sql=sql+' limit 100' #테스트용 10개만 뽑아볼때쓰는 코드
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

def normalize(array,ifnormalize=1): #-0.5~+0.5
    if ifnormalize:
      array=numpy.array(array,dtype='float32')
      for col_num in range(0,array.shape[1]):
        array[:,col_num]=(array[:,col_num]-array[:,col_num].min(0))/array[:,col_num].ptp(0)-0.5
      return array
    else:
      return array

def randomize(labels,dataset):
    permutation = numpy.random.permutation(labels.shape[0])
    shuffled_dataset=dataset[permutation,:]
    shuffled_labels = labels[permutation]
    return shuffled_labels, shuffled_dataset

def dataDivide(dataset,test_ratio): #일정비율로 테스트와 트레인셋을 나눔
    divide_position=int(dataset.shape[0]*test_ratio)
    test= dataset[:divide_position]
    train = dataset[divide_position:]
    return test, train

def pickletest(pickle_name):
    with open(pickle_name,'rb') as g:
        data=pickle.load(g)
        print data['test_label'][10]
        print data['test_data'][10]

def autoCategoricalIndex(array,n_category_limit=100): #numpy array 받음
    #유니크 자료수가 100개 미만이면 categorical 로 분류해 [true, false, false,.... ] 로 만들어 내보낸다.
    if n_category_limit>0:
      autocat=numpy.array(unqCount(array)<n_category_limit)
    else : #0또는 그 아래 값일때 
      autocat=numpy.zeros(array.shape[0]) #다 false 로 반환한다.
    return autocat


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
        print('받은 배열의 컬럼이 limit 개수보다 많아서 더미화 하지 않습니다.')
        return -1

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
        print('dummylize cancelled. passing original array...')
        cat_index=numpy.zeros(cat_index.shape[0])
    column_names=columnNames(sql) #더미화된 결과 컬럼이름 받기위해 sql 을 받아오기로 함. 
    print '\nbefore dummylize, ',array.shape[1],' columns. ' 
    # print 'got index ',cat_index.shape[0],'columns'
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
    # print 'after dummylyze, ',array.shape[1],' columns.'
    return column_names, array

def chkDistri(data, divide=10): #기본 값구간 10개로 나눔.  [총평균,총개수, 구간1평균,구간1개수, 구간2평균,구간2개수 ... ]
    data=numpy.array(data,dtype='float32')
    print data.shape, 'will be divided into ',divide,' sections. ',1./divide,' for each sectins   *total: -0.5~ +0.5)'
    # print 'A warning    \'RuntimeWarning: Mean of empty slice\'    can appear if there is no data in specific section. \n but that\'s OK'
    distri=numpy.zeros((data.shape[1],2*(divide+1))) #컬럼수,쪼갬수(평균,개수 2개씩이라 *2, 총평균/개수 포함이라 +1)
    for n_col in range(0,data.shape[1]): #컬럼별.
        #print(data[:,col])
        data_col= numpy.sort(data[:,n_col]) #구간별로 쪼개기위해 커지는 순서로 정렬. ascending order
        indicator = numpy.array([(slit+1)*1./divide-0.5 for slit in range(0,divide)],dtype='float32') #dtype 안맞추면 이상하게 비교함. 
        for div_step in range(0,2): #평균을 divide 개로 나누는데 처음 한번은 전체평균과 개수를 넣고 두번째는 구간평균과 개수 넣으려 함. 
            if div_step == 0 : #처음 3개는 전체평균, 전체개수, 조각개수를 구하고
                distri[n_col,div_step]=numpy.average(data_col) #전체 평균
                distri[n_col,div_step+1]=data_col.shape[0] #전체 개수
            else: #첫번째가 아니면 -0.5~+0.5를 지정개수대로 쪼갠뒤 구간별 평균과 개수를 만든다.
                index_array=numpy.searchsorted(data_col,indicator,side='right') #sort 된 컬럼에서 indecator 값들이 몇번째에 있는지 배열로 나타냄
                item_prev=0
                for i, item in enumerate(index_array): #인덱스번호를 index_array 로 한방에 만드는바람에 위치지정이 꼬였음. 
                    #print i,item, div_step
                    #개수는 0으로 표현되지만 평균은 개수가 0일때 nan 표기됨. 이건 nonetype 이 되어 모든 데이터를 nonetype 만들고, 나중에 pickle 화나 excel 변환시 타입오류 만듬.
                    temp = numpy.average(data_col[item_prev:item])#구간별 평균을 삽입
                    if not (temp==temp) : #nan 은 서로 == 연산해도 false 인걸 이용해서. 
                        distri[n_col,2*(i+1)]= 0.
                    else : 
                        distri[n_col,2*(i+1)]= temp
                    distri[n_col,2*(i+1)+1]= item - item_prev #구간별 개수를 삽입
                    item_prev = item #현재값 저장
    #print distri[1] #잘나왔나 한줄 집어서 확인
    return distri

def labelWithJoin(y,n): #a는 1로, b는 0으로 라벨링한후 합쳐진 라벨을 반환한다.
    join=numpy.concatenate((numpy.zeros(y.shape[0])+1,numpy.zeros(n.shape[0])),axis=0)
    return join


def normAndDummy(get_y,get_n,get_submit): 
    get=numpy.concatenate((get_y,get_n,get_submit),0) #왜 나눠서 가져왔냐면, classification index 만들기 위해서임
    print 'after concatenate :', get.shape
    #아래는 자동으로 카테고리 컬럼이 뭔지 생성. 
    get_cat_tf_index=autoCategoricalIndex(get,showCategoricalLimit(get,afterdummy_variables_limit))
    get_cnames, get=dummylize(get, get_cat_tf_index, sql_input)
    get=normalize(get,ifnormalize)
    print 'get shape : ',get.shape
    get_y=get[:get_y.shape[0]]
    get_n=get[get_y.shape[0]:get_y.shape[0]+get_n.shape[0]]
    get_submit=get[get_y.shape[0]+get_n.shape[0]:]
    del get #메모리를 위해. 
    print '\n','after divide & normalize & dummylize'
    print'get_y shape : ',get_y.shape
    print'get_n shape : ',get_n.shape,
    print'get_submit shape : ',get_submit.shape,'\n'
    return get_y, get_n, get_submit, get_cnames


#실제 실행 시작 =================================================
#==========================================================

try:
#자료 가져와서, 변수타입 float로 바꾸고, numpy 배열로 변경
    get_y=numpy.array(allFloat(getdata('1 Order By  rand()')),dtype='float32')
    print'original get_y shape : ',get_y.shape
    # print get_y
    get_n=numpy.array(allFloat(getdata('0 Order By  rand()')),dtype='float32')
    print'original get_n shape : ',get_n.shape
    # print get_n
    get_s=numpy.array(allFloat(getdata('2')),dtype='float32') #제출데이터. 순서 섞지않고 받아온다. 
    print'data for submit shape: ',get_s.shape
    print'submit : ',get_s

#submit 의 경우 cust_id 도 가져와야 한다 
    cur.execute(sql_custid_submit)
    get_s_custid = numpy.array([list(a) for a in cur.fetchall()])
    print 'get_s_custid shape :',get_s_custid.shape
    print 'get_s_custid :',get_s_custid

#dummy,normalize. SQL에서 클래스별 자료를 따로 받아왔지만 노멀라이즈는 합쳐서 해야하고, 더미도 유니크 항목 기준이기때문에 합쳤다 다시나눔.
#내부적으로 합쳐서 노멀, 더미 후에 다시 나눠서 반환함. 
#더미시에 컬럼 늘기때문에 컬럼명도 여기서 추가됨.  
    get_y,get_n, get_s, get_cnames = normAndDummy(get_y,get_n,get_s) 
    print 'get_s shape : ',get_s.shape

#더미화 끝난 y, n 을 각각 test/train 으로 나눔
    test_y, train_y = dataDivide(get_y,test_ratio)
    test_n, train_n = dataDivide(get_n,test_ratio)
    del get_y, get_n #나누기 전 자료는 필요없음

#라벨링하며 test는 test끼리, train 은 train끼리 합쳐 하나의 큰 배열로 만듬. train시 순서 섞기 위함
    test_label=labelWithJoin(test_y,test_n)
    train_label=labelWithJoin(train_y,train_n)
#데이터도 합쳐줌. 라벨이 y-n 순서였으니 이것도 같은 순서로 합침. 
    test_data=numpy.concatenate((test_y,test_n),axis=0)
    train_data=numpy.concatenate((train_y,train_n),axis=0)
    print' test label, data : ',test_label.shape, test_data.shape
    print' train label, data : ',train_label.shape, train_data.shape
    del test_y, test_n, train_y, train_n #사용끝난 변수 삭제

#학습을 위해 랜덤으로 위치 섞기
    test_label,test_data=randomize( test_label,test_data)
    train_label,train_data=randomize(train_label,train_data)
    print 'test_label : ',test_label
    print 'train_label : ',train_label

#for train set distribution analysis [전체평균,전체개수,구간1평균, 구간1개수, 구간2평균, 구간2개수 ... ]
    train_distri = chkDistri(train_data)

#picklelize
    f = open(pickle_name,'wb')
    save={
        'test_label' : test_label,
        'test_data' : test_data,
        'train_label' : train_label,
        'train_data' : train_data,
        'col_names' : get_cnames,
        'train_distri' : train_distri,
        'submit_data' : get_s,
        'submit_custid' : get_s_custid
        }
    pickle.dump(save,f,pickle.HIGHEST_PROTOCOL)
    f.close()
    print '\npicklize finished.  filename :',pickle_name,' Size : ',os.stat(pickle_name).st_size/1024/1024,'MByte'
    pickletest(pickle_name)

finally:
    print("closing")
    cur.close()
    mydb.close()
