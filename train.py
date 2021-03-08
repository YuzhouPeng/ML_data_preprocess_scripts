# -*- coding: utf-8 -*-
import numpy as np
import os,sys,csv
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib

import shutil
import math,random
import data_pre_process as dpp
import datetime

"""
====================================================================================
<<1.数据预处理>>
====================================================================================

"""

ORIGIN_PATH = 'C:\\Users\\admin\\Desktop\\雪浪\\dataset\\detect_patch_origin'
TRAIN_PATH = 'C:\\Users\\admin\\Desktop\\雪浪\\dataset\\train'
VAL_PATH = 'C:\\Users\\admin\\Desktop\\雪浪\\dataset\\val'

# =====================================================
# 预处理原始patch图像，split成train和val
# =====================================================
def pre_process_origin_data():
    
    # 获取未split之前的数据目录分类结构字典
    class_names , class_indexes , class_name_index_dict , class_index_name_dict , patch_img_index_dict = dpp.get_dataset_info(ORIGIN_PATH)

    # 将原始数据split成Train和Val两个目录,按照ratio比例提取Val数据
    dpp.generate_train_val_split(class_names , class_indexes , class_name_index_dict , class_index_name_dict , 
                                patch_img_index_dict, ORIGIN_PATH,TRAIN_PATH, VAL_PATH , ratio=0.2)


# =====================================================
# 预处理train和val数据，填充图片路径以获得平衡的类型数据
# =====================================================
def pre_process_train_val():

    # 获取Train的目录结构信息
    class_names_train , class_indexes_train , class_name_index_dict_train , class_index_name_dict_train , patch_img_index_dict_train = dpp.get_dataset_info(TRAIN_PATH)

    # 通过获取的Train目录结构信息按照num_per_class的设定值填充类别数据,并将文件名转换成绝对路径放入字典
    train_dict = dpp.generate_train_data_for_ds(TRAIN_PATH, class_names_train , class_indexes_train , 
                                                class_name_index_dict_train , class_index_name_dict_train , 
                                                patch_img_index_dict_train, num_per_class= 2500)

    # 获取Val的目录结构信息
    class_names_val , class_indexes_val , class_name_index_dict_val , class_index_name_dict_val , patch_img_index_dict_val = dpp.get_dataset_info(VAL_PATH)

    # 通过获取的Val目录结构信息按照num_per_class的设定值填充类别数据,并将文件名转换成绝对路径放入字典
    val_dict = dpp.generate_val_data_for_ds(VAL_PATH, class_names_val , class_indexes_val , class_name_index_dict_val ,class_index_name_dict_val , patch_img_index_dict_val)

    return train_dict, class_names_train , val_dict , class_names_val

#pre_process_origin_data()
train_dict, class_names_train , val_dict , class_names_val = pre_process_train_val()


"""
====================================================================================
<<2.tf.Dataset准备>>
====================================================================================


"""
# import tensorflow as tf
# AUTOTUNE = tf.data.experimental.AUTOTUNE

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

BATCH_SIZE = 128
IMG_WIDTH = 224
IMG_HEIGHT = 224
NUM_CLASS = len(train_dict.keys())

def count_image_num(dict):
    count = 0 
    for key in dict.keys():
        count = count + len(dict[key])
    return count

IMAGE_COUNT_TRAIN = count_image_num(train_dict)
IMAGE_COUNT_VAL = count_image_num(val_dict)


def process_train_val_dict(train_dict):
    filepaths = []
    labels = []
    for index in train_dict.keys():
        for item in train_dict[index]:
            filepaths.append(item)
            labels.append(index)
    return filepaths,labels

filepaths,labels = process_train_val_dict(train_dict)
filepaths_val,labels_val = process_train_val_dict(val_dict)

def show_batch(image_batch, label_batch):
    plt.figure(figsize=(5,10))
    for n in range(50):
        ax = plt.subplot(5,10,n+1)
        plt.imshow(image_batch[n])
        plt.title(class_names_val[label_batch[n]])
        plt.axis('off')
    plt.show()

def decode_img(img):
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    return tf.image.resize(img, [IMG_WIDTH, IMG_HEIGHT])

def process_path(file_path,label):
    img = tf.io.read_file(file_path)
    img = decode_img(img)
    return img,label

def img_aug(img,label):
    # image = tf.expand_dims(img,0)
    return tf.image.random_flip_left_right(img),label

