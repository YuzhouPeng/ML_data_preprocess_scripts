import cv2
import os
filepath = "/home/pengyuzhou/workspace/fire_escape_imgs/night"
filepath1 = "/home/pengyuzhou/workspace/fire_escape_imgs/"
for parent,_,files in os.walk(filepath):
    for file in files:
        pic_path = os.path.join(parent,file)
        img = cv2.imread(pic_path)
        # print(img)
        img = cv2.resize(img,(1024,1024))
        cv2.imwrite(filepath1+"/"+file,img)