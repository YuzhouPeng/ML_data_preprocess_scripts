import xml.etree.ElementTree as ET
import os
import glob
import cv2

class_dict = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '0': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35, 'ADD': 36, 'COLON': 37, 'DASH': 38, 'DOT': 39, 'LOGO': 40, 'SLASH': 41, 'STAR': 42}

def parse_xml(xml_path, pic_path, txt_path):
    '''
    输入：
        xml_path: xml的文件路径
    输出：
        从xml文件中提取bounding box信息, 格式为[[x_min, y_min, x_max, y_max, name]]
    '''
    tree = ET.parse(xml_path)		
    root = tree.getroot()
    objs = root.findall('object')
    x_O = 0
    y_O = 0
    x_M = 0
    y_M = 0
    crop_w = 0
    crop_h = 0
    img_path = xml_path.replace("xml", "jpg")
    img_name = os.path.basename(img_path)
    print(img_name)
    txt_name = img_name.replace("jpg", "txt")
    image = cv2.imread(img_path)
    for ix, obj in enumerate(objs):
        name = obj.find('name').text
        if name == "TEXT":
            box = obj.find('bndbox')
            x_O = int(box[0].text)
            y_O = int(box[1].text)
            x_M = int(box[2].text)
            y_M = int(box[3].text)
            crop_w = x_M - x_O
            crop_h = y_M - y_O
    crop_img = image[y_O:y_M, x_O:x_M]
    border = crop_w - crop_h
    crop_img = cv2.copyMakeBorder(crop_img, 0, border, 0, 0, 0, value=0)
    crop_img = cv2.resize(crop_img, (416, 416))
    cv2.imwrite(os.path.join(pic_path, img_name), crop_img)

    dw = 1./crop_w
    dh = 1./crop_w

    txt_path = os.path.join(txt_path, txt_name)

    with open(txt_path, 'w') as f:
        for ix, obj in enumerate(objs):
            if obj.find('name').text != "TEXT":
                id = class_dict[obj.find('name').text]
                box = obj.find('bndbox')
                x_min = int(box[0].text) - x_O
                y_min = int(box[1].text) - y_O
                x_max = int(box[2].text) - x_O
                y_max = int(box[3].text) - y_O
                x = (x_min + x_max) / 2.0
                y = (y_min + y_max) / 2.0
                w = x_max - x_min
                h = y_max - y_min
                x = round(x * dw, 4)
                w = round(w * dw, 4)
                y = round(y * dh, 4)
                h = round(h * dh, 4)
                f.write(str(id) + " ")
                f.write(str(x) + " ")
                f.write(str(y) + " ")
                f.write(str(w) + " ")
                f.write(str(h) + "\n")



txt_path = "/home/meixun/workplace/xianggang/YOLOv3_PyTorch_C/data/mianpen100_1_train/labels"
pic_path = "/home/meixun/workplace/xianggang/YOLOv3_PyTorch_C/data/mianpen100_1_train/images"
xml_path = "/home/meixun/workplace/xianggang/YOLOv3_PyTorch_C/data/mianpen100_1"

xml_paths = glob.glob(os.path.join(xml_path, "*.xml"))

for xml in xml_paths:
    parse_xml(xml, pic_path, txt_path)