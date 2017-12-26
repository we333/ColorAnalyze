
def create_data(file):
	fname = file.split("./")[-1].split("_")[0]
	
	f_w = open("./done/" + fname + '_data.csv', 'w')

	f_r = open(file)
	for line in f_r:
		data = line.split(",")
		f_w.write("self." + fname + "[tuple((" + data[0] + "," + data[1] + "))] = " + data[2])

import os
def auto(path):
	for _,_,fs in os.walk(path):
		print fs
		for f in fs:
			create_data(path + f)

#auto('./')

create_data('./GM_wcslab.csv')
