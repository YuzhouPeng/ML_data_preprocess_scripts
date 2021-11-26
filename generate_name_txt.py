import os

txtpath = "/home/pengyuzhou/workspace/UNIT/datasets/firepath/list_trainB.txt"
imgpath = "/home/pengyuzhou/workspace/UNIT/datasets/firepath/trainB"
with open(txtpath,"w") as f: 
    for parent,_,files in os.walk(imgpath):
        for file in files:
            f.write("\n./"+file)
