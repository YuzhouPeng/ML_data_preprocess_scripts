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
import yolov3_tf2


# --------------------------------------------------


##剪切图像至crop文件夹


def crop_image(img, file_name, cut_size, flag, rwidth, rheight, resultpath, result, zoomrate):
    '''
    输入：
        大图的文件路径
    输出：
        剪切过后的图片
    '''
    if flag == True:
        jpgpath = resultpath + '/' + str(rwidth) + "X" + str(rheight) + '/' + file_name + "/"
        if not os.path.exists(jpgpath):
            os.makedirs(jpgpath)
        rwidth = int(rwidth / zoomrate)
        rheight = int(rheight / zoomrate)
        img = cv2.resize(img, (rwidth, rheight))
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        print(img)
        print(jpgpath)
        rw = rwidth % cut_size
        widthcount = int((rwidth - rw) / cut_size)
        rh = rheight % cut_size
        heicount = int((rheight - rh) / cut_size)
        print("开始剪切： {}".format(file_name))
        #######----------------------
        croppedimg = []
        for w in range(widthcount + 1):
            for h in range(heicount + 1):
                if w != widthcount and h != heicount:
                    cropped = img.crop(
                        (w * cut_size, h * cut_size, w * cut_size + cut_size, h * cut_size + cut_size))
                    croppedimg.append([cropped, (h), (w)])
                    cropped.save(jpgpath + str(h) + '_' + str(w) + '.jpg')
                elif w == widthcount and h != heicount:
                    cropped = img.crop((rwidth - cut_size, h * cut_size, rwidth, h * cut_size + cut_size))
                    croppedimg.append([cropped, (h), (w)])
                    cropped.save(jpgpath + str(h) + '_' + str(w) + '.jpg')
                elif w != widthcount and h == heicount:
                    cropped = img.crop((w * cut_size, rheight - cut_size, w * cut_size + cut_size, rheight))
                    croppedimg.append([cropped, (h), (w)])
                    cropped.save(jpgpath + str(h) + '_' + str(w) + '.jpg')
                elif w == widthcount and h == heicount:
                    cropped = img.crop((rwidth - cut_size, rheight - cut_size, rwidth, rheight))
                    croppedimg.append([cropped, (h), (w)])
                    cropped.save(jpgpath + str(h) + '_' + str(w) + '.jpg')
        print("结束剪切")
        result.append([croppedimg, file_name, rwidth, rheight, widthcount, heicount, zoomrate])


# 将检测出的图像ROI绘制到大图上

