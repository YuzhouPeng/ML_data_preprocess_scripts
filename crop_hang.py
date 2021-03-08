import numpy as np
import glob
import os
from PIL import Image

coordlist = []
s = 0
def cut_text_line(geo, scale_ratio_w, scale_ratio_h, im_array, img_path, img_name):
    global s
    geo /= [scale_ratio_w, scale_ratio_h]
    p_min = np.amin(geo, axis=0)
    p_max = np.amax(geo, axis=0)
    min_xy = p_min.astype(int)
    max_xy = p_max.astype(int) + 2
    # print(img_name)
    if min_xy[0]<0:
        min_xy[0]=0
    if min_xy[1]<0:
        min_xy[1]=0
    if max_xy[0]<0:
        max_xy[0]=0
    if max_xy[1]<0:
        max_xy[1]=0
    if min_xy[0]>=0 and min_xy[1]>=0 and max_xy[0]>=0 and max_xy[1]>=0:
        sub_im = im_array.crop((min_xy[0], min_xy[1], max_xy[0], max_xy[1]))
        string = img_name + '_subim'+str(s)+".jpg "+str(min_xy[0])+" "+str(min_xy[1])+" "+str(max_xy[0])+" "+str(max_xy[1])
        coordlist.append(string)
        sub_im.save(os.path.join(img_path, img_name + '_subim%d.jpg' % s))

data_path = "/home/pengyuzhou/data_outputs/05.06_cluster_crop_output_data/"
outputpath = "/home/pengyuzhou/data_outputs/"
txt_paths = glob.glob(os.path.join(data_path, "*.txt"))
img_path = "/home/pengyuzhou/data_outputs/05.06_cluster_crop_out/"
# print(txt_paths)
for txt_path in txt_paths:
    img_path_origin = txt_path.replace("txt", "jpg")
    img_name = os.path.basename(img_path_origin)[:-4]
    im_array = Image.open(img_path_origin)
    # print(img_path_origin)
    f = open(txt_path,"r")
    if os.path.exists(img_path_origin):
        line = f.readlines()
        line = [l.strip() for l in line]
        for l in line:
            anno_colums = l.split(',')
            anno_array = np.array(anno_colums)
            geo = np.reshape(anno_array[:8].astype(float), (4, 2))
            # scale_ratio_w = 896/2448
            # scale_ratio_h = 896/2048
            cut_text_line(geo, 1, 1, im_array, img_path,  img_name)
            s += 1

for file_name in coordlist:
    with open(outputpath+"05.06.roi_coords_1000_test.txt","a") as f:
        f.write(file_name + "\n")
        # print(file_name)
    f.close()


