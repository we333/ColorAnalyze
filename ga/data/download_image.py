#coding=utf-8

import urllib
import re
import os
import uuid
import urllib2
import cookielib

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    with open("temp.txt","w") as f:
    	f.write(html)
    return html

def get_file_extension(file):  
    return os.path.splitext(file)[1]  

def mkdir(path):
    
    path=path.strip()
    
    path=path.rstrip("\\")

    if not os.path.exists(path):
        os.makedirs(path)
        
    return path

def unique_str():
    return str(uuid.uuid1())

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

def save_url(url, saveto):
	with open(saveto, "a") as f:
		print ("write is %s"%url)
		f.write(url)

def save_file(path, file_name, data):
	if data == None:
	    return

	mkdir(path)
	if(not path.endswith("/")):
	    path=path+"/"

	num_of_token = 0
	f = []
	res = ''
	try:
		f.append(file_name.split('/')[0])
		num_of_token = 0
		f.append(file_name.split('/')[1])
		num_of_token = 1
		f.append(file_name.split('/')[2])
		num_of_token = 2
		f.append(file_name.split('/')[3])
		num_of_token = 3
		f.append(file_name.split('/')[4])
		num_of_token = 4
	except:
		pass
	else:
		pass

	for i in range(0, num_of_token+1):
		res += f[i]
	res += '.jpg'

	file=open(path+res, "wb")
	file.write(data)
	file.flush()
	file.close()

def download_image(url_file):
	file = open(url_file)

	for line in file:
		sitename = line.split('--')[0]
		html = getHtml(sitename)
		nam = ''
		res = ''
		with open("temp.txt","r") as f:
			while True:
				html_line = f.readline()
				if html_line:
					if 'detail-img-wrap' in html_line:
						res = html_line.split('href="')[1]
						res = res.split('"')[0]
						print (res)
					if 'keywords' in html_line:	# html中更准确的颜色描述信息
						nam = html_line.split('content="')[1]
						nam = nam.split('"')[0]
						nam = nam.split(",IROZA,イロザ")[0]
						num = line.split('--')[0].split('/')[-1]
						nam = num + '--' + nam
						os.remove("temp.txt")
				else:
					break
		save_file(url_file.split('.')[0], '%s' % nam , get_file(res))

##################################################################
# 	
##################################################################
def download_test_image(url_file, category_name):
	file = open(url_file)

	for line in file:
		sitename = line.split('--')[0]
		html = getHtml(sitename)
		nam = ''
		res = ''
		with open("temp.txt","r") as f:
			while True:
				html_line = f.readline()
				if html_line:
					if category_name in html_line:
						name = line.split('--')[0].split('/')[-1]
						save_url(line, "result.txt")
						continue
				else:
					break
	
#download_test_image('2017-07.txt', 'アウター')
download_image("result.txt")