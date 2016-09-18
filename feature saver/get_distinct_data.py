# -*- coding: utf-8 -*-
#가장 가까운 값을 찾기위해서 컬럼의 unique 값들을 값이 점점 커지도록 정렬했고 , 테이블네임은 dict 로 찾고 세부 컬럼은 numpy 라서 이진서치 searchsorted 사용가능. 
#사용시에도 numpy import 필요.


#코드내에 한글로 된 경로가 있을때 위 인코딩줄 빼면 세이브가 안되어 실행되지 않는다. 
import MySQLdb, pickle, os, numpy as np

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

def pickler(skima):
    pickle_filename='distinct_data.pickle'
    f = open(pickle_filename,'wb')
    pickle.dump(skima,f,pickle.HIGHEST_PROTOCOL)
    f.close()
    print'\n pickle_size : ',os.stat(pickle_filename).st_size,'\n'


try:
    skima=getSkima()
    for table in skima:
        print '\n table ',table, 'is being processed below ------------------------------------------------------------'
        i=0
        for column in skima[table]:
            sql_check_date = 'SHOW FIELDS FROM '+table+' where Field ="'+column+'"'
            sql_type_date =  'select DISTINCT unix_timestamp('+column+')  from '+table+' order by '+column
            sql_type_notdate = 'select DISTINCT '                      +column+ '  from '+table+' order by '+column
            
            cur.execute(sql_check_date) #컬럼타입이 date 면 비교시에 비교불가라 뜨므로 숫자로 바꿔 가져오기 위해서 . 
            column_type=cur.fetchall()[0][1]
            print(column_type)
            if column_type=='date' :
                cur.execute(sql_type_date)
            else:
                cur.execute(sql_type_notdate)
            distinct_data=np.array([a[0] for a in cur.fetchall()])
            print(distinct_data)
            skima[table][i]=distinct_data
            i = i+1
        #break #한번만 동작하도록
    #print(skima) #전체 들어간거 확인
    pickler(skima)

finally:
    cur.close()
    mydb.close()
    print('Database Closed')

