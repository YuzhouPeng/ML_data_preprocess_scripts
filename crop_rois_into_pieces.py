import os,cv2,random
import imgaug as ia
from imgaug import augmenters as iaa
from generate_xml import change2xml
import xml.etree.ElementTree as ET
characterpaths = "/home/pengyuzhou/data_gangyin/gangyin/total_data/"
outputpath = "/home/pengyuzhou/data_croped/123/"
count= 0
repeattime = 2
crop_size =992
base_path = outputpath
fileprefix = "gangyin_"
"""
读取xml中的roi框并且随机选择框中一点作中心切割正方形图像同时保留ROI，超出边界的部分填充黑色

"""
def parse_xml(xml_path,imgpath,filename):
    '''
    输入：
        xml_path: xml的文件路径
    输出：
        从xml文件中提取bounding box信息, 格式为[[x_min, y_min, x_max, y_max, name]]并输出图像
    '''
    global count
    bbox_list = []
    tree = ET.parse(xml_path)		
    root = tree.getroot()
    objs = root.findall('object')
    # print(imgpath)
    img = cv2.imread(imgpath)
    height,width,channel = img.shape
    x = list()
    y = list()
    ul_x = 0
    ul_y = 0
    br_x = 0
    br_y = 0
    #遍历bbox,保存bbox坐标信息，筛选出所有bbox左上和右下角
    for ix, obj in enumerate(objs):
        # count+=1
        name = obj.find('name').text
        box = obj.find('bndbox')
        x_min = int(box[0].text)
        y_min = int(box[1].text)
        x_max = int(box[2].text)
        y_max = int(box[3].text)
        bbox = [x_min, y_min, x_max, y_max, name]
        bbox_list.append(bbox)
        ul_x = min(ul_x,x_min)
        ul_y = min(ul_x,y_min)
        br_x = max(br_x,x_max)
        br_y = max(br_y,y_max)

    ul_x += 10
    ul_y += 10
    br_x -= 10
    br_y -= 10
    if ul_x>=0 and ul_y>=0 and  br_x>=0 and br_y>=0 and br_y>ul_y and br_x>ul_x:
        for i in range(repeattime):
            ylength = br_y-ul_y
            xlength = br_x-ul_x
            y = random.randint(1,int(ylength))
            x = random.randint(1,int(xlength))

            cropImgUpperLeft = cv2.copyMakeBorder(img[0 if y<=crop_size else y-crop_size:y,0 if x<crop_size else x-crop_size:x],0 if y>crop_size else crop_size-y,0,0 if x>crop_size else crop_size-x,0, cv2.BORDER_CONSTANT,value=[0,0,0])
            cropImgUpperRight =  cv2.copyMakeBorder(img[0 if y<=crop_size else y-crop_size:y,x:xlength if xlength-x<crop_size else x+crop_size],0 if y>crop_size else crop_size-y,0,0,0 if xlength-x>crop_size else crop_size-xlength+x, cv2.BORDER_CONSTANT,value=[0,0,0])
            cropImgBottomLeft = cv2.copyMakeBorder(img[y:ylength if ylength-y<crop_size else y+crop_size,0 if x<crop_size else x-crop_size:x],0,0 if ylength-y>crop_size else crop_size-ylength+y,0 if x>crop_size else crop_size-x,0, cv2.BORDER_CONSTANT,value=[0,0,0])
            cropImgBottomRight = cv2.copyMakeBorder(img[y:ylength if ylength-y<crop_size else y+crop_size,x:xlength  if xlength-x<crop_size else x+crop_size],0,0 if ylength-y>crop_size else crop_size-ylength+y,0,0 if xlength-x>crop_size else crop_size-xlength+x, cv2.BORDER_CONSTANT,value=[0,0,0])
            lefttop_x = x-crop_size//2 if x-crop_size//2>=0 else 0
            lefttop_y = y-crop_size//2 if y-crop_size//2>=0 else 0
            rightbottom_x = x+crop_size//2 if x+crop_size//2<=width else width
            rightbottom_y = y+crop_size//2 if y+crop_size//2<=height else height
            make_border_left = 0 if x-crop_size//2>=0 else crop_size//2-x
            make_border_top = 0 if y-crop_size//2>=0 else crop_size//2-y
            make_border_right = 0 if x+crop_size//2<=width else x+crop_size//2-width
            make_border_bottom = 0 if y+crop_size//2<=height else y+crop_size//2-height

            ImgCenterCrop = cv2.copyMakeBorder(img[lefttop_y:rightbottom_y,lefttop_x:rightbottom_x],make_border_top,make_border_bottom,make_border_left,make_border_right, cv2.BORDER_CONSTANT,value=[0,0,0])
            xmin_temp = x - (crop_size // 2)
            ymin_temp = y - (crop_size // 2)
            bbox_list_last = []
            label_list_last = []
            bbox_list_copy = bbox_list.copy()
            #检查bbox中有没有在以x,y为中心的正方形中
            #以中心点为坐标
            for i in range(len(bbox_list_copy)):
                #bbox左上角
                if ((bbox_list_copy[i][0] >= xmin_temp) and (bbox_list_copy[i][0] <= xmin_temp + crop_size) and (bbox_list_copy[i][1] >= ymin_temp) and (bbox_list_copy[i][1] <= ymin_temp + crop_size)):
                    xmin_new_up_right = bbox_list_copy[i][0] - xmin_temp 
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp
                    xmax_new_up_right = min(bbox_list_copy[i][2], xmin_temp + crop_size) - xmin_temp
                    ymax_new_up_right = min(bbox_list_copy[i][3], ymin_temp + crop_size) - ymin_temp
                    
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last.append([bbox_list_copy[i][4]])
                #bbox右下角
                elif (bbox_list_copy[i][2]<=xmin_temp+crop_size) and (bbox_list_copy[i][2]>=xmin_temp) and (bbox_list_copy[i][3] >= ymin_temp) and (bbox_list_copy[i][3] <= ymin_temp + crop_size):
                    
                    xmin_new_up_right = 0
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp
                    xmax_new_up_right = bbox_list_copy[i][2] - xmin_temp
                    ymax_new_up_right = bbox_list_copy[i][3] - ymin_temp

                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last.append([bbox_list_copy[i][4]])
                
                
                #bbox右上角
                elif (bbox_list_copy[i][2]<=xmin_temp+crop_size) and (bbox_list_copy[i][2]>=xmin_temp) and (bbox_list_copy[i][1]>=ymin_temp) and (bbox_list_copy[i][1]<=ymin_temp+crop_size):
                    xmin_new_up_right = 0
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp
                    xmax_new_up_right = bbox_list_copy[i][2] - xmin_temp
                    ymax_new_up_right = crop_size
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last.append([bbox_list_copy[i][4]])
                #bbox左下角
                elif (bbox_list_copy[i][0]>=xmin_temp) and (bbox_list_copy[i][0]<=xmin_temp+crop_size) and (bbox_list_copy[i][3] >= ymin_temp) and (bbox_list_copy[i][3] <= ymin_temp + crop_size):
                    xmin_new_up_right = bbox_list_copy[i][0] - xmin_temp
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp
                    xmax_new_up_right = crop_size
                    ymax_new_up_right = bbox_list_copy[i][3]-ymin_temp
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last.append([bbox_list_copy[i][4]])
                    




                #bbox竖直，左上角
                #bbox竖直，右上角
                #从中间水平穿过的情况
                elif (bbox_list_copy[i][0]<xmin_temp) and (bbox_list_copy[i][2]>xmin_temp+crop_size) and (bbox_list_copy[i][1]>=ymin_temp) and (bbox_list_copy[i][3]<=ymin_temp+crop_size):
                    xmin_new_up_right = 0
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp
                    xmax_new_up_right = crop_size
                    ymax_new_up_right = bbox_list_copy[i][3]-ymin_temp
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last.append([bbox_list_copy[i][4]])
                #从中间竖直穿过的情况
                elif (bbox_list_copy[i][0]>=xmin_temp) and (bbox_list_copy[i][2]<=xmin_temp+crop_size) and (bbox_list_copy[i][1]<ymin_temp) and (bbox_list_copy[i][3]>ymin_temp+crop_size):
                    xmin_new_up_right = bbox_list_copy[i][0]-xmin_temp
                    ymin_new_up_right = 0
                    xmax_new_up_right = bbox_list_copy[i][2]-xmin_temp
                    ymax_new_up_right = crop_size
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last.append([bbox_list_copy[i][4]])


            xmin_temp_up_left = x - crop_size
            ymin_temp_up_left = y - crop_size
            bbox_list_last_up_left = []
            label_list_last_up_left = []
            #左上角坐标
            for i in range(len(bbox_list_copy)):
                #bbox左上角
                if ((bbox_list_copy[i][0] >= xmin_temp_up_left) and (bbox_list_copy[i][0] <= xmin_temp_up_left + crop_size) and (bbox_list_copy[i][1] >= ymin_temp_up_left) and (bbox_list_copy[i][1] <= ymin_temp_up_left + crop_size)):
                    xmin_new_up_right = bbox_list_copy[i][0] - xmin_temp_up_left
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_up_left
                    xmax_new_up_right = min(bbox_list_copy[i][2], xmin_temp_up_left + crop_size) - xmin_temp_up_left
                    ymax_new_up_right = min(bbox_list_copy[i][3], ymin_temp_up_left + crop_size) - ymin_temp_up_left
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_up_left.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_up_left.append([bbox_list_copy[i][4]])
                #bbox右下角
                elif (bbox_list_copy[i][2]<=xmin_temp_up_left+crop_size) and (bbox_list_copy[i][2]>=xmin_temp_up_left) and (bbox_list_copy[i][3] >= ymin_temp_up_left) and (bbox_list_copy[i][3] <= ymin_temp_up_left + crop_size):
                    
                    xmin_new_up_right = 0
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_up_left
                    xmax_new_up_right = bbox_list_copy[i][2] - xmin_temp_up_left
                    ymax_new_up_right = bbox_list_copy[i][3] - ymin_temp_up_left
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_up_left.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_up_left.append([bbox_list_copy[i][4]])



                #bbox右上角
                elif (bbox_list_copy[i][2]<=xmin_temp_up_left+crop_size) and (bbox_list_copy[i][2]>=xmin_temp_up_left) and (bbox_list_copy[i][1]>=ymin_temp_up_left) and (bbox_list_copy[i][1]<=ymin_temp_up_left+crop_size):
                    xmin_new_up_right = 0
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_up_left
                    xmax_new_up_right = bbox_list_copy[i][2] - xmin_temp_up_left
                    ymax_new_up_right = crop_size
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_up_left.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_up_left.append([bbox_list_copy[i][4]])
                #bbox左下角
                elif (bbox_list_copy[i][0]>=xmin_temp_up_left) and (bbox_list_copy[i][0]<=xmin_temp_up_left+crop_size) and (bbox_list_copy[i][3] >= ymin_temp_up_left) and (bbox_list_copy[i][3] <= ymin_temp_up_left + crop_size):
                    xmin_new_up_right = bbox_list_copy[i][0] - xmin_temp_up_left
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_up_left
                    xmax_new_up_right = crop_size
                    ymax_new_up_right = bbox_list_copy[i][3]-ymin_temp_up_left
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_up_left.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_up_left.append([bbox_list_copy[i][4]])



                #bbox竖直，左上角
                #bbox竖直，右上角
                #从中间水平穿过的情况
                elif (bbox_list_copy[i][0]<xmin_temp_up_left) and (bbox_list_copy[i][2]>xmin_temp_up_left+crop_size) and (bbox_list_copy[i][1]>=ymin_temp_up_left) and (bbox_list_copy[i][3]<=ymin_temp_up_left+crop_size):
                    xmin_new_up_right = 0
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_up_left
                    xmax_new_up_right = crop_size
                    ymax_new_up_right = bbox_list_copy[i][3]-ymin_temp_up_left
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_up_left.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_up_left.append([bbox_list_copy[i][4]])
                #从中间竖直穿过的情况
                elif (bbox_list_copy[i][0]>=xmin_temp_up_left) and (bbox_list_copy[i][2]<=xmin_temp_up_left+crop_size) and (bbox_list_copy[i][1]<ymin_temp_up_left) and (bbox_list_copy[i][3]>ymin_temp_up_left+crop_size):
                    xmin_new_up_right = bbox_list_copy[i][0]-xmin_temp_up_left
                    ymin_new_up_right = 0
                    xmax_new_up_right = bbox_list_copy[i][2]-xmin_temp_up_left
                    ymax_new_up_right = crop_size
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_up_left.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_up_left.append([bbox_list_copy[i][4]])
            #右上角坐标
            xmin_temp_up_right = x
            ymin_temp_up_right = y - crop_size
            bbox_list_last_up_right = []
            label_list_last_up_right = []
            for i in range(len(bbox_list_copy)):
                #bbox左上角
                if ((bbox_list_copy[i][0] >= xmin_temp_up_right) and (bbox_list_copy[i][0] <= xmin_temp_up_right + crop_size) and (bbox_list_copy[i][1] >= ymin_temp_up_right) and (bbox_list_copy[i][1] <= ymin_temp_up_right + crop_size)):
                    xmin_new_up_right = bbox_list_copy[i][0] - xmin_temp_up_right
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_up_right
                    xmax_new_up_right = min(bbox_list_copy[i][2], xmin_temp_up_right + crop_size) - xmin_temp_up_right
                    ymax_new_up_right = min(bbox_list_copy[i][3], ymin_temp_up_right + crop_size) - ymin_temp_up_right
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_up_right.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_up_right.append([bbox_list_copy[i][4]])
                #bbox右下角
                elif (bbox_list_copy[i][2]<=xmin_temp_up_right+crop_size) and (bbox_list_copy[i][2]>=xmin_temp_up_right) and (bbox_list_copy[i][3] >= ymin_temp_up_right) and (bbox_list_copy[i][3] <= ymin_temp_up_right + crop_size):
                    
                    xmin_new_up_right = 0
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_up_right
                    xmax_new_up_right = bbox_list_copy[i][2] - xmin_temp_up_right
                    ymax_new_up_right = bbox_list_copy[i][3] - ymin_temp_up_right
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_up_right.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_up_right.append([bbox_list_copy[i][4]])



                #bbox右上角
                elif (bbox_list_copy[i][2]<=xmin_temp_up_right+crop_size) and (bbox_list_copy[i][2]>=xmin_temp_up_right) and (bbox_list_copy[i][1]>=ymin_temp_up_right) and (bbox_list_copy[i][1]<=ymin_temp_up_right+crop_size):
                    xmin_new_up_right = 0
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_up_right
                    xmax_new_up_right = bbox_list_copy[i][2] - xmin_temp_up_right
                    ymax_new_up_right = crop_size
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_up_right.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_up_right.append([bbox_list_copy[i][4]])
                #bbox左下角
                elif (bbox_list_copy[i][0]>=xmin_temp_up_right) and (bbox_list_copy[i][0]<=xmin_temp_up_right+crop_size) and (bbox_list_copy[i][3] >= ymin_temp_up_right) and (bbox_list_copy[i][3] <= ymin_temp_up_right + crop_size):
                    xmin_new_up_right = bbox_list_copy[i][0] - xmin_temp_up_right
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_up_right
                    xmax_new_up_right = crop_size
                    ymax_new_up_right = bbox_list_copy[i][3]-ymin_temp_up_right
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_up_right.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_up_right.append([bbox_list_copy[i][4]])





                #bbox竖直，左上角
                #bbox竖直，右上角
                #从中间水平穿过的情况
                elif (bbox_list_copy[i][0]<xmin_temp_up_right) and (bbox_list_copy[i][2]>xmin_temp_up_right+crop_size) and (bbox_list_copy[i][1]>=ymin_temp_up_right) and (bbox_list_copy[i][3]<=ymin_temp_up_right+crop_size):
                    xmin_new_up_right = 0
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_up_right
                    xmax_new_up_right = crop_size
                    ymax_new_up_right = bbox_list_copy[i][3]-ymin_temp_up_right
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_up_right.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_up_right.append([bbox_list_copy[i][4]])
                #从中间竖直穿过的情况
                elif (bbox_list_copy[i][0]>=xmin_temp_up_right) and (bbox_list_copy[i][2]<=xmin_temp_up_right+crop_size) and (bbox_list_copy[i][1]<ymin_temp_up_right) and (bbox_list_copy[i][3]>ymin_temp_up_right+crop_size):
                    xmin_new_up_right = bbox_list_copy[i][0]-xmin_temp_up_right
                    ymin_new_up_right = 0
                    xmax_new_up_right = bbox_list_copy[i][2]-xmin_temp_up_right
                    ymax_new_up_right = crop_size
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_up_right.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_up_right.append([bbox_list_copy[i][4]])
                     
            #左下角
            xmin_temp_bottom_left = x - (crop_size)
            ymin_temp_bottom_left = y
            bbox_list_last_bottom_left = []
            label_list_last_bottom_left = []
            for i in range(len(bbox_list_copy)):
                #bbox左上角
                if ((bbox_list_copy[i][0] >= xmin_temp_bottom_left) and (bbox_list_copy[i][0] <= xmin_temp_bottom_left + crop_size) and (bbox_list_copy[i][1] >= ymin_temp_bottom_left) and (bbox_list_copy[i][1] <= ymin_temp_bottom_left + crop_size)):
                    xmin_new_up_right = bbox_list_copy[i][0] - xmin_temp_bottom_left
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_bottom_left
                    xmax_new_up_right = min(bbox_list_copy[i][2], xmin_temp_bottom_left + crop_size) - xmin_temp_bottom_left
                    ymax_new_up_right = min(bbox_list_copy[i][3], ymin_temp_bottom_left + crop_size) - ymin_temp_bottom_left
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_bottom_left.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_bottom_left.append([bbox_list_copy[i][4]])
                #bbox右下角
                elif (bbox_list_copy[i][2]<=xmin_temp_bottom_left+crop_size) and (bbox_list_copy[i][2]>=xmin_temp_bottom_left) and (bbox_list_copy[i][3] >= ymin_temp_bottom_left) and (bbox_list_copy[i][3] <= ymin_temp_bottom_left + crop_size):
                    
                    xmin_new_up_right = 0
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_bottom_left
                    xmax_new_up_right = bbox_list_copy[i][2] - xmin_temp_bottom_left
                    ymax_new_up_right = bbox_list_copy[i][3] - ymin_temp_bottom_left
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_bottom_left.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_bottom_left.append([bbox_list_copy[i][4]])



                #bbox右上角
                elif (bbox_list_copy[i][2]<=xmin_temp_bottom_left+crop_size) and (bbox_list_copy[i][2]>=xmin_temp_bottom_left) and (bbox_list_copy[i][1]>=ymin_temp_bottom_left) and (bbox_list_copy[i][1]<=ymin_temp_bottom_left+crop_size):
                    xmin_new_up_right = 0
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_bottom_left
                    xmax_new_up_right = bbox_list_copy[i][2] - xmin_temp_bottom_left
                    ymax_new_up_right = crop_size
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_bottom_left.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_bottom_left.append([bbox_list_copy[i][4]])
                #bbox左下角
                elif (bbox_list_copy[i][0]>=xmin_temp_bottom_left) and (bbox_list_copy[i][0]<=xmin_temp_bottom_left+crop_size) and (bbox_list_copy[i][3] >= ymin_temp_bottom_left) and (bbox_list_copy[i][3] <= ymin_temp_bottom_left + crop_size):
                    xmin_new_up_right = bbox_list_copy[i][0] - xmin_temp_bottom_left
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_bottom_left
                    xmax_new_up_right = crop_size
                    ymax_new_up_right = bbox_list_copy[i][3]-ymin_temp_bottom_left
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_bottom_left.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_bottom_left.append([bbox_list_copy[i][4]])





                #bbox竖直，左上角
                #bbox竖直，右上角
                #从中间水平穿过的情况
                elif (bbox_list_copy[i][0]<xmin_temp_bottom_left) and (bbox_list_copy[i][2]>xmin_temp_bottom_left+crop_size) and (bbox_list_copy[i][1]>=ymin_temp_bottom_left) and (bbox_list_copy[i][3]<=ymin_temp_bottom_left+crop_size):
                    xmin_new_up_right = 0
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_bottom_left
                    xmax_new_up_right = crop_size
                    ymax_new_up_right = bbox_list_copy[i][3]-ymin_temp_bottom_left
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_bottom_left.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_bottom_left.append([bbox_list_copy[i][4]])
                #从中间竖直穿过的情况
                elif (bbox_list_copy[i][0]>=xmin_temp_bottom_left) and (bbox_list_copy[i][2]<=xmin_temp_bottom_left+crop_size) and (bbox_list_copy[i][1]<ymin_temp_bottom_left) and (bbox_list_copy[i][3]>ymin_temp_bottom_left+crop_size):
                    xmin_new_up_right = bbox_list_copy[i][0]-xmin_temp_bottom_left
                    ymin_new_up_right = 0
                    xmax_new_up_right = bbox_list_copy[i][2]-xmin_temp_bottom_left
                    ymax_new_up_right = crop_size
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_bottom_left.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_bottom_left.append([bbox_list_copy[i][4]])

            xmin_temp_bottom_right = x 
            ymin_temp_bottom_right = y
            bbox_list_last_bottom_right = []
            label_list_last_bottom_right = []
            #右下角
            for i in range(len(bbox_list_copy)):
                #bbox左上角
                if ((bbox_list_copy[i][0] >= xmin_temp_bottom_right) and (bbox_list_copy[i][0] <= xmin_temp_bottom_right + crop_size) and (bbox_list_copy[i][1] >= ymin_temp_bottom_right) and (bbox_list_copy[i][1] <= ymin_temp_bottom_right + crop_size)):
                    xmin_new_up_right = bbox_list_copy[i][0] - xmin_temp_bottom_right
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_bottom_right
                    xmax_new_up_right = min(bbox_list_copy[i][2], xmin_temp_bottom_right + crop_size) - xmin_temp_bottom_right
                    ymax_new_up_right = min(bbox_list_copy[i][3], ymin_temp_bottom_right + crop_size) - ymin_temp_bottom_right
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_bottom_right.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_bottom_right.append([bbox_list_copy[i][4]])
                #bbox右下角
                elif (bbox_list_copy[i][2]<=xmin_temp_bottom_right+crop_size) and (bbox_list_copy[i][2]>=xmin_temp_bottom_right) and (bbox_list_copy[i][3] >= ymin_temp_bottom_right) and (bbox_list_copy[i][3] <= ymin_temp_bottom_right + crop_size):
                    
                    xmin_new_up_right = 0
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_bottom_right
                    xmax_new_up_right = bbox_list_copy[i][2] - xmin_temp_bottom_right
                    ymax_new_up_right = bbox_list_copy[i][3] - ymin_temp_bottom_right
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_bottom_right.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_bottom_right.append([bbox_list_copy[i][4]])

                #bbox右上角
                elif (bbox_list_copy[i][2]<=xmin_temp_bottom_right+crop_size) and (bbox_list_copy[i][2]>=xmin_temp_bottom_right) and (bbox_list_copy[i][1]>=ymin_temp_bottom_right) and (bbox_list_copy[i][1]<=ymin_temp_bottom_right+crop_size):
                    xmin_new_up_right = 0
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_bottom_right
                    xmax_new_up_right = bbox_list_copy[i][2] - xmin_temp_bottom_right
                    ymax_new_up_right = crop_size
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_bottom_right.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_bottom_right.append([bbox_list_copy[i][4]])
                #bbox左下角
                elif (bbox_list_copy[i][0]>=xmin_temp_bottom_right) and (bbox_list_copy[i][0]<=xmin_temp_bottom_right+crop_size) and (bbox_list_copy[i][3] >= ymin_temp_bottom_right) and (bbox_list_copy[i][3] <= ymin_temp_bottom_right + crop_size):
                    xmin_new_up_right = bbox_list_copy[i][0] - xmin_temp_bottom_right
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_bottom_right
                    xmax_new_up_right = crop_size
                    ymax_new_up_right = bbox_list_copy[i][3]-ymin_temp_bottom_right
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_bottom_right.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_bottom_right.append([bbox_list_copy[i][4]])


                #bbox竖直，左上角
                #bbox竖直，右上角
                #从中间水平穿过的情况
                elif (bbox_list_copy[i][0]<xmin_temp_bottom_right) and (bbox_list_copy[i][2]>xmin_temp_bottom_right+crop_size) and (bbox_list_copy[i][1]>=ymin_temp_bottom_right) and (bbox_list_copy[i][3]<=ymin_temp_bottom_right+crop_size):
                    xmin_new_up_right = 0
                    ymin_new_up_right = bbox_list_copy[i][1] - ymin_temp_bottom_right
                    xmax_new_up_right = crop_size
                    ymax_new_up_right = bbox_list_copy[i][3]-ymin_temp_bottom_right
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_bottom_right.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_bottom_right.append([bbox_list_copy[i][4]])
                #从中间竖直穿过的情况
                elif (bbox_list_copy[i][0]>=xmin_temp_bottom_right) and (bbox_list_copy[i][2]<=xmin_temp_bottom_right+crop_size) and (bbox_list_copy[i][1]<ymin_temp_bottom_right) and (bbox_list_copy[i][3]>ymin_temp_bottom_right+crop_size):
                    xmin_new_up_right = bbox_list_copy[i][0]-xmin_temp_bottom_right
                    ymin_new_up_right = 0
                    xmax_new_up_right = bbox_list_copy[i][2]-xmin_temp_bottom_right
                    ymax_new_up_right = crop_size
                    if ymax_new_up_right-ymin_new_up_right>5 and xmax_new_up_right-xmin_new_up_right>5:
                        bbox_list_last_bottom_right.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
                        label_list_last_bottom_right.append([bbox_list_copy[i][4]])
            xml_dir = os.path.join(base_path, "data")
            xml_name = os.path.join(base_path, "data",  fileprefix+filename + '_' + str(count) + '.xml')
            xml_name_ul = os.path.join(base_path, "data",  fileprefix+filename + '_ul_' + str(count) + '.xml')
            xml_name_ur = os.path.join(base_path, "data",  fileprefix+filename + '_ur_' + str(count) + '.xml')
            xml_name_bl = os.path.join(base_path, "data",  fileprefix+filename + '_bl_' + str(count) + '.xml')
            xml_name_br = os.path.join(base_path, "data", fileprefix+filename + '_br_' + str(count) + '.xml')
            if len(bbox_list_last)>0:
                change2xml(image = xml_name, bbox = bbox_list_last, labels = label_list_last, save_dir = xml_dir, width = crop_size, height = crop_size)
                cv2.imwrite(os.path.join(outputpath, "data",  fileprefix+filename + '_' + str(count) + '.jpg'),ImgCenterCrop)
            if len(bbox_list_last_up_left)>0:
                change2xml(image = xml_name_ul, bbox = bbox_list_last_up_left, labels = label_list_last_up_left, save_dir = xml_dir, width = crop_size, height = crop_size)
                cv2.imwrite(os.path.join(outputpath, "data",  fileprefix+filename + '_ul_' + str(count) + '.jpg'),cropImgUpperLeft)
            if len(bbox_list_last_up_right)>0:
                change2xml(image = xml_name_ur, bbox = bbox_list_last_up_right, labels = label_list_last_up_right, save_dir = xml_dir, width = crop_size, height = crop_size)
                cv2.imwrite(os.path.join(outputpath, "data",  fileprefix+filename + '_ur_' + str(count) + '.jpg'),cropImgUpperRight)
            if len(bbox_list_last_bottom_left)>0:
                change2xml(image = xml_name_bl, bbox = bbox_list_last_bottom_left, labels = label_list_last_bottom_left, save_dir = xml_dir, width = crop_size, height = crop_size)
                cv2.imwrite(os.path.join(outputpath, "data",  fileprefix+filename + '_bl_' + str(count) + '.jpg'),cropImgBottomLeft)
            if len(bbox_list_last_bottom_right)>0:
                change2xml(image = xml_name_br, bbox = bbox_list_last_bottom_right, labels = label_list_last_bottom_right, save_dir = xml_dir, width = crop_size, height = crop_size)
                cv2.imwrite(os.path.join(outputpath, "data",  fileprefix+filename + '_br_' + str(count) + '.jpg'),cropImgBottomRight)
            # cv2.imwrite(outputpath+file+"_ur_"+str(count)+".jpg",cropImgUpperRight)
            # cv2.imwrite(outputpath+file+"_bl_"+str(count)+".jpg",cropImgBottomLeft)
            # cv2.imwrite(outputpath+file+"_br_"+str(count)+".jpg",cropImgBottomRight)
            count+=1


for parent,_,files in os.walk(characterpaths):
    for file in files:
        if file[-3:]=="xml":
            singlexmlpath = os.path.join(parent,file)
            filepath = singlexmlpath[:-3]+"jpg"
            parse_xml(singlexmlpath,filepath,file)
