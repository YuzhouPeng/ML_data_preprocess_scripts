import os,shutil
targetpath = "D:\\guangdong2019\\defect_results"
def get_non_temp(file_path):
    for parent, _, files in os.walk(file_path):
        for file in (files):
            if file[-3:]=="jpg" and file[:8]!="template":
                shutil.copy(os.path.join(parent, file),targetpath)


if __name__ == '__main__':
    get_non_temp("D:\\guangdong2019\\defect_img")