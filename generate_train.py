import os
from PIL import Image
from generate_xml import change2xml

base_path = r"/home/sycv/workplace/meixun/data_prepare"
list_file = os.path.join(base_path,  "data_pre", "data_preoriginal_remarked123.txt")
imgs_path = os.path.join(base_path, "data", "original_remarked") 
crop_size = 416

with open(list_file) as f:
    img_dataset = f.readlines()


for line in img_dataset:
    img_info = line.strip().split(',')
    img_name = img_info[0]
    img_name_temp, hzm = os.path.splitext(img_name)
    file_name = img_info[1]
    num_object = int(img_info[2])
    bbox_list = []
    img_path = os.path.join(imgs_path, file_name, img_name)
    img = Image.open(img_path)
    for i in range(num_object):
        # 4个坐标类型为字符类型
        xmin = int(img_info[3 + 5 * i])
        ymin = int(img_info[4 + 5 * i])
        xmax = int(img_info[5 + 5 * i])
        ymax = int(img_info[6 + 5 * i])
        label = img_info[7 + 5 * i]
        bbox = [xmin, ymin, xmax, ymax, label]
        bbox_list.append(bbox)
    while len(bbox_list) > 0:
        j = 0
        xmin_center = bbox_list[0][0]
        ymin_center = bbox_list[0][1]
        if xmin_center - (crop_size // 2) < 0:
            xmin_center = (crop_size // 2)
        elif ymin_center - (crop_size // 2) < 0:
            ymin_center = (crop_size // 2)
        elif xmin_center + (crop_size // 2) > 2560:
            xmin_center = 2560 - (crop_size // 2)
        elif ymin_center + (crop_size // 2) > 1920:
            xmin_center = 1920 - (crop_size // 2)
        xmin_temp = xmin_center - (crop_size // 2)
        ymin_temp = ymin_center - (crop_size // 2)
        img_new = img.crop((xmin_temp, ymin_temp, (xmin_temp + crop_size), (ymin_temp + crop_size)))
        if not os.path.exists(os.path.join(base_path, "data", "416", label)):
            os.mkdir(os.path.join(base_path, "data", "416", label))
        img_new.save(os.path.join(base_path, "data", "416", label, img_name_temp + '_' + str(j) + '.jpg'))
        bbox_list_last = []
        label_list_last = []
        bbox_list_copy = bbox_list.copy()
        for i in range(len(bbox_list_copy)):
            if (bbox_list_copy[i][0] >= xmin_temp) and (bbox_list_copy[i][0] <= xmin_temp + crop_size) and (bbox_list_copy[i][1] >= ymin_temp) and (bbox_list_copy[i][1] <= ymin_temp + crop_size):
                xmin_new = bbox_list_copy[i][0] - xmin_temp
                ymin_new = bbox_list_copy[i][1] - ymin_temp
                xmax_new = min(bbox_list_copy[i][2], xmin_temp + crop_size) - xmin_temp
                ymax_new = min(bbox_list_copy[i][3], ymin_temp + crop_size) - ymin_temp
                bbox_list_last.append([xmin_new, ymin_new, xmax_new, ymax_new])
                label_list_last.append([bbox_list_copy[i][4]])
                bbox_list.remove(bbox_list_copy[i])
        xml_dir = os.path.join(base_path, "data", "416", label)
        xml_name = os.path.join(base_path, "data", "416", label, img_name_temp + '_' + str(j) + '.xml')
        change2xml(image = xml_name, bbox = bbox_list_last, labels = label_list_last, save_dir = xml_dir, width = crop_size, height = crop_size)
        j += 1