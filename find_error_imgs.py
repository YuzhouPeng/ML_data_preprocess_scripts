from shutil import copyfile
gtpath = "/home/pengyuzhou/data/2020.03.27data/03_30_Report_diff.txt"
strlist = []
with open(gtpath,encoding='UTF-8-sig') as f:
    contents = f.readlines()
    contents = [c.strip() for c in (contents)]
    
    for content in contents:
        if content!="---------------------------------------------------------------------------------------------------------------------":
            ele = content.split(" ")
            if len(ele)>1:
                strlist.append(ele[0])
                # print(string)
for file_name in strlist:
    # "a"表示以不覆盖的形式写入到文件中,当前文件夹如果没有"save.txt"会自动创建
    print(file_name)
    eles = file_name.split("_")
    file_name = eles[0]+"_"+eles[1]+".jpg"
    copyfile("/home/pengyuzhou/data/2020.03.27data/03.30_pred_draw_with_gt/" + file_name, "/home/pengyuzhou/data/2020.03.27data/03_30_pred_error/"+file_name)