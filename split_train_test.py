import os
import shutil
import glob
from sklearn.model_selection import train_test_split


def split_train_test(data_path, train_path, valid_path, valid_size):
    if os.path.exists(train_path):
        shutil.rmtree(train_path)
    
    # if os.path.exists(valid_path):
    #     shutil.rmtree(valid_path)
    # os.mkdir(valid_path)

    shutil.copytree(data_path, train_path)

    for root, dirs, files in os.walk(train_path):
        imgs = glob.glob(os.path.join(root, "*.jpg"))
        img_len = len(imgs)
        if img_len > 1:
            train, val = train_test_split(imgs, test_size = valid_size)
            for img in val:
                img_name = img.split('/')[-1]
                # label_name = img.split('/')[-2]
                # xml_name = img_name.replace('png', 'xml')
                img_path = os.path.join(root, img_name)
                # xml_path = os.path.join(root, xml_name)
                # if not os.path.exists(os.path.join(valid_path, label_name)):
                #     os.mkdir(os.path.join(valid_path, label_name))
                shutil.move(img_path, valid_path+'/'+img_name)
                # shutil.move(xml_path, os.path.join(valid_path, label_name, xml_name))

if __name__ == "__main__":
    outputpath = "/home/pengyuzhou/workspace/smoke_cellphone/train/train_datasets/smoke"
    data_path = "/home/pengyuzhou/workspace/smoke_cellphone/train/train/smoke"
    train_path = os.path.join(outputpath, "train")
    if not os.path.exists(train_path):
        os.mkdir(train_path)
    valid_path = os.path.join(outputpath, "val")
    if not os.path.exists(valid_path):
        os.mkdir(valid_path)
    valid_size = 0.3
    split_train_test(data_path, train_path, valid_path, valid_size)