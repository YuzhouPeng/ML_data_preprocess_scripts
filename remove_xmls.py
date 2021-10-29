import os
def remove_pics(file_path):
    for parent, _, files in os.walk(file_path):
        for file in (files):
            if file[-3:]=="jpg":
                #  or file[-7:]=="act.jpg" or file[-11:]=="predict.jpg":
                os.remove(os.path.join(parent, file))


if __name__ == '__main__':
    remove_pics("/home/pengyuzhou/workspace/fire_path_data")
    # remove_pics(r"D:\images_3T736_copy")