import numpy as np
import os,re,cv2,time
numpypath = "/home/dev_shared/04.30_mask_predictions/"
outputpath = "/home/pengyuzhou/data_outputs/concat_outputs/"
savefiles = []
iheight = 8
iwidth = 16
rows = []
index = []
channel0 = {}
channel1 = {}

def readfiles():
    global savefiles
    time1 = time.time()
    for parent,_,files in os.walk(numpypath):
        for file in files:
            if file[-3:]=="npy":
                filename = file.split("_")[4]+"_"+file.split("_")[5]
                channel0[filename] = np.zeros((992*iheight,992*iwidth))
                channel1[filename] = np.zeros((992*iheight,992*iwidth))
                savefiles.append(file)
                
    for i in range(len(savefiles)):
        ele = savefiles[i].split("_")
        indexh,indexw = int(ele[0]),int(ele[1])
        filename = ele[4]+"_"+ele[5]
        filearray0 = np.load(numpypath+savefiles[i])[:,:,0]*255
        filearray1 = np.load(numpypath+savefiles[i])[:,:,1]*255
        channel0[filename][992*indexh:992*(indexh+1),992*indexw:992*(indexw+1)] = filearray0
        channel1[filename][992*indexh:992*(indexh+1),992*indexw:992*(indexw+1)] = filearray1
    time2 = time.time()
    for key in channel0.keys():
        np.save(outputpath+key+"_ch0.npy",channel0[key])
        cv2.imwrite(outputpath+key+"_ch0.jpg",channel0[key])

    for key in channel1.keys():
        np.save(outputpath+key+"_ch1.npy",channel1[key])
        cv2.imwrite(outputpath+key+"_ch1.jpg",channel1[key])

    print("cost time = {}".format(time2-time1))



imgarrays =  readfiles()

