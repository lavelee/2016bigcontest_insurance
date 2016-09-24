# -*- coding: utf-8 -*-
#graphviz 라는 외부프로그램 사용. http://www.graphviz.org/Download_windows.php 에서 윈도우용 다운. 35메가쯤됨.
#그 후에 pydotplus pip로  설치 (순서 지켜야 dot.exe 가 생성됨. )
#그후에 또 dot.exe 존재하는 경로를 찾아서  윈도우 환경변수 path에 등록.
#path 등록후엔 재부팅 필수. 재부팅전엔 추가 안된걸로 나옴.
#너무 커서 pdf 가로길이가 일정수준 넘으면 뷰어가 포기해서 희게나옴. 그럴땐 max_depth제한 지정+컬럼명 길경우 rotate=true
from sklearn.ensemble import AdaBoostClassifier as abc
from sklearn.ensemble import RandomForestClassifier as rf
from sklearn import tree
from sklearn.externals.six import StringIO
import pydotplus
import pickle
import numpy as np
import sys

picklename='nullfix01 outdel0 dummy0 0.pickle'
trainer_select = 'adaboost'
# trainer_select = 'tree'
# trainer_select = 'randomforest'
n_estimators=1000
learning_rate=0.8
pdfname='test.pdf'
ifpdf=0

try : #변수를 외부에서 받아오는거 설정하고 없으면 pass
    picklename= sys.argv[1]
    trainer_select = sys.argv[2] #adaboost, tree, randomforest 3중 하나를 받아옴. 없으면 지정값으로
    if trainer_select =='adaboost':
        n_estimators=int(sys.argv[3])
        learning_rate=float(sys.argv[4])
    elif trainer_select =='randomforest':
        n_estimators=int(sys.argv[3])
    elif trainer_select =='tree':
        filename      =sys.argv[3]
    else:
        raise NameError('Wrong argv : only adaboost/tree/randomforest available')
except IndexError :
    pass

def f1Score(predictions, labels):
    #print 'predictions_raw=',predictions
    predictions=np.array(predictions)
    predictions=np.arange(2) == predictions[:,None].astype(np.float32)
    labels     =np.array(labels)
    labels     =np.arange(2) == labels[:,None].astype(np.float32)
    predictions = np.array(predictions==predictions.max(axis=1)[:,None],dtype='float32')
    predict = np.sum(predictions,0)
    real = np.sum(labels,0)
    correct_predict = np.sum(labels*(np.argmax(predictions, 1) == np.argmax(labels, 1))[:,None],0)
    precision = float(correct_predict[1])/predict[1]
    recall = float(correct_predict[1])/real[1]
    f1_score=2*precision*recall/(precision+recall)
    #print 'predictions =',predictions
    print'sin predict :',predict[1]
    print'sin correct predict :',correct_predict[1]
    print'sin real :',real[1]
    print'sin F1 score :',f1_score
    return f1_score

with open(picklename,'rb') as f:
    data=pickle.load(f)
train_label=data['train_label']
train_data =data['train_data']
test_label =data['test_label']
test_data  =data['test_data']
column_names=data['col_names']
del data

#조건별로 트레이너와 변수 세팅
if trainer_select =='adaboost':
    trainer = abc(n_estimators=n_estimators,learning_rate=learning_rate).fit(train_data,train_label)
elif trainer_select =='randomforest':
    trainer = rf(n_estimators=n_estimators).fit(train_data,train_label)
elif trainer_select =='tree': #tree 는 pdf 파일도 작성
    trainer = tree.DecisionTreeClassifier().fit(train_data,train_label)
    if ifpdf==1: #필요하다면 pdf로 출력
        dot_data=StringIO()
        tree.export_graphviz(trainer,
                             out_file=dot_data,
                             feature_names=column_names,
                             class_names=['innocent','sin'],
                             filled=True, rounded=True,
                             impurity=False,max_depth=6,rotate=True
                             )
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        graph.write_pdf(pdfname)
    else:
        pass
else:   
    raise NameError('Wrong trainer select : only adaboost/tree/randomforest available')

#prediction 수행후 f1 출력
tr_prediction = trainer.predict(test_data)
f1Score(tr_prediction,test_label)
print 'finished'
