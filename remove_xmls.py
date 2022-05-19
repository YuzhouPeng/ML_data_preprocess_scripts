import os
def remove_pics(file_path):
    for parent, _, files in os.walk(file_path):
        for file in (files):
            if file[-4:]=="json":
                #  or file[-7:]=="act.jpg" or file[-11:]=="predict.jpg":
                os.remove(os.path.join(parent, file))


if __name__ == '__main__':
    remove_pics("/opt/DataDisk2/pyz/3.2_not_wear")
    # remove_pics(r"D:\images_3T736_copy")