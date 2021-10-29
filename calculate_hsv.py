from cv2 import cv2
import numpy as np
img0 = cv2.imread('/home/pengyuzhou/workspace/ML_data_preprocess_scripts/123213.png')
hsv_img = cv2.cvtColor(img0, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(hsv_img) #这是OpenCV给出的范围

'''转换为计算公式给出的范围'''
H = h.astype(np.float)
S = s.astype(np.float)
V = v.astype(np.float)
print("h is {}, s is {}, v is {}".format(H,S,V))
