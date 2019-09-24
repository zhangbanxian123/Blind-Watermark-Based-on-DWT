import os
import cv2
import numpy as np

img = np.array(cv2.imread('./data/wm2.png'))
print(img.shape)
img1 = img[:,:,0]
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        if img1[i,j] == 255:
            img1[i,j] = 255
        elif img1[i,j] <222:
            img1[i,j] = 0
cv2.imwrite('./data/wm5.png',img1)