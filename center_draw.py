import os
from PIL import Image,ImageDraw

def draw_imgs(imgpath,mean,filename,drawoutput,radius,box_coords):
    print("start print")

    img = Image.open(imgpath).convert('RGB')
    # print(filename)
    draw = ImageDraw.Draw(img)
    for center,coord in zip(mean,box_coords):
        y,x = center
        xmin,ymin,xmax,ymax = coord
        draw.rectangle([(int(xmin), int(ymin)), (int(xmax), int(ymax))],outline ="red",width = 20)
        draw.ellipse([(int(x-radius*2), int(y-radius*2)), (int(x+radius*2), int(y+radius*2))],fill ="red")
        # save in new file
    img.save(drawoutput+"draw_"+filename+".jpg")