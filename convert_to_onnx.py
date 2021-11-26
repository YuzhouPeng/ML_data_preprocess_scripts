from torch.autograd import Variable
import torch.onnx
import torchvision
import torch

dummy_input = Variable(torch.randn(1, 3, 1472, 828))
state_dict = torch.load('/opt/DataDisk/pengyuzhou/ai/semantic-segmentation/weights/seg_weights/boe_semantic1.pth')
model.load_state_dict(state_dict)
torch.onnx.export(model, dummy_input,"semantic1_onnx.onnx")