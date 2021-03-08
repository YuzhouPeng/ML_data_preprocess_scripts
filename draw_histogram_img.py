import cv2
import numpy as np
from matplotlib import pyplot as plt
 
img = cv2.imread('/home/sycv/workplace/pengyuzhou/el_webservice/algorithm/after_proc_algo/black_center_ring.jpg',0)
plt.hist(img.ravel(),256,[0,256])
plt.savefig("/home/sycv/workplace/pengyuzhou/el_webservice/algorithm/after_proc_algo/hist_result.jpg")
plt.show()