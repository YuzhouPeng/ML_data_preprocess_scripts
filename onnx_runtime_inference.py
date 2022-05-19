
import cv2
import numpy as np
import onnxruntime as rt
 
def image_process(image_path):
    mean = np.array([[[0.485, 0.456, 0.406]]])      # 训练的时候用来mean和std
    std = np.array([[[0.229, 0.224, 0.225]]])
 
    img = cv2.imread(image_path)
    img = cv2.resize(img, (128, 384)) 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    # (96, 96, 3)
 
    image = img.astype(np.float32)/255.0
    # image = (image - mean)/ std
 
    # image = image.transpose((2, 0, 1))              # (3, 96, 96)
    image = image[np.newaxis,:,:,:]                 # (1, 3, 96, 96)
 
    image = np.array(image, dtype=np.float32)
    
    return image
 
def onnx_runtime():
    imgdata = image_process('/home/pengyuzhou/workspace/ML_data_preprocess_scripts/test1_result.jpg')
    
    sess = rt.InferenceSession('/home/pengyuzhou/workspace/FlipReID/Market1501_resnesta50_onnx_train.onnx')
    input_name = sess.get_inputs()[0].name  
    output_name = sess.get_outputs()[0].name
 
    pred_onnx = sess.run([output_name], {input_name: imgdata})
    print("pred onnx")
    print(pred_onnx)
    with open("onnx concatenate_result.txt","w") as f:
        f.write(str(pred_onnx))
    result = np.concatenate((pred_onnx))
    print("outputs:")
    with open("concatenate_result.txt","w") as f:
        f.write(str(result))
    print(result)
 
onnx_runtime()
