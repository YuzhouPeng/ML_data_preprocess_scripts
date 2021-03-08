import os,shutil
from PIL import Image
def move_file(file_path,outputpath):
    for parent, _, files in os.walk(file_path):
        for file in (files):
            if file[-3:]=="png":
                #  or file[-7:]=="act.jpg" or file[-11:]=="predict.jpg":
                filename = os.path.join(parent,file)
                im = Image.open(filename)
                im = im.convert('RGB')
                r, g, b = im.split()
                r = r.point(lambda i: i * 255)
                g = g.point(lambda i: i * 255)
                b = b.point(lambda i: i * 255)
                out = Image.merge('RGB', (r, g, b))
                # shutil.copy(os.path.join(parent, file), os.path.join(outputpath, file))
                out.save(os.path.join(outputpath,file))
            # if file[-3:]=="png":
            #     #  or file[-7:]=="act.jpg" or file[-11:]=="predict.jpg":
            #     shutil.move(os.path.join(parent, file), os.path.join(mask_path, file))

if __name__ == '__main__':
    move_file("/home/sycv/workplace/pengyuzhou/CascadePSP/data/set","/home/sycv/workplace/pengyuzhou/CascadePSP/data/sat_val")
    # remove_pics(r"D:\images_3T736_copy")