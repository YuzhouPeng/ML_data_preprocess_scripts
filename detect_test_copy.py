import time
from absl import app, flags, logging
from absl.flags import FLAGS
import cv2
import numpy as np
import tensorflow as tf
import os
from PIL import Image
from yolov3_tf2.models import (
    YoloV3, YoloV3Tiny, YoloLoss,
    yolo_anchors, yolo_anchor_masks,
    yolo_tiny_anchors, yolo_tiny_anchor_masks
)

from yolov3_tf2.dataset import transform_images
from yolov3_tf2.utils import draw_outputs
from yolov3_tf2.models import YoloV3_with_trained_darknet


# --------------------------------------------------


##剪切图像至crop文件夹


def crop_image(file_path, cut_size, wstep, hstep, flag, rwidth, rheight, resultpath):
    '''
    输入：
        大图的文件路径
    输出：
        剪切过后的图片
    '''
    if flag == True:
        result = []
        for parent, _, files in os.walk(file_path):
            for file in (files):

                file_name = os.path.join(parent, file)

                jpgpath = resultpath+'/'+file+"/"
                if not os.path.exists(jpgpath):
                    os.mkdir(jpgpath)
                # img = Image.open(file_name[:-3]+'jpg')
                img = Image.open(file_name)
                img = img.resize((rwidth, rheight))
                weight = img.size[0]
                print(weight)
                hight = img.size[1]
                print(hight)
                print(img)
                remainwidth = weight - cut_size
                remainheight = hight - cut_size
                weightstep = int(remainwidth / wstep)
                print(weightstep)
                heightstep = int(remainheight / hstep)
                print(heightstep)
                print(jpgpath)

                rw = weight % cut_size
                widthcount = int((weight - rw) / cut_size)
                rh = hight % cut_size
                heicount = int((hight - rh) / cut_size)
                print("开始剪切： {}".format(file))
                #######----------------------
                croppedimg = []
                for w in range(widthcount + 1):
                    for h in range(heicount + 1):
                        if w != widthcount and h != heicount:
                            cropped = img.crop(
                                (w * cut_size, h * cut_size, w * cut_size + cut_size, h * cut_size + cut_size))
                            # # img[y_min:y_min+h*cut_size,x_min:x_min+w*cut_size]
                            croppedimg.append([cropped,(h),(w)])
                            cropped.save(jpgpath + str(h) + '_' + str(w) + '.jpg')
                        elif w == widthcount and h != heicount:
                            cropped = img.crop((2560 - 416, h * cut_size, 2560, h * cut_size + cut_size))
                            croppedimg.append([cropped,(h),(w)])
                            # # img[y_min:y_min+h*cut_size,x_min:x_min+w*cut_size]
                            cropped.save(jpgpath + str(h) + '_' + str(w) + '.jpg')
                        elif w != widthcount and h == heicount:
                            cropped = img.crop((w * cut_size, 1920 - 416, w * cut_size + cut_size, 1920))
                            croppedimg.append([cropped,(h),(w)])
                            # # img[y_min:y_min+h*cut_size,x_min:x_min+w*cut_size]
                            cropped.save(jpgpath + str(h) + '_' + str(w) + '.jpg')
                        elif w == widthcount and h == heicount:
                            cropped = img.crop((2560 - 416, 1920 - 416, 2560, 1920))
                            croppedimg.append([cropped,(h),(w)])
                            cropped.save(jpgpath + str(h) + '_' + str(w) + '.jpg')
                print("结束剪切")
                result.append([img,croppedimg,file])
        return result


# 将检测出的图像ROI绘制到大图上


