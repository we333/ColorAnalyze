#coding=utf-8
import urllib
import re

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    with open("temp.txt","w") as f:
    	f.write(html)
    return html

html = getHtml("https://iroza.jp/products/10000")

with open("temp.txt","r") as f:
	while True:
		line = f.readline()
		if line:
			if 'detail-img-wrap' in line:
				res = line.split('href="')[1]
				res = res.split('"')[0]
				print (res)
				break
		else:
			break
