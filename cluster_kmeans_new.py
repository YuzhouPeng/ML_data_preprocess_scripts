import numpy as np
import time,os
import matplotlib.pyplot as plt
import glog as log
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN  # 进行DBSCAN聚类
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score ,calinski_harabasz_score,davies_bouldin_score # 计算 轮廓系数，CH 指标，DBI 
from center_crop_img_by_coord import center_crop
from PIL import Image,ImageDraw,ImageFont

inputpath = "/home/pengyuzhou/data_outputs/concat_outputs/"
clustercropoutput = "/home/pengyuzhou/data_outputs/05.06_kmean_test/"
def cluster_kmean(filenames,channeldict0,channeldict1):
    for file in filenames:
        result = []
        channelnames = []
        mean_distance = []
        img_paths = []
        channel0 = channeldict0[file]
        channel1 = channeldict1[file]
        
        X = np.array(channel0)

        time1 = time.time()
        kmeans = KMeans(n_clusters=1)
        data = kmeans.fit_transform(X)
        kmeans = kmeans.fit(X)
        centroids = kmeans.cluster_centers_
        cluster_labels = kmeans.labels_
        time2 = time.time()
        # data = 
        # print(data)
        mean_distance.append(int(np.mean(data))*5)
        print("k_mean cluster time: {}".format(time2-time1))
        newname = file
        imgpath = "/home/pengyuzhou/data_croped/04.30.test_output/crop_edge_"+newname+"_.jpg"
        print(imgpath)
        img_paths.append(imgpath)
        # imgpath = "/home/pengyuzhou/data_outputs/ori1.jpg"
        filename = newname
        # centroids = [[4096, 11972], [4521, 1547], [4353, 11970]]
        print(centroids)
        result.append(centroids[0])
        channelnames.append("ch0")

        X = np.array(channel1)
        print("get coord cost time: {}".format(time2-time1))
        time1 = time.time()
        kmeans = KMeans(n_clusters=1)
        data = kmeans.fit_transform(X)
        kmeans = kmeans.fit(X)
        centroids = kmeans.cluster_centers_
        cluster_labels = kmeans.labels_
        time2 = time.time()
        # data = 
        # print(data)
        mean_distance.append(int(np.mean(data))*5)
        print("k_mean cluster time: {}".format(time2-time1))
        newname = file
        imgpath = "/home/pengyuzhou/data_croped/04.30.test_output/crop_edge_"+newname+"_.jpg"
        img_paths.append(imgpath)
        # imgpath = "/home/pengyuzhou/data_outputs/ori1.jpg"
        filename = newname
        # centroids = [[4096, 11972], [4521, 1547], [4353, 11970]]
        print(centroids)
        result.append(centroids[0])
        channelnames.append("ch1")

        center_crop(img_paths,result,file,clustercropoutput,mean_distance,channelnames)

 