def prepare_train_val_ds(filepaths,labels):
    global BATCH_SIZE
    paths_ds = tf.data.Dataset.from_tensor_slices(filepaths)
    labels_ds = tf.data.Dataset.from_tensor_slices(labels)
    paths_labels_ds = tf.data.Dataset.zip((paths_ds,labels_ds))
    images_labels_ds = paths_labels_ds.shuffle(buffer_size=300000)
    
    ds = images_labels_ds.map(process_path, num_parallel_calls=AUTOTUNE)
    ds = ds.map(img_aug, num_parallel_calls=AUTOTUNE)

    ds = ds.repeat()
    ds = ds.batch(BATCH_SIZE)
    ds = ds.prefetch(buffer_size = AUTOTUNE)

    return ds

train_ds = prepare_train_val_ds(filepaths,labels)
val_ds = prepare_train_val_ds(filepaths_val,labels_val)

for img,label in train_ds.take(1):
    print("Image shape: ", img.numpy())
    print("Label: ", label.numpy())
image_batch, label_batch = next(iter(train_ds))
show_batch(image_batch.numpy(), label_batch.numpy())

for img,label in val_ds.take(2):
    print("Image shape: ", img.numpy().shape)
    print("Label: ", label.numpy())
image_batch, label_batch = next(iter(val_ds))
show_batch(image_batch.numpy(), label_batch.numpy())

exit()


"""
====================================================================================
<<3.建模>>
====================================================================================


# """
#
# from tensorflow.keras.layers import concatenate, Activation, GlobalAveragePooling2D, Flatten
# from tensorflow.keras.layers import Dense, Input, Dropout, MaxPooling2D, Concatenate, GlobalMaxPooling2D, GlobalAveragePooling2D
# from tensorflow.keras.models import Model
# from tensorflow.keras.applications.nasnet import NASNetMobile
#
# nasnet = NASNetMobile(include_top=False, input_shape=(224, 224, 3))
# x1 = GlobalMaxPooling2D()(nasnet.output)
# x2 = GlobalAveragePooling2D()(nasnet.output)
# x3 = Flatten()(nasnet.output)
# out = Concatenate(axis=-1)([x1, x2, x3])
# out = Dropout(0.5)(out)
# predictions = Dense(NUM_CLASS, activation="softmax",name = 'predictions')(out)
# model = Model(inputs=nasnet.input, outputs=predictions)
#
# model.trainable = True
# # for layer in model.layers[:-3]:
# #   layer.trainable = False
#
# optimizer = tf.keras.optimizers.Adam(lr = 0.0001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
# loss_func = tf.keras.losses.SparseCategoricalCrossentropy()

# train_loss = tf.keras.metrics.Mean(name='train_loss')
# train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')

# val_loss = tf.keras.metrics.Mean(name='test_loss')
# val_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='test_accuracy')

# model.summary()

# exit()

# """
# ====================================================================================
# <<3.训练>>
# ====================================================================================
#
# 这边使用keras的训练方法来训练网络
#
# """
#
# model.compile(loss=loss_func,
#               optimizer = optimizer,
#               metrics = ['accuracy'])
#
#
# steps_per_epoch = math.ceil(IMAGE_COUNT_TRAIN/BATCH_SIZE)
# validation_steps = math.ceil(IMAGE_COUNT_VAL/BATCH_SIZE)
#
# checkpoint_path = 'C:/mynuts/cmsr/cloth_inspection/ckp/cp.ckpt'
# checkpoint_dir = os.path.dirname(checkpoint_path)
#
# print(checkpoint_dir)
#
#
# # exit()
# cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
#                                                  save_weights_only=True,
#                                                  save_best_only=True,
#                                                  monitor='val_accuracy',
#                                                  mode='max',
#                                                  verbose = 1)
#
# log_dir="logs\\fit\\" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
#
# tb_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, update_freq='batch',histogram_freq=0, write_graph=True, write_images=True)
#
# # model.load_weights(checkpoint_path)
#
# model.fit(train_ds,
#         epochs=20,
#         steps_per_epoch=steps_per_epoch,
#         # validation_split = 0.2,
#         validation_data = val_ds,
#         validation_steps = validation_steps,
#         callbacks = [cp_callback,tb_callback],
#         workers=1,
#         use_multiprocessing=False
#         )
#
# # print()
# # print()
# # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>evaluate>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
#
# # model.load_weights(checkpoint_path)
#
# # loss,acc = model.evaluate(val_ds,steps=validation_steps)
# # print("Restored model, accuracy: {:5.2f}%".format(100*acc))


  