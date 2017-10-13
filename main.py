# -- coding: utf-8 --
import cv2

import color_analyzer
import color_category
import emd
import utils

'''
case1: 无任何推荐
case2：
'''

# 计算iroya浏览履历图片的颜色
iroya = color_analyzer.analyzer('./images/user_color/', 50, 10)

category = color_category.category()
category.detect_category(iroya.color)

