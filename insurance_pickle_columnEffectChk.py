# -*- coding: utf-8 -*-
#코드내에 한글로 된 경로가 있을때 위 인코딩줄 빼면 세이브가 안되어 실행되지 않는다. 

import MySQLdb
import datetime
import pickle
import numpy
import os, sys
import pandas

#sql_selectall 에다가 select 할 쿼리를 적고
#그 아래부분에 join 등 기타부분을 적고 
#파일명 표시를 위해 dbname과 tryno 를 적고
#피클생성시 outdel 실행 또는 dummylize 하기위해 변수를 적는다. 

#서버접속 설정과 한글사용위한 인코딩 설정
mydb=MySQLdb.connect(host='localhost',user='root', passwd='tjdgus123', db='insurance_nullfix')
cur=mydb.cursor()
mydb.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')


dbname = 'rand01' #손으로 적어준다. DB이름 구분하기 위함 
ifoutdel = 0 #0 또는 1
afterdummy_variables_limit = 0 #0, 100, 1000
#9/15 수정사항 : dummylize 0, 1 로 더미화 할꺼 체크하는게 아니라, dummy 리미트가 자기 고유컬럼수보다 적으면 작동안함. 0 넣으면 됨.
tryno = '02' #같은피클 여러번 만들어서 검증해야한다. 각 피클 메이킹 프로세스 구분. 손으로 바꿔주면서 돌린다. 파일명 마지막에 들어감

#query . 끝에 Y/N 은 제외했다 나중에 붙임.
#변수 구조상 cntt 를 뺄수는 없다. claim 변수가 메인이므로 cucntt 는 작게 줄여넣었다. dummylize도 0으로 고정시킴. 
sql_cucntt="""Select
  cntt.CUST_ROLE,
  cntt.MAIN_INSR_AMT,
  cntt.SUM_ORIG_PREM,
  cntt.RECP_PUBL
  From
  cntt Left Join
  cust
    On cntt.CUST_ID = cust.CUST_ID
  Where
  cust.SIU_CUST_YN ="""


#쿼리를 그대로 쓰는게 아니고, select 안의 컬럼과 나머지를 분리한다. 
sql_selectall = """insurance_nullfix.claim.HOSP_CODE,
  insurance_nullfix.cust.AGE,
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
  insurance_nullfix.cust.SEX,
  insurance_nullfix.cust.RESI_COST,
  insurance_nullfix.cust.RESI_TYPE_CODE,
  insurance_nullfix.cust.FP_CAREER,
  insurance_nullfix.cust.CUST_RGST,
  insurance_nullfix.cust.CTPR,
  insurance_nullfix.cust.OCCP_GRP1,
  insurance_nullfix.cust.OCCP_GRP2,
  insurance_nullfix.cust.TOTALPREM,
  insurance_nullfix.cust.MINCRDT,
  insurance_nullfix.cust.MAXCRDT,
  insurance_nullfix.cust.WEDD_YN,
  insurance_nullfix.cust.MATE_OCCP_GRP1,
  insurance_nullfix.cust.MATE_OCCP_GRP2,
  insurance_nullfix.cust.CHLD_CNT,
  insurance_nullfix.cust.LTBN_CHLD_AGE,
  insurance_nullfix.cust.MAX_PAYM_YM,
  insurance_nullfix.cust.MAX_PRM,
  insurance_nullfix.cust.CUST_INCM,
  insurance_nullfix.cust.RCBASE_HSHD_INCM,
  insurance_nullfix.cust.JPBASE_HSHD_INCM,
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
  insurance_nullfix.claim.VLID_HOSP_OTDA
  """

