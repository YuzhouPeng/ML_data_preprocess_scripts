#coding:utf-8
import os
import cv2
import numpy as np
 
def add_mask2image_binary(images_path, masks_path, masked_path):
# Add binary masks to images
  for img_item in os.listdir(images_path):
    print(img_item)
    img_path = os.path.join(images_path, img_item)
    img = cv2.imread(img_path)
    if img is not None:
      mask_path = os.path.join(masks_path, img_item[:-4]+'.png') # mask是.png格式的，image是.jpg格式的

      mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE) # 将彩色mask以二值图像形式读取
      # mask = mask.astype('uint')
      # img = img.astype('uint')
      # print(img.size)
      width = mask.shape[1]
      height = mask.shape[0]
      img = cv2.resize(img,(width,height))
      # print(mask.size)
      # mask = np.uint8(mask)

      print("start add")
      # mask = np.zeros(mask.shape[0:2], dtype='uint8')
      masked = cv2.add(img, np.zeros(np.shape(img), dtype=np.uint8), mask=mask)
      #  将image的相素值和mask像素值相加得到结果
      cv2.imwrite(os.path.join(masked_path, img_item), masked)
images_path = '/home/pengyuzhou/workspace/fire_path_origin/occupied'
masks_path = '/home/pengyuzhou/workspace/fire_path_mask/occupy_filter_res'
masked_path = '/home/pengyuzhou/workspace/fire_path_cutout/occupy'
add_mask2image_binary(images_path, masks_path, masked_path)
