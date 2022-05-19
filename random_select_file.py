import random
import os
from shutil import copyfile

path= "/home/pengyuzhou/workspace/yolov5_22_1_12/yolov5/runs/detect/exp7/crops/person/"
outputpath = "/home/pengyuzhou/workspace/person_phone_3_12_selected/"
imgs = []

for parent,_,files in os.walk(path):
# for x in os.listdir(path):
    for file in files:
        if file.endswith('jpg'):
            imgs.append(file)
    # print(x)
    # if x.endswith('jpg'):
	#     imgs.append(x)
print(len(imgs))

selected_imgs = []
for i in range(0,len(imgs),10):
    selected_imgs.append(imgs[i])
# selected_imgs=random.sample(imgs,k = 2006)
print(selected_imgs)


for img in selected_imgs:
    src=os.path.join(path,img)
    dst=os.path.join(outputpath,img)    
    copyfile(src,dst)
print("copy done")