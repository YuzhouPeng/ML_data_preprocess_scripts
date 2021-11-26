import os
def check_pics(file_path):
    for parent, _, files in os.walk(file_path):
        for file in (files):
            xmlname = file[:-3]+"xml"
            xmlpath = os.path.join(parent,)
            if =="jpg":
                #  or file[-7:]=="act.jpg" or file[-11:]=="predict.jpg":
                os.remove(os.path.join(parent, file))


if __name__ == '__main__':
    xmlpath = "/home/pengyuzhou/workspace/dust/Annotations/"
    check_pics("/home/pengyuzhou/workspace/dust/JPEGImages")
    # remove_pics(r"D:\images_3T736_copy")