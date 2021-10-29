import cv2,os
import numpy as np

## Read
outputpath = "/home/pengyuzhou/workspace/fire_path_data/not_occupy_filter_res"
for parent,_,files in os.walk("/home/pengyuzhou/workspace/fire_path_data/not_occupied_output"):
    for file in files:
        imgpath = os.path.join(parent,file)
        img = cv2.imread(imgpath)
        print(file)
        ## convert to hsv
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        ## mask of green (36,25,25) ~ (86, 255,255)
        # mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
        mask = cv2.inRange(hsv, (150, 128, 128), (151, 129,129))

        ## slice the green
        imask = mask>0
        green = np.zeros_like(img, np.uint8)
        green[imask] = img[imask]

        outputres = os.path.join(outputpath,file)
        ## save 
        cv2.imwrite(outputres, green)