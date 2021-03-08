import os
import cv2
maskpath = r"D:\projects\train"
nonmaskpath = r"D:\projects\mask_man"
for parent,_,files in os.walk(maskpath):
    for file in files:
        filename = os.path.join(parent,file)
        img = cv2.imread(filename)
        if img is None:
            os.remove(filename)
        elif img is not None:
            sp = img.shape
            height = sp[0]  # height(rows) of image
            width = sp[1]
            if height<640 or width<480:
                os.remove(filename)
#
# for parent,_,files in os.walk(nonmaskpath):
#     for file in files:
#         filename = os.path.join(parent,file)
#         img = cv2.imread(filename)
#         if img is None:
#             os.remove(filename)
#         elif img is not None:
#             sp = img.shape
#             height = sp[0]  # height(rows) of image
#             width = sp[1]
#             if height<640 or width<480:
#                 os.remove(filename)