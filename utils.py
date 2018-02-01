# -- coding: utf-8 --

import heapq

'''
    目的：返回前k个最大值(用于去除RGB结果中的低占比杂色)
'''
class top_k_heap(object):
    def __init__(self, k):
        self.k = k
        self.data = []
 
    def push(self, elem):
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0]
            if elem > topk_small:
                heapq.heapreplace(self.data, elem)
 
    def top_k(self):
        return [x for x in reversed([heapq.heappop(self.data) for x in xrange(len(self.data))])]

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

	if 		len(strHes) == 1:	res = '#00000' + strHes
	elif	len(strHes) == 2:	res = '#0000' + strHes
	elif	len(strHes) == 3:	res = '#000' + strHes
	elif	len(strHes) == 4:	res = '#00' + strHes
	elif	len(strHes) == 5:	res = '#0' + strHes
	else:	res = '#' + strHes

	return res 

'''
    目的：RGBをLabに変更(Lab色で、Munsell上の座標を決める)
    ps：wcslab.csv的数据是基于lab色的，【把wcslab里的lab换成rgb，以后直接通过rgb计算Munsell坐标】效率会更高。但不想修改wcslab.csv原式数据，所以还是要rgb转lab
'''
def rgb2lab(inputColor) :
    num = 0
    RGB = [0, 0, 0]

    for value in inputColor :
        value = float(value) / 255
        if value > 0.04045 :
           value = ((value + 0.055) / 1.055) ** 2.4
        else :
           value = value / 12.92
        RGB[num] = value * 100
        num = num + 1

    XYZ = [0, 0, 0,]
    X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
    Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
    Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9505
    XYZ[0] = round(X, 4)
    XYZ[1] = round(Y, 4)
    XYZ[2] = round(Z, 4)

    XYZ[0] = float( XYZ[0] ) / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
    XYZ[1] = float( XYZ[1] ) / 100.0          # ref_Y = 100.000
    XYZ[2] = float( XYZ[2] ) / 108.883        # ref_Z = 108.883

    num = 0
    for value in XYZ :
        if value > 0.008856 :
           value = value ** (0.3333333333333333)
        else :
           value = (7.787 * value) + (16 / 116)
        XYZ[num] = value
        num = num + 1

    Lab = [0, 0, 0]
    L = (116 * XYZ[1] ) - 16
    a = 500 * ( XYZ[0] - XYZ[1] )
    b = 200 * ( XYZ[1] - XYZ[2] )

    Lab [0] = round(L, 4)
    Lab [1] = round(a, 4)
    Lab [2] = round(b, 4)

    return Lab

import sys
from colormath.color_diff import delta_e_cie2000, delta_e_cmc
from colormath.color_objects import LabColor

'''
    目的：カラーベースフィルタリング実行する前に、wcslabのデータを読み込んで、調性格を推定する時使われる
    wcslabのデータ：各Lab色と対応するMunsell上の座標
'''
class calc_wcslab_cie2000(object):
    def __init__(self, wcslab_file):
        self.wl = []
        self.wl_file = wcslab_file

        self._load_wcslab()

    def _load_wcslab(self):
        f_r = open(self.wl_file, 'r')
        for line in f_r:
            data = line.split(",")
            self.wl.append(data)
    
    def _get_location(self, lab_color):
        min_dis = sys.maxint
        lab = LabColor(lab_l = lab_color[0], lab_a = lab_color[1], lab_b = lab_color[2])
        
        for i in range(len(self.wl)):
            tmp_lab = LabColor(lab_l = self.wl[i][0], lab_a = self.wl[i][1], lab_b = self.wl[i][2])
            dis = delta_e_cie2000(lab, tmp_lab)
            if min_dis > dis:
                min_dis = dis
                min_line = i
                min_chip_x = self.wl[i][3]
                min_chip_y = self.wl[i][4]
    #    print min_chip_x,min_chip_y,min_dis,min_line
        return float(min_chip_x), float(min_chip_y)

    def create_chart(self, rgb):
        chart = {}
        for i in rgb:
            lab = rgb2lab(i)
            x,y = self._get_location(lab)
            point = tuple((x, y))
            if chart.has_key(point):
                chart[point] = chart[point] + 1
            else:
                chart[point] = 1
        return chart

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
