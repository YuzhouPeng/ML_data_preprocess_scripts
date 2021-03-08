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

coord
def k_mean_distance(data, cx, cy, i_centroid, cluster_labels):
    # Calculate Euclidean distance for each data point assigned to centroid 
    distances = [np.sqrt((int(x)-cx)**2+(int(y)-cy)**2) for (x, y) in data[cluster_labels == i_centroid]]
    # return the mean value
    return np.mean(distances)


def drawimg(filename,imgpath,xmin,ymin,xmax,ymax,x,y):
    print("start print")

    img = Image.open(imgpath).convert('RGB')
    # print(filename)
    draw = ImageDraw.Draw(img)
    draw.point((x,y), (255, 0, 0))
    draw.rectangle([(int(xmin), int(ymin)), (int(xmax), int(ymax))],outline ="red",width = 20)
    draw.rectangle([(int(x-100), int(y-100)), (int(x+100), int(y+100))],fill ="red")

        # save in new file
    img.save(outputpath+"draw_"+filename+".jpg")


inputpath = "/home/pengyuzhou/data_outputs/concat_outputs/"
clustercropoutput = "/home/pengyuzhou/data_outputs/04.30_cluster_crop_output/"
if __name__=='__main__':

    for parent,_,files in os.walk(inputpath):
        for file in files:
            if file[-3:]=="npy":
                npypath = os.path.join(parent,file)
                X = np.load(npypath)
                print(X.shape)
                data = []
                time1 = time.time()
                for y in range(X.shape[0]):
                    for x in range(X.shape[1]):
                        if X[y,x]!=0:
                            data.append([y,x])
                X = np.array(data)
                time2 = time.time()
                print("get coord cost time: {}".format(time2-time1))
                time1 = time.time()
                time1 = time.time()
                kmeans = KMeans(n_clusters=1)
                data = kmeans.fit_transform(X)
                kmeans = kmeans.fit(X)
                centroids = kmeans.cluster_centers_
                cluster_labels = kmeans.labels_
                time2 = time.time()
                # data = 
                # print(data)
                cy,cx = int(centroids[0][0]),int(centroids[0][1])
                mean_distance = int(np.mean(data))*5


                print("k_mean cluster time: {}".format(time2-time1))
                newname = file.split("_")[0]+"_"+file.split("_")[1]
                imgpath = "/home/pengyuzhou/data_croped/04.30.test_output/crop_edge_"+newname+"_.jpg"
                print(imgpath)
                # imgpath = "/home/pengyuzhou/data_outputs/ori1.jpg"
                filename = newname
                # centroids = [[4096, 11972], [4521, 1547], [4353, 11970]]
                print(centroids)
                center_crop(imgpath,centroids,file,clustercropoutput,mean_distance)

 