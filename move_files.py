import os,shutil
def move_file(file_path,img_path,mask_path):
    for parent, _, files in os.walk(file_path):
        for file in (files):
            if file[-3:]=="jpg":
                #  or file[-7:]=="act.jpg" or file[-11:]=="predict.jpg":
                shutil.copy(os.path.join(parent, file), os.path.join(img_path, file))
            # if file[-3:]=="png":
            #     #  or file[-7:]=="act.jpg" or file[-11:]=="predict.jpg":
            #     shutil.move(os.path.join(parent, file), os.path.join(mask_path, file))

if __name__ == '__main__':
    move_file("/home/sycv/workplace/pengyuzhou/CascadePSP/data/set","/home/sycv/workplace/pengyuzhou/CascadePSP/data/sat_test","")
    # remove_pics(r"D:\images_3T736_copy")