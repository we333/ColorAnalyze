# -- coding: utf-8 --
import cv2
import sys
import os

import color_analyzer
import color_category
import emd
import utils

'''
	1．q_fileから商品IDを取得
	2．IDを用いて、image_pathの中で各画像ファイルを抽出
	3．抽出された画像ファイルのPathをimage_listに保存する
	4．return　image_list
	
	ps：ans_fileを使っていないそうです
'''
def get_image_list(q_file, ans_file, image_path):
	item_num = []
	image_list = []
	f_r = open(q_file, 'r')
	for line in f_r:
		p_num = line.split('.jpg')[0]
		item_num.append(p_num)

	for files in os.listdir(image_path):
		for num in item_num:
			if num == files.split(' ')[0]:
				image_list.append(image_path + files)

	return image_list

def color_style(q_file, ans_file, image_path, wcslab_file):
	
	image_list = get_image_list(q_file, ans_file, image_path)	
	
	#　image_listの画像のRGB色を取得
	iroya = color_analyzer.analyzer(image_list, image_path, 50, 10)
	print iroya.rgb

	#　RGB色をMunsell上の分布を取得
	wcslab = utils.calc_wcslab_cie2000(wcslab_file)
	hist = wcslab.create_chart(iroya.rgb)

	#　各調性格のMunsell分布とEMD距離計算して、調性格styleを推測
	category = color_category.category()
	dis, style = category.detect_category(hist)

	#　推測された調性格結果をファイルに書き込む
	print ("dis = %f, stype = %s"%(dis, style))
	f_w = open(ans_file, 'w')
	f_w.write(style)

'''
	argv[1]：q_color.csv、ユーザーのIDを書き込んだファイル
	argv[2]：ans_color.csv、レコメンド結果の商品IDを書き込む予定ファイル
	argv[3]：./images/、すべての商品画像を保存する経路（大きいので自分で用意する）
	argv[4]：wcslab.csv、Lab色とMunsell座標の対応関係を示すファイル
	python main.py q_color.csv ans_color.csv color_style.csv wcslab.csvで実行できる
'''
color_style(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])