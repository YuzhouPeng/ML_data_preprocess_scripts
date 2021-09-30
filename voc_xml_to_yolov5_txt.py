作者：xiyou
链接：https://zhuanlan.zhihu.com/p/365191541
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

#该脚本的作用是将xml格式的文件转换成yolo需要的格式

import xml.etree.ElementTree as ET
import pickle
import os
from collections import OrderedDict
from os import listdir, getcwd
from os.path import join
'''
fire-detect:
    VOC2020 to yolo format code
'''
sets = [('2020', 'train')]
classes = ['reflective_clothes', 'other_clothes']

# VOC2020 folder root
#data_root = r'/home/fire_data/'

# voc的训练txt 验证txt 必须在VOC*** 以及目录下  不能在Main目录下面；它是在统计目录下
def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(year, image_id):
    global data_root
    in_file = open('Annotations/%s.xml'%(image_id), encoding='utf-8')
    out_file = open('labels/%s.txt'%(image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes: # or int(difficult)==1 不关心difficult
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

# wd = getcwd()

for year, image_set in sets:
    # if not os.path.exists(data_root + 'VOC%s/labels/'%(year)):
    #     os.makedirs(data_root + 'VOC%s/labels/'%(year))
    image_ids = open('ImageSets/Main/%s.txt'%(image_set)).read().strip().split()#有空格的就不行了
    list_file = open('%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        print(image_id)
        list_file.write('JPEGImages/%s.jpg\n'%(image_id))
        convert_annotation(year, image_id)
    list_file.close()

'''
fire-detect：
    train.txt
    test.txt
'''
root = r'./JPEGImages/'
f = open(r'./2020_train.txt', 'w')
names = os.listdir(root)
for name in names:
    print(name)
    f.write(os.path.join(root, name)+'\n')
f.close()

# 6：4 -> train.txt test.txt