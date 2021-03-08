import xml.etree.ElementTree as ET
import os
from PIL import Image
# 裁剪原图，可定制大小
# crop pics with custom size
def crop_image(file_path,cut_size,flag,rwidth,rheight,resultpath):
    '''
    输入：
        xml_path: xml的文件路径
    输出：
        剪切过后的图片
    '''
    if flag==True:
        for parent, _, files in os.walk(file_path):
            # 跳过test数据以及无瑕疵即正常的数据

            if 'test' in parent.split('_') or '正常' in parent.split('/') or 'xml' in parent.split('/'):
                continue
            for file in (files):

                file_name = os.path.join(parent, file)
                if file_name[-3:] == 'xml':

                    tree = ET.parse(file_name)
                    root = tree.getroot()
                    name = ''
                    objs = root.findall('object')
                    for ix, obj in enumerate(objs):
                        name= obj.find('name').text+'_'
                    jpgpath = resultpath+str(file[:-4])+'_'+name+'\\'
                    # img = Image.open(file_name[:-3]+'jpg')
                    os.mkdir(jpgpath)
                    img= Image.open(file_name[:-3]+'jpg')
                    img = img.resize((rwidth,rheight))
                    weight = img.size[0]
                    print(weight)
                    hight = img.size[1]
                    print(hight)
                    print(img)
                    weightcount = int(weight/cut_size)
                    heightcount = int(hight/cut_size)
                    print(jpgpath)
                    #######----------------------

                    ######----------------------------
                    for w in range(weightcount+1):
                        for h in range(heightcount+1):
                            if w!=weightcount and h !=heightcount:
                                cropped = img.crop((w * cut_size, h * cut_size, (w + 1) * cut_size, (h + 1) * cut_size))
                                # # img[y_min:y_min+h*cut_size,x_min:x_min+w*cut_size]
                                cropped.save(jpgpath +  str(w) + '_' + str(h) + '.jpg')
                            elif w==weightcount and h ==heightcount:
                                cropped = img.crop((weight-416,hight-416,weight,hight))
                                cropped.save(jpgpath +  str(weightcount) + '_' + str(heightcount) + '.jpg')
                            elif w==weightcount:
                                cropped = img.crop((weight-416,h*cut_size,weight,(h+1)*cut_size))
                                cropped.save(jpgpath + str(weightcount) + '_' + str(h) + '.jpg')
                            elif h==heightcount:
                                cropped = img.crop((w*cut_size,hight-416,(w+1)*cut_size,hight))
                                cropped.save(jpgpath +  str(w) + '_' + str(heightcount) + '.jpg')

def remove_pics(file_path,string):
    for parent, _, files in os.walk(file_path):
        for file in (files):
            if len(str(file))==len(string):
                os.remove(os.path.join(parent, file))

if __name__ == '__main__':
    string = "J01_2018.06.22 09_57_59.jpg"
    #文件夹路径
    path = "C:\\Users\\admin\\Desktop\\雪浪\\chusai\\xuelang_round1_train_part2_20180705"

    #剪切文件
    crop_image(path,416,True,2560,1920,"C:\\Users\\admin\\Desktop\\雪浪\\chusai\\xuelang_data\\crop\\")
    #去除原图和XML文件
    # remove_pics(path,string)
