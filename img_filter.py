import os, sys
import random
import shutil


if __name__ == '__main__':
    # open /textiles
    #原文件夹，包含多个瑕疵类别的子文件夹
    path = "C:\\Users\\admin\\Desktop\\select_11"
    #目标文件夹
    target_path = "C:\\Users\\admin\\Desktop\\select_results"


    folderpath_results = os.listdir(path)
    # print(folderpath_results)
    for folderpath in folderpath_results:
        target_pic_path = os.path.join(target_path + '/' + folderpath+'/')
        #自动创建瑕疵文件夹
        if not os.path.exists(target_pic_path):
            os.makedirs(target_pic_path)
        filepath = os.path.join(path,folderpath)
        print(filepath)
        files = os.listdir(filepath)
        # print(files)
        resultfilename = []
        for file in files:
            if file[-3:]=="jpg":
                resultfilename.append(file)
        print(resultfilename)
        random.shuffle(resultfilename)
        if len(resultfilename)>1:
            limit = int(0.3 * len(resultfilename))
            cnt = 0
            while cnt<limit:
                imgname = resultfilename.pop()
                source_pic_path = filepath+"/"+ imgname
                source_xml_path = source_pic_path[:-3]+"xml"

                shutil.move(source_pic_path, target_pic_path)
                shutil.move(source_xml_path, target_pic_path)
                cnt += 1
        else:
            print("该瑕疵图片数量小于2: {}".format(folderpath))
