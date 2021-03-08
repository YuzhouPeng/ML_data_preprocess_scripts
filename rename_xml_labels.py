import xml.etree.ElementTree as ET
import os,cv2
import glob,split_train_val
from generate_xml import change2xml
import xml.etree.ElementTree as ET
xmlpath ="/home/sycv/workplace/pengyuzhou/fabric_1024x1024_0909/"
namedict = {"斑渍":"banzi","擦伤":"cashang","搭线":"daxian","断经":"duanjing","横档":"hengdang","破洞":"podong","浅斑":"qianban","色渍":"sezi","水渍":"shuizi","停车印":"tincheyin","斜皱":"xiezhou","油渍":"youzi","预缩皱":"yusuozhou","沾污":"zhanwu","皱条":"zhoutiao","竹夹":"zhujia","竹节":"zhujie"}
# dict = {}
# filenamelist = []
def parse_xml(xml_path,imgpath,filename,parent):
    '''
    输入：
        xml_path: xml的文件路径
    输出：
        从xml文件中提取bounding box信息, 格式为[[x_min, y_min, x_max, y_max, name]]并输出图像
    '''
    global count
    if filename.split("_")[0]!="img":
        print(filename)
        # print(imgpath)
        # print(xml_path)
        tree = ET.parse(xml_path)		
        root = tree.getroot()
        objs = root.findall('object')
        # print(imgpath)
        img = cv2.imread(imgpath)
        print(img)
        crop_size = (img.shape)[0]

        newlabels = []
        oldbboxs = []
        for _, obj in enumerate(objs):
            # count+=1
            name = obj.find('name').text
            box = obj.find('bndbox')
            x_min = int(box[0].text)
            y_min = int(box[1].text)
            x_max = int(box[2].text)
            y_max = int(box[3].text)
            oldbboxs.append([x_min,y_min,x_max,y_max])
            if name not in namedict.keys():
                newlabels.append(name)
            else:
                newlabels.append(namedict[name])

            # cv2.imwrite(resultpath+str(count)+".jpg",newimg)

        # xml_name_ul = os.path.join(base_path, "data",  fileprefix+filename + '_ul_' + str(count) + '.xml')

        change2xml(image = imgpath, bbox = oldbboxs, labels = newlabels, save_dir = parent, width = crop_size, height = crop_size)


if __name__ == "__main__":
    count = 0

    for parent,_,files in os.walk(xmlpath):
        for file in files:
            if file[-3:]=="xml":
                singlexmlpath = os.path.join(parent,file)
                filepath = singlexmlpath[:-3]+"png"
                parse_xml(singlexmlpath,filepath,file,parent)
