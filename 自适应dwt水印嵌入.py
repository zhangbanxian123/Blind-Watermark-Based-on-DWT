
# coding: utf-8

# In[16]:

import numpy as np
import cv2
import os
import pywt
import matplotlib.pyplot as plt
import time
import random


# In[61]:

def generate_LL_2(conver_img):
    #转换RGB到YCRCB，在Y分量上加水印
    Y_split = conver_img[:,:,0]

    #为确保正确进行dwt变换，要将长宽条成为被8整除
#     height,weith = Y_split.shape
#     if not height%8 == 0:
#         height -= height%8
#     if not weith%8 == 0:
#         weith -=weith%8
#     Y_split = Y_split[:height,:weith]
#     conver_img = conver_img[:height,:weith,:]

    #dwt变换3次
    LL,(HL,LH,HH) = pywt.dwt2(np.array(Y_split),'haar')
    LL_1,(HL_1,LH_1,HH_1) = pywt.dwt2(np.array(LL),'haar')
    LL_2,(HL_2,LH_2,HH_2) = pywt.dwt2(np.array(LL_1),'haar')

    return LL_2,(HL_2,LH_2,HH_2),(HL_1,LH_1,HH_1),(HL,LH,HH)


# In[3]:

def embed(LL_2, dwt_2, dwt_1, dwt_0, wm):
    h,w = LL_2.shape
    print(h,w)
    wm = cv2.resize(wm,(w,h)) #缩放至于LL_2相同大小进行嵌入
    #水印依次嵌入
    for i in range(h):
        for j in range(w):
            a = np.mod(LL_2[i,j], Q)
            if wm[i,j] <160  and 0<=a<3*Q/4:
                LL_2[i,j] = LL_2[i,j] - a + (Q/4)
            elif wm[i,j] <160 and 3*Q/4<=a<Q:
                LL_2[i,j] = LL_2[i,j] - a + 5*(Q/4)
            elif  wm[i,j]==255 and 0<=a<Q/4:
                LL_2[i,j] = LL_2[i,j] - a - (Q/4)
            elif  wm[i,j]==255 and Q/4<=a<Q:
                LL_2[i,j] = LL_2[i,j] - a + 3*(Q/4)   

    #嵌入完之后反变换回去
    LL_1 = pywt.idwt2((LL_2,dwt_2),'haar')
    LL = pywt.idwt2((LL_1,dwt_1),'haar')
    Y_split_embed = pywt.idwt2((LL,dwt_0),'haar')

    return Y_split_embed


# In[4]:

def save_embed_img(Y_split_embed):
    #保存嵌入水印后的图并展示
    conver_img[:,:,0] = Y_split_embed
    img = cv2.cvtColor(conver_img, cv2.COLOR_YCrCb2BGR)
    cv2.imwrite(outname, img)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # plt.imshow(img)
    # plt.show()


# In[25]:

def extract(ex_img, wm_outname):
    ex_wm = []
    ex_img = cv2.cvtColor(ex_img, cv2.COLOR_BGR2YCrCb) 
    Y_split = ex_img[:,:,0]

    LL,(HL,LH,HH) = pywt.dwt2(np.array(Y_split),'haar')
    LL_1,(HL_1,LH_1,HH_1) = pywt.dwt2(np.array(LL),'haar')
    LL_2,(HL_2,LH_2,HH_2) = pywt.dwt2(np.array(LL_1),'haar')
    h1,w1 = LL_2.shape

    #提取水印并展示
    for x in range(h1):
        for y in range(w1):
            a = np.mod(LL_2[x,y], Q)
            if a > Q/3:
                ex_wm.append(255)
            else:
                ex_wm.append(0)
    ex_wm = np.array(ex_wm).reshape((h1,w1))
    plt.imsave(wm_outname, ex_wm, cmap='Greys_r')
#     plt.imshow(ex_wm, cmap='Greys_r')
#     plt.show()


# In[8]:

def crop(img):
    '''至少保留图像中心1/4的裁减'''
    h, w = img.shape[:2]
    h_crop = np.random.randint(int(h/10),int(h/4))
    w_crop = np.random.randint(int(w/10),int(w/4))
