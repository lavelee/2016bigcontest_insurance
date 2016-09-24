# -*- coding: utf-8 -*-
#graphviz 라는 외부프로그램 사용. http://www.graphviz.org/Download_windows.php 에서 윈도우용 다운. 35메가쯤됨.
#그 후에 pydotplus pip로  설치 (순서 지켜야 dot.exe 가 생성됨. )
#그후에 또 dot.exe 존재하는 경로를 찾아서  윈도우 환경변수 path에 등록.
#path 등록후엔 재부팅 필수. 재부팅전엔 추가 안된걸로 나옴.
#너무 커서 pdf 가로길이가 일정수준 넘으면 뷰어가 포기해서 희게나옴. 그럴땐 max_depth제한 지정+컬럼명 길경우 rotate=true
from sklearn.ensemble import AdaBoostClassifier as abc
from sklearn.externals.six import StringIO
import pydotplus
import pickle
import numpy as np

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
    print 'predict =',predict
    print 'real =',real
    print 'correct_predict =',correct_predict
    print 'precision =',precision
    print 'recall =',recall
    print 'f1_score =',f1_score
    return f1_score

with open('clcntt_randfix01.pickle','rb') as f:
    data=pickle.load(f)
train_label=data['train_label']
train_data =data['train_data']
test_label =data['test_label']
test_data  =data['test_data']
column_names=data['col_names']
del data

trainer = abc(n_estimators=100,learning_rate=0.9).fit(train_data,train_label)
tr_prediction = trainer.predict(test_data)
f1Score(tr_prediction,test_label)

"""
dot_data=StringIO()
tree.export_graphviz(trainer,
                     out_file=dot_data,
                     feature_names=column_names,
                     class_names=['innocent','sin'],
                     filled=True, rounded=True,
                     impurity=False,max_depth=6,rotate=True
                     )
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("test.pdf")
"""