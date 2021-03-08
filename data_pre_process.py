# -*- coding: utf-8 -*-
import numpy as np
import os,sys,csv
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import myimageutil as iu
import shutil
import math,random

"""
====================================================================================
<<数据预处理>>
====================================================================================

"""

def get_dataset_info(root_path):

    class_names = os.listdir(root_path)
    '''
    class_names = ['修印', '剪洞', '厚段', '厚薄段', '吊弓', '吊纬', '吊经', '回边', '夹码', '嵌结', '弓纱', '愣断', '扎梳', '扎洞', '扎纱', '擦伤', '擦毛', '擦洞', '明嵌线', '楞断', '正常', '毛斑', '毛洞', '毛粒', '污渍', '油渍', '破洞', '破边', '粗纱', '紧纱', '纬粗纱', '线印', '织入', '织稀', '经粗纱', '经跳花', '结洞', '缺纬', '缺经', '耳朵', '蒸呢印', '跳花', '边扎洞', '边白印', '边缺纬', '边缺经', '边针眼', '黄渍']
    '''
    class_indexes = [i for i in range(len(class_names))]
    '''
    class_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]
    '''
    class_name_index_dict = {}
    for i in range(len(class_names)):
        class_name_index_dict[class_names[i]] = i
    '''
    class_name_index_dict = {'修印': 0, '剪洞': 1, '厚段': 2, '厚薄段': 3, '吊弓': 4, '吊纬': 5, ... }
    '''
    class_index_name_dict = {}
    for i in range(len(class_indexes)):
        class_index_name_dict[i] = class_names[i] 
    '''
    class_index_name_dict = {0: '修印', 1: '剪洞', 2: '厚段', 3: '厚薄段', 4: '吊弓', 5: '吊纬',...}
    '''

    patch_img_index_dict = {}
    for class_name in class_names:
        patch_img_index_dict[class_name_index_dict[class_name]] = [item for item in os.listdir(root_path+'/'+class_name) if '.jpg' in str(item)]
    '''
    patch_img_index_dict = {0: ['J01_2018.06.16 10_24_16.jpg'], 1: ['J01_2018.06.22 08_45_25.jpg', 'J01_2018.06.23 09_09_55.jpg', 'J01_2018.06.23 13_28_32.jpg', 'J01_2018.06.26 09_55_27.jpg', 'J01_2018.06.26 14_01_55.jpg'], 
    2: ['J01_2018.06.13 13_52_56.jpg'], 3: ['J01_2018.06.16 10_35_51.jpg'], 4: ['J01_2018.06.16 10_51_31.jpg', 'J01_2018.06.17 14_37_37.jpg', 'J01_2018.06.27 13_29_13.jpg'],
    '''

    return class_names , class_indexes , class_name_index_dict , class_index_name_dict , patch_img_index_dict

# class_names , class_indexes , class_name_index_dict , class_index_name_dict , patch_img_index_dict = get_dataset_info(ORIGIN_PATH)

def get_img_full_path(root,class_name,image_name):        
    return root+'/'+class_name+'/'+image_name
 
        
def copy_imgs_of_class_to_des(root,class_name,source_img_names,des_root):
    des_folder = des_root+'/'+class_name
    if not os.path.exists(des_folder):
        os.makedirs(des_folder)
    for item in source_img_names:
        shutil.copy(get_img_full_path(root,class_name,item),des_folder)


def generate_train_val_split(class_names , class_indexes , class_name_index_dict , class_index_name_dict , 
                                patch_img_index_dict , origin_path, train_path, val_path ,ratio = 0.2):
    if(os.path.exists(train_path)): 
        shutil.rmtree(train_path,True)
    if(os.path.exists(val_path)):
        shutil.rmtree(val_path,True)

    for index in patch_img_index_dict.keys():
        class_name_s = class_index_name_dict[index]
        patch_images_of_this_class = patch_img_index_dict[index]
        random.shuffle(patch_images_of_this_class)
        count = len(patch_images_of_this_class)
        quant_for_val = math.ceil(count*ratio)
        quant_for_train = count - quant_for_val
        if quant_for_train == 0:
            quant_for_train = 1
        patches_for_val = patch_images_of_this_class[0:quant_for_val]
        patches_for_train = patch_images_of_this_class[-quant_for_train:]

        copy_imgs_of_class_to_des(origin_path,class_name_s,patches_for_val,val_path)
        copy_imgs_of_class_to_des(origin_path,class_name_s,patches_for_train,train_path)


def get_img_full_path(root,class_name,image_name):        
    return root+'/'+class_name+'/'+image_name


def copy_imgs_of_class_to_des(root,class_name,source_img_names,des_root):
    des_folder = des_root+'/'+class_name
    if not os.path.exists(des_folder):
        os.makedirs(des_folder)
    for item in source_img_names:
        shutil.copy(get_img_full_path(root,class_name,item),des_folder)


def generate_train_val_split(class_names , class_indexes , class_name_index_dict , 
                                class_index_name_dict , patch_img_index_dict , origin_path, 
                                train_path, val_path ,ratio = 0.2):
    if(os.path.exists(train_path)): 
        shutil.rmtree(train_path,True)
    if(os.path.exists(val_path)):
        shutil.rmtree(val_path,True)

    for index in patch_img_index_dict.keys():
        class_name_s = class_index_name_dict[index]
        patch_images_of_this_class = patch_img_index_dict[index]
        random.shuffle(patch_images_of_this_class)
        count = len(patch_images_of_this_class)
        quant_for_val = math.ceil(count*ratio)
        quant_for_train = count - quant_for_val
        if quant_for_train == 0:
            quant_for_train = 1
        patches_for_val = patch_images_of_this_class[0:quant_for_val]
        patches_for_train = patch_images_of_this_class[-quant_for_train:]

        copy_imgs_of_class_to_des(origin_path,class_name_s,patches_for_val,val_path)
        copy_imgs_of_class_to_des(origin_path,class_name_s,patches_for_train,train_path)


def generate_train_data_for_ds(train_root, class_names , class_indexes , 
                                class_name_index_dict , class_index_name_dict , 
                                patch_img_index_dict, num_per_class = 5):
    result = {}
    for index in patch_img_index_dict.keys():
        class_name = class_index_name_dict[index]
        return_list = []
        img_names = patch_img_index_dict[index]
        img_paths = [train_root +'/'+class_name+'/'+img_name for img_name in img_names]
        if len(img_paths)>num_per_class:
            shuffle(img_paths)
            return_list = img_paths[0:num_per_class]
        else:
            if len(img_paths) is not 0:
                round = math.floor( num_per_class / len(img_paths) )
                diff = num_per_class - len(img_paths)*round
                for i in range(round):
                    return_list.extend(img_paths)
                seq = [i for i in range(len(img_paths))]
                random.shuffle(seq)
                for x in seq[0:diff]:
                    return_list.append(img_paths[x])
        random.shuffle(return_list)
        result[index] = return_list
    return result


def generate_val_data_for_ds(val_root, class_names , class_indexes , class_name_index_dict , 
                                class_index_name_dict , patch_img_index_dict):
    result = {}
    for index in patch_img_index_dict.keys():
        class_name = class_index_name_dict[index]
        return_list = []
        img_names = patch_img_index_dict[index]
        img_paths = [val_root +'/'+class_name+'/'+img_name for img_name in img_names]
        return_list = img_paths
        result[index] = return_list
    return result