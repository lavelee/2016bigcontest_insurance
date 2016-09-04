# -*- coding: utf-8 -*-
#코드내에 한글로 된 경로가 있을때 위 인코딩줄 빼면 세이브가 안되어 실행되지 않는다. 

import MySQLdb
import datetime
import pickle
import numpy
import os
import pandas
import xlwt
import scipy.stats

#서버접속 설정과 한글사용위한 인코딩 설정
mydb=MySQLdb.connect(host='localhost',user='root', passwd='tjdgus123', db='insurance_nullfix')
cur=mydb.cursor()
mydb.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')

#cucntt
#sql="SELECT CUST_ROLE, IRKD_CODE_DTAL, IRKD_CODE_ITEM, GOOD_CLSF_CDNM, CNTT_YM, CLLT_FP_PRNO, REAL_PAYM_TERM, SALE_CHNL_CODE, CNTT_STAT_CODE, EXPR_YM, EXTN_YM, LAPS_YM, PAYM_CYCL_CODE, MAIN_INSR_AMT, SUM_ORIG_PREM, RECP_PUBL, CNTT_RECP, MNTH_INCM_AMT, DISTANCE, SEX, AGE, RESI_COST, RESI_TYPE_CODE, FP_CAREER, CUST_RGST, CTPR, OCCP_GRP1, OCCP_GRP2, TOTALPREM, MINCRDT, MAXCRDT, WEDD_YN, MATE_OCCP_GRP1, MATE_OCCP_GRP2, CHLD_CNT, LTBN_CHLD_AGE, MAX_PAYM_YM, MAX_PRM, CUST_INCM, RCBASE_HSHD_INCM, JPBASE_HSHD_INCM, cust.SIU_CUST_YN FROM cntt LEFT JOIN cust ON cntt.CUST_ID=cust.CUST_ID"
#cuclaim
sql="SELECT ACCI_OCCP_GRP1, ACCI_OCCP_GRP2, CHANG_FP_YN, RECP_DATE, ORIG_RESN_DATE, RESN_DATE, CRNT_PROG_DVSN, ACCI_DVSN, CAUS_CODE, CAUS_CODE_DTAL, DMND_RESN_CODE, DMND_RSCD_SQNO, HOSP_OTPA_STDT, HOSP_OTPA_ENDT, RESL_CD1, VLID_HOSP_OTDA, HOUSE_HOSP_DIST, HOSP_CODE, ACCI_HOSP_ADDR, HOSP_SPEC_DVSN, CHME_LICE_NO, PAYM_DATE, DMND_AMT, PAYM_AMT, PMMI_DLNG_YN, SELF_CHAM, NON_PAY, TAMT_SFCA, PATT_CHRG_TOTA, DSCT_AMT, COUNT_TRMT_ITEM, DCAF_CMPS_XCPA, NON_PAY_RATIO, HEED_HOSP_YN, SEX, AGE, RESI_COST, RESI_TYPE_CODE, FP_CAREER, CUST_RGST, CTPR, OCCP_GRP1, OCCP_GRP2, TOTALPREM, MINCRDT, MAXCRDT, WEDD_YN, MATE_OCCP_GRP1, MATE_OCCP_GRP2, CHLD_CNT, LTBN_CHLD_AGE, MAX_PAYM_YM, MAX_PRM, CUST_INCM, RCBASE_HSHD_INCM, JPBASE_HSHD_INCM, SIU_CUST_YN from claim left join cust on claim.CUST_ID=cust.CUST_ID"

def columnNames(sql,initial="select",end="from"): #컬럼네임 리스팅 좌우 단어 받아서 컬럼네임 배열로 출력. 
    sql=sql.upper()
    initial=initial.upper()
    end=end.upper()
    column_names=sql[sql.find(initial)+len(initial)+1 : sql.find(end)] #select 이후 띄어쓰기 하나 때문에 +1
    column_names=column_names.replace(" ","").split(",")
    #print (column_names)
    #print len(column_names)
    return column_names

def getdata(sql):
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
            #print 'unique items vector : ',unq_array
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


try:
    #자료 가져와서, 변수타입 float로 바꾸고, numpy 배열로 업그레이드하고 -0.5~+0.5 normalize 까지 한방에! getdata만 바꿔주면됨.
    data_sql=numpy.array(allFloat(getdata(sql)),dtype="float32")
    afterdummy_variables_limit=100  #고유항목수 N개(N>1) , N의 비율로(0~1값) dummy 화 할지 결정. 
                                                #더미화로 추가될 컬럼수를 의미(항목 몇개이하~가 아님).   더미화 안된 컬럼+더미화 컬럼은 이 숫자보다 클수 있음.  
    data_cat_tf_index=autoCategoricalIndex(data_sql, showCategoricalLimit(data_sql,afterdummy_variables_limit)) #자동변수 . 아니면 수동으로
    #print  'data_cat_tf_index : ',data_cat_tf_index,data_cat_tf_index.shape
    data_cnames, data_dummylized = dummylize(data_sql, data_cat_tf_index, sql,1)
    data_dummylized = normalize(data_dummylized)

    data_pvalue=[]  #아래에서 골라쓰세영
    #data_corr = corrPearson(data_dummylized)
    data_corr , data_pvalue = corrSpearman(data_dummylized)
    print 'data_dummylized_shape : ',data_dummylized.shape
    print 'correlation data shape : ',data_corr.shape

    #picklelize
    pickle_name='data_corr.pickle'
    f = open(pickle_name,'wb')
    save={
        'correlation coeff' : data_corr,
        'category names' : data_cnames,
        'pvalue pearson' : data_pvalue
        }
    pickle.dump(save,f,pickle.HIGHEST_PROTOCOL)
    f.close()
    print '\npicklize finished.   Size : ',os.stat(pickle_name).st_size/1024/1024,'MByte'

    excel_name=pickle_name[:pickle_name.find(".pickle")]+'.xls'
    if os.path.isfile(excel_name): #이미 파일이 있으면 삭제함 #엑셀파일이 열려있으면 삭제도 못하고 오류남. 
	os.remove(excel_name)
	print('target excel file exists. continue after deleting')
    sheetmake(pickleread(pickle_name))

    os.remove(pickle_name)#피클 제거

finally:
    print("closing")
    cur.close()
    mydb.close()
