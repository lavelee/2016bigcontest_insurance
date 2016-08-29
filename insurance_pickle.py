# -*- coding: utf-8 -*-
#코드내에 한글로 된 경로가 있을때 위 인코딩줄 빼면 세이브가 안되어 실행되지 않는다. 

import MySQLdb
import datetime
import pickle

#서버접속 설정과 한글사용위한 인코딩 설정
mydb=MySQLdb.connect(host='localhost',user='root', passwd='tjdgus123', db='insurance_nullfix')
cur=mydb.cursor()
mydb.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')

#query . 끝에 Y/N 은 제외했다 나중에 붙임.
sql_cucntt="select CUST_ROLE, IRKD_CODE_DTAL, IRKD_CODE_ITEM, GOOD_CLSF_CDNM, CNTT_YM, CLLT_FP_PRNO, REAL_PAYM_TERM, SALE_CHNL_CODE, CNTT_STAT_CODE, EXPR_YM, EXTN_YM, LAPS_YM, PAYM_CYCL_CODE, MAIN_INSR_AMT, SUM_ORIG_PREM, RECP_PUBL, CNTT_RECP, MNTH_INCM_AMT, DISTANCE, cust.* from cntt left join cust on cntt.CUST_ID=cust.CUST_ID where cust.SIU_CUST_YN="
sql_cuclaim="select ACCI_OCCP_GRP1, ACCI_OCCP_GRP2, CHANG_FP_YN, RECP_DATE, ORIG_RESN_DATE, RESN_DATE, CRNT_PROG_DVSN, ACCI_DVSN, CAUS_CODE, CAUS_CODE_DTAL, DMND_RESN_CODE, DMND_RSCD_SQNO, HOSP_OTPA_STDT, HOSP_OTPA_ENDT, RESL_CD1, VLID_HOSP_OTDA, HOUSE_HOSP_DIST, HOSP_CODE, ACCI_HOSP_ADDR, HOSP_SPEC_DVSN, CHME_LICE_NO, PAYM_DATE, DMND_AMT, PAYM_AMT, PMMI_DLNG_YN, SELF_CHAM, NON_PAY, TAMT_SFCA, PATT_CHRG_TOTA, DSCT_AMT, COUNT_TRMT_ITEM, DCAF_CMPS_XCPA, NON_PAY_RATIO, HEED_HOSP_YN, cust.* from claim left join cust on claim.CUST_ID=cust.CUST_ID where cust.SIU_CUST_YN="


def getdata(target,yn):
    yn=str(yn) #숫자로 넘어온거 문자로 바꿔서 더할수있게
    if target=="cucntt":
        sql=sql_cucntt+yn
    elif target=="cuclaim":
        sql=sql_cuclaim+yn
    sql=sql+' limit 2' #테스트용 10개만 뽑아볼때쓰는 코드
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
        print '\n printing data_type \n',data_type #첫줄에서 만든 데이터 타입
    return array

    #첫줄 타입 판단 , 저장
    #둘째줄부터 float 로 바꾸기

try:
    cucntt_y=getdata("cucntt",1)
    cucntt_n=getdata("cucntt",0)
    cucntt_y=getdata("cuclaim",1)
    cuclaim_n=getdata("cuclaim",0)

    allFloat(cucntt_y)
    print '변경 후 타입'
    allFloat(allFloat(cucntt_y))

finally:
    print("closing")
    cur.close()
    mydb.close()
