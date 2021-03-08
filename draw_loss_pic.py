import string
import time
import numpy as np
import matplotlib.pyplot as plt
def dataload():
    file = open('C:\\Users\\admin\\Desktop\\test\\cascade_70e\\20191231_145240_cascade_70e.log')
    s0 = []
    s1 = []
    s2 = []
    loss = []
    count = 0
    for line in file.readlines():
        if count % 86 == 0:
            count = 0

            print("xxxx")

            list = line.strip().split(" ")
            print(len(list))
            if len(list)==42:
                print(list)
                # print(list[24])
                # print(list[25])
                s0.append(float(list[25][:-1]))
                # print(list[30])
                # print(list[31])
                s1.append(float(list[31][:-1]))
                # print(list[36])
                # print(list[37])
                s2.append(float(list[37][:-1]))
                # print(list[40])
                print(list[41][:-1])
                print(float(list[41][:-1]))
                loss.append(float(list[41][:-1]))
            elif len(list)==40:
                print(list)
                # print(list[24])
                # print(list[25])
                s0.append(float(list[23][:-1]))
                # print(list[30])
                # print(list[31])
                s1.append(float(list[29][:-1]))
                # print(list[36])
                # print(list[37])
                s2.append(float(list[35][:-1]))
                print(list[38])
                print(list[39][:-1])
                print(float(list[39][:-1]))
                loss.append(float(list[39][:-1]))
        else:
            print(count)
        count += 1


    plt.plot(s0, color='red', label='s0')
    plt.plot(s1, color='pink', label='s1')
    plt.plot(s2, color='green', label='s2')
    plt.xlabel("epoch")  #
    plt.ylabel("acc")
    plt.legend()
    plt.title("cascade-rcnn acc value by different RPN")
    plt.ylim(90, 100)  #
    plt.savefig('C:\\Users\\admin\\Desktop\\acc.png', dpi=120, bbox_inches='tight')


    # plt.plot(loss, color='blue')
    # plt.xlabel("epoch")  #
    # plt.ylabel("loss")
    # # plt.legend()
    # plt.title("loss value")
    # plt.ylim(0, 1.5)  #
    # plt.savefig('C:\\Users\\admin\\Desktop\\loss.png', dpi=120, bbox_inches='tight')
    # print(s0)
    # print(s1)
    # print(s2)
    # print(loss)


if __name__ == '__main__':
    # string1 = "2019-12-31 16:08:42,030 - INFO - Epoch [3][50/4354]	lr: 0.00500, eta: 1 day, 18:47:11, time: 0.599, data_time: 0.057, memory: 8078, loss_rpn_cls: 0.0574, loss_rpn_bbox: 0.0405, s0.loss_cls: 0.1154, s0.acc: 96.8516, s0.loss_bbox: 0.0704, s1.loss_cls: 0.0565, s1.acc: 96.5703, s1.loss_bbox: 0.0746, s2.loss_cls: 0.0276, s2.acc: 96.7344, s2.loss_bbox: 0.0480, loss: 0.4904"
    # list = string1.split(" ")
    # print(len(list))
    # print(list[40])
    # print(list[41][:-1])
    dataload()
