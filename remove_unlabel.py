import os
def remove_pics(file_path):
    for parent, _, files in os.walk(file_path):
        for file in (files):
            # print(file)
            if file[-3:]=='jpg':
                print(os.path.join(parent,file))
                eles = file.split(".")
                file_prefix = eles[0]+'.'+eles[1]
                print(parent+file_prefix+'.xml')
                print(parent+file_prefix+'.txt')
                if not os.path.exists(parent+file_prefix+'.xml') and not os.path.exists(parent+file_prefix+'.txt'):
                    print(file)
                    print(os.path.join(parent, file))
                #  or file[-7:]=="act.jpg" or file[-11:]=="predict.jpg":
                    os.remove(os.path.join(parent, file))


if __name__ == '__main__':
    remove_pics("/home/pengyuzhou/workspace/seatbeltv2/Annotations/")
    # remove_pics(r"D:\images_3T736_copy")