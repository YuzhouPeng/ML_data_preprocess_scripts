import cv2

cap = cv2.VideoCapture("rtsp://admin:Boe888888@10.141.17.181:554/h264/ch1/main/av_stream")
ret,frame = cap.read()
save_folder = '/home/pengyuzhou/workspace/playcellphone_rtsp_imgs'
idx = 1
while ret:
    ret,frame = cap.read()
    if ret == True:
        # cv2.imshow('video', prev)
        idx += 1
        # if idx%80==0:
        if idx%15==0:
            cv2.imwrite(save_folder+'/%s_%0.7d.jpg'%("playcellphone_rtsp_", idx), frame)
            print("img output: %d"%idx)