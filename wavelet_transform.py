import numpy as np
import pywt
import cv2    
import os,time
import matplotlib.pyplot as plt

inputfolder = "/home/sycv/workplace/pengyuzhou/fabric_erode_and_dilate_output/"
outputfolder = "/home/sycv/workplace/pengyuzhou/fabric_wavelet_trans_output/"

def w2d(img,outputs,filename, mode='haar', level=1):
    imArray = cv2.imread(img)
    #Datatype conversions
    #convert to grayscale
    imArray = cv2.cvtColor( imArray,cv2.COLOR_RGB2GRAY )
    #convert to float
    time1 = time.time()
    imArray =  np.float32(imArray)   
    imArray /= 255
    # compute coefficients 
    coeffs=pywt.wavedec2(imArray, mode, level=level)

    #Process Coefficients
    coeffs_H=list(coeffs)  
    coeffs_H[0] *= 0;  

    # reconstruction
    imArray_H=pywt.waverec2(coeffs_H, mode)
    imArray_H *= 255
    imArray_H =  np.uint8(imArray_H)
    time2 = time.time()
    print("cost time: {}".format(time2-time1))
    #Display result
    plt.imshow(imArray_H,cmap='gray')
    plt.show()
    # cv2.imshow('image',imArray_H)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    plt.savefig(os.path.join(outputs,filename))

tag = inputfolder.split('/')[-1]
if not os.path.exists(outputfolder+tag):
    os.mkdir(outputfolder+tag)
for parent,_,files in os.walk(inputfolder):
    # tag = parent.split('/')[-1]
    # if not os.path.exists(outputfolder+tag):
    #     os.mkdir(outputfolder+tag)
    for file in files:
        filepath = os.path.join(parent,file)
        outpath = os.path.join(outputfolder,tag)
        w2d(filepath,outpath, file,'db1',10)


# w2d("/home/sycv/workplace/pengyuzhou/data_fabric_1024x1024_0909_rename_relabel/youzi/img_c4211a_26306299123_2.png",'db1',10)
