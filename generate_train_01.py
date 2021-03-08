import os
import numpy as np
import random
from PIL import Image
from generate_xml import change2xml

base_path = "C:\\Users\\admin\\Desktop\\"
label_file = os.path.join(base_path,   "large_pics_remarked123.txt")
imgs_path = os.path.join(base_path,  "large_pics")
path_416 = os.path.join(base_path, "data/416")
crop_size = 416
with open(label_file) as f:
    lines = f.readlines()
# 遍历每一行
for line in lines:
    img_info = line.strip().split(',')
    img_name = img_info[0]
    print(img_name)
    img_name_temp, hzm = os.path.splitext(img_name)
    file_name = img_info[1]
    num_object = int(img_info[2])
    bbox_list = []
    img_path = os.path.join(imgs_path, file_name, img_name)
    img = Image.open(img_path)
    width = img.width
    height = img.height
    print("总共有" + str(num_object) + "个瑕疵")             
    # 4个坐标类型为字符类型
    for i in range(num_object):
        print("第" + str(i) + "个瑕疵")
        xmin = img_info[3 + 5 * i]
        ymin = img_info[4 + 5 * i]
        xmax = img_info[5 + 5 * i]
        ymax = img_info[6 + 5 * i]
        label = img_info[7 + 5 * i]
        w, h = int(xmax) - int(xmin), int(ymax) - int(ymin)
        # 都小于420
        # 中心点坐标
        cent_coord = np.array(
            [int(ymin) + (int(ymax) - int(ymin)) // 2, int(xmin) + (int(xmax) - int(xmin)) // 2])
        # 拿到图像左上角坐标
        # 判断是否超出原图范围
        if (cent_coord[0] - (crop_size // 2)) < 0:
            y1 = 0
        else:
            y1 = cent_coord[0] - (crop_size // 2)
        y2 = int(ymin)

        if (cent_coord[1] - (crop_size // 2)) < 0:
            x1 = 0
        else:
            x1 = cent_coord[1] - (crop_size // 2)
        x2 = int(xmin)
        # 随机在这个范围内产生一个左上角坐标   宽高都为crop_size  420
        # print("裁第" + str(j) + "个框")
        print(y1)
        print(y2)
        if y1!=y2+1:
            y_min_random = random.randint(y1, y2)
            x_min_random = random.randint(x1, x2)
            if y_min_random + crop_size > height:
                y_min_random = height - crop_size
                y_max_random = height
            else:
                y_max_random = y_min_random + crop_size

            if x_min_random + crop_size > width:
                x_min_random = width - crop_size
                x_max_random = width
            else:
                x_max_random = x_min_random + crop_size
            # 裁剪目标
            # img = Image.open(img_path_origin)
            img_crop = img.crop((x_min_random, y_min_random, x_max_random, y_max_random))
            boxList = []
            labelList = []
            for j in range(num_object):
                origin_x_min = int(img_info[3 + 5 * j])
                origin_y_min = int(img_info[4 + 5 * j])
                origin_x_max = int(img_info[5 + 5 * j])
                origin_y_max = int(img_info[6 + 5 * j])
                if ((origin_x_min >= x_min_random) and  (origin_x_min <= x_max_random)) and ((origin_y_min >= y_min_random) and (origin_y_min <= y_max_random)):
                    # 分别是瑕疵在原图的位置
                    new_x_min = origin_x_min - x_min_random
                    new_y_min = origin_y_min - y_min_random
                    new_x_max = min(origin_x_max, x_max_random) - x_min_random
                    new_y_max = min(origin_y_max, y_max_random) - y_min_random
                    box = [new_x_min, new_y_min, new_x_max, new_y_max]
                    boxList.append(box)
                    labelList.append([label])
            # img = img[y_begin:(y_begin + crop_size), x_begin:(x_begin + crop_size), ]
            if not os.path.exists(os.path.join(base_path, path_416, label)):
                os.mkdir(os.path.join(base_path, path_416, label))
            img_crop.save(os.path.join(base_path, path_416, label, img_name_temp + '_' + str(i) + '_' + ".jpg"))
            xml_dir = os.path.join(base_path, path_416, label)
            xml_name = img_name_temp + '_' + str(i) + '_' + ".jpg"
            change2xml(image = xml_name, bbox = boxList, labels = labelList, save_dir = xml_dir, width = crop_size, height = crop_size)