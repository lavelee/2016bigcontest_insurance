# -*- coding: utf-8 -*-
import subprocess

#pickle_file = sys.argv[1] #full picklefile path
#layer2_nodes =  sys.argv[2] #100 or 1024
#learning_rate_init= sys.argv[3] #0.5

pickle_file = '/home/rbl/Documents/TensorFlow/insurance/pickle_files/cucntt_cuclaim_null_randomfix.pickle'
layer2_nodes = str(100)
learning_rate_init = str(0.5)

syscommand = 'python /home/rbl/Documents/TensorFlow/insurance/Insurance_model.py '+pickle_file+' '+layer2_nodes+' '+learning_rate_init
#print '\n',syscommand

k=subprocess.check_output(syscommand, shell=True)
print '\n', k     #출력값을 변수로 받아올 수 있음

