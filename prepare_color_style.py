# -*- coding:utf-8

import os

import color_analyzer
import color_category
import emd
import utils

def calc_style_by_emd(path):
	fw = open("color_style.csv","w")

	for _,_,fs in os.walk(path):
		for f in fs:
			imgs = []
			imgs.append(path + f)
			color = color_analyzer.analyzer(imgs,50,10)
			category = color_category.category()
			dis, style = category.detect_category(color.color)
		#	print ("dis = %f, stype = %s"%(dis, style))
			pid = f.split(' ')[0]
			print (pid)
			fw.write(pid +','+style+'\n')

# 对path路径下每一张图片计算调性格，图片id和调性格结果写入文件
calc_style_by_emd("../dl-keyword/done/")