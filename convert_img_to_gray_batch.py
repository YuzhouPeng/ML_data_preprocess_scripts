import cv2
import os
from PIL import Image

outputpath = '/home/pengyuzhou/workspace/gongpai_val'
path = '/home/pengyuzhou/workspace/gongpai_val'
for parent,_,files in os.walk(path):
    for file in files:
        print("filename is {}".format(file))
        filepath = os.path.join(parent,file)
        filename = file[:-3]+'jpg'
        # print(filename)
        img = cv2.imread(filepath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(filepath,gray)
