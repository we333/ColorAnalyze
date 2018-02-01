# -- coding: utf-8 --

import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import utils
import cie2000

class analyzer(object):
    def __init__(self, file_list, file_path, bin_num = 10, bin_thresh = 10):
        self.bin_num = bin_num          # hsv空间所能分辨的颜色种类
        self.bin_thresh = bin_thresh    # 统计时每张图中，某一颜色的self.bin_num少于多少时被忽略
        self.bin_w = 24                 # 绘制直方图的宽度

        self.path = file_path
        self.file_list = file_list
        self.file_num = 0
        self.images = []
        self.rgb = {}

        ## 可能图片名中既有white也有green，导致图片没有被分析直接定义为white
        ## 所以在有如下颜色时，需要分析图片
        self.enable_calc_color = ['GREEN', 'RED', 'BLUE', 'YELLOW', 'ORANGE', 'NAVY', 'PURPLE', 'YELLOW', 'CORAL']

        self.run()

    def _find_exist_color_top_k(self, hist ,top_k):
        tk = utils.top_k_heap(top_k)
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
        bgr = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        return bgr

    def _calc_hist(self, hist):
        img = self._draw_hist(hist)
    #    cv2.imshow('rgb', img)

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

    ## opencv bgr to rgb
        for i in range(len(color)):
            tmp = color[i]
            first = tmp[0]
            last = tmp[-1]
            color[i][0] = last
            color[i][-1] = first

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
    #    cv2.imshow('object', image)
        ## calc hist in hsv
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist( [hsv], [0], mask, [self.bin_num], [0, 180] )
     #   cv2.imshow('hsv', hist)
        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)      # 每张图的像素不一样，需要正则化

        ## 从直方图中计算颜色比例
        return self._calc_hist(hist)    #.reshape(-1))

    # 直接从self.file_list里获取文件路径，并读取image
    def _load_image_from_list(self):
        for i in self.file_list:
            tmp1,tmp2 = None, None
            cnt1,cnt2 = 50,50
            upper_str = i.upper()

            enable_calc = True

            if 'PANDA' in upper_str or ('BLACK' in upper_str and 'WHITE' in upper_str):
                tmp1 = tuple((0,0,0))
                tmp2 = tuple((250,250,250))
                cnt1 = cnt2 = 25
                enable_calc = False
            elif 'BLACK' in upper_str or 'ブラック' in upper_str:
                tmp1 = tuple((0,0,0))
                enable_calc = False
            elif 'WHITE' in upper_str or '白' in upper_str:
                tmp1 = tuple((250,250,250))
                enable_calc = False
            elif 'GRAY'in upper_str or 'グレー' in upper_str:
                tmp1 = tuple((192,192,192))
                enable_calc = False
            else:
                pass

            for word in self.enable_calc_color:
                if word in upper_str:
                    print "!!!"
                    enable_calc = True

            # 如果此图片是无法分辨的颜色，直接指定它的颜色和比例
            if enable_calc == False:
                print "pass calc ......"
                if self.rgb.has_key(tmp1):
                    self.rgb[tmp1] = self.rgb[tmp1] + cnt1
                else:
                    self.rgb[tmp1] = cnt1

                if tmp2 is not None:
                    if self.rgb.has_key(tmp2):
                        self.rgb[tmp2] = self.rgb[tmp2] + cnt2
                    else:
                        self.rgb[tmp2] = cnt2

            else:
                print "calc ......"
                print i
                self.images.append(cv2.imread(i))
            
            self.file_num += 1

    def _load_image_from_path(self):
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
            upper_str = i.upper()

            enable_calc = True

            if 'PANDA' in upper_str or ('BLACK' in upper_str and 'WHITE' in upper_str):
                tmp1 = tuple((0,0,0))
                tmp2 = tuple((250,250,250))
                cnt1 = cnt2 = 25
                enable_calc = False
            elif 'BLACK' in upper_str or 'ブラック' in upper_str:
                tmp1 = tuple((0,0,0))
                enable_calc = False
            elif 'WHITE' in upper_str or '白' in upper_str:
                tmp1 = tuple((250,250,250))
                enable_calc = False
            elif 'GRAY'in upper_str or 'グレー' in upper_str:
                tmp1 = tuple((192,192,192))
                enable_calc = False
            else:
                pass

            # 如果此图片是无法分辨的颜色，直接指定它的颜色和比例
            if enable_calc == False:
                if self.rgb.has_key(tmp1):
                    self.rgb[tmp1] = self.rgb[tmp1] + cnt1
                else:
                    self.rgb[tmp1] = cnt1

                if tmp2 is not None:
                    if self.rgb.has_key(tmp2):
                        self.rgb[tmp2] = self.rgb[tmp2] + cnt2
                    else:
                        self.rgb[tmp2] = cnt2
            
            else:
                # 如果颜色可分辨，则之后再分析颜色
                self.images.append(cv2.imread(i))

    def _count_color(self):
        for i in self.images:
            color, percent = self._calc_color(i)
            for j in range(len(color)):
                tmp = tuple(color[j])
                if self.rgb.has_key(tmp):
                    self.rgb[tmp] = self.rgb[tmp] + percent[j]
                else:
                    self.rgb[tmp] = percent[j]

    def _show_plot(self):
        colors = []
        occupy = []

        for k,v in self.rgb.items():
            print ('%s = %d'%(k, float(v)/self.file_num))
            c = utils.rgb2hex(k)
            colors.append(c)
            occupy.append(v)
            cv2.waitKey()
            cv2.destroyAllWindows()

        plt.bar(range(len(occupy)), occupy, color=list(colors))
        plt.show()

    def run(self):
        self._load_image_from_list()
        self._count_color()
     #   self._show_plot()

 