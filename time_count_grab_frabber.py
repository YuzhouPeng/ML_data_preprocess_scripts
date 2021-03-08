videoFile = "C:\\Users\\admin\\Desktop\\FiberFault.mp4"
imagesFolder = "C:\\Users\\admin\\Desktop\\video_pics\\"
import cv2

vidcap = cv2.VideoCapture('C:\\Users\\admin\\image1\\video.avi')
count = 0
success = True
fps = int(vidcap.get(cv2.CAP_PROP_FPS))
# fps = 1
while success:
    success,image = vidcap.read()
    print('read a new frame:',success)
    if count%(4*fps) == 0 :
         cv2.imwrite("C:\\Users\\admin\\Desktop\\video_pics\\"+'{}.jpg'.format(count),image)
         print('successfully written 4th frame')
    count+=1