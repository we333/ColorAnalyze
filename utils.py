
def hex2rgb(hexcolor):
	rgb = [(hexcolor >> 16) & 0xff,
	  (hexcolor >> 8) & 0xff,
	  hexcolor & 0xff
	 ]
	return rgb

def rgb2hex(rgbcolor):
	r, g, b = rgbcolor
	Hex = ((r << 16) + (g << 8) + b)
	strHes = str(hex(Hex)).split('0x')[1]
	strHes = strHes.split('L')[0]

	if 	len(strHes) == 1:	res = '#00000' + strHes
	elif	len(strHes) == 2:	res = '#0000' + strHes
	elif	len(strHes) == 3:	res = '#000' + strHes
	elif	len(strHes) == 4:	res = '#00' + strHes
	elif	len(strHes) == 5:	res = '#0' + strHes
	else:	res = '#' + strHes

	return res 

def plot(obj):
	colors = []
	occupy = []

	for k,v in obj.color.items():
	#	print ('%s = %d'%(k, float(v)/obj.file_num))
		c = rgb2hex(k)
		colors.append(c)
		occupy.append(v)
		#cv2.waitKey()
		#cv2.destroyAllWindows()

	plt.bar(range(len(occupy)), occupy, color=list(colors))
	plt.show()
