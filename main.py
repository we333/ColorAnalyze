# -- coding: utf-8 --
import cv2

import color_analyzer
import emd
import utils


# 计算iroya浏览履历图片的颜色
iroya = color_analyzer.analyzer('../global_images/bak/', 50, 10)
iroya.run()

# 计算pantone杂志中的颜色比例
pantone_2015_spring = color_analyzer.analyzer('./pantone/', 50, 10)
pantone_2015_spring.run()

# 计算两个文件夹下图片的emd距离
distance = emd.calc_emd(iroya.color, pantone_2015_spring.color)
print (distance)