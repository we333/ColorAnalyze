import sys

import emd

class category(object):
	def __init__(self):
		self.AbM = {}
		self.AM = {}
		self.BbM = {}
		self.CM = {}
		self.DbM = {}
		self.DM = {}
		self.EbM = {}
		self.EM = {}
		self.FM = {}
		self.GM = {}
		self.HM = {}	# origin is BM

		self.list = []
		self.list.append(self.AbM)
		self.list.append(self.AM)
		self.list.append(self.BbM)
		self.list.append(self.CM)
		self.list.append(self.DbM)
		self.list.append(self.DM)
		self.list.append(self.EbM)
		self.list.append(self.EM)
		self.list.append(self.FM)
		self.list.append(self.GM)
		self.list.append(self.HM)

		self.AbM[tuple((0,   102, 255))] = 15
		self.AbM[tuple((255, 26,  0  ))] = 17
		self.AbM[tuple((255, 0,   0  ))] = 35
		self.AbM[tuple((255, 0,   111))] = 30

		self.AM[tuple((255, 0,   221))] = 11
		self.AM[tuple((255, 0,   68 ))] = 13
		self.AM[tuple((255, 85,  0  ))] = 23
		self.AM[tuple((255, 0,   34 ))] = 13
		self.AM[tuple((255, 0,   0  ))] = 38

#		self.BbM[tuple((255, 238, 0  ))] = 8
#		self.BbM[tuple((0,   255, 255))] = 3
		self.BbM[tuple((0,   255, 128))] = 20
#		self.BbM[tuple((255, 119, 0  ))] = 3
		self.BbM[tuple((255, 153, 0  ))] = 62

		self.CM[tuple((0,   255, 187))] = 15
		self.CM[tuple((0,   255, 221))] = 25
		self.CM[tuple((255, 0,   0  ))] = 50

		self.DbM[tuple((255,  238, 0  ))] = 22
		self.DbM[tuple((255,  119, 0  ))] = 18
		self.DbM[tuple((255,  85,  0  ))] = 17
		self.DbM[tuple((255,  0,   34 ))] = 36

		self.DM[tuple((255, 119, 0  ))] = 30
		self.DM[tuple((255, 213, 0  ))] = 45
		self.DM[tuple((255, 85,  0  ))] = 20

		self.EbM[tuple((0,  255,  68 ))] = 12
		self.EbM[tuple((255, 0,   221))] = 15
		self.EbM[tuple((230, 0,   255))] = 29
		self.EbM[tuple((51,  255, 0  ))] = 15
		self.EbM[tuple((255, 153, 0  ))] = 27

		self.EM[tuple((255, 238, 0  ))] = 32
		self.EM[tuple((0  , 255, 9  ))] = 19
		self.EM[tuple((51,  255, 0  ))] = 18
		self.EM[tuple((25,  255, 0  ))] = 25

		self.FM[tuple((255, 238, 0  ))] = 19
		self.FM[tuple((255, 213, 0  ))] = 25
		self.FM[tuple((85,  255, 0  ))] = 18
		self.FM[tuple((25,  255, 0  ))] = 16
		self.FM[tuple((255, 153, 0  ))] = 20

		self.GM[tuple((0,   102, 255))] = 13
		self.GM[tuple((0,   255, 255))] = 35
		self.GM[tuple((0,   170, 255))] = 17
		self.GM[tuple((0,   255, 187))] = 17
		self.GM[tuple((0,   195, 255))] = 16

		self.HM[tuple((255, 0,   246))] = 23
		self.HM[tuple((255, 0,   221))] = 27
		self.HM[tuple((255, 238, 0  ))] = 10
		self.HM[tuple((0,   255, 187))] = 29

	def detect_category(self, color):
		min_distance = sys.maxint

		for i in self.list:
			dis = emd.calc_emd(color, i)
			print (dis)
			if dis < min_distance:
				min_distance = dis
				
		print ("min_distance = %f"%min_distance)
		return min_distance