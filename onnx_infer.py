 # -*-coding: utf-8 -*-
 
import os, sys
sys.path.append(os.getcwd())
import onnxruntime
import onnx
import cv2
import torch
import numpy as np
import torchvision
import torchvision.transforms as transforms
from PIL import Image


class ONNXModel():
    def __init__(self, onnx_path):
        """
        :param onnx_path:
        """
        self.onnx_session = onnxruntime.InferenceSession(onnx_path)
        self.input_name = self.get_input_name(self.onnx_session)
        self.output_name = self.get_output_name(self.onnx_session)
        print("input_name:{}".format(self.input_name))
        print("output_name:{}".format(self.output_name))

    def get_output_name(self, onnx_session):
        """
        output_name = onnx_session.get_outputs()[0].name
        :param onnx_session:
        :return:
        """
        output_name = []
        for node in onnx_session.get_outputs():
            output_name.append(node.name)
        return output_name

    def get_input_name(self, onnx_session):
        """
        input_name = onnx_session.get_inputs()[0].name
        :param onnx_session:
        :return:
        """
        input_name = []
        for node in onnx_session.get_inputs():
            input_name.append(node.name)
        return input_name

    def get_input_feed(self, input_name, image_numpy):
        """
        input_feed={self.input_name: image_numpy}
        :param input_name:
        :param image_numpy:
        :return:
        """
        input_feed = {}
        for name in input_name:
            input_feed[name] = image_numpy
        return input_feed

    def forward(self, image_numpy):
        '''
        # image_numpy = image.transpose(2, 0, 1)
        # image_numpy = image_numpy[np.newaxis, :]
        # onnx_session.run([output_name], {input_name: x})
        # :param image_numpy:
        # :return:
        '''
        # 输入数据的类型必须与模型一致,以下三种写法都是可以的
        # scores, boxes = self.onnx_session.run(None, {self.input_name: image_numpy})
        # scores, boxes = self.onnx_session.run(self.output_name, input_feed={self.input_name: iimage_numpy})
        input_feed = self.get_input_feed(self.input_name, image_numpy)
        scores, boxes = self.onnx_session.run(self.output_name, input_feed=input_feed)
        return scores, boxes



def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

r_model_path="/home/zigangzhao/DMS/mtcnn-pytorch/test0815/onnx_model/rnet.onnx"
o_model_path="/home/pengyuzhou/workspace/pytorch-train/safety_belt_mobilenet_v3_small_onnxs.onnx"



# img = cv2.imread("/home/zigangzhao/DMS/mtcnn-pytorch/data_set/train/24/positive/999.jpg")
# img = cv2.resize(img, 224, 224), interpolation=cv2.INTER_CUBIC)

# """
# # scipy.misc.imread 读取的图片数据是 RGB 格式
# # cv2.imread 读取的图片数据是 BGR 格式
# # PIL.Image.open 读取的图片数据是RGB格式
# # 注意要与pth测试时图片读入格式一致
# """
# to_tensor = transforms.ToTensor()
# img = to_tensor(img)
# img = img.unsqueeze_(0)

# ------------------------------------------------------------------------------------
# 方法1：

# rnet1 = ONNXModel(r_model_path)
# out = rnet1.forward(to_numpy(img))
# print(out)
# ------------------------------------------------------------------------------------
# 方法2：
# rnet_session = onnxruntime.InferenceSession(r_model_path)
# onet_session = onnxruntime.InferenceSession(o_model_path)
# # compute ONNX Runtime output prediction
# inputs = {onet_session.get_inputs()[0].name: to_numpy(img)}
# outs = onet_session.run(None, inputs)
# img_out_y = outs
 
# print(img_out_y)
train_trans = torchvision.transforms.Compose([
    # transforms.Grayscale(num_output_channels=1),
    # transforms.Grayscale(num_output_channels=1),
    #transforms.RandomCrop(10),
    transforms.Resize([224,224]),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])
for parent,_,files in os.walk("/home/pengyuzhou/workspace/safety_belt12.23/test1"):
    for file in files:
        filepath = os.path.join(parent,file)
        # img = cv2.imread(filepath)
        img = Image.open(filepath)
        # img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_CUBIC)
        """
        # scipy.misc.imread 读取的图片数据是 RGB 格式
        # cv2.imread 读取的图片数据是 BGR 格式
        # PIL.Image.open 读取的图片数据是RGB格式
        # 注意要与pth测试时图片读入格式一致
        """
        img = train_trans(img)
        # to_tensor = transforms.ToTensor()
        # img = to_tensor(img)
        img = img.unsqueeze_(0)
        onet_session = onnxruntime.InferenceSession(o_model_path)
        # compute ONNX Runtime output prediction
        inputs = {onet_session.get_inputs()[0].name: to_numpy(img)}
        outs = onet_session.run(None, inputs)
        img_out_y = outs
        
        print(img_out_y)