import cv2
import os
filepath = "C:\\Users\\admin\\Desktop\\image2\\"
filepath1 = "C:\\Users\\admin\\Desktop\\image1\\"
for parent,_,files in os.walk(filepath):
    for file in files:
        pic_path = os.path.join(parent,file)
        img = cv2.imread(pic_path)
        print(img)
        img = cv2.resize(img,(2560,1920))
        cv2.imwrite(filepath1+file,img)