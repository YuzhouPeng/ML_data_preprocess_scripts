import xml.etree.ElementTree as ET
import os,cv2
import glob,split_train_val
xmlpath ="/home/dev_shared/tot/total/"
resultpath = "/home/pengyuzhou/data/2020.03.27data/train_3900_output/"
outputpath = "/home/pengyuzhou/data/2020.03.27data/"
# count = 0
dict = {}
filenamelist = []
def parse_xml(xml_path,imgpath,filename):
    '''
    输入：
        xml_path: xml的文件路径
    输出：
        从xml文件中提取bounding box信息, 格式为[[x_min, y_min, x_max, y_max, name]]并输出图像
    '''
    global count
    tree = ET.parse(xml_path)		
    root = tree.getroot()
    objs = root.findall('object')
    # print(imgpath)
    img = cv2.imread(imgpath)
    x = list()
    y = list()
    for ix, obj in enumerate(objs):
        count+=1



if __name__ == "__main__":
    count = 0

    for parent,_,files in os.walk(xmlpath):
        for file in files:
            if file[-3:]=="xml":
                singlexmlpath = os.path.join(parent,file)
                filepath = singlexmlpath[:-3]+"jpg"
                parse_xml(singlexmlpath,filepath,file)
    print(count)