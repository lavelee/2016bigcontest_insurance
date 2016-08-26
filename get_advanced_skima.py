# -*- coding: utf-8 -*-
#코드내에 한글로 된 경로가 있을때 위 인코딩줄 빼면 세이브가 안되어 실행되지 않는다. 

import MySQLdb, pickle, os

#서버접속 설정과 한글사용위한 인코딩 설정
mydb=MySQLdb.connect(host='localhost',user='root', passwd='tjdgus123', db='insurance')
cur=mydb.cursor()
mydb.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')

#데이터베이스에서 모든 테이블명과 컬럼명을 받아와 테이블명 : 컬럼명 의 딕셔너리 데이터로 합침. 
def getSkima(database_name='insurance'):
    db_skima = {}
    cur.execute('show tables')
    tables=[a[0] for a in cur.fetchall()]  #안하면 (('befo_job',), ('caus_1',), ('caus_2',), ('caus_3',)) 식으로 2개씩 뜸.
    #print(tables)
    for table in tables :
        #print(table)
        sql='SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA ="'+database_name+'" AND TABLE_NAME="'+table+'"'
        #print(sql)
        cur.execute(sql)
        columns=[a[0] for a in cur.fetchall()]
        #print(columns)
        db_skima[table]=columns
    #print(db_skima)
    return db_skima

#테이블명 : 컬럼들 구조의 딕셔너리 데이터를 받아 컬럼마다 평균과 분산을 삽입 . 기본값 안주면 자동으로 insurance에서 만들어온다.  getskima 함수를 필요로 함.
def getAdvSkima(database_name='insurance'):
    db_skima=getSkima(database_name)
    for table in db_skima:
        columns=db_skima[table]
        i=0
        for column in columns:
            cur.execute('SELECT avg('+column+') from '+table)
            avg = cur.fetchall()[0][0]
            cur.execute('SELECT stddev('+column+') from '+table)
            stddev = cur.fetchall()[0][0]
            cur.execute('SHOW FIELDS FROM '+table+' where Field ="'+column+'"')
            column_type = cur.fetchall()[0][1]
            db_skima[table][i]=[column,avg,stddev,column_type]
            i=i+1
        #print(db_skima[table])
    return db_skima

#평균과 분산 삽입이 잘 되었나 확인하려고 만듬. db_skima 를 addFeature 로 adv_skima로 만들고 , advSkima[테이블명][컬럼명,평균,분산] 순으로 가져옴. 
def test_advSkima(test_tablename='claim'):
    test_skima=getAdvSkima()
    for column in test_skima[test_tablename]: #test table name
        print'table_name     : ',test_tablename
        print'column_name : ',column[0]
        print'average          : ','text_data' if column[1]==0 else column[1]
        print'std dev           : ','text_data' if column[2]==0 else column[2]
        print'field type         : ',column[3],'\n'

def pickler(pickle_filename='adv_skima.pickle'):
    f = open(pickle_filename,'wb')
    pickle.dump(getAdvSkima(),f,pickle.HIGHEST_PROTOCOL)
    f.close()
    print('pickle_size : ',os.stat(pickle_filename).st_size)


try:
    print(getAdvSkima()['cust']) #cust 테이블을 예시로 가져와봄.
    pickler() #이렇게 켜면 파일 제작

finally:
    cur.close()
    mydb.close()
    print('Database Closed')

