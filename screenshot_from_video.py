
import cv2
import os

image_folder = '/opt/DataDisk2/pyz/APY181231016_1003人驾驶员行为采集数据/seated_output'
path = '/opt/DataDisk2/pyz/APY181231016_1003人驾驶员行为采集数据/data' # 这里处理一个文件夹中的视频
# for vid in os.listdir(path):
for parent,_,files in os.walk(path):
    print(parent)
    for vid in files:
        video_name = os.path.join(parent,vid)
        prefix = video_name.split("/")[-4]
        # video_name = path + vid
        save_folder = image_folder
        if 'call_noglasses' in video_name or 'drinking_noglasses' in video_name or 'nosteering_noglasses' in video_name or 'smoking_noglasses' in video_name:
            capture = cv2.VideoCapture(video_name)  # 打开视频
        
            idx = 1
            
            if capture.isOpened():
                while True:
                    ret, prev = capture.read()  # ret是布尔值，如果读取帧是正确的则返回True，如果文件读取到结尾，返回值就为False。frame就是每一帧的图像
                    if ret == True:
                        # cv2.imshow('video', prev)
                        idx += 1
                        # if idx%80==0:
                        if idx==80:
                            cv2.imwrite(save_folder+'/%s_%0.7d.jpg'%(prefix+'_'+vid, idx), prev)
                            print("img output: %d"%idx)
                    else:
                        break
                    # if cv2.waitKey(20) == 27:
                    #     break

