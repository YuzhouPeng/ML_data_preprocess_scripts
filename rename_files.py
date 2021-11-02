import os
folderpath = "/home/pengyuzhou/workspace/pytorch-CycleGAN-and-pix2pix/datasets/fire_path/B/val"
# namedict = {"斑渍":"banzi","擦伤":"cashang","搭线":"daxian","断经":"duanjing","横档":"hengdang","破洞":"podong","浅斑":"qianban","色渍":"sezi","水渍":"shuizi","停车印":"tincheyin","斜皱":"xiezhou","油渍":"youzi","预缩皱":"yusuozhou","沾污":"zhanwu","皱条":"zhoutiao","竹夹":"zhujia","竹节":"zhujie","图层":"tuceng"}

# for parent,_,files in os.walk(folderpath):
#     count = 0
#     for file in files:
#         # prefix = os.path.join(file).split(".")
#         # if prefix[1]!="jpg":
#         #     count+=1
#         #     filename = os.path.join(parent,file)
#         #     # print(parent)
#         #     # jsonfilename = parent+ "\\" +prefix[0]+".json"
#         #     # print(jsonfilename)
#         #     # newstr = prefix[0].split("_")
#         #     newname = os.path.join(parent,"g_",file)
#         #     # newjsonname = parent + "\\20200210PYZ_1_" + str(count) + ".json"
#         #     print(newname)
#         #     # print(newjsonname)
#         #     os.rename(filename,newname)
#             # os.rename(jsonfilename,newjsonname)
#         count+=1
#         filename = os.path.join(parent,file)
#         eles = file.split("_")
#         print(filename)
#         if eles[0]!="img":
#             tag = file.split(" ")[1]
#             n1 = eles[0]
#             n2 = eles[1][:2]
#             n = namedict[n1]+"_"+namedict[n2]+"_"+tag
#             # n = "".join(file.split("_"))
#             # print(n)
#             newname = os.path.join(parent,n)
#             # print(newname)
#             os.rename(filename,newname)


for parent,_,files in os.walk(folderpath):
    count = 1
    for file in files:
        # prefix = os.path.join(file).split(".")
        filename = os.path.join(parent,file)
        n = str(count)+".jpg"
        newname = os.path.join(parent,n)
        os.rename(filename,newname)
        count+=1