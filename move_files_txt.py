import os,shutil

xml_img_path = '/home/pengyuzhou/workspace/construction_waste_img_label/xml_img'
xml_path = '/home/pengyuzhou/workspace/construction_waste_img_label/xml'
txt_img_path ='/home/pengyuzhou/workspace/construction_waste_img_label/txt_img'
txt_path = '/home/pengyuzhou/workspace/construction_waste_img_label/txt'


def remove_pics(file_path):
    for parent, _, files in os.walk(file_path):
        for file in (files):
            # print(file)
            if file[-3:]=='jpg':
                # print(file)
                file_prefix = file.split(".")[0]
                print(parent+"/"+file_prefix+'.xml')
                print(parent+"/"+file_prefix+'.txt')
                if os.path.exists(parent+"/"+file_prefix+'.xml'):
                    shutil.move(os.path.join(parent, file), os.path.join(xml_img_path, file))
                    shutil.move(os.path.join(parent, file_prefix+'.xml'), os.path.join(xml_path, file_prefix+'.xml'))
                elif os.path.exists(parent+"/"+file_prefix+'.txt'):
                    shutil.move(os.path.join(parent, file), os.path.join(txt_img_path, file))
                    shutil.move(os.path.join(parent, file_prefix+'.txt'), os.path.join(txt_path, file_prefix+'.txt'))
                #  or file[-7:]=="act.jpg" or file[-11:]=="predict.jpg":
                    # os.remove(os.path.join(parent, file))


if __name__ == '__main__':
    remove_pics("/home/pengyuzhou/workspace/建筑垃圾标注-修正后/")
    # remove_pics(r"D:\images_3T736_copy")