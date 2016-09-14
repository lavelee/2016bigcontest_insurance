# -*- coding: utf-8 -*-
#코드내에 한글로 된 경로가 있을때 위 인코딩줄 빼면 세이브가 안되어 실행되지 않는다. 

# 이 파일은 이미 MySQL에 존재하는 insurance DB를 읽어 평균/분산을 구해오므로, 대입할 CSV만 있을때는 동작하지 않는다. 
# 평균/분산을 파일로 빼서 쓰게하면 좋겠지만 귀찮 귀찮..

import MySQLdb
import unicodecsv
import os
import numpy as np
import pickle

#서버접속 설정과 한글사용위한 인코딩 설정
mydb=MySQLdb.connect(host='localhost',user='root', passwd='tjdgus123', db='insurance_nullfix')
cur=mydb.cursor()
mydb.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')

search_db=MySQLdb.connect(host='localhost',user='root', passwd='tjdgus123', db='insurance')
search_cur=search_db.cursor()


sql=""
table_name=""
column_names=[]


def allfiles(path):
    res = []
    for root, dirs, files in os.walk(path):
        rootpath = os.path.join(os.path.abspath(path), root)
        for file in files:
            filepath = os.path.join(rootpath, file)
            res.append(filepath)
    return res

def tableName(filepath):
    return(filepath[filepath.find('\\')+1:filepath.find('.')])

def columnNames(row):
    return  "(" + ",".join(row) + ")"

def querymake(filepath,row) :
    table_name=tableName(filepath)
    column_names=columnNames(row)
    values=" VALUES (" + (len(row)-1)*"%s," + "%s)"
    sql='INSERT INTO '+table_name+' '+column_names+values
    return sql


filelist=allfiles("D:/CSV/") 
#csv 파일은 제목이 테이블명, 첫줄에는 컬럼명, 인코딩 utf-8 필수임
#테이블 의존성 (왜래키) 감안해서 폴더명 1,2,3 등으로 이름정렬 순서생각해 만들어 그안에 파일넣기. 
#한글경로 있는 폴더에 넣었더니 utf-8 인데도 못읽어옴.

with open('insurance_adv_skima.pickle','rb') as f:
    adv_skima=pickle.load(f)
    #for i in range(0,100):
    #   print(adv_skima['cust'][i][0])

def randNull(table,column):
    #print'column number = ',column,'    adv_skima[table][column][0] = ',adv_skima[table][column][0]
    col_avg=adv_skima[table][column][1]
    col_std=adv_skima[table][column][2]
    #print(col_avg)
    #print(col_std)
    rand_data=np.random.normal(col_avg,col_std,1)[0]
    sql='select '+table+'.'+adv_skima[table][column][0]+', '+ 'abs('+table+'.'+adv_skima[table][column][0]+'-'+str(rand_data)+') as distance from '+table+' where length('+table+'.'+adv_skima[table][column][0]+')>0 order by distance limit 1'
    #print(sql)
    search_cur.execute(sql)
    get_rand=search_cur.fetchall()[0][0]
    #print'New number : ',get_rand
    return get_rand

def progress(table_name,i):
    if table_name == 'claim':
        print i*100/141212,'% done.'
    elif table_name == 'poly_no':
        print i*100/113120,'% done.'
    elif table_name == 'cntt':
        print i*100/110066,'% done.'
    elif table_name == 'cust':
        print i*100/22417,'% done.'
    elif table_name == 'fpinfo':
        print i*100/31099,'% done.'


try:
    for filepath in filelist : 
        nullnum=0
        csv_data=unicodecsv.reader(file(filepath),encoding='utf-8-sig')
        i=0
        global sql
        global table_name
        global column_names

        print("inserting "+filepath) #작업중인 파일. 이건 주석해제하지 마세요 . 
        for row in csv_data:
            if i==0:
                #print(row) #헤더 보기
                table_name=tableName(filepath)
                column_names=row
                sql=querymake(filepath,row)
            else:
                #print(sql) # 만들어진 쿼리 보기
                j=0
                if i%1000==0:
                    progress(table_name,i)
                for x in row:
                    if x=="":
                        #print('null found ------------------------')
                        #print'j value : ',j,'       table :',table_name,'      column : ',column_names[j]
                        #print'from row : ',row
                        row[j]=randNull(table_name,j)
                        #print'new row : ',row
                        #print('success ---------------------------')
                        nullnum=nullnum+1
                    j=j+1
                #print(row) # 내용 보기
                cur.execute(sql,row)
            i=i+1

        #한개파일 끝날때마다 널 개수 출력    
        print nullnum,' Nulls in ',table_name
    mydb.commit() #모든파일 끝날때 커밋하는 위치임
        #print("break") 
        #break #파일 하나만 넣도록 제한하는 테스트코드

finally:
    cur.close()
    mydb.close()
    search_cur.close()
    search_db.close()
    print('Database Closed')
