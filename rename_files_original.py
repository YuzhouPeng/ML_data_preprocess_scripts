import os
import pandas as pd
folderpath = "/home/pengyuzhou/workspace/safetybelt_label_v1/Annotations"



for parent,_,files in os.walk(folderpath):
    count = 1
    for file in files:
        if file[-3:]=='jpg' or file[-3:]=='png':
            # prefix = parent.split("/")[-1]
            file_prefix = file.split(".")[0]
                # print(prefix)
                # print(file)
                # # prefix = os.path.join(file).split(".")
            xml = file[:-3]+'xml'
            print(file)
            print(xml)
            filename = os.path.join(parent,file)
            xmlname = os.path.join(parent,xml)
            n = str(count)+".jpg"
            xmln = str(count)+".xml"
            newname = os.path.join(parent,n)
            newxmlname = os.path.join(parent,xmln)
            os.rename(filename,newname)
            os.rename(xmlname,newxmlname)
            # temp = []
            # if prefix in namedict:
            #     temp.append(n)
            #     temp.append(str(namedict[prefix]))         
            # elif prefix in namedict_train:
            #     temp.append(n)
            #     temp.append(str(namedict_train[prefix]))         
            count+=1
                # res.append(temp)
    print(count)

# print(res)
# res = sorted(res,key=lambda x:x[1])
# res = colname+res
# test=pd.DataFrame(columns=colname,data=res)

# print(test)

# test.to_csv('testcsv1.csv',encoding='utf-8',header=None,index=None)