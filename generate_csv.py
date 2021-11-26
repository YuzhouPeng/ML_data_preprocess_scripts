import pandas as pd
import os

# for parent,_,files in os.walk(folderpath):
#     for file in files:



list=[[1,2,3],[4,5,6],[7,9,9]]

name=['one','two','three']

name2=['a','b','c']

test=pd.DataFrame(columns=name,index=name2,data=list)

print(test)

test.to_csv('testcsv.csv',encoding='utf-8')