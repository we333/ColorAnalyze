import matplotlib.pyplot as plt

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

class plot(object):
	def __init__(self,color):
		self.color = color
		self.colors = []
		self.occupy = []

	def show(self):
		for k,v in self.color.items():
			c = rgb2hex(k)
	    	self.colors.append(c)
	    	self.occupy.append(v)

		plt.bar(range(len(self.occupy)), self.occupy, color=list(self.colors))
		plt.show()