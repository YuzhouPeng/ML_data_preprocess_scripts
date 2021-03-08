import cv2
import numpy as np
import matplotlib.pyplot as plt
import collections

#计算灰度图的直方图
def clczhifangtu(gray) :
    hist_new = []
    num = []
    hist_result = []
    hist_key = []
    gray1 = list(gray.ravel())
    obj = dict(collections.Counter(gray1))
    obj = sorted(obj.items(),key=lambda item:item[0])
    for each in obj :
        hist1 = []
        key = list(each)[0]
        each =list(each)[1]
        hist_key.append(key)
        hist1.append(each)
        hist_new.append(hist1)
    
    #检查从0-255每个通道是否都有个数，没有的话添加并将值设为0
    for i in range (0,256) :
        if i in hist_key :
            num = hist_key.index(i)
            hist_result.append(hist_new[num])
        else :
            hist_result.append([0])
    if len(hist_result) < 256 :
        for i in range (0,256-len(hist_result)) :
            hist_new.append([0])
    hist_result = np.array(hist_result)

    return hist_result

#计算均衡化
def clcresult(hist_new ,lut ,gray) :
    sum = 0
    Value_sum = []
    hist1 = []
    binValue = []

    for hist1 in hist_new :
        for j in hist1:
            binValue.append(j)
            sum += j
            Value_sum.append(sum)

    min_n = min(Value_sum)
    max_num = max(Value_sum)

    # 生成查找表
    for i, v in enumerate(lut):
        lut[i] = int(254.0 * Value_sum[i] / max_num + 0.5)
    # 计算
    result = lut[gray]
    return result

def main() :
    image = cv2.imread('/home/sycv/workplace/pengyuzhou/data_preprocess_scripts/result_median.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 创建空的查找表
    lut = np.zeros(256, dtype=gray.dtype)
    #直方图转化
    hist_new = clczhifangtu(gray)
    #并绘制直方图
    plt.plot(hist_new)
    plt.show()

    result = clcresult(hist_new,lut,gray)
    cv2.imshow('yuantu',gray)
    cv2.imshow("Result",result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()