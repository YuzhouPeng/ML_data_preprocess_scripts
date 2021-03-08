import os,cv2

penmatestpath = "/home/pengyuzhou/data/2600_test_origin_output/"
gangyintestpath = "/home/pengyuzhou/data_rotate/train_folder/train/3/"


inputpath = "/home/dev_shared/04.29_crop_include_G_P/"
outputpath = "/home/pengyuzhou/data_rotate/"
angles = ["testc90","testc180","testc270"]
prefix = ""
# 顺时针旋转90度
def RotateClockWise90(img):
    trans_img = cv2.transpose( img )
    new_img = cv2.flip(trans_img, 1)
    return new_img
def RotateAntiClockWise90(img):
    trans_img = cv2.transpose( img )
    new_img = cv2.flip(trans_img, 0)
    return new_img

# 顺时针旋转180度
def RotateClockWise180(img):
    trans_img = cv2.flip(img,1)
    new_img = cv2.flip( trans_img, 0 )
    return new_img

#顺时针旋转270度
def RotateClockWise270(img):
    # trans_img = cv2.transpose( img )
    trans_img = cv2.transpose( img )
    new_img = cv2.flip( trans_img, 0 )
    return new_img
def RotateAntiClockWise270(img):
    trans_img = cv2.transpose( img )
    trans_img = cv2.transpose( trans_img )
    new_img = cv2.flip( trans_img, 0 )
    return new_img

def test_rot(img_path,filename):
    img = cv2.imread(img_path)
    # cv2.imwrite(outputpath, img)

    r_90_img = RotateClockWise270(img)
    cv2.imwrite( img_path, r_90_img )

    # r_180_img = RotateClockWise180(img)
    # cv2.imwrite( outputpath+"/"+angles[1]+"/"+filename, r_180_img )

    # r_270_img = RotateClockWise270(img)
    # cv2.imwrite(outputpath+"/"+angles[2]+"/"+filename, r_270_img)


def recover_imgs(imgpath,imglist,pred_labels,outputpath):
    for imgname,label in zip(imglist,pred_labels):
        if label==1:
            newimg = RotateAntiClockWise90(img_path+imglist)
            cv2.imwrite( outputpath+imgname, newimg )
        elif label==2:
            newimg = RotateClockWise180(img_path+imglist)
            cv2.imwrite( outputpath+imgname, newimg )
        elif label==3:
            newimg = RotateAntiClockWise90(img_path+imglist)
            newimg = RotateAntiClockWise90(img_path+imglist)
            cv2.imwrite( outputpath+imgname, newimg )            

for parent,_,files in os.walk(gangyintestpath):
    for file in files:
        img_path = os.path.join(parent,file)
        test_rot(img_path,prefix+file)
    