def merge_pics(flag, cut_size, origin_large_img, image_crop_results, model, class_names, output_path, file, pic_path,
               folder_path):
    # output_path, cut_size, True, coords, class_names,filename,rwidth,rheight,widthcount,heicount,zoomrate
    # origin_large_img, output_path, cut_size, flag, coords, class_names,filename,rwidth,rheight,widthcount,heicount,zoomrate
    # def merge_pics(flag,origin_large_img,image_crop_results,model,class_names,output_path):
    # 根据坐标画出ROI图像
    def draw_outputs(img, coord, row, col, rwidth, rheight, widthcount, heicount, zoomrate):
        # zoomrate =1
        # new method
        x0, y0, x1, y1 = coord[0], coord[1], coord[2], coord[3]
        if col != widthcount and row != heicount:
            x0y0 = tuple(((x0 + col * cut_size) * zoomrate, (y0 + row * cut_size) * zoomrate))
            x1y1 = tuple(((x1 + col * cut_size) * zoomrate, (y1 + row * cut_size) * zoomrate))
            img = cv2.rectangle(img,
                                x0y0, x1y1,
                                (255, 0, 0), 2)
            img = cv2.putText(img, '{} {:.4f}'.format(
                coord[4], coord[5]),
                              ((x1 + col * cut_size) * zoomrate, (y1 + row * cut_size) * zoomrate),
                              cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                              (0, 0, 255), 2)
        elif row != heicount and col == widthcount:
            x0y0 = tuple(((rwidth - cut_size + x0) * zoomrate, (y0 + row * cut_size) * zoomrate))
            x1y1 = tuple(((rwidth - cut_size + x1) * zoomrate, (y1 + row * cut_size) * zoomrate))
            img = cv2.rectangle(img,
                                x0y0, x1y1,
                                (255, 0, 0), 2)
            img = cv2.putText(img, '{} {:.4f}'.format(
                coord[4], coord[5]),
                              ((rwidth - cut_size + x1) * zoomrate, (y1 + row * cut_size) * zoomrate),
                              cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                              (0, 0, 255), 2)
        elif row == heicount and col != widthcount:
            x0y0 = tuple(((x0 + col * cut_size) * zoomrate, (rheight - cut_size + y0) * zoomrate))
            x1y1 = tuple(((x1 + col * cut_size) * zoomrate, (rheight - cut_size + y1) * zoomrate))
            img = cv2.rectangle(img,
                                x0y0, x1y1,
                                (255, 0, 0), 2)
            img = cv2.putText(img, '{} {:.4f}'.format(
                coord[4], coord[5]),
                              ((x1 + col * cut_size) * zoomrate, (rheight - cut_size + y1) * zoomrate),
                              cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                              (0, 0, 255), 2)
        elif row == heicount and col == widthcount:
            x0y0 = tuple(((rwidth - cut_size + x0) * zoomrate, (rheight - cut_size + y0) * zoomrate))
            x1y1 = tuple(((rwidth - cut_size + x1) * zoomrate, (rheight - cut_size + y1) * zoomrate))
            img = cv2.rectangle(img,
                                x0y0, x1y1,
                                (255, 0, 0), 2)
            img = cv2.putText(img, '{} {:.4f}'.format(
                coord[4], coord[5]),
                              (rwidth - cut_size + x1, rheight - cut_size + y1), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
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
        ori_img1 = (origin_large_img)
        ori_img1 = cv2.resize(ori_img1, (2560, 1920))
        zoom_coord_results = []
        for croppedimglist, filename, rwidth, rheight, widthcount, heicount, zoomrate in image_crop_results:
            origin_large_img = Image.open(pic_path)
            origin_large_img = cv2.cvtColor(np.asarray(origin_large_img), cv2.COLOR_RGB2BGR)
            origin_large_img = cv2.resize(origin_large_img, (2560, 1920))
            ori_img = (origin_large_img)
            # coords数组保存每张图检测框相关信息
            coords = []
            path = folder_path + str(rwidth) + "X" + str(rheight) + '/' + file + "/"
            if not os.path.exists(path):
                os.makedirs(path)
            # 读取crop文件夹中的文件，获取文件和检测框的信息
            # croppedimg为二维数组，每个元素含有剪切后图像，row和col
            for cropimg, row, col in croppedimglist:
                img = cv2.cvtColor(np.asarray(cropimg), cv2.COLOR_RGB2BGR)
                img = tf.expand_dims(img, 0)
                img = transform_images(img, cut_size)
                tim1 = time.time()
                boxes, scores, classes, nums = model(img)
                # 重新读取剪切图像，保存图像文件，坐标信息至coords数组中
                img = cv2.cvtColor(np.asarray(cropimg), cv2.COLOR_RGB2BGR)
                coords.append([boxes, scores, classes, nums, img, row, col])
                tim2 = time.time()
                print("model process time : {}".format(tim2 - tim1))
                # 将切割后的图绘制检测框并保存
                img = cv2.cvtColor(np.asarray(cropimg), cv2.COLOR_RGB2BGR)
                img = yolov3_tf2.utils.draw_outputs(img, (boxes, scores, classes, nums), class_names)
                cut_file_name = str(row) + "_" + str(col) + "_" + (filename)
                cv2.imwrite(path + cut_file_name, img)

            # 获取图片集地址下的所有图片名称
            print("-------------开始绘制检测框: {}------------".format(file))
            # print(coords)
            for coord in (coords):
                output = (coord[0], coord[1], coord[2], coord[3])
                # print(coord[4])
                img_coord = coord_outputs(coord[4], output, class_names)
                # print(img_coord)
                row, col = coord[5], coord[6]
                for img_c in img_coord:
                    print(img_c)
                    zoom_coord_results.append([img_c, row, col, rwidth, rheight, widthcount, heicount, zoomrate])
                    draw_outputs(ori_img, img_c, row, col, rwidth, rheight, widthcount, heicount, zoomrate)
            # print(resultlist)
            print("---------end---------")
            output_final_path = output_path + '/' + str(rwidth) + "X" + str(rheight) + '/' + file + '/'
            if not os.path.exists(output_final_path):
                os.makedirs(output_final_path)
            cv2.imwrite(output_final_path + file, ori_img)
        for img_c, row, col, rwidth, rheight, widthcount, heicount, zoomrate in zoom_coord_results:
            draw_outputs(ori_img1, img_c, row, col, rwidth, rheight, widthcount, heicount, zoomrate)
        cv2.imwrite("/home/sycv/workplace/pengyuzhou/yolov3-tf2/output_zoom_result/" + filename[-6:], ori_img1)


# ----------------------------------------------------
def get_frames(video_full_path, frame_output_path):
    cap = cv2.VideoCapture(video_full_path)
    print(cap.isOpened())
    frame_count = 1
    success = True
    while (success):
        success, frame = cap.read()
        # print('Read a new frame: ', success)

        params = []
        # params.append(cv.CV_IMWRITE_PXM_BINARY)
        params.append(1)
        if (frame_count % 4) == 0:
            cv2.imwrite(frame_output_path + "_%d.jpg" % frame_count, frame, params)
            print('捕捉到帧 {}'.format(frame_count))
        frame_count = frame_count + 1


def detect_faults(file_path, cut_size, r_width, r_height, zoomratelist):
    # 全局变量
    # 剪切后原图及剪切后图像数组
    # crop函数读取大图路径
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
    # 输出画完检测框之后的图片
    output_path = '/home/sycv/workplace/pengyuzhou/yolov3-tf2/output_pic/'

    anchors = yolo_anchors
    anchor_masks = yolo_anchor_masks

    origin_model = YoloV3(input_size, training=True, classes=80)

    model = YoloV3_with_trained_darknet(origin_model, size=416, channels=3, anchors=anchors,
                                        masks=anchor_masks, classes=num_classes, training=False)

    model.load_weights(weights_path)
    print(weights_path)

    class_names = [c.strip() for c in open('class.names').readlines()]
    print('classes loaded')
    t1 = time.time()
    # 开始读取文件夹中的原图
    for parent, _, files in os.walk(file_path):
        for file in files:
            image_crop_results = []
            pic_path = os.path.join(parent, file)
            origin_large_img = Image.open(pic_path)
            origin_large_img = cv2.cvtColor(np.asarray(origin_large_img), cv2.COLOR_RGB2BGR)
            origin_large_img = cv2.resize(origin_large_img, (2560, 1920))
            print("-------------开始剪切程序------------")
            for zoomrate in zoomratelist:
                crop_image(origin_large_img, file, cut_size, True, r_width, r_height, resultpath, image_crop_results,
                           zoomrate)
            print("------------结束剪切程序--------")
            # 调用绘制检测框函数
            merge_pics(True, input_size, origin_large_img, image_crop_results, model, class_names, output_path, file,
                       pic_path, folder_path)

        # 将剪切图片检测出的ROI绘制到大图上，保存至output_path
    t2 = time.time()
    print("total time: {}".format(t2 - t1))


if __name__ == '__main__':
    video_full_path = "/home/sycv/workplace/pengyuzhou/yolov3-tf2/video/video.avi"
    frame_output_path = "/home/sycv/workplace/pengyuzhou/yolov3-tf2/original_large_pic/"
    file_path = frame_output_path
    zoomlist = [1, 2, 4]

    get_frames(video_full_path, frame_output_path)
    detect_faults(file_path, 416, 2560, 1920, zoomlist)
