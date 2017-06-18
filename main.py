# -- coding: utf-8 --

# 获取物品的轮廓，然后对轮廓进行直方图计算，结果很准确
# 但是有些图片物品与背景颜色相近，物品轮廓难以获取

import sys
import numpy as np
import cv2
import math
import colorsys
import heapq
import random
 
#def hsv2rgb(h,s,v):
#    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
#
#def hsv_to_rgb(h, s, v):
#    if s == 0.0: return (v, v, v)
#    i = int(h*6.) # XXX assume int() truncates!
#    f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
#    if i == 0: return (v, t, p)
#    if i == 1: return (q, v, p)
#    if i == 2: return (p, v, t)
#    if i == 3: return (p, q, v)
#    if i == 4: return (t, p, v)
#    if i == 5: return (v, p, q)

class TopkHeap(object):
    def __init__(self, k):
        self.k = k
        self.data = []
 
    def Push(self, elem):
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0]
            if elem > topk_small:
                heapq.heapreplace(self.data, elem)
 
    def TopK(self):
        return [x for x in reversed([heapq.heappop(self.data) for x in xrange(len(self.data))])]

def find_exist_color_topK(hist, bin_count,top_k):
    tk = TopkHeap(top_k)
    for i in xrange(bin_count):
        tk.Push(hist[i])
    return tk.TopK()

def find_exist_color_thresh(hist,bin_count,thresh):
    ret = []
    for i in xrange(bin_count):
        if hist[i] >= thresh:
            ret.append(hist[i])
    return ret

## 计算color的各个颜色所占比重，并返回比重结果的百分值(1~99)
def calc_color_percent(color, pixel):
    percent = []

    total_count = sum(pixel)
    for i in range(len(color)): 
        percent.append(int(pixel[i]/total_count*100))
    return percent

def analyze_color(hist):
## 绘制颜色直方图
    bin_count = hist.shape[0]
    bin_w = 24
    img = np.zeros((256, bin_count*bin_w, 3), np.uint8) # numpy.ndarray
    for i in xrange(bin_count):
        h = hist[i] = int(hist[i])  # hist中的float数量变成int，便于计算
        print (h)
        cv2.rectangle(img, (i*bin_w+2, 255), ((i+1)*bin_w-2, 255-h), (int(180.0*i/bin_count), 255, 255), -1)
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    cv2.imshow('hist', img)
    
############## 找出最大的几个颜色的rgb以及比例 ##############
## 先抽取hist中出现最多的几个bin
    exist_color = find_exist_color_thresh(hist, bin_count, 2)

## 找到着几个bin对应的hist的位置，获取对应的颜色
    list_hist = list(hist)
    color,color_index = [],[]
    for i in range(len(exist_color)):
        idx = list_hist.index(exist_color[i])
        color_index.append(idx)
        # img[y,x] 获取像素值时，下标[0]是img中的y坐标，下标[1]是img中的x坐标
        color.append(img[255-int(list_hist[idx]), bin_w*idx+2]) # img[y,x]

## 计算bin中各个颜色所占比例
    percent = calc_color_percent(color, hist[color_index])

    return color, percent

def run():
    frame = cv2.imread('./hat/hat_0.jpeg')
    cv2.imshow('frame', frame)

## 抽取目标对象的局部图像
    thresh = cv2.threshold(cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY) , 100, 255, cv2.THRESH_BINARY_INV)[1]
    es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,3))
    mask = cv2.dilate(thresh,es,iterations = 4)
    res = cv2.bitwise_and(frame,frame, mask = mask)
    hsv = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)
    cv2.imshow('frame', res)

## 分析局部图像的颜色比例
    hist = cv2.calcHist( [hsv], [0], mask, [10], [0, 180] )
    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    color, percent = analyze_color(hist.reshape(-1))
    print (color)
    print (percent)

run()
cv2.waitKey()
cv2.destroyAllWindows()