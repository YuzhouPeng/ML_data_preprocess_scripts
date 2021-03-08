import os,cv2,random
# characterset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789x+:.,/$_&*()abcdefghijklmnopqrstuvwyz"
inputsize = 20
characterset = "ABCDEFGHI234"
characterpath = ""
inputimage = ""
gt = ""
pixel_per_char = 16
def random_generate_complementary_str(origin_img,gt,characterset,length):
    
    for l in range(length):
        rand_ele = (random.choice(characterset))
        dirs = os.listdir(characterpath+"/"+rand_ele)
        gt+=rand_ele
        rand_img = cv2.imread(characterpath +"/"+random.sample(dirs,1))
        rand_img = cv2.resize(rand_img,(pixel_per_char,32))
        origin_img = cv2.hconcat([origin_img,rand_img])
    return origin_img,gt

def crnn_str_fill(inputimage,gt):
    img = cv2.imread(inputimage)
    resize_input_img = cv2.resize(img,(len(gt)*pixel_per_char,32))
    resize_output_image = random_generate_complementary_str(resize,gt,characterset,inputsize-len(gt))
    return resize_output_image