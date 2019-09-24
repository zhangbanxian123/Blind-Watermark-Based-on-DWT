# 一种仅基于DWT但提取效果较好的盲水印算法
## 步骤
### 嵌入过程
1.直接在整幅图上做三级小波变换  
2.在三级变换后的低频LL_3分量上依次量化嵌入水印，水印图片是提前设计好的具有多个重复证明版权字段的图像，且需要将水印图片resize成LL_3的尺寸  
3.嵌入完成后三级小波逆变换得到迁入后图像  
## 水印图片  
![image](https://github.com/dong-zhang1/Blind-Watermark-Based-on-DWT/blob/master/data/wm3.png)
## 待嵌入图像
![image](https://github.com/dong-zhang1/Blind-Watermark-Based-on-DWT/blob/master/data/6.jpg)
## 嵌入后图像
![image](https://github.com/dong-zhang1/Blind-Watermark-Based-on-DWT/blob/master/output/dwt_6.jpg)
### 提取过程
1.在整幅图上做三级小波变换   
2.在三级变换后的低频LL_3分量上依次量化提取水印  
3.得到水印图像  
## 在这里，我设计了4种不同的攻击模式，包括裁减、缩放、先裁减后缩放、先缩放后裁减，裁减缩放的比例都是随机的，对应的图片为  
![image](https://github.com/dong-zhang1/Blind-Watermark-Based-on-DWT/blob/master/output/crop_dwt_10.jpg)
![image](https://github.com/dong-zhang1/Blind-Watermark-Based-on-DWT/blob/master/output/scale_dwt_10.jpg)
![image](https://github.com/dong-zhang1/Blind-Watermark-Based-on-DWT/blob/master/output/crop_scale_dwt_10.jpg)
![image](https://github.com/dong-zhang1/Blind-Watermark-Based-on-DWT/blob/master/output/scale_crop_dwt_10.jpg)
## 对应提取出的水印图片如下
![image](https://github.com/dong-zhang1/Blind-Watermark-Based-on-DWT/blob/master/output/ex_crop_dwt_10.jpg)  
![image](https://github.com/dong-zhang1/Blind-Watermark-Based-on-DWT/blob/master/output/ex_scale_dwt_10.jpg)  
![image](https://github.com/dong-zhang1/Blind-Watermark-Based-on-DWT/blob/master/output/ex_crop_scale_dwt_10.jpg)  
![image](https://github.com/dong-zhang1/Blind-Watermark-Based-on-DWT/blob/master/output/ex_scale_crop_dwt_10.jpg)  

# 需要说明的是，此方法仅在图像画面不复杂时有效，对lena图进行测试时无论有误攻击，提取出的都是噪声！  
