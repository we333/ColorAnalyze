import sys

import emd

'''
	各調性格のMunsell上分布データを初期化
	分布データを用いてEMD距離計算して、商品の調性格を推定
'''
class category(object):
	def __init__(self):
		self.result = ["AbM", "AM", "BbM", "BM", "CM", "DbM", "DM", "EbM", "EM", "FM", "FsM", "GM"]

		self.AbM = {}
		self.AM = {}
		self.BbM = {}
		self.BM = {}
		self.CM = {}
		self.DbM = {}
		self.DM = {}
		self.EbM = {}
		self.EM = {}
		self.FM = {}
		self.FsM = {}
		self.GM = {}

		self.list = []
		self.list.append(self.AbM)
		self.list.append(self.AM)
		self.list.append(self.BbM)
		self.list.append(self.BM)
		self.list.append(self.CM)
		self.list.append(self.DbM)
		self.list.append(self.DM)
		self.list.append(self.EbM)
		self.list.append(self.EM)
		self.list.append(self.FM)
		self.list.append(self.FsM)
		self.list.append(self.GM)

		#　AbM調性格がMunsell上の分布、例えば座標(20,3)の占有率は3%
		#　内容は長いから、Pythonで作成されます
		self.AbM[tuple((20,3))] = 0.03
		self.AbM[tuple((11,2))] = 0.03
		self.AbM[tuple((17,3))] = 0.03
		self.AbM[tuple((8,5))] = 0.03
		self.AbM[tuple((5,5))] = 0.03
		self.AbM[tuple((38,6))] = 0.03
		self.AbM[tuple((37,6))] = 0.091
		self.AbM[tuple((26,3))] = 0.03
		self.AbM[tuple((19,3))] = 0.03
		self.AbM[tuple((22,3))] = 0.03
		self.AbM[tuple((2,6))] = 0.03
		self.AbM[tuple((13,2))] = 0.091
		self.AbM[tuple((15,3))] = 0.03
		self.AbM[tuple((9,3))] = 0.061
		self.AbM[tuple((14,2))] = 0.03
		self.AbM[tuple((41,7))] = 0.061
		self.AbM[tuple((8,3))] = 0.03
		self.AbM[tuple((4,6))] = 0.152
		self.AbM[tuple((13,3))] = 0.03
		self.AbM[tuple((21,3))] = 0.03
		self.AbM[tuple((41,6))] = 0.03
		self.AbM[tuple((38,5))] = 0.03
		self.AbM[tuple((10,2))] = 0.03

		self.AM[tuple((34,7))] = 0.025
		self.AM[tuple((4,7))] = 0.025
		self.AM[tuple((5,6))] = 0.012
		self.AM[tuple((11,2))] = 0.025
		self.AM[tuple((37,7))] = 0.012
		self.AM[tuple((17,3))] = 0.025
		self.AM[tuple((9,4))] = 0.025
		self.AM[tuple((32,9))] = 0.012
		self.AM[tuple((3,7))] = 0.012
		self.AM[tuple((29,4))] = 0.012
		self.AM[tuple((12,2))] = 0.012
		self.AM[tuple((5,5))] = 0.037
		self.AM[tuple((37,6))] = 0.049
		self.AM[tuple((16,3))] = 0.074
		self.AM[tuple((31,5))] = 0.012
		self.AM[tuple((32,7))] = 0.012
		self.AM[tuple((33,6))] = 0.025
		self.AM[tuple((30,5))] = 0.025
		self.AM[tuple((35,7))] = 0.012
		self.AM[tuple((41,7))] = 0.025
		self.AM[tuple((12,3))] = 0.012
		self.AM[tuple((22,3))] = 0.037
		self.AM[tuple((6,4))] = 0.025
		self.AM[tuple((36,4))] = 0.012
		self.AM[tuple((37,5))] = 0.037
		self.AM[tuple((4,5))] = 0.012
		self.AM[tuple((9,3))] = 0.012
		self.AM[tuple((40,6))] = 0.025
		self.AM[tuple((4,6))] = 0.173
		self.AM[tuple((2,7))] = 0.025
		self.AM[tuple((34,6))] = 0.012
		self.AM[tuple((18,3))] = 0.012
		self.AM[tuple((6,8))] = 0.025
		self.AM[tuple((36,5))] = 0.037
		self.AM[tuple((3,6))] = 0.025
		self.AM[tuple((14,3))] = 0.012
		self.AM[tuple((32,8))] = 0.025
		self.AM[tuple((8,4))] = 0.012

		self.BbM[tuple((34,7))] = 0.012
		self.BbM[tuple((8,4))] = 0.012
		self.BbM[tuple((17,7))] = 0.012
		self.BbM[tuple((11,2))] = 0.025
		self.BbM[tuple((37,3))] = 0.012
		self.BbM[tuple((16,2))] = 0.012
		self.BbM[tuple((2,6))] = 0.012
		self.BbM[tuple((29,4))] = 0.012
		self.BbM[tuple((8,5))] = 0.012
		self.BbM[tuple((12,2))] = 0.012
		self.BbM[tuple((31,8))] = 0.012
		self.BbM[tuple((5,5))] = 0.025
		self.BbM[tuple((13,3))] = 0.025
		self.BbM[tuple((37,6))] = 0.012
		self.BbM[tuple((16,3))] = 0.049
		self.BbM[tuple((26,3))] = 0.012
		self.BbM[tuple((32,7))] = 0.012
		self.BbM[tuple((6,3))] = 0.012
		self.BbM[tuple((1,5))] = 0.025
		self.BbM[tuple((40,5))] = 0.025
		self.BbM[tuple((1,1))] = 0.012
		self.BbM[tuple((12,3))] = 0.012
		self.BbM[tuple((22,3))] = 0.012
		self.BbM[tuple((17,5))] = 0.012
		self.BbM[tuple((36,4))] = 0.025
		self.BbM[tuple((13,2))] = 0.012
		self.BbM[tuple((4,5))] = 0.012
		self.BbM[tuple((15,3))] = 0.037
		self.BbM[tuple((9,3))] = 0.086
		self.BbM[tuple((33,5))] = 0.012
		self.BbM[tuple((21,4))] = 0.012
		self.BbM[tuple((6,4))] = 0.025
		self.BbM[tuple((14,2))] = 0.025
		self.BbM[tuple((38,4))] = 0.012
		self.BbM[tuple((8,3))] = 0.012
		self.BbM[tuple((4,6))] = 0.111
		self.BbM[tuple((15,2))] = 0.074
		self.BbM[tuple((22,4))] = 0.012
		self.BbM[tuple((36,5))] = 0.025
		self.BbM[tuple((38,6))] = 0.012
		self.BbM[tuple((21,3))] = 0.012
		self.BbM[tuple((7,4))] = 0.012
		self.BbM[tuple((37,8))] = 0.012
		self.BbM[tuple((32,8))] = 0.025
		self.BbM[tuple((10,2))] = 0.037


		self.BM[tuple((22,3))] = 0.062
		self.BM[tuple((39,3))] = 0.031
		self.BM[tuple((36,3))] = 0.031
		self.BM[tuple((13,2))] = 0.062
		self.BM[tuple((4,6))] = 0.062
		self.BM[tuple((38,4))] = 0.031
		self.BM[tuple((37,6))] = 0.094
		self.BM[tuple((16,3))] = 0.219
		self.BM[tuple((36,4))] = 0.062
		self.BM[tuple((26,3))] = 0.031
		self.BM[tuple((1,4))] = 0.031
		self.BM[tuple((11,2))] = 0.031
		self.BM[tuple((38,3))] = 0.031
		self.BM[tuple((1,5))] = 0.031
		self.BM[tuple((6,2))] = 0.031
		self.BM[tuple((3,6))] = 0.031
		self.BM[tuple((36,2))] = 0.031
		self.BM[tuple((14,2))] = 0.031
		self.BM[tuple((1,1))] = 0.062


		self.CM[tuple((31,6))] = 0.014
		self.CM[tuple((16,2))] = 0.014
		self.CM[tuple((17,3))] = 0.029
		self.CM[tuple((41,5))] = 0.014
		self.CM[tuple((12,2))] = 0.029
		self.CM[tuple((22,2))] = 0.014
		self.CM[tuple((3,3))] = 0.014
		self.CM[tuple((37,6))] = 0.043
		self.CM[tuple((4,4))] = 0.014
		self.CM[tuple((23,2))] = 0.029
		self.CM[tuple((3,6))] = 0.014
		self.CM[tuple((1,1))] = 0.214
		self.CM[tuple((22,3))] = 0.071
		self.CM[tuple((14,2))] = 0.014
		self.CM[tuple((2,6))] = 0.014
		self.CM[tuple((13,2))] = 0.029
		self.CM[tuple((9,3))] = 0.014
		self.CM[tuple((24,2))] = 0.014
		self.CM[tuple((25,3))] = 0.029
		self.CM[tuple((5,5))] = 0.029
		self.CM[tuple((4,6))] = 0.2
		self.CM[tuple((21,3))] = 0.014
		self.CM[tuple((32,8))] = 0.043
		self.CM[tuple((3,4))] = 0.014
		self.CM[tuple((38,5))] = 0.029
		self.CM[tuple((10,2))] = 0.043


		self.DbM[tuple((20,3))] = 0.03
		self.DbM[tuple((11,2))] = 0.03
		self.DbM[tuple((17,3))] = 0.03
		self.DbM[tuple((8,5))] = 0.03
		self.DbM[tuple((5,5))] = 0.03
		self.DbM[tuple((38,6))] = 0.03
		self.DbM[tuple((37,6))] = 0.091
		self.DbM[tuple((26,3))] = 0.03
		self.DbM[tuple((19,3))] = 0.03
		self.DbM[tuple((22,3))] = 0.03
		self.DbM[tuple((2,6))] = 0.03
		self.DbM[tuple((13,2))] = 0.091
		self.DbM[tuple((15,3))] = 0.03
		self.DbM[tuple((9,3))] = 0.061
		self.DbM[tuple((14,2))] = 0.03
		self.DbM[tuple((41,7))] = 0.061
		self.DbM[tuple((8,3))] = 0.03
		self.DbM[tuple((4,6))] = 0.152
		self.DbM[tuple((13,3))] = 0.03
		self.DbM[tuple((21,3))] = 0.03
		self.DbM[tuple((41,6))] = 0.03
		self.DbM[tuple((38,5))] = 0.03
		self.DbM[tuple((10,2))] = 0.03


		self.DM[tuple((5,6))] = 0.037
		self.DM[tuple((11,2))] = 0.013
		self.DM[tuple((17,3))] = 0.013
		self.DM[tuple((23,2))] = 0.013
		self.DM[tuple((10,2))] = 0.013
		self.DM[tuple((12,2))] = 0.025
		self.DM[tuple((22,2))] = 0.013
		self.DM[tuple((5,5))] = 0.025
		self.DM[tuple((13,3))] = 0.125
		self.DM[tuple((4,4))] = 0.013
		self.DM[tuple((26,3))] = 0.025
		self.DM[tuple((32,7))] = 0.025
		self.DM[tuple((29,3))] = 0.013
		self.DM[tuple((40,5))] = 0.013
		self.DM[tuple((1,1))] = 0.013
		self.DM[tuple((12,3))] = 0.062
		self.DM[tuple((22,3))] = 0.013
		self.DM[tuple((6,4))] = 0.013
		self.DM[tuple((5,4))] = 0.013
		self.DM[tuple((2,6))] = 0.013
		self.DM[tuple((13,2))] = 0.075
		self.DM[tuple((37,5))] = 0.013
		self.DM[tuple((9,3))] = 0.037
		self.DM[tuple((14,3))] = 0.037
		self.DM[tuple((3,5))] = 0.013
		self.DM[tuple((38,4))] = 0.05
		self.DM[tuple((8,3))] = 0.025
		self.DM[tuple((4,6))] = 0.138
		self.DM[tuple((36,5))] = 0.013
		self.DM[tuple((11,3))] = 0.013
		self.DM[tuple((7,4))] = 0.037
		self.DM[tuple((25,2))] = 0.013
		self.DM[tuple((32,8))] = 0.013
		self.DM[tuple((41,6))] = 0.013
		self.DM[tuple((2,4))] = 0.013
		self.DM[tuple((8,4))] = 0.013


		self.EbM[tuple((40,3))] = 0.013
		self.EbM[tuple((20,3))] = 0.025
		self.EbM[tuple((17,7))] = 0.013
		self.EbM[tuple((37,3))] = 0.013
		self.EbM[tuple((17,8))] = 0.013
		self.EbM[tuple((39,4))] = 0.013
		self.EbM[tuple((23,3))] = 0.013
		self.EbM[tuple((17,3))] = 0.013
		self.EbM[tuple((30,4))] = 0.013
		self.EbM[tuple((10,3))] = 0.013
		self.EbM[tuple((12,2))] = 0.013
		self.EbM[tuple((5,5))] = 0.013
		self.EbM[tuple((13,3))] = 0.037
		self.EbM[tuple((37,6))] = 0.013
		self.EbM[tuple((16,3))] = 0.125
		self.EbM[tuple((31,5))] = 0.013
		self.EbM[tuple((17,2))] = 0.013
		self.EbM[tuple((30,5))] = 0.013
		self.EbM[tuple((15,4))] = 0.013
		self.EbM[tuple((12,3))] = 0.025
		self.EbM[tuple((22,3))] = 0.025
		self.EbM[tuple((17,5))] = 0.037
		self.EbM[tuple((2,6))] = 0.013
		self.EbM[tuple((13,2))] = 0.062
		self.EbM[tuple((3,6))] = 0.013
		self.EbM[tuple((16,4))] = 0.013
		self.EbM[tuple((15,3))] = 0.013
		self.EbM[tuple((36,4))] = 0.013
		self.EbM[tuple((6,4))] = 0.013
		self.EbM[tuple((14,2))] = 0.013
		self.EbM[tuple((17,4))] = 0.013
		self.EbM[tuple((38,4))] = 0.025
		self.EbM[tuple((8,3))] = 0.013
		self.EbM[tuple((19,9))] = 0.013
		self.EbM[tuple((18,3))] = 0.087
		self.EbM[tuple((4,6))] = 0.1
		self.EbM[tuple((36,5))] = 0.013
		self.EbM[tuple((3,4))] = 0.013
		self.EbM[tuple((7,4))] = 0.013
		self.EbM[tuple((14,3))] = 0.025
		self.EbM[tuple((32,8))] = 0.013
		self.EbM[tuple((41,6))] = 0.013
		self.EbM[tuple((8,4))] = 0.037


		self.EM[tuple((22,3))] = 0.061
		self.EM[tuple((40,3))] = 0.03
		self.EM[tuple((2,6))] = 0.03
		self.EM[tuple((18,3))] = 0.061
		self.EM[tuple((5,5))] = 0.03
		self.EM[tuple((15,2))] = 0.03
		self.EM[tuple((38,6))] = 0.03
		self.EM[tuple((36,5))] = 0.03
		self.EM[tuple((20,2))] = 0.03
		self.EM[tuple((16,3))] = 0.121
		self.EM[tuple((13,3))] = 0.03
		self.EM[tuple((37,6))] = 0.03
		self.EM[tuple((23,3))] = 0.03
		self.EM[tuple((13,2))] = 0.242
		self.EM[tuple((27,2))] = 0.03
		self.EM[tuple((12,3))] = 0.061
		self.EM[tuple((4,6))] = 0.121


		self.FM[tuple((34,7))] = 0.025
		self.FM[tuple((16,6))] = 0.012
		self.FM[tuple((17,7))] = 0.012
		self.FM[tuple((5,6))] = 0.025
		self.FM[tuple((11,2))] = 0.012
		self.FM[tuple((32,6))] = 0.012
		self.FM[tuple((17,3))] = 0.062
		self.FM[tuple((9,4))] = 0.012
		self.FM[tuple((30,4))] = 0.012
		self.FM[tuple((11,4))] = 0.012
		self.FM[tuple((29,4))] = 0.012
		self.FM[tuple((10,3))] = 0.012
		self.FM[tuple((25,3))] = 0.012
		self.FM[tuple((6,7))] = 0.012
		self.FM[tuple((5,5))] = 0.012
		self.FM[tuple((13,3))] = 0.049
		self.FM[tuple((37,6))] = 0.025
		self.FM[tuple((16,3))] = 0.074
		self.FM[tuple((16,4))] = 0.012
		self.FM[tuple((17,6))] = 0.025
		self.FM[tuple((12,3))] = 0.012
		self.FM[tuple((22,3))] = 0.049
		self.FM[tuple((17,5))] = 0.012
		self.FM[tuple((7,6))] = 0.012
		self.FM[tuple((13,2))] = 0.037
		self.FM[tuple((10,4))] = 0.012
		self.FM[tuple((11,7))] = 0.012
		self.FM[tuple((9,3))] = 0.025
		self.FM[tuple((26,4))] = 0.012
		self.FM[tuple((8,7))] = 0.012
		self.FM[tuple((40,6))] = 0.025
		self.FM[tuple((14,2))] = 0.012
		self.FM[tuple((6,5))] = 0.012
		self.FM[tuple((38,4))] = 0.012
		self.FM[tuple((8,3))] = 0.012
		self.FM[tuple((18,3))] = 0.037
		self.FM[tuple((4,6))] = 0.049
		self.FM[tuple((15,2))] = 0.012
		self.FM[tuple((36,5))] = 0.025
		self.FM[tuple((38,6))] = 0.025
		self.FM[tuple((11,3))] = 0.025
		self.FM[tuple((7,4))] = 0.012
		self.FM[tuple((14,3))] = 0.012
		self.FM[tuple((32,8))] = 0.012
		self.FM[tuple((27,3))] = 0.012
		self.FM[tuple((11,6))] = 0.012
		self.FM[tuple((8,4))] = 0.049


		self.FsM[tuple((22,3))] = 0.062
		self.FsM[tuple((39,3))] = 0.031
		self.FsM[tuple((36,3))] = 0.031
		self.FsM[tuple((13,2))] = 0.062
		self.FsM[tuple((4,6))] = 0.062
		self.FsM[tuple((38,4))] = 0.031
		self.FsM[tuple((37,6))] = 0.094
		self.FsM[tuple((16,3))] = 0.219
		self.FsM[tuple((36,4))] = 0.062
		self.FsM[tuple((26,3))] = 0.031
		self.FsM[tuple((1,4))] = 0.031
		self.FsM[tuple((11,2))] = 0.031
		self.FsM[tuple((38,3))] = 0.031
		self.FsM[tuple((1,5))] = 0.031
		self.FsM[tuple((6,2))] = 0.031
		self.FsM[tuple((3,6))] = 0.031
		self.FsM[tuple((36,2))] = 0.031
		self.FsM[tuple((14,2))] = 0.031
		self.FsM[tuple((1,1))] = 0.062


		self.GM[tuple((34,7))] = 0.013
		self.GM[tuple((30,3))] = 0.013
		self.GM[tuple((26,2))] = 0.025
		self.GM[tuple((32,6))] = 0.038
		self.GM[tuple((17,3))] = 0.025
		self.GM[tuple((32,9))] = 0.013
		self.GM[tuple((30,4))] = 0.013
		self.GM[tuple((29,4))] = 0.051
		self.GM[tuple((13,3))] = 0.076
		self.GM[tuple((37,6))] = 0.025
		self.GM[tuple((16,3))] = 0.076
		self.GM[tuple((31,5))] = 0.063
		self.GM[tuple((26,3))] = 0.013
		self.GM[tuple((32,7))] = 0.013
		self.GM[tuple((30,5))] = 0.025
		self.GM[tuple((12,3))] = 0.013
		self.GM[tuple((22,3))] = 0.101
		self.GM[tuple((5,4))] = 0.013
		self.GM[tuple((37,5))] = 0.013
		self.GM[tuple((28,3))] = 0.013
		self.GM[tuple((25,2))] = 0.013
		self.GM[tuple((26,4))] = 0.013
		self.GM[tuple((31,3))] = 0.013
		self.GM[tuple((25,3))] = 0.025
		self.GM[tuple((17,4))] = 0.038
		self.GM[tuple((29,6))] = 0.013
		self.GM[tuple((8,3))] = 0.013
		self.GM[tuple((4,6))] = 0.063
		self.GM[tuple((36,5))] = 0.013
		self.GM[tuple((14,3))] = 0.025
		self.GM[tuple((32,8))] = 0.127
		self.GM[tuple((27,3))] = 0.013

	'''
		color：商品のLab色
		return：商品の調性格結果(AbM、AMなどの文字列)
	'''
	def detect_category(self, color):
		min_distance = sys.maxint
		ret = 0

		for i in range(len(self.list)):

			dis = emd.calc_emd(color, self.list[i])
			print ("%s --> %.2f"%(self.result[i], dis))
			if dis < min_distance:
				min_distance = dis
				ret = i

		return min_distance, self.result[ret]