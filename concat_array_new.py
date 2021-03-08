import numpy as np
import os,re,cv2,time
from cluster_kmeans_new import cluster_kmean
from cluster_dbscan import dbscan_cluster
numpypath = "/home/dev_shared/0508_new_crop_segment_results/"
outputpath = "/home/pengyuzhou/data_outputs/concat_outputs/"
savefiles = []
iheight = 8
iwidth = 16
rows = []
index = []
channel0_x = {}
channel0_y = {}
channel1_x = {}
channel1_y = {}
channel0_coord = {}
channel1_coord = {}
crop_size = 992
namekey = {}
def readfiles():
    global savefiles
    time1 = time.time()
    for parent,_,files in os.walk(numpypath):
        for file in files:
            if file[-3:]=="npy":
                filename = file.split("_")[2]
                # channel0[filename] = np.zeros((992*iheight,992*iwidth))
                # channel1[filename] = np.zeros((992*iheight,992*iwidth))
                savefiles.append(file)
    print(len(savefiles))

    for i in range(len(savefiles)):
        ele = savefiles[i].split("_")
        filename = ele[2]
        indexh,indexw = int(ele[0]),int(ele[1])
        filearray0 = np.load(numpypath+savefiles[i])[:,:,0]
        filearray0 = filearray0.reshape((992,992))
        # print(filearray0)
        coord0 = np.where(filearray0 == 1)
        filearray1 = np.load(numpypath+savefiles[i])[:,:,1]
        filearray1 = filearray1.reshape((992,992))
        coord1 = np.where(filearray1 == 1)
        # print(filearray1.size)
        # print(coord0)

        new_coord0_0 = np.asarray(coord0[0])
        new_coord0_1 = np.asarray(coord0[1])
        # print(new_coord0_0)
        # print(new_coord0_1)
        new_coord0_0 = new_coord0_0+crop_size*indexh
        new_coord0_1 = new_coord0_1+crop_size*indexw
        # print(new_coord0_0)
        # print(new_coord0_1)
        new_coord1_0 = np.asarray(coord1[0])
        new_coord1_1 = np.asarray(coord1[1])
        new_coord1_0 = new_coord1_0+crop_size*indexh
        new_coord1_1 = new_coord1_1+crop_size*indexw
        if (len(new_coord0_0)>0 and len(new_coord0_1)>0):
            if filename not in namekey.keys():
                namekey[filename]=1
        # if coord1[0].size!=0 and coord1[1].size!=0:
            if filename not in channel0_x.keys():
                channel0_x[filename] = new_coord0_0
            elif filename in channel0_x.keys():
                channel0_x[filename] = np.append(channel0_x[filename],new_coord0_0)
            if filename not in channel0_y.keys():
                channel0_y[filename] = new_coord0_1
            elif filename in channel0_y.keys():
                channel0_y[filename] = np.append(channel0_y[filename],new_coord0_1)       
        if (len(new_coord1_0)>0 and len(new_coord1_1)>0):
            if filename not in namekey.keys():
                namekey[filename]=1
            if filename not in channel1_x.keys():
                channel1_x[filename] = new_coord1_0
            elif filename in channel1_x.keys():
                channel1_x[filename] = np.append(channel1_x[filename],new_coord1_0)
            if filename not in channel1_y.keys():
                channel1_y[filename] = new_coord1_1
            elif filename in channel1_y.keys():
                channel1_y[filename] = np.append(channel1_y[filename],new_coord1_1)
    # print(channel0_x)
    # print(len(channel0_x))
    # print(len(channel0_y))
    # for key in channel0_x.keys():
    #     print(channel0_x[key].shape)``
    # for key in channel0_y.keys():
    #     print(channel0_y[key].shape)
    # print(channel1_y)
    for ele in namekey.keys():
        if ele in channel0_x.keys() and ele in channel0_y.keys():
            # x = channel0_x[ele].shape[0]
            channel0_coord[ele] = np.stack((channel0_x[ele],channel0_y[ele]),axis=1)
            pointnum,_ = channel0_coord[ele].shape
            idx = np.random.choice(range(pointnum),size = pointnum//1000)
            channel0_coord[ele] = channel0_coord[ele][idx,:]
            print(channel0_coord[ele].shape)
        if ele in channel1_x.keys() and ele in channel1_y.keys():
            channel1_coord[ele] = np.stack((channel1_x[ele],channel1_y[ele]),axis=1)
            pointnum,_ = channel1_coord[ele].shape
            idx = np.random.choice(range(pointnum),size = pointnum//100)
            channel1_coord[ele] = channel1_coord[ele][idx,:]
            print(channel1_coord[ele].shape)
    filenames = namekey.keys()
    # print(channel0_coord)
    # print(channel1_coord)
    time2 = time.time()
    print("cost time = {}".format(time2-time1))
    # cluster_kmean(filenames,channel0_coord,channel1_coord)
    dbscan_cluster(filenames,channel0_coord,channel1_coord)
# test = np.load(numpypath+"1_0_1.npy")
# print(test.shape)
# print(test)

imgarrays =  readfiles()

