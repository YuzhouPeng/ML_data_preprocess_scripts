# 导入所需要的库
import cv2
import numpy as np
  
# 定义保存图片函数
# image:要保存的图片名字
# addr；图片地址与相片名字的前部分
# num: 相片，名字的后缀。int 类型
def save_image(image,addr,num):
  address = addr + str(num)+ '.jpg'
  cv2.imwrite(address,image)
  
# 读取视频文件
videoCapture = cv2.VideoCapture("/home/pengyuzhou/workspace/yolov5/ca4336074669486170f3673eda4bfd67.mp4")
# 通过摄像头的方式
# videoCapture=cv2.VideoCapture(1)
  
#读帧
success, frame = videoCapture.read()
i = 0
timeF = 12
j=0
while success :
  i = i + 1
  if (i % timeF == 0):
    j = j + 1
    save_image(frame,'/home/pengyuzhou/workspace/VehicleInfo/test_vid',j)
    print('save image:',i)
  success, frame = videoCapture.read()
