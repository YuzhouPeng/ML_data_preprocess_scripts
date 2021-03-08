import xml.etree.ElementTree as ET
import os,cv2
import glob,split_train_val
xmlpath ="/home/pengyuzhou/data_gangyin/gangyin/test/04.15_499_image_without_label/"
resultpath = "/home/pengyuzhou/data_gangyin/gangyin/test/04.15_499_test_crop/"
outputpath = "/home/pengyuzhou/data_gangyin/gangyin/test/"

dict = {}
filenamelist = []
def parse_xml(txt_path,imgpath,filename):
    '''
    输入：
        xml_path: xml的文件路径
    输出：
        从xml文件中提取bounding box信息, 格式为[[x_min, y_min, x_max, y_max, name]]并输出图像
    '''
    global count

    f = open(txt_path,"r")
    if os.path.exists(imgpath):
        line = f.readlines()
        line = [l.strip() for l in line]
        img = cv2.imread(imgpath)
        for l in line:
            count+=1
            x_min,y_min,x_max,y_max = l.split(" ")
            if int(y_min)>=0 and int(y_max)>=0 and int(x_min)>=0 and int(x_max)>=0:
                newimg = img[int(y_min):int(y_max), int(x_min):int(x_max)]
                # print(filename)
                #按标签建立文件夹输出
                # if not os.path.exists(resultpath+"\\"+str(name)+"\\"):
                #     os.mkdir(resultpath+"\\"+str(name)+"\\")
                # cv2.imwrite(resultpath+"\\"+str(name)+"\\"+filename[:-3]+str(ix)+".jpg",newimg)
                #直接输出到文件夹中 格式为label+label类型下的第i张
                
                dict[filename[:-4]+"_"+str(count)+".jpg"] =  str(x_min)+" "+ str(y_min)+" "+ str(x_max)+" "+ str(y_max)+" "

                # string = str(count)+" "+str(name)
                # filenamelist.append(string)
                cv2.imwrite(resultpath+filename[:-4]+"_"+str(count)+".jpg",newimg)


if __name__ == "__main__":
    count = 0

    for parent,_,files in os.walk(xmlpath):
        for file in files:
            if file[-3:]=="txt":
                singlexmlpath = os.path.join(parent,file)
                filepath = singlexmlpath[:-3]+"jpg"
                parse_xml(singlexmlpath,filepath,file)
    for parent,_,files in os.walk(resultpath):
        for file in files:
            # count = int(file.split(".")[0])
            name = dict[file]
            string = file+" "+str(name)
            filenamelist.append(string)
    for file_name in filenamelist:
        # "a"表示以不覆盖的形式写入到文件中,当前文件夹如果没有"save.txt"会自动创建
        with open(outputpath + "04.15_gangying_coord.txt", "a") as f:
            f.write(file_name + "\n")
            # print(file_name)
        f.close()