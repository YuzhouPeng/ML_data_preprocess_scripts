import cv2
import os
filepath = "/home/pengyuzhou/workspace/fire_path_cutout_1/occupy"
filepath1 = "/home/pengyuzhou/workspace/fire_path_resize/occupy"
for parent,_,files in os.walk(filepath):
    for file in files:
        pic_path = os.path.join(parent,file)
        img = cv2.imread(pic_path)
        # print(img)
        img = cv2.resize(img,(256,256))
        cv2.imwrite(filepath1+"/"+file,img)