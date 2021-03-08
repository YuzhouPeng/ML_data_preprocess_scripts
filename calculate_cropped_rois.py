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
    types = list()
    typecount = list()
    for parent, dirs, files in os.walk(xml_path):
        # 跳过test数据以及无瑕疵即正常的数据
        # print(parent)
        # print(dirs)
        filecount = 0
        if count==0:
            for dir in dirs:
                types.append(dir)
        if count>0:
            typecount.append(len(files))
            print(files)
        count+=1

    print(types)
    print(len(types))
    print(typecount)
    print(len(typecount))


    plt.figure(figsize=(30, 30))

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 步骤一（替换sans-serif字体）
    plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）
    # 绘图
    plt.bar(range(10), typecount, align='center', color='steelblue', alpha=0.8)
    # 添加轴标签
    plt.ylabel('数量')
    # 添加标题
    plt.title('瑕疵ROI区域剪切后数量对比图')
    # 添加刻度标签
    plt.xticks(range(10), types)
    # 设置Y轴的刻度范围
    plt.ylim([0, 1500])

    # 为每个条形图添加数值标签
    for x, y in enumerate(typecount):
        plt.text(x, y + 100, '%s' % round(y, 1), ha='center')  # 显示图形plt.show()
    # plt.show()


    plt.savefig("C:\\Users\\admin\\Desktop\\FiberFault_after_crop.jpg")


if __name__ == '__main__':
    parse_xml("C:\\Users\\admin\\Desktop\\dataset\\复赛data")
