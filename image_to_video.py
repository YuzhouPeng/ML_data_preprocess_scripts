# import cv2
# import os

# image_folder = '/home/pengyuzhou/workspace/ML_data_preprocess_scripts/tempframe/'
# video_name = '/home/pengyuzhou/workspace/ML_data_preprocess_scripts/outputvid/test1.avi'

# images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
# frame = cv2.imread(os.path.join(image_folder, images[0]))
# height, width, layers = frame.shape

# video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc('M','J','P','G'), 10, (width,height))

# for image in images:
#     video.write(cv2.imread(os.path.join(image_folder, image)))

# cv2.destroyAllWindows()
# video.release()


import cv2
import numpy as np
import glob



frames = []
for filename in glob.glob('/home/pengyuzhou/workspace/ML_data_preprocess_scripts/tempframe/*.jpg'):
    frames.append(filename)
image = cv2.imread(frames[0])

size = image.shape

w = size[1] #宽度

h = size[0] #高度
frameSize = (w, h)
out = cv2.VideoWriter('/home/pengyuzhou/workspace/ML_data_preprocess_scripts/outputvid/test6_mobilenetv3_output.avi',cv2.VideoWriter_fourcc(*'DIVX'), 30, frameSize)

frames = sorted(frames,key = lambda x: int(x.split('/')[-1].split('.')[0]) )
# print(frames)
for f in frames:
    img = cv2.imread(f)
    out.write(img)

out.release()


# import cv2
# import numpy as np
# import glob

# frameSize = (500, 500)

# out = cv2.VideoWriter('/home/pengyuzhou/workspace/ML_data_preprocess_scripts/outputvid/test1.avi',cv2.VideoWriter_fourcc(*'DIVX'), 30, frameSize)

# for filename in glob.glob('/home/pengyuzhou/workspace/ML_data_preprocess_scripts/tempframe/*.jpg'):
#     img = cv2.imread(filename)
#     out.write(img)

# out.release()
