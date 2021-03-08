import cv2 as cv
import matplotlib

matplotlib.use('TkAgg')  # 大小写无所谓 tkaGg ,TkAgg 都行

import matplotlib.pyplot as plt

img = cv.imread("/home/sycv/workplace/pengyuzhou/el_webservice/algorithm/after_proc_algo/black_center_ring3.jpg",0)
hist = cv.calcHist([img],[0],None,[256],[0,256])
plt.subplot(121)
plt.imshow(img,'gray')
plt.xticks([])
plt.yticks([])
plt.title("Original")
plt.subplot(122)
plt.hist(img.ravel(),256,[0,256])
plt.show()