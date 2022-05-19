import cv2
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
  
cap = cv2.VideoCapture('/home/pengyuzhou/workspace/ML_data_preprocess_scripts/tempvideo/test1.mp4')
device = torch.device("cpu")

count = 0
net = torch.load('/home/pengyuzhou/workspace/pytorch-train/safety_belt9_Lpreprocess_dataaug_torch1.4_optim_48_resnet50_opencv4.5_epoch_150.pt')
pred_res = []
net = net.to(device)#同样用GPU
torch.no_grad()
while(True):
      
    # Capture frames in the video
    ret, frame = cap.read()
    # describe the type of font
    # to be used.
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Use putText() method for
    # inserting text on video
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    cv2.resize(img, (299,299))

    img = torchvision.transforms.ToTensor()(img)
    image = img.unsqueeze(0)
    #由于训练的时候还有一个参数，是batch_size,而推理的时候没有，所以我们为了保持维度统一，就得使用.unsqueeze(0)来拓展维度
    
    time1 = time.time()
    image = image.to(device)

    #同样将图片数据放入cuda(GPU)中
    output = net(image)
    # print(output)
    _, pre = torch.max(output, 1)
    if (int(pre))==2:
        cv2.putText(frame, 
                    '<label: '+str(int(pre))+'wear_safetybelt>', 
                    (800, 100), 
                    font, 1, 
                    (255, 0, 0), 
                    2, 
                    cv2.LINE_4)
    else (int(pre))==1:
        cv2.putText(frame, 
                    'label: '+str(int(pre))+'not_wear_safetybelt>', 
                    (800, 100), 
                    font, 1, 
                    (255, 0, 0), 
                    2, 
                    cv2.LINE_4)
    else:
        cv2.putText(frame, 
                    'label: '+str(int(pre)), 
                    (800, 100), 
                    font, 1, 
                    (255, 0, 0), 
                    2, 
                    cv2.LINE_4)      
    # Display the resulting frame
    # cv2.imshow('video', frame)
    cv2.imwrite("/home/pengyuzhou/workspace/ML_data_preprocess_scripts/tempframe/"+str(count)+'.jpg',frame)
    # creating 'q' as the quit 
    # button for the video
    count+=1
    print(count)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
  
# release the cap object
cap.release()
# close all windows
cv2.destroyAllWindows()