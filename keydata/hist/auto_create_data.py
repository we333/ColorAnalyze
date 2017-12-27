
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

#auto('./')

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
