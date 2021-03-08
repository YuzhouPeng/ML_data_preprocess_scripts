import numpy as np
import cv2
import matplotlib.pyplot as plt
########     四个不同的滤波器    #########
########     four different filters    #########
img = cv2.imread('/home/sycv/workplace/pengyuzhou/el_webservice/algorithm/after_proc_algo/black_center_ring1.jpg')

# 均值滤波
# mean filter
img_mean = cv2.blur(img, (5,5))
cv2.imwrite("result_mean.jpg",img_mean)

# 高斯滤波
# gaussian filter
img_Guassian = cv2.GaussianBlur(img,(15,15),0)
cv2.imwrite("result_gaussian.jpg",img_Guassian)

# 中值滤波
# median filter
img_median = cv2.medianBlur(img, 21)
cv2.imwrite("result_median.jpg",img_median)

# 双边滤波
# bilateral filter
img_bilater = cv2.bilateralFilter(img,9,75,75)

cv2.imwrite("result_biniliar.jpg",img_bilater)
# 展示不同的图片
# show different images
titles = ['srcImg','mean', 'Gaussian', 'median', 'bilateral']
imgs = [img, img_mean, img_Guassian, img_median, img_bilater]

for i in range(5):
    plt.subplot(2,3,i+1)
    #注意，这和matlab中类似，没有0，数组下标从1开始, index starts from 1 instead of 0
    plt.imshow(imgs[i])
    plt.title(titles[i])
plt.show()
fig2 = plt.figure()
fig2.savefig("f2.png")