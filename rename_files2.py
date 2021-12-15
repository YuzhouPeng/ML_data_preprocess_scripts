import os
import pandas as pd
folderpath = "/home/pengyuzhou/workspace/chip_test_final"
# namedict = {"斑渍":"banzi","擦伤":"cashang","搭线":"daxian","断经":"duanjing","横档":"hengdang","破洞":"podong","浅斑":"qianban","色渍":"sezi","水渍":"shuizi","停车印":"tincheyin","斜皱":"xiezhou","油渍":"youzi","预缩皱":"yusuozhou","沾污":"zhanwu","皱条":"zhoutiao","竹夹":"zhujia","竹节":"zhujie","图层":"tuceng"}
namedict = {"anormal":0,"missing":1,"normal":2,"spin":3}
namedict_train = {"anormal_train":0,"missing_train":1,"normal_train":2,"spin_train":3}
names = ["anormal","missing","normal","spin","anormal_train","missing_train","normal_train","spin_train"]
names1 = ["YiWu","LouGu","zc","XuanZhuan"]
names2 = ["anormal","missing","normal","spin"]
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

# colname = [["FileID","SpeciesID"]]
colname = [["image_id","anormal","missing","normal","spin"]]
res = []

for parent,_,files in os.walk(folderpath):
    count = 1
    for file in files:
        if file[-3:]=='jpg' or file[-4:]=='jpeg':
            prefix = parent.split("/")[-1]
            file_prefix = file.split(".")[0]
            print(prefix)
            print(file)
            # prefix = os.path.join(file).split(".")
            filename = os.path.join(parent,file)

            n = prefix+'_'+file_prefix+".jpg"
            n1 = prefix+'_'+file_prefix
            newname = os.path.join(parent,n)
            os.rename(filename,newname)
            temp = []
            if prefix in names2:
                temp.append(n1)
                label = [0,0,0,0]
                label[names2.index(prefix)] = 1
                for i in range(len(label)):
                    temp.append(label[i])
                # temp.append(label)         
            # elif prefix in namedict_train:
            #     temp.append(n1)
            #     label = [0,0,0,0]
            #     label[namedict_train[prefix]]=1
            #     for i in range(len(label)):
            #         temp.append(label[i])
                # temp.append(label)         
            # count+=1
            res.append(temp)

print(res)
res = sorted(res,key=lambda x:x[1])
res = colname+res
test=pd.DataFrame(columns=colname,data=res)

print(test)

test.to_csv('chips_test_final.csv',encoding='utf-8',header=None,index=None)