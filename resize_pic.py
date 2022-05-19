import cv2
import os
filepath = "/home/pengyuzhou/workspace/safty_belt11/val/wear"
filepath1 = "/home/pengyuzhou/workspace/safty_belt11_resize_seg/val/wear"
for parent,_,files in os.walk(filepath):
    for file in files:
        pic_path = os.path.join(parent,file)
        img = cv2.imread(pic_path)
        # print(img)
        img = cv2.resize(img,(513,513))
        cv2.imwrite(filepath1+"/"+file,img)