import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
from sklearn.utils import shuffle
import os

def readImage(path):
    # OpenCV reads the image in bgr format by default
    bgr_img = cv2.imread(path)
    # We flip it to rgb for visualization purposes
    b,g,r = cv2.split(bgr_img)
    rgb_img = cv2.merge([r,g,b])
    return rgb_img


def plotSamples(dataframe,train_path):
    shuffled_data = shuffle(dataframe)

    fig, ax = plt.subplots(2,5, figsize=(20,8))
    fig.suptitle('Histopathologic scans of lymph node sections',fontsize=20)
    # Negatives
    for i, idx in enumerate(shuffled_data[shuffled_data['label'] == 0]['id'][:5]):
        path = os.path.join(train_path, idx)
        ax[0,i].imshow(readImage(path + '.tif'))
        # Create a Rectangle patch
        box = patches.Rectangle((32,32),32,32,linewidth=4,edgecolor='b',facecolor='none', linestyle=':', capstyle='round')
        ax[0,i].add_patch(box)
    ax[0,0].set_ylabel('Negative samples', size='large')
    # Positives
    for i, idx in enumerate(shuffled_data[shuffled_data['label'] == 1]['id'][:5]):
        path = os.path.join(train_path, idx)
        ax[1,i].imshow(readImage(path + '.tif'))
        # Create a Rectangle patch
        box = patches.Rectangle((32,32),32,32,linewidth=4,edgecolor='r',facecolor='none', linestyle=':', capstyle='round')
        ax[1,i].add_patch(box)
    ax[1,0].set_ylabel('Tumor tissue samples', size='large')
    plt.show()

if __name__ == '__main__':
    plotSamples()