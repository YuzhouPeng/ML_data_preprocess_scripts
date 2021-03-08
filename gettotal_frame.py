import cv2

video_full_path = "C:\\Users\\admin\\Desktop\\image1\\video.avi"
cap = cv2.VideoCapture(video_full_path)
print(cap.isOpened())
frame_count = 1
success = True
while (success):
    success, frame = cap.read()
    print('Read a new frame: ', success)

    params = []
    # params.append(cv.CV_IMWRITE_PXM_BINARY)
    params.append(1)
    if (frame_count%4)==0:
        cv2.imwrite("C:\\Users\\admin\\Desktop\\video_pics\\video" + "_%d.jpg" % frame_count, frame, params)
    frame_count = frame_count + 1
