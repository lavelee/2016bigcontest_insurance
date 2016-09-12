# -*- coding: utf-8 -*-
import subprocess
k=subprocess.check_output('python D:\codesample_forshell.py "the beginning" 2')  #실행할 파일경로에 한글 있으면 오류남 
print '\n the result is : ', k                                                      #출력값을 변수로 받아올 수 있음

