# -*- coding: utf-8 -*-
#실행시 옵션값을줘서 변수를 받아올수 있게 했다
#쉘파일이 불러올때 이 파일 경로에 한글이 있으면 제대로 실행되지 않는다. 
#이 파일을 직접 실행할때는 경로에 한글이 있어도 괜찮다.

#변수할당시 파일명 뒤에 한칸띄우고 - 없이 바로 적는다. 씌어쓰기가 구분자이다. 순서대로 들어간다
# codesample_forshell.py 1 2 이런식. 


import sys

try :
    var1 = sys.argv[1]
except IndexError :
    var1 = 'no option 1'

try :
    var2 = sys.argv[2]
except IndexError :
    var2 = 'no option 2'

f = open('shelltest','wb')
f.close()

print sys.argv[0] , var1, var2
