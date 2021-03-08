import os
folderpath = r"C:\Users\76078\Desktop\valid_data1"
outputpath = r"C:\Users\76078\Desktop"
filenamelist = []
for parent,_,files in os.walk(folderpath):
    for file in files:
        string = file+" "+file[:-4].split("_")[0]
        filenamelist.append(string)

for file_name in filenamelist:
    # "a"表示以不覆盖的形式写入到文件中,当前文件夹如果没有"save.txt"会自动创建
    with open(outputpath+"\\valid_label1.txt","a") as f:
        f.write(file_name + "\n")
        # print(file_name)
    f.close()
