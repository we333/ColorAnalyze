#coding:utf-8
from googletrans import Translator
translator = Translator()

class trans(object):
	def __init__(self):
		self.translator = Translator()
	def run(self, text):
		
		tmp = text.replace(' ',',')
		str1s = tmp.split(',')
		res = ''
		for str1 in str1s:	
			translated = self.translator.translate(str1,dest='en')
			res = res + translated.text + ' '
		print res
		return res
