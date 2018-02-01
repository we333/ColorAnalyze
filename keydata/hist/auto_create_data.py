'''
	目的：各調性格に対応する色分布は多いから、自動的に下記のようなコードを作成
	self.GM[tuple((34,7))] = 0.013
	作成されたコードの内容は./done/に保存する
'''

def create_data(file):
	fname = file.split("./")[-1].split("_")[0]
	
	f_w = open("./done/" + fname + '_data.csv', 'w')

	cnt = 0
	f_r = open(file)
	for line in f_r:
		data = line.split(",")
		cnt = cnt + int(data[2])
	f_r.close()
	print cnt

	f_r = open(file)
	for line in f_r:
		data = line.split(",")
		per = float(data[2])/cnt
		p3 = float('%.3f'%per)
		print p3
		f_w.write("self." + fname + "[tuple((" + data[0] + "," + data[1] + "))] = " + str(p3) + '\n')

import os
def auto(path):
	for _,_,fs in os.walk(path):
		print fs
		for f in fs:
			create_data(path + f)

#auto('./')	#　こう呼び出すと問題が出たので、下記のように12回create_data()関数を呼び出した

create_data('./AbM_wcslab.csv')
create_data('./AM_wcslab.csv')
create_data('./BbM_wcslab.csv')
create_data('./BM_wcslab.csv')
create_data('./CM_wcslab.csv')
create_data('./DbM_wcslab.csv')
create_data('./DM_wcslab.csv')
create_data('./EbM_wcslab.csv')
create_data('./EM_wcslab.csv')
create_data('./FM_wcslab.csv')
create_data('./FsM_wcslab.csv')
create_data('./GM_wcslab.csv')
