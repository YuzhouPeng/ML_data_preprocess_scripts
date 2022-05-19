import sys
# sys.path.append("/home/pengyuzhou/workspace/FlipReID/")
import tensorflow as tf
import numpy as np
import cv2
import tf2onnx
import onnxruntime as rt
from tensorflow.keras import backend as K
from tensorflow.keras.applications.imagenet_utils import (decode_predictions,
                                                          preprocess_input)
from tensorflow.keras.layers import (GlobalAveragePooling2D, Input, Lambda,
                                     Layer, Softmax)
from tensorflow.keras.models import Model, load_model

import applications.common as common
import applications.ibnresnet as ibnresnet
import applications.resnesta as resnesta
import applications.resnet as resnet

# 读取h5模型
model = tf.keras.models.load_model("/home/pengyuzhou/workspace/Market1501_resnesta50_18209984.h5")
 
# 推理h5模型
preds = model.predict(image)
 
# 保存h5模型为tf的save_model格式
# model.save("./" + model.name))
 
 
######################################################################################################################
# 定义模型转onnx的参数
spec = (tf.TensorSpec((None, 64, 128, 3), tf.float32, name="input"),)  # 输入签名参数，(None, 128, 128, 3)决定输入的size
output_path =  "Market1501_resnesta50_onnx.onnx"                                   # 输出路径

# 转换并保存onnx模型，opset决定选用的算子集合
model_proto, _ = tf2onnx.convert.from_keras(model, input_signature=spec, opset=13, output_path=output_path)
output_names = [n.name for n in model_proto.graph.output]
print(output_names)  # 查看输出名称，后面推理用的到


# ######################################################################################################################
# # 读取onnx模型，安装GPUonnx，并设置providers = ['GPUExecutionProvider']，可以实现GPU运行onnx
# providers = ['CPUExecutionProvider']
# m = rt.InferenceSession(output_path, providers=providers)
 
# # 推理onnx模型
# output_names = output_names
# onnx_pred = m.run(output_names, {"input": image})
 
# # 对比两种模型的推理结果
# print('Keras Predicted:', preds)
# print('ONNX Predicted:', onnx_pred[0])
 
# # make sure ONNX and keras have the same results
# np.testing.assert_allclose(preds, onnx_pred[0], rtol=1e-4)
