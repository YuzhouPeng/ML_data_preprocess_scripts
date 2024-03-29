import os
import xml.etree.ElementTree as ET

classes = ['Dustbin',
        'Car',
        'Bus',
        'Truck',
        'Van',
        'Patrol',
        'Bicycle',
        'Motorcycle',
        'Tricycle',
        'Pedestrian',
        'Head',
        'Face',
        'BabyCarriage',
        'NoDustbin',
        'FakePerson',
        'Trolley',
        'Animal',
        'Chair'
       ]

outputpath = '/home/pengyuzhou/workspace/seated_label_txt/'
# 将x1, y1, x2, y2转换成yolov5所需要的x, y, w, h格式
def xyxy2xywh(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[2]) / 2 * dw
    y = (box[1] + box[3]) / 2 * dh
    w = (box[2] - box[0]) * dw
    h = (box[3] - box[1]) * dh
    return (x, y, w, h)         # 返回的都是标准化后的值


def voc2yolo(path):
    # 可以打印看看该路径是否正确
    print(len(os.listdir(path)))
    # 遍历每一个xml文件
    for file in os.listdir(path):
        if file[-3:]=='xml':
            # xml文件的完整路径
            label_file = path + file
            # 最终要改成的txt格式文件,这里我是放在voc2007/labels/下面
            out_file = open(outputpath + file.replace('xml', 'txt'), 'w')
            # print(label_file)

            # 开始解析xml文件
            tree = ET.parse(label_file)
            root = tree.getroot()
            size = root.find('size')            # 图片的shape值
            w = int(size.find('width').text)
            h = int(size.find('height').text)
            print("img {} size is w: {} h:{}".format(file,w,h))
            if w>0 and h>0:
                for obj in root.iter('object'):
                    difficult = obj.find('difficult').text
                    cls = obj.find('name').text
                    if cls not in classes or int(difficult) == 1:
                        continue
                    # 将名称转换为id下标
                    cls_id = classes.index(cls)
                    # 获取整个bounding box框
                    bndbox = obj.find('bndbox')
                    # xml给出的是x1, y1, x2, y2
                    box = [float(bndbox.find('xmin').text), float(bndbox.find('ymin').text), float(bndbox.find('xmax').text),
                        float(bndbox.find('ymax').text)]

                    # 将x1, y1, x2, y2转换成yolov5所需要的x, y, w, h格式
                    bbox = xyxy2xywh((w, h), box)
                    # 写入目标文件中，格式为 id x y w h
                    out_file.write(str(cls_id) + " " + " ".join(str(x) for x in bbox) + '\n')

if __name__ == '__main__':
	# 这里要改成自己数据集路径的格式
    path = '/home/pengyuzhou/workspace/seated_labels_xml/'
    voc2yolo(path)