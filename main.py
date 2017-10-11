# -- coding: utf-8 --
import cv2

import color_analyzer
import color_category
import emd
import utils

# 计算iroya浏览履历图片的颜色
iroya = color_analyzer.analyzer('./user_color/', 50, 10)

category = color_category.category(iroya.color)
category.detect_category(iroya.color)