#select+자동 컬럼선택 + from to end (마지막에 YN=  까지만 적어서 자동 카테고리 되게)
from_to_end=""" From
        insurance_nullfix.claim Left Join 
        insurance_nullfix.cust 
        On insurance_nullfix.claim.CUST_ID = insurance_nullfix.cust.CUST_ID
        Left Join
        insurance_nullfix.cntt
        On insurance_nullfix.claim.POLY_NO = insurance_nullfix.cntt.POLY_NO And
        insurance_nullfix.cntt.CUST_ID = insurance_nullfix.claim.CUST_ID
        where
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
        #print data['test_cuclaim_label'][10]
        #print data['test_cuclaim_data'][10]

def autoCategoricalIndex(array,n_category_limit=100): #numpy array 받음. cat limit이 - 값(자기 컬럼수보다 기준이 작을때)이면 분류 안함. 
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
        #print '\nvariable limit : ',total_variable_limit
    else:
        limit=total_variable_limit*array.shape[0]
        #print '\nvariable limit ratio : ',total_variable_limit*100,'%   ',total_variable_limit*array.shape[0]

    n_total_variables=array.shape[1]
    if limit < n_total_variables:
        #print('받은 배열의 컬럼이 limit 개수보다 많아서 더미화 하지 않습니다.')
        return -1

    for i in range(0,unq_sorted.shape[0]):
        n_total_variables += unq_sorted[i]-1 #해당 변수를 dummylize 해서 추가된 변수개수를 포함하면 총 변수개수는 몇개가 되는가.
        if n_total_variables > limit: #총 데이터 라인수*지정비율 보다 변수 수가 많아질때
            #print '\n now total variables calculated : ', n_total_variables 
            #print 'unique items vector : ',unq_array
            #print 'unique items sorted vector : ',unq_sorted
            #print 'you can dummylize ',i,'columns counted from smallest'
            #print 'dummylize 할 수 있는 컬럼중 가장 항목수가 많은 컬럼의 항목수 : ',unq_sorted[i-1]
            #print 'Variable# sum expected after dummylize : ', n_total_variables-unq_sorted[i]
            return unq_sorted[i-1]+1 #가능한 가장 큰 값에 +1 함. 

def dummylize(array,cat_index,sql):
    column_names=columnNames(sql) #더미화된 결과 컬럼이름 받기위해 sql 을 받아오기로 함. 
    #print '\nbefore dummylize, ',array.shape[1],' columns. ' 
    #print 'got index 5 columns',cat_index.shape[0]
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
    #print 'after dummylyze, ',array.shape[1],' columns.'
    return column_names, array

def chkDistri(data, divide=10): #기본 값구간 10개로 나눔.  [총평균,총개수, 구간1평균,구간1개수, 구간2평균,구간2개수 ... ]
    data=numpy.array(data,dtype='float32')
    #print data.shape, 'will be divided into ',divide,' sections. ',1./divide,' for each sectins   *total: -0.5~ +0.5)'
    #print 'A warning    \'RuntimeWarning: Mean of empty slice\'    can appear if there is no data in specific section. \n but that\'s OK'
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


try:
    sql_selectall_list=sql_selectall.split(',')
    #print sql_selectall_list
    for i in range(0,len(sql_selectall_list)):
        pop_column=sql_selectall_list.pop(i)
        col_select=','.join(sql_selectall_list) #하나 빼서 쿼리 내용물 만들고
        sql_selectall_list.insert(i,pop_column) #바로 다시 되돌려둔다. 

        #실제로는 cuclcntt 로 세 테이블 합쳐지는 쿼리임. 변수명 귀찮아서 안 바꿈. 
        sql_cuclaim="""Select """+col_select+from_to_end



        #filename : (저장경로/)rand00 outdel0 dummy000 00 popcolumn.pickle
        pickle_name = dbname+' outdel'+str(ifoutdel)+' dummy'+str(afterdummy_variables_limit)+' tryno'+str(tryno)+' del-'+pop_column[pop_column.find('insurance_nullfix')+len('insurance_nullfix')+1:]+'.pickle'


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
        cucntt_cat_tf_index=autoCategoricalIndex(cucntt,showCategoricalLimit(cucntt,0)) #cucntt 는 언제나 더미화 안되게 하기.
        cuclaim_cat_tf_index=autoCategoricalIndex(cuclaim,showCategoricalLimit(cuclaim,afterdummy_variables_limit)) #값 크기에 따라 더미화 됨. 
        cucntt_cnames, cucntt  =dummylize(cucntt , cucntt_cat_tf_index , sql_cucntt) 
        cuclaim_cnames, cuclaim=dummylize(cuclaim, cuclaim_cat_tf_index, sql_cuclaim) 
        cucntt=normalize(cucntt) #합친김에 normalize
        cuclaim=normalize(cuclaim)
        #print 'cucntt shape : ',cucntt.shape
        print 'shape : ',cuclaim.shape #이름은 cuclaim 이지만 내용은 계속 바뀜.  
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

    #train set distribution analysis [전체평균,전체개수,구간1평균, 구간1개수, 구간2평균, 구간2개수 ... ]
        train_cucntt_distri=0 #off 시에도 동작하게 하려고 일단 변수는 생성.
        train_cuclaim_distri=0
        train_cucntt_distri = chkDistri(train_cucntt_data)
        train_cuclaim_distri = chkDistri(train_cuclaim_data)

    #picklelize
        f = open(pickle_name,'wb')
        save={
            'test_cucntt_label' : test_cucntt_label,
            'test_cucntt_data' : test_cucntt_data,
            'train_cucntt_label' : train_cucntt_label,
            'train_cucntt_data' : train_cucntt_data,
            'cucntt_column_names' : cucntt_cnames,
            'train_cucntt_distri' : train_cucntt_distri,

            'test_cuclaim_label' : test_cuclaim_label,
            'test_cuclaim_data' : test_cuclaim_data,
            'train_cuclaim_label' : train_cuclaim_label,
            'train_cuclaim_data' : train_cuclaim_data,
            'cuclaim_column_names' : cuclaim_cnames,
            'train_cuclaim_distri' : train_cuclaim_distri
            }
        pickle.dump(save,f,pickle.HIGHEST_PROTOCOL)
        f.close()
        print i+1,'/',len(sql_selectall_list),' filename :',pickle_name,' Size : ',os.stat(pickle_name).st_size/1024/1024,'MByte ....  picklize finished. '
        #print 'picklefile,'
        #pickletest(pickle_name)

finally:
    #print("closing DB")
    cur.close()
    mydb.close()
