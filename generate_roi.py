# -*- coding: UTF-8 -*-

from PIL import ImageDraw, ImageFont, Image
import os

img_path = "C:\\Users\\admin\\Desktop\\valid_xml_img"
coord_path = "C:\\Users\\admin\\Desktop\\test_predict\\test_predict"

dict = {"bianzhadong":"边扎洞", "cadong":"擦洞", "diaogong":"吊弓", "diaojing":"吊经", "diaowei":"吊纬", "jiandong":"剪洞",
        "maodong": "毛洞", "quejing":"缺经","quewei":"缺纬","zhadong":"扎洞","zhixi":"织稀"}
for parent, _, files in os.walk(img_path):
    for file in files:
        img = Image.open(os.path.join(parent, file))
        coord = []
        for line in open(coord_path + "\\" + file[:-3] + "txt","r"):
            coord.append(list(line.split(" ")))

        if len(coord)>0:
            draw = ImageDraw.Draw(img)  # 图片上打印
            for coordlist in coord:
                if len(coordlist)>5:
                    x0, y0, x1, y1 = [int(coordlist[2]), int(coordlist[3]), int(coordlist[4]), int(coordlist[5])]  # (x0,y0)左上，（x1,y1）右下
                    draw.rectangle([x0, y0, x1, y1], outline=(255, 0, 0), width=6)  # 画框
                    font = ImageFont.truetype("./simhei.ttf", 20, encoding="utf-8")
                    draw.text((x1, y1), dict[coordlist[0]], (255, 0, 0), font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
                    # image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                    img.save("C:\\Users\\admin\\Desktop\\TOVIDEO\\"+file)