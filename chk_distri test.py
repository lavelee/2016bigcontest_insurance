# -*- coding: utf-8 -*-
import numpy, pickle
pickle_name='cucntt_cuclaim_null_randomfix.pickle' 

def pickleread(pickle_name):
    with open(pickle_name,'rb') as f:
        data=pickle.load(f)
        return data


def chkDistri(data, divide=10): #기본 값구간 10개로 나눔.  [총평균,총개수, 구간1평균,구간1개수, 구간2평균,구간2개수 ... ]
    data=numpy.array(data,dtype='float32')
    print data.shape, 'will be divided into ',divide,' sections. ',1./divide,' for each sectins   *total: -0.5~ +0.5)'
    print 'A warning    \'RuntimeWarning: Mean of empty slice\'    can appear if there is no data in specific section. \n but that\'s OK'
    distri=numpy.zeros((data.shape[1],2*(divide+1))) #컬럼수,쪼갬수(평균,개수 2개씩이라 *2, 총평균/개수 포함이라 +1)

    for n_col in range(0,data.shape[1]): #컬럼별.
        #print(data[:,col])
        
        data_col= numpy.sort(data[:,n_col]) #구간별로 쪼개기위해 커지는 순서로 정렬. ascending order
        indicator = numpy.array([(slit+1)*1./divide-0.5 for slit in range(0,divide)],dtype='float32') #dtype 안맞추면 이상하게 비교함. 

        for div_step in range(0,2): #평균을 divide 개로 나누는데 처음 한번은 전체평균과 개수를 넣고 두번째는 구간평균과 개수 넣으려 함. 
            if div_step == 0 : #처음 3개는 전체평균, 전체개수, 조각개수를 구하고
                distri[n_col,div_step]=numpy.average(data_col) #전체 평균
                distri[n_col,div_step+1]=data_col.shape[0] #전체 개수

            else: #첫번째가 아니면 -0.5~+0.5를 지정개수대로 쪼갠뒤 구간별 평균과 개수를 만든다.
                index_array=numpy.searchsorted(data_col,indicator,side='right') #sort 된 컬럼에서 indecator 값들이 몇번째에 있는지 배열로 나타냄

                item_prev=0
                for i, item in enumerate(index_array): #인덱스번호를 index_array 로 한방에 만드는바람에 위치지정이 꼬였음. 
                    #print i,item, div_step
                    distri[n_col,2*(i+1)]= numpy.average(data_col[item_prev:item]) #구간별 평균을 삽입
                    distri[n_col,2*(i+1)+1]= item - item_prev #구간별 개수를 삽입
                    item_prev = item #현재값 저장
                    
    print distri[1] #잘나왔나 한줄 집어서 확인
    return distri

data=pickleread(pickle_name)
cntt=data['train_cucntt_data']
claim=data['train_cuclaim_data' ]
#print cntt.shape, claim.shape
#print cntt[0]

train_cucntt_distri = chkDistri(cntt)
#train_cuclaim_distri = chkDistri(claim)
