# -*- coding: utf-8 -*-
import MySQLdb

mydb=MySQLdb.connect(host='localhost',user='root', passwd='tjdgus123', db='insurance') #존재하는 아무 DB나 연결하면 된다 
cur=mydb.cursor()

cur.execute('drop database test') #콘솔에서는 drop 실행문 뒤엔 ; 붙여야 하는데 mysql db 는 안붙여도 된다. 
print('database test dropped')

#sql 파일로부터 DB 생성할땐 source 명령을 쓸수없고 아래처럼 생성->sql 읽어실행 해줘야 한다. 
#cur.execute('create database test') #DB를 SQL 내보낼때 생성에 체크를 했다면 이 줄을 안써도 된다.
cur.execute(open('D:/test_sql/test 1.sql').read()) #경로에 띄어쓰기 있어도 그냥 쓰면되고 끝에 ; 붙일 필요 없다. 
print('sql executed')

#cur.close() #insert 가 끝나는거 확인안하고 접근해서 you can't run this command now 오류난다. 
#mydb.close()