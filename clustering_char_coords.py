from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

inputpath = "/home/pengyuzhou/data_outputs/concat_outputs/"
clustercropoutput = "/home/pengyuzhou/data_outputs/05.06_kmean_test/"

def dbscan_cluster(filenames,channeldict0,channeldict1):
    for file in filenames:
        channel0 = channeldict0[file]
        channel1 = channeldict1[file]
        x = np.array(channel0)
        db = DBSCAN(eps=1.5, min_samples=3).fit(X) #DBSCAN聚类方法 还有参数，matric = ""距离计算方法
        clusters = [X[labels==i] for i in range(n_clusters_)]
        raito = len(labels[labels[:] == -1]) / len(labels)  #计算噪声点个数占总数的比例
        print('噪声比:', format(raito, '.2%'))


        print('分簇的数目: %d' % n_clusters_)
        print("轮廓系数: %0.3f" % metrics.silhouette_score(X, labels)) #轮廓系数评价聚类的好坏

        for i in range(n_clusters_):
            print('簇 ', i, '的所有样本:')
            one_cluster = X[labels == i]
            print(one_cluster)
            plt.plot(one_cluster[:,0],one_cluster[:,1],'o')
        plt.savefig("/home/pengyuzhou/data_outputs/cluster1.jpg")
        plt.show()
