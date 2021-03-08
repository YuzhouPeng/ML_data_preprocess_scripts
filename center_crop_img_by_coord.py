import os,cv2,random
import imgaug as ia
from imgaug import augmenters as iaa
from generate_xml import change2xml
import xml.etree.ElementTree as ET


from PIL import Image,ImageDraw,ImageFont


count= 0

# crop_size =3000
fileprefix = "roi_"
"""
按照输入的聚类中心点作中心，以输入的mean distance作边长切割正方形图像，超出边界的部分填充黑色

"""
def center_crop(imgpath,centerpoints,filename,outputpath,mean_distance,channelnames):
    '''
    输入：
        xml_path: xml的文件路径
    输出：
        从xml文件中提取bounding box信息, 格式为[[x_min, y_min, x_max, y_max, name]]并输出图像
    '''
    #如果是钢印，则切割边长为992
    for path,centerpoint,mean_dist,chan_name in zip(imgpath,centerpoints,mean_distance,channelnames):
        if chan_name=="ch1":
            mean_dist=2800
        crop_size = mean_dist
        img = cv2.imread(path)
        height,width,channel = img.shape
        coords = []
        global count
        y,x = centerpoint
        x = int(x)
        y = int(y)
        lefttop_x = x-crop_size//2 if x-crop_size//2>=0 else 0
        lefttop_y = y-crop_size//2 if y-crop_size//2>=0 else 0
        rightbottom_x = x+crop_size//2 if x+crop_size//2<=width else width
        rightbottom_y = y+crop_size//2 if y+crop_size//2<=height else height
        make_border_left = 0 if x-crop_size//2>=0 else crop_size//2-x
        make_border_top = 0 if y-crop_size//2>=0 else crop_size//2-y
        make_border_right = 0 if x+crop_size//2<=width else x+crop_size//2-width
        make_border_bottom = 0 if y+crop_size//2<=height else y+crop_size//2-height


        ImgCenterCrop = cv2.copyMakeBorder(img[lefttop_y:rightbottom_y,lefttop_x:rightbottom_x],make_border_top,make_border_bottom,make_border_left,make_border_right, cv2.BORDER_CONSTANT,value=[0,0,0])
        coords.append([lefttop_x,lefttop_y,rightbottom_x,rightbottom_y,make_border_left,make_border_top,make_border_right,make_border_bottom])
        cv2.imwrite(os.path.join(outputpath,  fileprefix+filename + '_'+chan_name+"_" + str(count) + '.jpg'),ImgCenterCrop)
        count+=1
    # return coords

