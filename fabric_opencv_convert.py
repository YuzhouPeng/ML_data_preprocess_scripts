import numpy as np
import pywt
import cv2    
import os,time
import matplotlib.pyplot as plt

inputfolder = "/home/sycv/workplace/pengyuzhou/fabric_erode_and_dilate_output/"
outputfolder = "/home/sycv/workplace/pengyuzhou/fabric_new/"

def w2d(img,outputs,filename, mode='haar', level=1):
    #################################################
    #小波变换
    #################################################
    def wavelet_convert(img,filename,mode='haar',level=1):
        # img = cv2.imread(img)
        # #Datatype conversions
        # #convert to grayscale
        imArray = img
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
        print("wavelet cost time: {}".format(time2-time1))
        #Display result
        # print(imArray_H.size())
        # cv2.imshow('image',imArray_H)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # cv2.imwrite(outputs+"/wavelet_"+filename,np.hstack(img,imArray_H))
        return "/wavelet_"+filename,imArray_H
    #################################################
    #腐蚀和膨胀
    #################################################    
    def erodeanddilate(img,filename):
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
        # cv2.imwrite(outputs+"/eroded_"+filename,np.stack(img,eroded))
        # cv2.imwrite(outputs+"/dilated_"+filename,np.stack(img,dilated))
        return "/eroded_"+filename,eroded,"/dilated_"+filename,dilated
    #################################################
    #形态学边缘获取
    #################################################
    def morphology(img,filename):        
        # img = cv2.imread("D:/building.jpg",0);
        #构造一个3×3的结构元素 
        time1 = time.time()
        element = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
        dilate = cv2.dilate(img, element)
        erode = cv2.erode(img, element)

        #将两幅图像相减获得边，第一个参数是膨胀后的图像，第二个参数是腐蚀后的图像
        result = cv2.absdiff(dilate,erode)

        #上面得到的结果是灰度图，将其二值化以便更清楚的观察结果
        retval, result = cv2.threshold(result, 40, 255, cv2.THRESH_BINARY); 
        #反色，即对二值图每个像素取反
        result = cv2.bitwise_not(result); 
        time2 = time.time()
        print("morphology time cost {}".format(time2-time1))   
        #显示图像
        # cv2.imshow("result",result); 
        return "/morphology_"+filename,result

    #小波->膨胀腐蚀
    filename_w,image_w = wavelet_convert(img,filename,mode,level)
    filename_w_e,image_w_e,filename_w_d,image_w_d = erodeanddilate(image_w,filename_w)
    print(len(img))
    print(len(img[0]))
    print(len(image_w_e))
    print(len(image_w_e[0]))
    print(img)
    print(image_w_e)
    cv2.imwrite(outputs+"/w_e/"+filename_w_e,np.hstack((img,image_w_e)))
    cv2.imwrite(outputs+"/w_d/"+filename_w_d,np.hstack((img,image_w_d)))   
    #膨胀腐蚀-小波
    filename_e,image_e,filename_d,image_d = erodeanddilate(img,filename)
    filename_e_w,image_e_w = wavelet_convert(image_e,filename_e,mode,level)
    filename_d_w,image_d_w = wavelet_convert(image_d,filename_d,mode,level)
    cv2.imwrite(outputs+"/e_w/"+filename_e_w,np.hstack((img,image_e_w)))
    cv2.imwrite(outputs+"/d_w/"+filename_d_w,np.hstack((img,image_d_w)))
    #形态学-小波
    filename_m,image_m = morphology(img,filename)
    filename_m_w,image_m_w = wavelet_convert(image_m,filename_m,mode,level)
    cv2.imwrite(outputs+"/m_w/"+filename_m_w,np.hstack((img,image_m_w)))
    #小波-形态学
    filename_w,image_w = wavelet_convert(img,filename,mode,level)
    filename_m,image_m = morphology(image_w,filename_w)
    cv2.imwrite(outputs+"/w_m/"+filename_m,np.hstack((img,image_m)))

convertlist = ["/w_e/","/w_d/","/e_w/","/d_w/","/m_w/","/w_m/"]
tag = inputfolder.split('/')[-1]
# if not os.path.exists(outputfolder+tag):
#     os.mkdir(outputfolder+tag)
#     for e in convertlist:
#         if  os.path.exists(outputfolder+tag+e):
#             os.mkdir(outputfolder+tag+e)
for parent,_,files in os.walk(inputfolder):
    tag = parent.split('/')[-1]
    if len(tag)<11 and not os.path.exists(outputfolder+tag):
        os.mkdir(outputfolder+tag)
        for e in convertlist:
            if not os.path.exists(outputfolder+tag+e):
                os.mkdir(outputfolder+tag+e)
    for file in files:
        filepath = os.path.join(parent,file)
        outpath = os.path.join(outputfolder,tag)
        img = cv2.imread(filepath)
        w2d(img,outpath, file,'db1',10)


# w2d("/home/sycv/workplace/pengyuzhou/data_fabric_1024x1024_0909_rename_relabel/youzi/img_c4211a_26306299123_2.png",'db1',10)
