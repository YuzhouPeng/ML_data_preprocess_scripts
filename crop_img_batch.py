import cv2
import os
from PIL import Image

path = '/opt/DataDisk2/pyz/APY181231016_1003人驾驶员行为采集数据/no_seatbelt_output/'
outputpath = '/opt/DataDisk2/pyz/APY181231016_1003人驾驶员行为采集数据/no_seatbelt_crop_output/'
for parent,_,files in os.walk(path):
    for file in files:
        print("filename is {}".format(file))
        filepath = os.path.join(parent,file)
        filename = file[:-3]+'jpg'
        # print(filename)
        img = Image.open(filepath)
        print(img.size)
        cropped = img.crop((640, 0, 1280, 480))  # (left, upper, right, lower)
        cropped.save(os.path.join(outputpath,filename))
