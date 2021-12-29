import cv2
import numpy 
from PIL import Image
img = cv2.imread("/home/pengyuzhou/workspace/chip_imgs/anormal_1.jpg")
Pheight, Pwidth, Pdepth = img.shape
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_test1 = cv2.resize(img, (10, 10),interpolation=cv2.INTER_NEAREST_EXACT)
print(img_test1)
print("pillow pillow pillow")
img1 = Image.open('/home/pengyuzhou/workspace/chip_imgs/anormal_1.jpg')
img1 = img1.resize((10, 10),Image.NEAREST)
data = numpy.asarray(img1)

print(data)