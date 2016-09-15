# -*- coding: utf-8 -*-

#윈도우에서 DB에서 테스트용 피클파일을 여럿 만들기위한 쉘파일.
#현재 DB 이름은 SQL 내보내기에서 미리 결정되어 sql 파일안에 들어가있는 상태이다. 따라서 insurance_nullfix  외에 다른 DB를 만드는 파일을 불러오면 현재 동작하지 않는다. 
#먼저 DB를 제거하고 시작하기때문에, 미리 insurace_nullfix 가 있어야 한다. 
import subprocess
import os
import pickle
import MySQLdb
import time
t1=time.localtime() #시작시간
print 'started at', time.strftime('%y%m%d %Hh%Mm',t1)

#설정변수들 
dbname='insurance_nullfix'                                                           #생성되고 삭제될 db 이름. 
sql_folder = 'D:/sql_to_pickle_forshell/db_sql/'               #nullfix DB 를 만들어주는 sql 폴더. 경로구분자를 \ 에서 / 로 변경했다. 경로에 한글이 있으면 안된다 . 마지막에 / 를 추가해줘야한다. 
subpy = 'D:/sql_to_pickle_forshell/shell_picklemake1.py'    #실행할 py 파일. 한글경로 들어가면 안됨



#폴더내 sql 파일들 리스트 얻기
files_name = os.listdir(sql_folder)
print files_name #파일명만 리스트 체크
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
    print command
    subprocess.check_output(command,shell=True)


try: 
    for i, file_wpath in enumerate(files_wpath):
        sql_execute(file_wpath) #파일1개 실행
        #print 'file# :', i              #현재 몇번째 파일인지 . 0부터 시작함
        print file_wpath+' executed' # 파일이름 실행되었습니다

        #i번째 sql 이 들어간 상태에서 subpy 실행

        #syscommand = 'python '+subpy+' "'+pickle_file+'" '+str(layer2_nodes)+' '+str(learning_rate_init)+' '+str(k+1)+' '+select
        #print '\n',syscommand
        #get=subprocess.check_output(syscommand, shell=True) #subpy 실행결과를 py파일로 얻기



finally:
    cur.close()
    mydb.close()
    print('\nDB closed')
    t2=time.localtime() #끝난 시간
    print 'started at', time.strftime('%y%m%d %Hh%Mm',t1)
    print 'ends at',  time.strftime('%y%m%d %Hh%Mm',t2)


