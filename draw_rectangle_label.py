from PIL import Image,ImageDraw,ImageFont
import os
coord ={}
inputpath = "/home/pengyuzhou/data/2600_split/total_2300/"
imagepath = "/home/pengyuzhou/data/2300_crop/04.02_pred_draw/"
coordpath = "/home/pengyuzhou/data/2300_crop/04.02.total.txt"
labelpath = "/home/pengyuzhou/crnn/tool/04.02.predict_labels_test_bs_32_with_gt.txt"
imglabels = {}
ratiow = 2448/896
ratioh = 2048/896
with open(coordpath) as f:
    content = f.readlines()
    content = [x.strip() for x in content]
    for line in content:
        ele = line.split(" ")
        img,xmin,ymin,xmax,ymax,labels = ele
        coord[img] = [xmin,ymin,xmax,ymax]
print("readlabels")
with open(labelpath) as f:
    content = f.readlines()
    content = [x.strip() for x in content]
    for line in content:
        ele = line.split(" ")
        if len(ele)>1:
            filename = ele[0]
            label = ele[1]
            prefix = filename.split("_")
            originfilename = prefix[0]+"_"+prefix[1]+".jpg"
            xmin, ymin, xmax, ymax = coord[filename]
            if originfilename not in imglabels.keys():
                imglabels[originfilename] = []
                imglabels[originfilename].append([xmin, ymin, xmax, ymax,label])
            else:
                imglabels[originfilename].append([xmin, ymin, xmax, ymax, label])
print("start print")
fontsize = 50  # starting font size
font = ImageFont.truetype("/home/pengyuzhou/data/arial.ttf", fontsize)
for filename in imglabels.keys():
    img = Image.open(inputpath+filename).convert('RGB')
    # print(filename)
    draw = ImageDraw.Draw(img)
    for ele in imglabels[filename]:
        # print(ele)
        xmin,ymin,xmax,ymax,label = ele
        draw.rectangle([(int(xmin), int(ymin)), (int(xmax), int(ymax))],outline ="red")
        draw.text((int(xmin), int(ymin)-20), label.replace("$","-"),font = font,fill="red")
        # save in new file
    img.save(imagepath+filename)