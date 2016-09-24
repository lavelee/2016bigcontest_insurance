# -*- coding: utf-8 -*-

import subprocess
import os
import pickle
import MySQLdb
import time
t1=time.localtime() #시작시간
print 'started at', time.strftime('%y%m%d %Hh%Mm',t1)

mydb=MySQLdb.connect(host='localhost',user='root', passwd='tjdgus123', db='insurance') #존재하는 아무 DB나 연결하면 된다 
cur=mydb.cursor()
mydb.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')

def sql_execute():
    command='"C:/Program Files/MariaDB 10.1/bin/mysql.exe" -uroot -ptjdgus123 -e "drop database test"'
    print 'inserting sql :',command,'\n'
    subprocess.check_output(command,shell=True)

sql_execute()

cur.close()
mydb.close()
print('\nDB closed')
t2=time.localtime() #끝난 시간
print 'started at', time.strftime('%y%m%d %Hh%Mm',t1)
print 'ends at',  time.strftime('%y%m%d %Hh%Mm',t2)


