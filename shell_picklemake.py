# -*- coding: utf-8 -*-

#윈도우에서 DB에서 테스트용 피클파일을 여럿 만들기위한 쉘파일.
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
sql_folder = 'c:/sql_to_pickle_forshell/db_sql/'               #nullfix DB 를 만들어주는 sql 폴더. 경로구분자를 \ 에서 / 로 변경했다. 경로에 한글이 있으면 안된다 . 마지막에 / 를 추가해줘야한다. 
subpy = 'c:/sql_to_pickle_forshell/insurance_pickle_forshell.py'    #실행할 py 파일. 한글경로 들어가면 안됨
#변화시킬 변수지정 
outdel=[0,1]
dummy=[0,100,1000] #원래 함수는 %로도 되어서 0.01 를 받았는데, subpy를 수정해서 int 로 변환하게 해놨으므로 정수만 넣자. 
n_pickle=4


#폴더내 sql 파일들 리스트 얻기
files_name = os.listdir(sql_folder)
print 'sql list : ',files_name,'\n' #파일명만 리스트 체크
files_wpath = [sql_folder+item for item in files_name]  #os.path.join 쓰면 경로와 파일사이에 \\ 를 넣어주는데 난 / 를 쓰고싶어서 직접. 
#print files_wpath #전체경로 포함한 리스트 체크

mydb=MySQLdb.connect(host='localhost',user='root', passwd='tjdgus123', db='insurance') #존재하는 아무 DB나 연결하면 된다 
cur=mydb.cursor()
mydb.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')

def sql_execute(file_wpath):
    command='"C:/Program Files/MariaDB 10.1/bin/mysql.exe" -uroot -ptjdgus123 < "'+file_wpath+'"'
    print 'inserting sql :',command,'\n'
    subprocess.check_output(command,shell=True)



def where(i,j,k,l,jmax=len(outdel),kmax=len(dummy),lmax=n_pickle): 
#현재위치 셈. imax는 필요가 없다
    position = (i*jmax*kmax*lmax +
                j*     kmax*lmax +
                k*          lmax +
                l+1                ) #마지막 digit에는 +1 해줘야함.
    return position

try: # i:sql파일번호 ,j:outdel 0/1 , k : dummy  l: duplicated pickle no
    total_num = len(files_wpath)*len(outdel)*len(dummy)*n_pickle #총 개수 자동계산
    for i, file_wpath in enumerate(files_wpath):
        sql_execute(file_wpath) #파일1개 실행
        #print 'file# :', i              #현재 몇번째 파일인지 . 0부터 시작함
        #print file_wpath+' executed' # 파일이름 실행되었습니다

        #i번째 sql 이 들어간 상태에서 subpy 실행. dummy 없이, 100, 1000, outdel 하고 없이, 100, 1000. 각각 4개씩 총 6*4=24개의 pickle 만듬.
        #filename : rand00 outdel0 dummy000 00.pickle
        for j,j_outdel in enumerate(outdel):
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
    cur.close()
    mydb.close()
    print('\nDB closed')
    t2=time.localtime() #끝난 시간
    print 'started at', time.strftime('%y%m%d %Hh%Mm',t1)
    print 'ends at',  time.strftime('%y%m%d %Hh%Mm',t2)


