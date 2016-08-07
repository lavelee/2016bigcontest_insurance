# -*- coding: utf-8 -*-
#코드내에 한글로 된 경로가 있을때 위 인코딩줄 빼면 세이브가 안되어 실행되지 않는다. 

import MySQLdb
import unicodecsv
import os


#서버접속 설정과 한글사용위한 인코딩 설정
mydb=MySQLdb.connect(host='localhost',user='root', passwd='tjdgus123', db='insurance')
cur=mydb.cursor()
mydb.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')


def allfiles(path):
    res = []
    for root, dirs, files in os.walk(path):
        rootpath = os.path.join(os.path.abspath(path), root)
        for file in files:
            filepath = os.path.join(rootpath, file)
            res.append(filepath)
    return res

def querymake(filepath,row) :
    table_name=filepath[filepath.find('\\')+1:filepath.find('.')]
    column_names= "(" + ",".join(row) + ")"
    values=" VALUES (" + (len(row)-1)*"%s," + "%s)"
    sql='INSERT INTO '+table_name+' '+column_names+values
    return sql


filelist=allfiles("D:/CSV/") 
#csv 파일은 제목이 테이블명, 첫줄에는 컬럼명, 인코딩 utf-8 필수임
#테이블 의존성 (왜래키) 감안해서 폴더명 1,2,3 등으로 이름정렬 순서생각해 만들어 그안에 파일넣기. 


sql=""
try:
    for filepath in filelist : 
        csv_data=unicodecsv.reader(file(filepath),encoding='utf-8-sig')

        i=0
        global sql
        print("inserting "+filepath) #작업중인 파일
        for row in csv_data:
            if i==0:
                #print(row) #헤더 보기
                sql=querymake(filepath,row)
            else:
                #print(sql) # 만들어진 쿼리 보기
                row = [None if x=="" else x for x in row] #빈 칸은 null로 넣게함 
                #print(row) # 내용 보기
                cur.execute(sql,row)
            i=i+1
        mydb.commit()
        #print("break") #파일 하나만 넣도록 제한하는 테스트코드
        #break #위와 동일

finally:
    print("closing")
    cur.close()
    mydb.close()
