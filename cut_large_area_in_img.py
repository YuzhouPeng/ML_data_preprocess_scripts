import os,cv2,random
import imgaug as ia
from imgaug import augmenters as iaa
from generate_xml import change2xml
import xml.etree.ElementTree as ET
characterpaths = "/home/pengyuzhou/data_outputs/large_img_1116/"
outputpath = "/home/pengyuzhou/data_croped/04.29_crop_992_992/"
count= 0
crop_size =992
base_path = outputpath
"""
读取xml中的roi框并且切出覆盖整个钢印喷码区域的ROI，重设坐标系

"""
def cut_large_area_in_img(xml_path,imgpath,filename):
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
    print(filename)
    #遍历bbox,保存bbox坐标信息，筛选出所有bbox左上和右下角
    gangyinlist = []
    gangyincoord = []
    penmalist = []
    penmacoord = []
    for ix, obj in enumerate(objs):
        # count+=1
        name = obj.find('name').text
        box = obj.find('bndbox')

        if name=="G":
            x_min = int(box[0].text)
            y_min = int(box[1].text)
            x_max = int(box[2].text)
            y_max = int(box[3].text)
            gangyincoord = [x_min, y_min, x_max, y_max,"gangyin"]
            gangyin_center_coord = [x_max-(x_max-x_min)//2,y_max-(y_max-y_min)//2]
            gangyin_longest_side = max((x_max-x_min),(y_max-y_min)) if max((x_max-x_min),(y_max-y_min))>992 else 992
        elif name == "P":
            x_min = int(box[0].text)
            y_min = int(box[1].text)
            x_max = int(box[2].text)
            y_max = int(box[3].text)
            penmacoord = [x_min, y_min, x_max, y_max, "penma"]
            penma_center_coord = [x_max-(x_max-x_min)//2,y_max-(y_max-y_min)//2]
            penma_longest_side = max((x_max-x_min),(y_max-y_min)) if max((x_max-x_min),(y_max-y_min))>992 else 992
        elif name.split("^")[0]=="G":
            x_min = int(box[0].text)
            y_min = int(box[1].text)
            x_max = int(box[2].text)
            y_max = int(box[3].text)
            gangyinlist.append([x_min, y_min, x_max, y_max,name])
        elif name.split("^")[0]=="P":
            x_min = int(box[0].text)
            y_min = int(box[1].text)
            x_max = int(box[2].text)
            y_max = int(box[3].text)
            penmalist.append([x_min, y_min, x_max, y_max,name])

    #钢印crop图像
    x,y = gangyin_center_coord
    lefttop_x = x-gangyin_longest_side//2 if x-gangyin_longest_side//2>=0 else 0
    lefttop_y = y-gangyin_longest_side//2 if y-gangyin_longest_side//2>=0 else 0
    rightbottom_x = x+gangyin_longest_side//2 if x+gangyin_longest_side//2<=width else width
    rightbottom_y = y+gangyin_longest_side//2 if y+gangyin_longest_side//2<=height else height
    make_border_left = 0 if x-gangyin_longest_side//2>=0 else gangyin_longest_side//2-x
    make_border_top = 0 if y-gangyin_longest_side//2>=0 else gangyin_longest_side//2-y
    make_border_right = 0 if x+gangyin_longest_side//2<=width else x+gangyin_longest_side//2-width
    make_border_bottom = 0 if y+gangyin_longest_side//2<=height else y+gangyin_longest_side//2-height
    croppedgangyin = cv2.copyMakeBorder(img[lefttop_y:rightbottom_y,lefttop_x:rightbottom_x],make_border_top,make_border_bottom,make_border_left,make_border_right, cv2.BORDER_CONSTANT,value=[0,0,0])

    
    #喷码crop图像

    x,y = penma_center_coord
    lefttop_x = x-penma_longest_side//2 if x-penma_longest_side//2>=0 else 0
    lefttop_y = y-penma_longest_side//2 if y-penma_longest_side//2>=0 else 0
    rightbottom_x = x+penma_longest_side//2 if x+penma_longest_side//2<=width else width
    rightbottom_y = y+penma_longest_side//2 if y+penma_longest_side//2<=height else height
    make_border_left = 0 if x-penma_longest_side//2>=0 else penma_longest_side//2-x
    make_border_top = 0 if y-penma_longest_side//2>=0 else penma_longest_side//2-y
    make_border_right = 0 if x+penma_longest_side//2<=width else x+penma_longest_side//2-width
    make_border_bottom = 0 if y+penma_longest_side//2<=height else y+penma_longest_side//2-height
    croppedpenma = cv2.copyMakeBorder(img[lefttop_y:rightbottom_y,lefttop_x:rightbottom_x],make_border_top,make_border_bottom,make_border_left,make_border_right, cv2.BORDER_CONSTANT,value=[0,0,0])


    xml_name_gangyin = os.path.join(base_path,    "gangyin" + filename +  str(count) + '.xml')
    xml_name_penma = os.path.join(base_path,    "penma" + filename +  str(count) + '.xml')
    xml_dir = base_path

    #保存钢印图像
    xmin_temp_up_left = gangyin_center_coord[0]-gangyin_longest_side//2
    ymin_temp_up_left = gangyin_center_coord[1]-gangyin_longest_side//2
    bbox_list_gangyin = []
    label_list_gangyin = []
    #左上角坐标
    for i in range(len(gangyinlist)):
        #bbox左上角
        xmin_new_up_right = gangyinlist[i][0] - xmin_temp_up_left
        ymin_new_up_right = gangyinlist[i][1] - ymin_temp_up_left
        xmax_new_up_right = gangyinlist[i][2] - xmin_temp_up_left
        ymax_new_up_right = gangyinlist[i][3] - ymin_temp_up_left
        bbox_list_gangyin.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
        label_list_gangyin.append([gangyinlist[i][4]])
    xmin_temp_up_left = penma_center_coord[0]-penma_longest_side//2
    ymin_temp_up_left = penma_center_coord[1]-penma_longest_side//2
    bbox_list_penma = []
    label_list_penma = []
    #左上角坐标
    for i in range(len(penmalist)):
        #bbox左上角
        xmin_new_up_right = penmalist[i][0] - xmin_temp_up_left
        ymin_new_up_right = penmalist[i][1] - ymin_temp_up_left
        xmax_new_up_right = penmalist[i][2] - xmin_temp_up_left
        ymax_new_up_right = penmalist[i][3] - ymin_temp_up_left
        bbox_list_penma.append([xmin_new_up_right if xmin_new_up_right>=0 else 0, ymin_new_up_right if ymin_new_up_right>=0 else 0, xmax_new_up_right if xmax_new_up_right>=0 else 0, ymax_new_up_right if ymax_new_up_right>=0 else 0])
        label_list_penma.append([penmalist[i][4]])

    #保存喷码图像

    change2xml(image = xml_name_gangyin, bbox = bbox_list_gangyin, labels = label_list_gangyin, save_dir = xml_dir, width = crop_size, height = crop_size)
    change2xml(image = xml_name_penma, bbox = bbox_list_penma, labels = label_list_penma, save_dir = xml_dir, width = crop_size, height = crop_size)

    cv2.imwrite(os.path.join(outputpath,  "gangyin" + filename +  str(count) + '.jpg'),croppedgangyin)
    cv2.imwrite(os.path.join(outputpath,  "penma" + filename +  str(count) + '.jpg'),croppedpenma)
    count+=1


for parent,_,files in os.walk(characterpaths):
    for file in files:
        if file[-3:]=="xml":
            singlexmlpath = os.path.join(parent,file)
            filepath = singlexmlpath[:-3]+"jpg"
            cut_large_area_in_img(singlexmlpath,filepath,file)
