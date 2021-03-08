import os,shutil
xmlfilepath =  "C:\\Users\\admin\\Desktop\\val_xml"
jpgfilepath = "C:\\Users\\admin\\Desktop\\val_jpg"
def remove_pics(file_path):
    for parent, _, files in os.walk(file_path):
        for file in (files):
            os.rename(os.path.join(parent, file), os.path.join(parent, "".join(file.split(" "))))

    for parent, _, files in os.walk(file_path):
        for file in (files):
            # print(file[:-3])
            # print(os.path.join(parent,file[:-3]+"xml"))
            # print(os.path.join(parent,file[:-3]+"jpg"))
            if os.path.exists(os.path.join(parent,file[:-3]+"xml")) and os.path.exists(os.path.join(parent,file[:-3]+"jpg")):
                shutil.copy(os.path.join(parent, file[:-3]+"xml"),xmlfilepath)
                shutil.copy(os.path.join(parent, file[:-3]+"jpg"),jpgfilepath)



if __name__ == '__main__':
    remove_pics("C:\\Users\\admin\\Desktop\\num_recognition_val")
