# -- coding: utf-8 --

import os
import numpy as np
import cv2
import heap

class analyzer(object):
    def __init__(self, path, bin_num = 10, bin_thresh = 10):
        self.bin_num = bin_num          # hsv空间所能分辨的颜色种类
        self.bin_thresh = bin_thresh    # 统计时每张图中，某一颜色的self.bin_num少于多少时被忽略
        self.bin_w = 24                 # 绘制直方图的宽度

        self.path = path
        self.file_num = 0
        self.images = []
        self.color = {}

    def _find_exist_color_top_k(self, hist ,top_k):
        tk = heap.top_k_heap(top_k)
        for i in xrange(self.bin_num):
            tk.push(hist[i])
        return tk.top_k()

    def _find_exist_color_thresh(self, hist):
        ret = []
        for i in xrange(self.bin_num):
            if hist[i] >= self.bin_thresh:
                ret.append(hist[i])
        return ret

    ## 计算color的各个颜色所占比重，并返回比重结果的百分值(1~99)
    def _calc_color_percent(self, color, pixel):
        percent = []

        total_count = sum(pixel)
        for i in range(len(color)): 
            percent.append(int(pixel[i]/total_count*100))
        return percent

    def _draw_hist(self, hist):               
        img = np.zeros((256, self.bin_num*self.bin_w, 3), np.uint8) # numpy.ndarray
        for i in xrange(self.bin_num):
            h = hist[i] = int(hist[i])  # hist中的float数量变成int，便于计算

            cv2.rectangle(img, (i*self.bin_w+2, 255), ((i+1)*self.bin_w-2, 255-h), (int(180.0*i/self.bin_num), 255, 255), -1)
        return cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        
    def _calc_hist(self, hist):
        img = self._draw_hist(hist)
        cv2.imshow('hist', img)

    ############## 找出最大的几个颜色的rgb以及比例 ##############
    ## 先抽取hist中出现最多的几个bin
        exist_color = self._find_exist_color_top_k(hist, 5)

    ## 找到着几个bin对应的hist的位置，获取对应的颜色
        list_hist = list(hist)
        color,color_index = [],[]
        for i in range(len(exist_color)):
            idx = list_hist.index(exist_color[i])
            color_index.append(idx)
            # img[y,x] 获取像素值时，下标[0]是img中的y坐标，下标[1]是img中的x坐标
            color.append(img[255-int(list_hist[idx]), self.bin_w*idx+2]) # img[y,x]

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
        cv2.imshow('object', image)
        ## 计算hsv空间的直方图
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist( [hsv], [0], mask, [self.bin_num], [0, 180] )
        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)      # 每张图的像素不一样，需要正则化

        ## 从直方图中计算颜色比例
        return self._calc_hist(hist)    #.reshape(-1))

    def _load_image(self):
        files = []
        if os.path.isdir(self.path):
            for _,_,f in os.walk(self.path):
                for name in f:  
                    self.file_num += 1 
                    files.append(self.path + name)
        elif os.path.isfile(self.path):
            files.append(self.path)
        else:
            print ('special fd')
            return

        for i in files:
            tmp1,tmp2 = None, None
            cnt1,cnt2 = 50,50
            if 'BLACK' in i or 'Black' in i:
                tmp1 = tuple((0,0,0))
            elif 'WHITE' in i or 'White' in i:
                tmp1 = tuple((250,250,250))
            elif 'GRAY'in i or 'Gray' in i:
                tmp1 = tuple((192,192,192))
            elif 'PANDA' in i or 'Panda' in i:
                tmp1 = tuple((0,0,0))
                tmp2 = tuple((250,250,250))
                cnt1 = cnt2 = 25
            else:
                pass

            # 如果此图片是无法分辨的颜色，直接指定它的颜色和比例
            if tmp1 is not None:
                if self.color.has_key(tmp1):
                    self.color[tmp1] = self.color[tmp1] + cnt1
                else:
                    self.color[tmp1] = cnt1

                if tmp2 is not None:
                    if self.color.has_key(tmp2):
                        self.color[tmp2] = self.color[tmp2] + cnt2
                    else:
                        self.color[tmp2] = cnt2
            # 如果颜色可分辨，则之后再分析颜色
            else:
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

 

