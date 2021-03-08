import cv2
import os
import numpy as np
def cv_imread(file_path = ""):
    cv_img = cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
    return cv_img



image_folder = 'C:\\Users\\admin\\Desktop\\TOVIDEO\\'

video_name = 'video.avi'
each_image_duration = 4 # in secs
fourcc = cv2.VideoWriter_fourcc(*'XVID') # define the video codec
images = []

for parent,_,files in os.walk(image_folder):
    for file in files:
        images.append(file)
print(len(images))
frame = cv_imread(os.path.join(image_folder, images[0]))
print(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(image_folder+video_name, fourcc, 1.0, (width, height))

for image in images:
    for _ in range(each_image_duration):
        frame = cv_imread(os.path.join(image_folder, image))
        video.write(frame)

cv2.destroyAllWindows()
video.release()