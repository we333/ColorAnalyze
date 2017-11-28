#coding:utf-8
from googletrans import Translator

translator = Translator()

def trans_keyword_to_eng(text):
	res = ''
	res = res + text.split(',')[0] + ','	# 首先写入id和逗号
	tmp = text.split(',')[1]				# 获取id之后的所有keyword
	tmp = tmp.replace(' ','|')			
	str1s = tmp.split('|')					# keyword字符串分解为一个个单词便于翻译
	
	for str1 in str1s:	# 对keyword进行逐个单词翻译
		translated = translator.translate(str1,dest='en')
		translated.text = translated.text.replace(',',' ')			# 日语、可能会被翻译为，
		res = res + translated.text + ' '
	return res

def trans_file(j_file, e_file):
	fr = open(j_file)
	fw = open(e_file, 'a')
	for line in fr:
		eng = trans_keyword_to_eng(line).encode('utf-8')
		fw.write(eng+'\n')
		print (eng)

trans_file("j_keyword.csv", "e_keyword.csv")