#     print('h_crop:{} w_crop:{}'.format(h_crop,w_crop))
#     img = img[(h//2)-h_crop:(h//2)+h_crop,(w//2)-h_crop:(w//2)+w_crop,:] #保留中间1/4的部分
    img = img[h_crop:h-h_crop, w_crop:w-w_crop,:] #保留中间1/4的部分
    return img


# In[9]:

def scale(img):
    '''长宽均小于3倍缩放的任意组合, scale_rate为缩放比例'''
    half_h,half_w = img.shape[:2]
    h_scale_rate = random.uniform(0.5,1.5)#随机生成长(0.5-1.5)之间的缩放比例
    w_scale_rate = random.uniform(0.5,1.5)#随机生成宽(0.5-1.5)之间的缩放比例
#     print('h_scale_rate:{:.1f} w_scale_rate:{:.1f}'.format(h_scale_rate,w_scale_rate))
    half_h = int(half_h*h_scale_rate)
    half_w = int(half_w*w_scale_rate)
    img = cv2.resize(img,(half_w,half_h))# 缩放攻击
    return img


# In[10]:

def crop_scale(img):
    '''先裁减再缩放攻击'''
    crop_img = crop(img)
    img = scale(crop_img)
    return img


# In[11]:

def scale_crop(img):
    '''先缩放再裁减攻击'''
    scale_img = scale(img)
    img = crop(scale_img)
    return img


# In[64]:

imgname = '9.jpg'
wmname = 'wm1.png'
outname = './output/'+'dwt_'+imgname
wm_outname = './extract/' + 'ex_' + imgname
Q = 32
img = cv2.imread('./data/' + imgname)
img= img-1 #确保 RGB分量不全为255，否则在原始图片上会显现水印
conver_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb) #转为YCRCB色彩空间上

# 为确保正确进行dwt变换，要将长宽条成为被8整除
height,weith = conver_img.shape[:2]
if not height%8 == 0:
    height -= height%8
if not weith%8 == 0:
    weith -=weith%8
conver_img = conver_img[:height,:weith,:]

wm = cv2.imread('./data/' + wmname, cv2.IMREAD_GRAYSCALE) #读取要嵌入的水印

start_time = time.clock() #记录时间
LL_2, dwt_2, dwt_1, dwt_0 = generate_LL_2(conver_img) #得到LL_2
Y_split_embed = embed(LL_2, dwt_2, dwt_1, dwt_0, wm) #得到嵌入水印后的Y分量
print('嵌入耗费时间：',(time.clock()-start_time))
save_embed_img(Y_split_embed) #保存嵌入水印的图片

embed_img = cv2.imread('./output/dwt_9.jpg')# 要提取水印的图片

#随机裁减
ex_img = crop(embed_img)
cv2.imwrite(('./output/crop_dwt_10.jpg'),ex_img)
start_time = time.clock() #记录时间
extract(ex_img,'./output/ex_crop_dwt_10.jpg') 
print('裁减提取耗费时间：',(time.clock()-start_time))
#随机缩放
ex_img = scale(embed_img)
cv2.imwrite(('./output/scale_dwt_10.jpg'),ex_img)
start_time = time.clock() #记录时间
extract(ex_img,'./output/ex_scale_dwt_10.jpg') #提取水印并显示
print('缩放提取耗费时间：',(time.clock()-start_time))
#随机裁减缩放
ex_img = crop_scale(embed_img)
cv2.imwrite(('./output/crop_scale_dwt_10.jpg'),ex_img)
start_time = time.clock() #记录时间
extract(ex_img,'./output/ex_crop_scale_dwt_10.jpg') #提取水印并显示
print('裁剪缩放耗费时间：',(time.clock()-start_time))
#随机缩放裁减
ex_img = scale_crop(embed_img)
cv2.imwrite(('./output/scale_crop_dwt_10.jpg'),ex_img)
start_time = time.clock() #记录时间
extract(ex_img,'./output/ex_scale_crop_dwt_10.jpg') #提取水印并显示
print('缩放裁减提取耗费时间：',(time.clock()-start_time))

