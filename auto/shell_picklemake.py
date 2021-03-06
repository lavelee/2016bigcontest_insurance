# -*- coding: utf-8 -*-

#SQL에서 DB에서 테스트용 피클파일을 여럿 만들기위한 쉘파일. SQL파일 모인 폴더가 필요하므로, 이미 들어간 파일을 단순 여럿 만들고싶다면 insurance_pickle 사용.
#현재 DB 이름은 SQL 내보내기에서 미리 결정되어 sql 파일안에 들어가있는 상태이다. 따라서 insurance_nullfix  외에 다른 DB를 만드는 파일을 불러오면 현재 동작하지 않는다. 
#먼저 DB를 제거하고 시작하기때문에, 미리 insurace_nullfix 가 있어야 한다. 
#SQL 이 든 폴더에 pickle 파일을 만들기 때문에 재실행시 생성된 pickle 파일을 지워줘야 한다. 아니면 오류남 

import subprocess
import os
import pickle
import MySQLdb
import time
t1=time.localtime() #시작시간
print 'started at', time.strftime('%y%m%d %Hh%Mm',t1)

#파일저장위치, DB이름 
dbname='insurance_nullfix'                                                           #생성되고 삭제될 db 이름. 
sql_folder = 'D:/sql_to_pickle_forshell/db_sql/'               #nullfix DB 를 만들어주는 sql 폴더. 경로구분자를 \ 에서 / 로 변경했다. 경로에 한글이 있으면 안된다 . 마지막에 / 를 추가해줘야한다. 
subpy = 'D:/sql_to_pickle_forshell/insurance_pickle_cufix.py'    #실행할 py 파일. 한글경로 들어가면 안됨
#변화시킬 변수지정 : 
outdel=[0,1] #outdel은 0이나 1 적으면 그냥넘어가고 [0,1] 주면 1에서 outdel 쿼리 실행함.
dummy=[0, 100, 300] #원래 함수는 %로도 되어서 0.01 를 받았는데, subpy를 수정해서 int 로 변환하게 해놨으므로 정수만 넣자.  배열가능
n_pickle=3 #조건당 피클 몇개만듬


#폴더내 sql 파일들 리스트 얻기
files_name = os.listdir(sql_folder)
print 'sql list : ',files_name,'\n' #파일명만 리스트 체크
files_wpath = [sql_folder+item for item in files_name]  #os.path.join 쓰면 경로와 파일사이에 \\ 를 넣어주는데 난 / 를 쓰고싶어서 직접. 
#print files_wpath #전체경로 포함한 리스트 체크


#outdel 용 update 쿼리. 주석문 있으면 안되고 한줄씩 구분해둬야 한다. for line 으로 실행할꺼니까. 주석있거나 끝에 엔터있으면 빈쿼리 오류남. 
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



mydb=MySQLdb.connect(host='localhost',user='root', passwd='tjdgus123', db=dbname)
cur=mydb.cursor()
# mydb.set_character_set('utf8')
# cur.execute('SET NAMES utf8;')
# cur.execute('SET CHARACTER SET utf8;')
# cur.execute('SET character_set_connection=utf8;')

def sqlExecute_bypy(lines): #여러줄로 되었고 빈 주석문이나 빈 엔터줄 없는 sql 을 라인으로 잘라서 실행. 
    mydb=MySQLdb.connect(host='localhost',user='root', passwd='tjdgus123', db=dbname)
    cur=mydb.cursor()
    for line in outdel_sql.splitlines() : #outdel용 update 쿼리의 한줄씩 실행
        if line.find('*/')-line.find('/*')+2 == len(line) or line=='\n' : #한 줄 전체가 주석인 경우나 엔터만 있는경우 패스
            #print 'passing line : ',line
            pass
        else: #아닐때만 실행한다. 
            # print 'executing line : ',line
            cur.execute(line)
    cur.close()
    mydb.close()
    print 'outdel sql executed'

def sqlExecute_byshell(file_wpath):
    command='"C:/Program Files/MariaDB 10.1/bin/mysql.exe" -uroot -ptjdgus123 < "'+file_wpath+'"'
    print 'inserting sql :',command,'\n'
    subprocess.check_output(command,shell=True)

def dropDatabase(dbname):
    print 'trying to drop database :',dbname
    command='"C:/Program Files/MariaDB 10.1/bin/mysql.exe" -uroot -ptjdgus123 -e "drop database '+dbname+'"'
    subprocess.check_output(command,shell=True)
    print 'database dropped :',dbname

def where(i,j,k,l,jmax=len(outdel),kmax=len(dummy),lmax=n_pickle): 
#현재위치 셈. imax는 필요가 없다
    position = (i*jmax*kmax*lmax +
                j*     kmax*lmax +
                k*          lmax +
                l+1                ) #마지막 digit에는 +1 해줘야함.
    return position


total_num = len(files_wpath)*len(outdel)*len(dummy)*n_pickle #총 개수 자동계산
try: # i:sql파일번호 ,j:outdel 0/1 , k : dummy  l: duplicated pickle no
    for i, file_wpath in enumerate(files_wpath):
        # if i>0:   #drop 안해도 기본적으로 내용물 싹 비우고 다시 넣도록 sql 만들었기 때문에 괜춘. 
        #     dropDatabase(dbname) #2번째부터 기존 db 삭제. 뭘삭제는 소스파일 위쪽에 dbname 
        sqlExecute_byshell(file_wpath) #파일1개 실행
        #print 'file# :', i              #현재 몇번째 파일인지 . 0부터 시작함
        #print file_wpath+' executed' # 파일이름 실행되었습니다
        #i번째 sql 이 들어간 상태에서 subpy 실행. dummy 없이, 100, 1000, outdel 하고 없이, 100, 1000. 각각 4개씩 총 6*4=24개의 pickle 만듬.
        #filename : rand00 outdel0 dummy000 00.pickle
        for j,j_outdel in enumerate(outdel):
            if j==1: #0, 1로 주었었다면 처음에는 곱게 지나가고 1 일때는 아래 실행하고 진행함. 
                sqlExecute_bypy(outdel_sql.splitlines())
            for k,k_dummy in enumerate(dummy):
                for l in range(0,n_pickle):
                    sql_name = files_wpath[i][:files_wpath[i].find('.sql')] #sql 파일말고 딴거 넣지 않도록 조심.
                    ifoutdel = j_outdel
                    afterdummy_variables_limit = k_dummy
                    tryno = l

                    syscommand = 'python '+subpy+' '+str(sql_name)+' '+str(ifoutdel)+' '+str(afterdummy_variables_limit)+' '+str(tryno)
                    print where(i,j,k,l),'/',total_num,', executing ',': ',syscommand
                    get=subprocess.check_output(syscommand,shell=True)
                    print get

                    """ subpy 에서 변수 받는부분.
                    dbname = sys.argv[1] #sql 파일의 이름. nullfix01.sql 에서 .sql 떼고 nullfix01
                    ifoutdel = sys.argv[2] #0 또는 1
                    afterdummy_variables_limit = sys.argv[3] #0, 100, 1000
                    #randfix 등 DB 이름을 받아서 변수와 결합해 피클파일명 생성
                    tryno = sys.argv[4] #몇번째 제작중인 picklefile 인지 #0,1,2,3,4...
                    """
finally:
    t2=time.localtime() #끝난 시간
    print 'started at', time.strftime('%y%m%d %Hh%Mm',t1)
    print 'ends at',  time.strftime('%y%m%d %Hh%Mm',t2)


