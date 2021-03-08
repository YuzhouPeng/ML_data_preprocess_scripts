# -*- coding=utf-8 -*-
import xml.etree.ElementTree as ET
import os, cv2
import glob
xmlpathl = "/home/pengyuzhou/data/2020.03.27data/third_data_train_large/"
xmlpaths = "/home/pengyuzhou/data/2020.03.27data/third_data_train_small/"
dict = {}

def rename_file(path,notification):
    for parent,_,files in os.walk(path):
        for file in files:
            ele = file.split(".")
            prefix,end = ele[0],ele[1]
            NewFileName = os.path.join(path, prefix+"."+notification+'.'+end)
            OldFileName = os.path.join(path, file)
            os.rename(OldFileName, NewFileName)

def parse_xml_and_expand_roi(xml_path, ratio):
    '''
    输入：
        xml_path: xml的文件路径
    输出：
        从xml文件中提取bounding box信息, 格式为[[x_min, y_min, x_max, y_max, name]]并输出图像
    '''
    tree = ET.parse(xml_path)
    root = tree.getroot()
    objs = root.findall('object')
    for ix, obj in enumerate(objs):
        name = obj.find('name').text
        box = obj.find('bndbox')
        x_min = int(box[0].text)
        y_min = int(box[1].text)
        x_max = int(box[2].text)
        y_max = int(box[3].text)
        scale_x = int((x_max-x_min)*ratio)
        scale_y = int((y_max-y_min)*ratio*5)
        new_x_min = x_min-scale_x if x_min-scale_x>0 else 0
        new_x_max = x_max+scale_x if x_max+scale_x>0 else 0
        new_y_min = y_min-scale_y if y_min-scale_y>0 else 0
        new_y_max = y_max+scale_y if y_max+scale_y>0 else 0
        box[0].text = str(new_x_min)
        box[1].text = str(new_y_min)
        box[2].text = str(new_x_max)
        box[3].text = str(new_y_max)
    tree.write(xmlpath,encoding="utf-8")

def parse_xml_and_smaller_roi(xml_path, ratio):
    '''
    输入：
        xml_path: xml的文件路径
    输出：
        从xml文件中提取bounding box信息, 格式为[[x_min, y_min, x_max, y_max, name]]并输出图像
    '''
    tree = ET.parse(xml_path)
    root = tree.getroot()
    objs = root.findall('object')
    for ix, obj in enumerate(objs):
        name = obj.find('name').text
        box = obj.find('bndbox')
        x_min = int(box[0].text)
        y_min = int(box[1].text)
        x_max = int(box[2].text)
        y_max = int(box[3].text)
        scale_x = int((x_max-x_min)*(ratio/5))
        scale_y = int((y_max-y_min)*ratio)
        new_x_min = x_min+scale_x if x_min+scale_x>0 else 0
        new_x_max = x_max-scale_x if x_max-scale_x>0 else 0
        new_y_min = y_min+scale_y if y_min+scale_y>0 else 0
        new_y_max = y_max-scale_y if y_max-scale_y>0 else 0
        box[0].text = str(new_x_min)
        box[1].text = str(new_y_min)
        box[2].text = str(new_x_max)
        box[3].text = str(new_y_max)
    tree.write(xmlpath,encoding="utf-8")

if __name__ == "__main__":
    for parent, _, files in os.walk(xmlpaths):
        for file in files:
            print(file)
            if file[-3:] == "xml":
                xmlpath = os.path.join(parent, file)
                # print(xmlpath)
                # parse_xml_and_expand_roi(xmlpath,0.05)
                parse_xml_and_smaller_roi(xmlpath,0.1)
    rename_file(xmlpaths,"s")


    for parent, _, files in os.walk(xmlpathl):
        for file in files:
            if file[-3:] == "xml":
                xmlpath = os.path.join(parent, file)
                # print(xmlpath)
                # parse_xml_and_expand_roi(xmlpath,0.05)
                parse_xml_and_expand_roi(xmlpath,0.05)
    rename_file(xmlpathl,"l")
