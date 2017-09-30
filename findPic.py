#coding=utf-8
import urllib
import re
import os
import uuid
import urllib2
import cookielib

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    with open("temp.txt","w") as f:
    	f.write(html)
    return html

#def getImg(html):
#    reg = r'src="(.+?\.jpg)" pic_ext'
#    imgre = re.compile(reg)
#    imglist = re.findall(imgre,html)
#    x = 0
#    for imgurl in imglist:
#        urllib.urlretrieve(imgurl,'%s.jpg' % x)
#        x+=1


#html = getHtml("http://tieba.baidu.com/p/2460150866")

#print getImg(html)
html = getHtml("https://iroza.jp/products/10000")

nam = ''

with open("temp.txt","r") as f:
	while True:
		line = f.readline()
		if line:
			if 'detail-img-wrap' in line:
				res = line.split('href="')[1]
				res = res.split('"')[0]
				print (res)
			if 'twitter:description' in line:
				nam = line.split('content="')[1]
				nam = nam.split(' | ドリーアンドモリー | 色でアイテムを探せるセレクトショップIROZA(イロザ)')[0]
				print ('1111')
				print (nam)
		else:
			break

def get_file_extension(file):  
    return os.path.splitext(file)[1]  

'''創建文件目录，并返回该目录'''
def mkdir(path):
    # 去除左右两边的空格
    path=path.strip()
    # 去除尾部 \符号
    path=path.rstrip("\\")

    if not os.path.exists(path):
        os.makedirs(path)
        
    return path

'''自动生成一个唯一的字符串，固定长度为36'''
def unique_str():
    return str(uuid.uuid1())

'''
抓取网页文件内容，保存到内存

@url 欲抓取文件 ，path+filename
'''
def get_file(url):
    try:
        cj=cookielib.LWPCookieJar()
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        
        req=urllib2.Request(url)
        operate=opener.open(req)
        data=operate.read()
        return data
    except BaseException as e:
        print (e)
        return None
    
'''
保存文件到本地

@path  本地路径
@file_name 文件名
@data 文件内容
'''
def save_file(path, file_name, data):
    if data == None:
        return
    
    mkdir(path)
    if(not path.endswith("/")):
        path=path+"/"

    file_name = file_name.split('/')[0] + '.jpg'
    file=open(path+file_name, "wb")
    file.write(data)
    file.flush()
    file.close()


save_file("test/", '%s.jpg' % nam , get_file(res))
