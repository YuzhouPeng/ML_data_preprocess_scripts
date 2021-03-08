import os,cv2,time
imgpath = "/home/pengyuzhou/data_outputs/05.08_multi/origin_large_img/"
output_crop_img_path = "/home/pengyuzhou/data_outputs/05.08_multi/multi_crop/"
crop_height = 992
crop_width = 992
resize_ratio = 992
cropwidthpixel = 128
cropheightpixel = 64
for parent,_,files in os.walk(imgpath):
    for file in files:
        if file[-3:]=="jpg":
            imgname = os.path.join(parent,file)
            img = cv2.imread(imgname)
            print(img)
            height,width,channel = img.shape
            img = img[cropheightpixel//2:height-cropheightpixel//2,cropwidthpixel//2:width-cropwidthpixel//2]
            height,width,channel = img.shape
            heightcount = int(height/crop_height) if height%crop_height==0 else int(height/crop_height)+1
            widthcount = int(width/crop_width) if width%crop_width==0 else int(width/crop_width)+1
            for h in range(heightcount):
                for w in range(widthcount):
                    time1 = time.time()
                    crop_img = img[h*crop_height:(h+1)*crop_height if h!=heightcount else height,w*crop_width:(w+1)*crop_width if w!=widthcount else width] 
                    # crop_img = cv2.resize(crop_img,(resize_ratio,resize_ratio))
                    time2 = time.time()
                    print("time cost = {}".format(time2-time1))
                    cv2.imwrite(output_crop_img_path+str(h)+"_"+str(w)+"_"+file,crop_img)
