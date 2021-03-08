import os
import xml.etree.ElementTree as ET
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


# --------------------------------------------------


def merge_pics(origin_path, output_path, cut_size, flag, coords, class_names, weightstep, heightstep):
    # 根据坐标画出ROI图像
    def draw_outputs(img, coord, row, col, result):
        # if len(coord)>0:
        x0, y0, x1, y1 = coord[0], coord[1], coord[2], coord[3]
        result.append(coord)
        x0y0 = tuple((x0 + col * weightstep, y0 + row * heightstep))
        x1y1 = tuple((x1 + col * weightstep, y1 + row * heightstep))
        img = cv2.rectangle(img,
                            x0y0, x1y1,
                            (255, 0, 0), 2)
        img = cv2.putText(img, '{} {:.4f}'.format(
            coord[4], coord[5]),
                          (x1 + col * weightstep, y1 + row * heightstep), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
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
        resultlist = []
        print("---------开始拼接---------")

        img = cv2.imread(origin_path)
        img = cv2.resize(img, (2560, 1920))
        # 获取图片集地址下的所有图片名称
        for coord in (coords):
            output = (coord[0], coord[1], coord[2], coord[3])
            # print(coord[4])
            filename = coord[4].split('_')
            row, col = int(filename[0]), int(filename[1].split(".")[0])

            img_coord = coord_outputs(coord[5], output, class_names)
            # print(img_coord)
            for img_c in img_coord:
                draw_outputs(img, img_c, row, col, resultlist)
        # print(resultlist)
        print("---------end---------")
        cv2.imwrite(output_path + '/result.jpg', img)


