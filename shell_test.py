# -*- coding: utf-8 -*-
import subprocess
import os

#pickle_file = sys.argv[1] #full picklefile path
#layer2_nodes =  sys.argv[2] #100 or 1024
#learning_rate_init= sys.argv[3] #0.5

#이 shell은 타겟파일에서 순서대로 피클네임, 노드수, 학습율 을 변수로 받고 결과를 pcrf 순으로 내보내는데 맞춰서 작성되었다. 

#folder = '/home/rbl/Documents/TensorFlow/insurance/pickle_files/' #실제 실행용
folder = '/home/rbl/Documents/TensorFlow/insurance/pickle_files_test/' #디버깅용으로 파일 2개만 넣어서 돌려봄
#변인수를 변수로 두는것은 총 개수를 동적으로 계산해 몇개중 몇번째것이 진행중인지 표시하기 위해서임.
n_node_var=2 # 노드 변인수. 변인을 이 값에 연동시켰으므로 변인수 바뀌면 다시 만들어야 함. 
n_Lrate_var=1 # 러닝레이트 변인수
n_test_per_var=4 # 한 조건세트당 몇번씩 수행
n_total_test = len(os.listdir(folder))*n_node_var*n_Lrate_var*n_test_per_var #총 횟수


def pcrfCollector(book):
#sin predict, sin correct predict, sin real, sin f1 score 부분을 텍스트에서 찾고 오른쪽의 값을 리턴한다
    targets =['\nsin predict : ','\nsin correct predict : ','\nsin real : ','\nsin F1 score : ','\n\npicklize finished']
    result =[] #위 targets 배열의 마지막은 stopper 로 실제 탐색에 사용되진 않지만 멈추는 위치 지정이다. 
    for i in range(0,len(targets)-1) : #마지막 배열은 ending point 라서 제거 
        start = book.find(targets[i])+len(targets[i])
        end = book.find(targets[i+1])
        result.append(float(book[start:end]))
    #print result
    return result


def where(h,i,j,k,imax=n_node_var,jmax=n_Lrate_var,kmax=n_test_per_var): 
#현재위치 셈. hmax는 필요가 없다
    position = (h*n_node_var*n_Lrate_var*n_test_per_var +
                    i*                 n_Lrate_var*n_test_per_var +
                    j*                                   n_test_per_var +
                    k+1                                                       ) #마지막 digit에는 +1 해줘야함.
    return position


test_result = [] #최종출력할 결과 


for h, filename in enumerate(os.listdir(folder)):
    pickle_file = os.path.join(folder,filename)
    for i in range(0,n_node_var):
        layer2_nodes = i*900+100
        for j in range(0,n_Lrate_var): #현재 learning_rate 는 0.5로 고정이니 1개라서 range(0,1) 
            learning_rate_init = 0.5
            for k in range(0,n_test_per_var): #같은 피클과 조건에 대해 몇번 반복할것인가 
                syscommand = 'python /home/rbl/Documents/TensorFlow/insurance/Insurance_model.py "'+pickle_file+'" '+str(layer2_nodes)+' '+str(learning_rate_init)
                #print '\n',syscommand
                get=subprocess.check_output(syscommand, shell=True)
                output = pcrfCollector(get)
                output.insert(0,learning_rate_init) #리턴값이 insert된 배열이 아니라.. 이거 실행만으로 insert 되는 함수임. 
                output.insert(0,layer2_nodes)
                output.insert(0,filename) #마지막에 0에 넣는게 가장 앞으로 오니까. 
                #print(h,i,j,k)
                print where(h,i,j,k), '/' ,n_total_test, output #현재 위치와 최대값 표시
                test_result.append(output) #이것도 재할당 안해도 자동 적용되는거. 
#output [피클명 , nodes , learningrate, predict, correct predict, real, f1score]


print '\n', test_result    #최종 출력배열 확인


