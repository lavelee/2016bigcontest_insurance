#import tensorflow as tf
import numpy as np
filename='trained_w12b12_cucntt'
with open(filename,"rb") as f :
    print(f)
    data=np.fromfile(f)
print(data)
print(data.shape)
