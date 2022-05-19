import os
inputpath = '/home/pengyuzhou/workspace/human_statue_origin_label'
outputpath = '/home/pengyuzhou/workspace/human_statue_output'
for parent,_,files in os.walk(inputpath):
    for file in files:
        origin_list = []
        new_list = []
        inputfile = os.path.join(parent,file)
        f = open(inputfile,'r')  #打开文件
        file_data = f.readlines() #读取所有行
        for r in file_data:
            eles = r.split()
            if int(eles[0])==32: #status
                eles[0] = str(18)
            elif int(eles[0])==31: #pedestrian
                eles[0] = str(9)
            new_ele = " ".join(eles)
            new_list.append(new_ele)
        f=open(os.path.join(outputpath,file),"w")
        for line in new_list:
            f.write(line+'\n')
