import cv2
import os

path = '/opt/DataDisk2/pyz/_datasets/playcellphone_rtsp_imgs_output_crop/exp2/crops/person/'
for parent,_,files in os.walk(path):
    for file in files:
        filepath = os.path.join(parent,file)
        img = cv2.imread(filepath)
        size = img.shape

        w = size[1] #宽度

        h = size[0] #高度
        if (w<=100 and h<=100 or w/h<=0.3 or h/w<=0.3):

            os.remove(os.path.join(parent, file))