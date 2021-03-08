import os,cv2
from generate_xml import change2xml
import xml.etree.ElementTree as ET
inputfilepath = "/home/pengyuzhou/data_croped/04.30test/"
outputfilepath = "/home/pengyuzhou/data_croped/04.30.test_output/"
cropwidthpixel = 128
cropheightpixel = 64
crop_size =992
fileprefix = "crop_edge_"
def parse_xml(xml_path,imgpath,filename):
    '''
    输入：
        xml_path: xml的文件路径
    输出：
        从xml文件中提取bounding box信息, 格式为[[x_min, y_min, x_max, y_max, name]]并输出图像
    '''
    bbox_list = []
    label_list =[]
    tree = ET.parse(xml_path)		
    root = tree.getroot()
    objs = root.findall('object')
    # print(imgpath)
    img = cv2.imread(imgpath)
    height,width,channel = img.shape
    img = img[cropheightpixel//2:height-cropheightpixel//2,cropwidthpixel//2:width-cropwidthpixel//2]
    #遍历bbox,保存bbox坐标信息，筛选出所有bbox左上和右下角
    for ix, obj in enumerate(objs):
        # count+=1
        name = obj.find('name').text
        box = obj.find('bndbox')
        x_min = int(box[0].text) 
        y_min = int(box[1].text) 
        x_max = int(box[2].text) 
        y_max = int(box[3].text) 

        x_min = x_min if x_min>=cropwidthpixel//2 else cropwidthpixel//2
        y_min = y_min if y_min>=cropheightpixel//2 else cropheightpixel//2
        x_max = x_max if x_max<=width-cropwidthpixel//2 else width-cropwidthpixel//2
        y_max = y_max if y_max<=height-cropheightpixel//2 else height-cropheightpixel//2
        bbox = [x_min, y_min, x_max, y_max]
        label = name
        bbox_list.append(bbox)
        label_list.append(label)
    xml_dir = outputfilepath
    xml_name = os.path.join(outputfilepath,   fileprefix+filename + '_'  + '.xml')
    change2xml(image = xml_name, bbox = bbox_list, labels = label_list, save_dir = xml_dir, width = 16000-cropwidthpixel, height = 8000-cropheightpixel)
    cv2.imwrite(os.path.join(outputfilepath,   fileprefix+filename + '_'  + '.jpg'),img)

for parent,_,files in os.walk(inputfilepath):
    for file in files:
        if file[-3:]=="xml":
            singlexmlpath = os.path.join(parent,file)
            filepath = singlexmlpath[:-3]+"jpg"
            parse_xml(singlexmlpath,filepath,file)
