import os

txtpath = ""
with open(txtpath,"w") as f: 
    for parent,_,files in os.walk(""):
        for file in files:
            f.write("./"+file)
