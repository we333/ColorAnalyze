# -- coding: utf-8 --
import cv2
import sys
import os
from skimage import color

import color_analyzer
import color_category
import emd
import utils

def get_image_list(q_file, ans_file, image_path):
	# 从input_file获取商品编号
	item_num = []
	image_list = []
	f_r = open(q_file, 'r')
	for line in f_r:
		# 不要使用strip函数来去掉'\n'
		p_num = line.split('.jpg')[0]
		item_num.append(p_num)

	# 根据商品编号，从图片文件夹中寻找图片的文件名，保存完整路径
	for files in os.listdir(image_path):
		for num in item_num:
			if num == files.split(' ')[0]:
				image_list.append(image_path + files)

	return image_list

def color_style(q_file, ans_file, image_path):
	image_list = get_image_list(q_file, ans_file, image_path)	
	
	iroya = color_analyzer.analyzer(image_list, image_path, 50, 10)

	chart = utils.create_chart(iroya.rgb)

	for k, v in chart.items():
		print k, " - > ", v

	tmp_chart = {}
	tmp_chart[tuple((16,6))] = 5
	print emd.calc_emd(chart, tmp_chart)

	# 计算iroya与哪种调性格最接近
#	category = color_category.category()

#	dis, style = category.detect_category(iroya.rgb)

#	print ("dis = %f, stype = %s"%(dis, style))
	# 调性格结果写入output_file
#	f_w = open(ans_file, 'w')
#	f_w.write(style)

color_style(sys.argv[1], sys.argv[2], sys.argv[3])