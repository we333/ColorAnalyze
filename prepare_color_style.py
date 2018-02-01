# -*- coding:utf-8

'''
	目的：path内のすべての画像を分析して、調性格を推定。推定結果はcolor_style.csvに書き込む
'''　

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
			color = color_analyzer.analyzer(imgs, path, 50, 10)
			wcslab = utils.calc_wcslab_cie2000('wcslab.csv')
			hist = wcslab.create_chart(color.rgb)
			category = color_category.category()
			dis, style = category.detect_category(hist)
		#	print ("dis = %f, stype = %s"%(dis, style))
			pid = f.split(' ')[0]
			print (pid)
			fw.write(pid +','+style+'\n')

calc_style_by_emd("../hp_images_key_j/")