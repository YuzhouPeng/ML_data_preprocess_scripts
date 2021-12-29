import os
import pandas as pd
folderpath = "/home/pengyuzhou/workspace/gt_db"



for parent,_,files in os.walk(folderpath):
    count = 1
    for file in files:
        # if file[-3:]=='jpg' or file[-4:]=='jpeg':
        prefix = parent.split("/")[-1]
            # file_prefix = file.split(".")[0]
            # print(prefix)
            # print(file)
            # # prefix = os.path.join(file).split(".")
        filename = os.path.join(parent,file)

        n = prefix+'_'+str(count)+".jpg"
        newname = os.path.join(parent,n)
        os.rename(filename,newname)
        # temp = []
        # if prefix in namedict:
        #     temp.append(n)
        #     temp.append(str(namedict[prefix]))         
        # elif prefix in namedict_train:
        #     temp.append(n)
        #     temp.append(str(namedict_train[prefix]))         
        count+=1
            # res.append(temp)

# print(res)
# res = sorted(res,key=lambda x:x[1])
# res = colname+res
# test=pd.DataFrame(columns=colname,data=res)

# print(test)

# test.to_csv('testcsv1.csv',encoding='utf-8',header=None,index=None)