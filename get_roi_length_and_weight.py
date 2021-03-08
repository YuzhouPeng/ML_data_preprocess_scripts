import xml.etree.ElementTree as ET
import os
import matplotlib.pyplot as plt
import collections


# 从xml文件中提取bounding box信息, 格式为[[x_min, y_min, x_max, y_max, name]]
def parse_xml(xml_path):
    '''
    输入：
        xml_path: xml的文件路径
    输出：
        从xml文件中提取bounding box信息, 格式为[[x_min, y_min, x_max, y_max, name]]
    '''
    coords = list()
    weights = list()
    heights = list()
    names = list()
    count = 0
    for parent, _, files in os.walk(xml_path):
        # 跳过test数据以及无瑕疵即正常的数据

        if 'test' in parent.split('_') or '正常' in parent.split('/') or 'xml' in parent.split('/'):
            continue
        for file in (files):

            file_name = os.path.join(parent, file)
            if file_name[-3:] == 'xml':
                count += 1
                tree = ET.parse(file_name)
                root = tree.getroot()
                objs = root.findall('object')

                for ix, obj in enumerate(objs):
                    name = obj.find('name').text
                    box = obj.find('bndbox')
                    x_min = int(box[0].text)
                    y_min = int(box[1].text)
                    x_max = int(box[2].text)
                    y_max = int(box[3].text)
                    coords.append([x_min, y_min, x_max, y_max, name])
    print(count)
    # return coords
    # get weights and length
    for cord in coords:
        weight = cord[2] - cord[0]
        hight = cord[3] - cord[1]
        weights.append(weight)
        heights.append(hight)
        names.append(cord[4])
    plt.figure(figsize=(30, 90))
    ax1 = plt.subplot(3, 1, 1)
    ax2 = plt.subplot(3, 1, 2)
    ax3 = plt.subplot(3, 1, 3)
    plt.sca(ax1)
    plt.title("布匹瑕疵 ROI 大小")
    plt.xlabel("width")
    plt.ylabel("height")
    plt.scatter(weights, heights)
    counter = collections.Counter(names)
    namecount = list()
    namelist = list()
    for name in counter.keys():
        namelist.append(name)
        namecount.append(counter[name])

    plt.sca(ax2)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 步骤一（替换sans-serif字体）
    plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）
    plt.title("布匹瑕疵种类百分比")
    plt.pie(namecount, labels=namelist, autopct='%1.1f%%', shadow=False, startangle=150)
    plt.axis('equal')
    plt.sca(ax3)
    plt.title("布匹瑕疵频率分布图")
    plt.hist(names, bins=44, normed=1, cumulative=0, facecolor="grey", edgecolor="black", alpha=0.7)
    plt.savefig("C:\\Users\\admin\\Desktop\\FiberFault.jpg")


if __name__ == '__main__':
    parse_xml("C:\\Users\\admin\\Desktop\\雪浪\\初赛1\\xuelang_round1_train_part2_20180705")
