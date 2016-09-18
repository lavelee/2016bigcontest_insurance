# -*- coding: utf-8 -*-
import numpy as np


def f1Score(predictions, labels):
    print 'predictions_raw=',predictions
    predictions = np.array(predictions==predictions.max(axis=1)[:,None],dtype='int')
    predict = np.sum(predictions,0)
    real = np.sum(labels,0)
    correct_predict = np.sum(labels*(np.argmax(predictions, 1) == np.argmax(labels, 1))[:,None],0)
    precision = correct_predict[1]/predict[1]
    recall = correct_predict[1]/real[1]
    f1_score=2*precision*recall/(precision+recall)
    print 'predictions =',predictions
    print 'predict =',predict
    print 'real =',real
    print 'correct_predict =',correct_predict
    print 'precision =',precision
    print 'recall =',recall
    print 'f1_score =',f1_score
    return f1_score

pr               =np.array([[0.3,0.4], [0.7,-0.3],[-0.1,-0.3],[-0.5,0.34]],dtype='float32')
#predictions     =np.array([  [0,1],      [1,0],     [1,0],      [0,1]   ],dtype='int')
lab              =np.array([[1,0],    [0,1],[0,1],[0,1]],dtype='float32')
#predict         =2    ([0,1] 로 예상한건 틀린것1개 맞는것1개로 총 2개)
#real            =3 
#correct_predict =1    (real[0,1] 과 일치하는건 1개  
#precision  1/2  =0.5
#recall     1/3  =0.33
#F1score         =0.4

#print pr
#print lab
f1Score(pr,lab)
