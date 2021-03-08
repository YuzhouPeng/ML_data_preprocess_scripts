from lxml.etree import Element, SubElement, tostring, fromstring
from xml.dom.minidom import parseString
import os

def save_xml(image_name, bbox, labels ,save_dir, width, height, channel=3):
    '''
    :param image_name:图片名
    :param bbox:对应的bbox
    :param save_dir:
    :param width:这个是图片的宽度，博主使用的数据集是固定的大小的，所以设置默认
    :param height:这个是图片的高度，博主使用的数据集是固定的大小的，所以设置默认
    :param channel:这个是图片的通道，博主使用的数据集是固定的大小的，所以设置默认
    :return:
    '''
    node_root = Element('annotation')

    # node_folder = SubElement(node_root, 'folder')
    # node_folder.text = 'JPEGImages'

    node_filename = SubElement(node_root, 'filename')
    node_filename.text = image_name

    source = SubElement(node_root, 'source')
    database = SubElement(source, 'database')
    database.text = "Unknown"

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = '%s' % width

    node_height = SubElement(node_size, 'height')
    node_height.text = '%s' % height

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '%s' % channel

    segmented = SubElement(node_root, 'segmented')
    segmented.text = '0'


    for box , label in zip(bbox, labels):
        left = box[0]
        top = box[1]
        right = box[2]
        bottom = box[3]
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        #此处根据输入的label格式来进行对应修改
        node_name.text = label
        pose = SubElement(node_object, 'pose')
        pose.text = "Unspecified"
        truncated = SubElement(node_object, 'truncated')
        truncated.text = "0"
        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'
        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = '%s' % left
        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = '%s' % top
        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = '%s' % right
        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = '%s' % bottom

    rough_string = tostring(node_root)
    root = fromstring(rough_string)

    xml = tostring(root, pretty_print=True, encoding = "utf-8").replace("  ".encode(), "	".encode())  
    # dom = parseString(xml)
    #此处根据需要修改文件后缀
    save_xml = os.path.join(save_dir, image_name.replace('png', 'xml'))
    with open(save_xml, 'wb') as f:
        f.write(xml)

    return


def change2xml(image, bbox, labels, save_dir, width, height):
    image_name = os.path.split(image)[-1]
    save_xml(image_name, bbox, labels, save_dir, width, height)
    return

if __name__ == "__main__":
    image = r"J01_2018.06.16 10_24_18.jpg"
    bbox = [[0, 7, 416, 116]]
    labels = [["白银"], ["你好"]]
    save_dir = r"/home/sycv/workplace/meixun/data_prepare/data_pre/VOC2007/Annotations"
    width = 1920
    height = 520
    change2xml(image, bbox, labels, save_dir, width, height)