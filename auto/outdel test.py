#-*-coding: utf-8 -*-
import MySQLdb
mydb=MySQLdb.connect(host='localhost',user='root', passwd='tjdgus123', db='insurance') #존재하는 아무 DB나 연결하면 된다 
cur=mydb.cursor()
mydb.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')
outdel_sql="""update  insurance_nullfix.cust  set CUST_RGST = '1981-10-01' where  CUST_RGST <'1981-10-01';
update  insurance_nullfix.cust  set TOTALPREM = 203900291 where  TOTALPREM >203900291;
update  insurance_nullfix.cust  set MINCRDT = 6 where  MINCRDT >10;
update  insurance_nullfix.cust  set MAXCRDT = 6 where  MAXCRDT >10;
update  insurance_nullfix.cust  set MAX_PAYM_YM = '2023-12-01' where  MAX_PAYM_YM >'2023-12-01';
update  insurance_nullfix.cust  set MAX_PRM = 11927425 where  MAX_PRM > 11927425;
Update  insurance_nullfix.claim set HOSP_CODE = 12537  Where  HOSP_CODE = 99999999;
Update  insurance_nullfix.claim set CHME_LICE_NO = 25697  Where   CHME_LICE_NO = 99999999;
update  insurance_nullfix.claim set SELF_CHAM = 3659410 where  SELF_CHAM >3659410;
update  insurance_nullfix.claim set NON_PAY = 7530660 where  NON_PAY >7530660;
update  insurance_nullfix.claim set TAMT_SFCA = 2894401 where  TAMT_SFCA >2894401;
update  insurance_nullfix.claim set PATT_CHRG_TOTA = 11686570 where  PATT_CHRG_TOTA >11686570;
update  insurance_nullfix.claim set DSCT_AMT = 1113921 where  DSCT_AMT >1113921;
update  insurance_nullfix.claim set DCAF_CMPS_XCPA = 3900000 where  DCAF_CMPS_XCPA >3900000;
update  insurance_nullfix.cntt  set CLLT_FP_PRNO = 82 where  CLLT_FP_PRNO = 99999999;
update  insurance_nullfix.cntt  set REAL_PAYM_TERM = 72 where  REAL_PAYM_TERM = 999;
update  insurance_nullfix.cntt  set MAIN_INSR_AMT = 240000000 where  MAIN_INSR_AMT > 240000000;
update  insurance_nullfix.cntt  set SUM_ORIG_PREM = 60000000 where  SUM_ORIG_PREM > 60000000;
update  insurance_nullfix.cntt  set MNTH_INCM_AMT = 20000000 where  MNTH_INCM_AMT > 20000000;"""
for line in outdel_sql.splitlines() : #outdel용 update 쿼리의 한줄씩 실행
    if line.find('*/')-line.find('/*')+2 == len(line) or line=='\n' : #한 줄 전체가 주석인 경우나 엔터만 있는경우 패스
        pass
    else: #아닐때만 실행한다. 
        print 'executing line : ',line
#print(cur.execute(sql))
cur.close()
mydb.close()