def merge_pics(origin_large_img, output_path, cut_size, flag, coords, class_names,filename):
    # 根据坐标画出ROI图像
    def draw_outputs(img, coord, row, col):

        # new method
        x0, y0, x1, y1 = coord[0], coord[1], coord[2], coord[3]
        if col != 6 and row != 4:
            # result.append(coord)
            x0y0 = tuple((x0 + col * cut_size, y0 + row * cut_size))
            x1y1 = tuple((x1 + col * cut_size, y1 + row * cut_size))
            img = cv2.rectangle(img,
                                x0y0, x1y1,
                                (255, 0, 0), 2)
            img = cv2.putText(img, '{} {:.4f}'.format(
                coord[4], coord[5]),
                              (x1 + col * cut_size, y1 + row * cut_size), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                              (0, 0, 255), 2)
        elif row != 4 and col == 6:
            x0y0 = tuple((2560 - cut_size + x0, y0 + row * cut_size))
            x1y1 = tuple((2560 - cut_size + x1, y1 + row * cut_size))
            img = cv2.rectangle(img,
                                x0y0, x1y1,
                                (255, 0, 0), 2)
            img = cv2.putText(img, '{} {:.4f}'.format(
                coord[4], coord[5]),
                              (2560 - cut_size + x1, y1 + row * cut_size), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                              (0, 0, 255), 2)
        elif row == 4 and col != 6:
            x0y0 = tuple((x0 + col * cut_size, 1920 - cut_size + y0))
            x1y1 = tuple((x1 + col * cut_size, 1920 - cut_size + y1))
            img = cv2.rectangle(img,
                                x0y0, x1y1,
                                (255, 0, 0), 2)
            img = cv2.putText(img, '{} {:.4f}'.format(
                coord[4], coord[5]),
                              (x1 + col * cut_size, 1920 - cut_size + y1), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                              (0, 0, 255), 2)
        elif row == 4 and col == 6:
            x0y0 = tuple((2560 - cut_size + x0, 1920 - cut_size + y0))
            x1y1 = tuple((2560 - cut_size + x1, 1920 - cut_size + y1))
            img = cv2.rectangle(img,
                                x0y0, x1y1,
                                (255, 0, 0), 2)
            img = cv2.putText(img, '{} {:.4f}'.format(
                coord[4], coord[5]),
                              (2560 - cut_size + x1, 1920 - cut_size + y1), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                              (0, 0, 255), 2)

            # 根据模型输出结果获取ROII坐标

    def coord_outputs(img, outputs, class_names):
        result = []
        boxes, objectness, classes, nums = outputs
        boxes, objectness, classes, nums = boxes[0], objectness[0], classes[0], nums[0]
        wh = np.flip(img.shape[0:2])
        for i in range(nums):
            x1y1 = tuple((np.array(boxes[i][0:2]) * wh).astype(np.int32))
            x2y2 = tuple((np.array(boxes[i][2:4]) * wh).astype(np.int32))
            result.append([x1y1[0], x1y1[1], x2y2[0], x2y2[1], class_names[int(classes[i])], objectness[i]])
        return result

    if flag:
        img = cv2.cvtColor(np.asarray(origin_large_img),cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, (2560, 1920))
        # 获取图片集地址下的所有图片名称
        print("-------------开始绘制检测框: {}------------".format(filename))
        # print(coords)
        for coord in (coords):
            output = (coord[0], coord[1], coord[2], coord[3])
            # print(coord[4])
            img_coord = coord_outputs(coord[5], output, class_names)
            # print(img_coord)
            row, col = coord[6],coord[7]
            for img_c in img_coord:
                print(img_c)
                draw_outputs(img, img_c, row, col)
        # print(resultlist)
        print("---------end---------")
        cv2.imwrite(output_path + filename, img)


# ----------------------------------------------------


def detect_faults():
    # 全局变量
    #剪切后原图及剪切后图像数组
    image_crop_results = []
    # crop函数读取大图路径
    file_path = '/home/sycv/workplace/pengyuzhou/yolov3-tf2/original_large_pic/'
    # 接收crop函数剪切后的图像
    resultpath = '/home/sycv/workplace/pengyuzhou/yolov3-tf2/crop'
    num_classes = 2
    learning_rate = 1e-3
    # batch_size = 10
    epochs = 50
    input_size = 416
    # 从路径读取剪切后的图像放到模型中训练
    folder_path = '/home/sycv/workplace/pengyuzhou/yolov3-tf2/crop_result/'
    weights_path = 'checkpoints_eager/yolov3_train_one.tf'
    # 读取大图的路径
    origin_path = "/home/sycv/cv_workspace/yolov3-tf2-working/full_res_imgs/apple1.JPG"
    # 输出画完检测框之后的图片
    output_path = '/home/sycv/workplace/pengyuzhou/yolov3-tf2/output_pic/'
    cut_size = 416
    remainwidth = 2560 - cut_size
    remainheight = 1920 - cut_size
    step = 16
    weightstep = int(remainwidth / step)
    print(weightstep)
    heightstep = int(remainheight / step)
    print(heightstep)
    print(step)
    anchors = yolo_anchors
    anchor_masks = yolo_anchor_masks

    origin_model = YoloV3(input_size, training=True, classes=80)
    # origin_model.load_weights(weights_path)
    # origin_model.summary()

    model = YoloV3_with_trained_darknet(origin_model, size=416, channels=3, anchors=anchors,
                                        masks=anchor_masks, classes=num_classes, training=False)

    model.load_weights(weights_path)
    print(weights_path)

    class_names = [c.strip() for c in open('class.names').readlines()]
    print('classes loaded')

    for parent, _, files in os.walk(file_path):
        print("-------------开始剪切程序------------")
        image_crop_results = crop_image(file_path, 416, 16, 16, True, 2560, 1920, resultpath)
        print("------------结束剪切程序--------")

        # 读取crop文件夹中的文件，获取文件和检测框的信息
        #origin_pic为原图，croppedimglist为二维数组，每个元素含有剪切后图像，row和col
        for origin_pic,croppedimglist,filename in image_crop_results:
            origin_large_img = origin_pic
            #保存每张图检测框相关信息
            coords = []
            for cropimg,row,col in croppedimglist:

                img = cv2.cvtColor(np.asarray(cropimg),cv2.COLOR_RGB2BGR)
                img = tf.expand_dims(img, 0)
                img = transform_images(img, input_size)
                boxes, scores, classes, nums = model(img)
                # 重新读取剪切图像，保存图像文件，坐标信息至coords数组中
                img = cv2.cvtColor(np.asarray(cropimg),cv2.COLOR_RGB2BGR)
                coords.append([boxes, scores, classes, nums, cropimg, img,row,col])


                #将切割后的图绘制检测框并保存
                img = cv2.cvtColor(np.asarray(cropimg),cv2.COLOR_RGB2BGR)
                img = draw_outputs(img, (boxes, scores, classes, nums), class_names)
                path = folder_path+str(row)+"_"+str(col)+"_"+(filename)
                cv2.imwrite(path, img)


            merge_pics(origin_large_img, output_path, cut_size, True, coords, class_names,filename)

        # 将剪切图片检测出的ROI绘制到大图上，保存至output_path
if __name__ == '__main__':
    detect_faults()

