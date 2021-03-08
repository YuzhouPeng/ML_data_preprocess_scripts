from sklearn.cluster import DBSCAN
import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from center_crop_img_by_coord import center_crop
from center_draw import draw_imgs
inputpath = "/home/pengyuzhou/data_outputs/concat_outputs/"
clustercropoutput = "/home/pengyuzhou/data_outputs/05.09_dbscan_output/"
imgpath = "/home/pengyuzhou/data_outputs/05.08_multi/origin_large_img/multi.jpg"


# dbscan cluster points
def dbscan_cluster(filenames,channeldict0,channeldict1):
    for file in filenames:
        channel0 = channeldict0[file]
        channel1 = channeldict1[file]
        X = np.array(channel0)
        time1 = time.time()
        db = DBSCAN(eps=200, min_samples=2).fit(X) #DBSCAN聚类方法 还有参数，matric = ""距离计算方法
        time2 = time.time()
        print("dbscan cluster time: {}".format(time2-time1))
        labels = db.labels_
        print("label length {}".format(len(labels)))
        # print(set(labels))
        # Number of clusters in labels, ignoring noise if present. 
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0) 
        print("cluster numbers: {}".format(n_clusters_))
        clusters = [X[labels==i] for i in range(n_clusters_)]
        print("clusters {}".format((clusters)))
        print("cluster length: {}".format(len(clusters)))
        box_coords = []
        for coord in clusters:
            xmin,ymin,xmax,ymax = np.min(coord[:,1]),np.min(coord[:,0]), np.max(coord[:,1]),np.max(coord[:,0])
            box_coords.append([xmin,ymin,xmax,ymax])
        mean = [np.mean(X[labels==i],axis=0) for i in range(n_clusters_)]
        # print(clusters)
        raito = len(labels[labels[:] == -1]) / len(labels)  #计算噪声点个数占总数的比例
        # print(clusters)
        # print(mean)
        channelnames = ["ch1" for i in range(len(mean))]
        mean_distance = range(len(mean))
        paths = [imgpath for i in range(len(mean))]
        # print(channelnames)
        # print(mean_distance)
        # print(paths)
        # center_crop(paths,mean,"multi.jpg",clustercropoutput,mean_distance,channelnames)
        draw_imgs(imgpath,mean,"multi.jpg",clustercropoutput,4,box_coords)