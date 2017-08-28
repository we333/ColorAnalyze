# -- coding: utf-8 --

import numpy as np
import cv2

import os

import top_k_heap

class analyzer(object):
    def __init__(self, path):
        self.color_num = 16     # hsv空间所能分辨的颜色种类
        self.bin_thresh = 10    # 统计时每张图中，某一颜色的bin_count少于多少时被忽略

        self.path = path
        self.images = []
        self.color = {}

    def _find_exist_color_top_k(self, hist, bin_count,top_k):
        tk = top_k_heap(top_k)
        for i in xrange(bin_count):
            tk.push(hist[i])
        return tk.top_k()

    def _find_exist_color_thresh(self, hist,bin_count,thresh):
        ret = []
        for i in xrange(bin_count):
            if hist[i] >= thresh:
                ret.append(hist[i])
        return ret

    ## 计算color的各个颜色所占比重，并返回比重结果的百分值(1~99)
    def _calc_color_percent(self, color, pixel):
        percent = []

        total_count = sum(pixel)
        for i in range(len(color)): 
            percent.append(int(pixel[i]/total_count*100))
        return percent

    def _analyze_color(self, hist):
    ## 绘制颜色直方图
        bin_count = hist.shape[0]
        bin_w = 24
        img = np.zeros((256, bin_count*bin_w, 3), np.uint8) # numpy.ndarray
        for i in xrange(bin_count):
            h = hist[i] = int(hist[i])  # hist中的float数量变成int，便于计算
            cv2.rectangle(img, (i*bin_w+2, 255), ((i+1)*bin_w-2, 255-h), (int(180.0*i/bin_count), 255, 255), -1)
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        cv2.imshow('hist', img)
        
    ############## 找出最大的几个颜色的rgb以及比例 ##############
    ## 先抽取hist中出现最多的几个bin
        exist_color = self._find_exist_color_thresh(hist, bin_count, self.bin_thresh)

    ## 找到着几个bin对应的hist的位置，获取对应的颜色
        list_hist = list(hist)
        color,color_index = [],[]
        for i in range(len(exist_color)):
            idx = list_hist.index(exist_color[i])
            color_index.append(idx)
            # img[y,x] 获取像素值时，下标[0]是img中的y坐标，下标[1]是img中的x坐标
            color.append(img[255-int(list_hist[idx]), bin_w*idx+2]) # img[y,x]

    ## 计算bin中各个颜色所占比例
        percent = self._calc_color_percent(color, hist[color_index])

        return color, percent

    def _extract_object_area(self, image):
        ## 抽取目标对象的局部图像
        thresh = cv2.threshold(cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY) , 200, 255, cv2.THRESH_BINARY_INV)[1]
        es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,3))
        mask = cv2.dilate(thresh,es,iterations = 4)
        image = cv2.bitwise_and(image,image, mask = mask)

        return image,mask

    def _calc_color(self, image):   
        image,mask = self._extract_object_area(image)
        
        ## 计算hsv空间的直方图
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist( [hsv], [0], mask, [self.color_num], [0, 180] )
        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
        
        ## 从直方图中计算颜色比例
        return self._analyze_color(hist.reshape(-1))

    def _load_image(self):
        files = []
        if os.path.isdir(self.path):
            for _,_,f in os.walk(self.path):
                for name in f:   
                    files.append(self.path + name)
        elif os.path.isfile(self.path):
            files.append(self.path)
        else:
            print ('special fd')
            return

        for i in files:
            self.images.append(cv2.imread(i))

    def _count_color(self):
        for i in self.images:
            color, percent = self._calc_color(i)
            for j in range(len(color)):
                tmp = tuple(color[j])
                if self.color.has_key(tmp):
                    self.color[tmp] = self.color[tmp] + percent[j]
                else:
                    self.color[tmp] = percent[j]

    def run(self):
        self._load_image()
        self._count_color()

 

