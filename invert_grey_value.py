import cv2
im = cv2.imread("/home/sycv/workplace/pengyuzhou/el_webservice/algorithm/after_proc_algo/result5.jpg")
print(im.size)
# imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
# avg_gray = calculate_gray_value1(imgray)
# variable = -20
# ret,thresh = cv2.threshold(imgray,int(avg_gray)+variable,255,cv2.THRESH_BINARY)
thresh = cv2.bitwise_not(im)
cv2.imwrite("/home/sycv/workplace/pengyuzhou/el_webservice/algorithm/after_proc_algo/result6.jpg",thresh)