import cv2,time,os
import numpy as np
import matplotlib.pyplot as plt 
inputfolder = "/home/sycv/workplace/pengyuzhou/data_fabric_1024x1024_0909_rename_relabel/"
outputfolder = "/home/sycv/workplace/pengyuzhou/fabric_erode_and_dilate_output/"

def erodeanddilateimg(image,outputs,filename):
    img = cv2.imread(image,0)
    #OpenCV定义的结构元素
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
    
    #腐蚀图像
    time1 = time.time()
    eroded = cv2.erode(img,kernel)
    time2 = time.time()
    print("erode time cost {}".format(time2-time1))
    #显示腐蚀后的图像
    # cv2.imshow("Eroded Image",eroded)
    
    #膨胀图像
    time1 = time.time()
    dilated = cv2.dilate(img,kernel)
    time2 = time.time()
    print("erode time cost {}".format(time2-time1))    
    #显示膨胀后的图像
    # cv2.imshow("Dilated Image",dilated)
    #原图像
    # cv2.imshow("Origin", img)
    
    #NumPy定义的结构元素
    NpKernel = np.uint8(np.ones((3,3)))
    cv2.imwrite(outputs+"/eroded_"+filename,eroded)
    cv2.imwrite(outputs+"/dilated_"+filename,dilated)
    # plt.savefig(os.path.join(outputs,prefix+filename))


# tag = inputfolder.split('/')[-1]
# if not os.path.exists(outputfolder+tag):
#     os.mkdir(outputfolder+tag)
for parent,_,files in os.walk(inputfolder):
    tag = parent.split('/')[-1]
    if not os.path.exists(outputfolder+tag):
        os.mkdir(outputfolder+tag)
    for file in files:
        filepath = os.path.join(parent,file)
        outpath = os.path.join(outputfolder,tag)
        erodeanddilateimg(filepath,outpath, file)
