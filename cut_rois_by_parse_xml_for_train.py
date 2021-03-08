import xml.etree.ElementTree as ET
import os,cv2
import glob,split_train_val
xmlpath ="/home/pengyuzhou/data/2020.03.27data/3900_data/"
resultpath = "/home/pengyuzhou/data/2020.03.27data/train_3900_output/"
outputpath = "/home/pengyuzhou/data/2020.03.27data/"

dict = {}
filenamelist = []
def parse_xml(xml_path,imgpath,filename):
    '''
    输入：
        xml_path: xml的文件路径
    输出：
        从xml文件中提取bounding box信息, 格式为[[x_min, y_min, x_max, y_max, name]]并输出图像
    '''
    global count
    tree = ET.parse(xml_path)		
    root = tree.getroot()
    objs = root.findall('object')
    # print(imgpath)
    img = cv2.imread(imgpath)
    x = list()
    y = list()
    for ix, obj in enumerate(objs):
        count+=1
        name = obj.find('name').text
        box = obj.find('bndbox')
        x_min = int(box[0].text)
        y_min = int(box[1].text)
        x_max = int(box[2].text)
        y_max = int(box[3].text)
        newimg = img[y_min:y_max, x_min:x_max]
        # print(filename)
        #按标签建立文件夹输出
        # if not os.path.exists(resultpath+"\\"+str(name)+"\\"):
        #     os.mkdir(resultpath+"\\"+str(name)+"\\")
        # cv2.imwrite(resultpath+"\\"+str(name)+"\\"+filename[:-3]+str(ix)+".jpg",newimg)
        #直接输出到文件夹中 格式为label+label类型下的第i张
        dict[count] = str(name)

        # string = str(count)+" "+str(name)
        # filenamelist.append(string)
        cv2.imwrite(resultpath+str(count)+".jpg",newimg)


if __name__ == "__main__":
    count = 0

    for parent,_,files in os.walk(xmlpath):
        for file in files:
            if file[-3:]=="xml":
                singlexmlpath = os.path.join(parent,file)
                filepath = singlexmlpath[:-3]+"jpg"
                parse_xml(singlexmlpath,filepath,file)
    data_path = resultpath
    train_path = outputpath+ "train_data"
    valid_path = outputpath+ "valid_data"
    valid_size = 0.3
    split_train_val.split_train_test(data_path, train_path, valid_path, valid_size)
    for parent,_,files in os.walk(train_path):
        for file in files:
            count = int(file.split(".")[0])
            name = dict[count]
            string = str(count)+".jpg"+" "+str(name)
            filenamelist.append(string)
    for file_name in filenamelist:
        # "a"表示以不覆盖的形式写入到文件中,当前文件夹如果没有"save.txt"会自动创建
        with open(outputpath + "train_label.txt", "a") as f:
            f.write(file_name + "\n")
            # print(file_name)
        f.close()
    filenamelist = []
    for parent,_,files in os.walk(valid_path):
        for file in files:
            count = int(file.split(".")[0])
            name = dict[count]
            string = str(count)+".jpg"+" "+str(name)
            filenamelist.append(string)
    for file_name in filenamelist:
        # "a"表示以不覆盖的形式写入到文件中,当前文件夹如果没有"save.txt"会自动创建
        with open(outputpath + "valid_label.txt", "a") as f:
            f.write(file_name + "\n")
            # print(file_name)
        f.close()