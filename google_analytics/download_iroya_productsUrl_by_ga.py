#!/usr/bin/env python
#coding=utf-8 

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import argparse

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2

import urllib
import re

class Ga(object):
    def __init__(self):
        self.token = '--'   # 分割pagePath和pageviews

        scope = ['https://www.googleapis.com/auth/analytics.readonly']
        discoveryURI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
        email = 'miyabi@miyabi-mix.iam.gserviceaccount.com'
        key = './client_secrets.p12'
        password = 'notasecret'
        credentials = ServiceAccountCredentials.from_p12_keyfile(email, key, private_key_password=password, scopes=scope)
        http = credentials.authorize(httplib2.Http())

        api_name = 'analytics'
        api_version = 'v4'
        self.service = build(api_name, api_version, http=http, discoveryServiceUrl=discoveryURI)

    def get_page_views(self, file_name, start_date, end_date):
        results = self.service.reports().batchGet(
            body={
                'reportRequests': [
                    {
                     #   'viewId': '119302976',
                        'viewId': '100411459',
                        'pageSize': 10000,
                        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                        'dimensions': [{'name': 'ga:pagePath',}],
                        'metrics': [{'expression': 'ga:pageviews',}] 
                    }
                ]
            }
        ).execute()

        if results:
            with open(file_name+'.txt', 'a') as f:
                for report in results.get('reports', []):
                    columnHeader = report.get('columnHeader', {})
                    dimensionHeaders = columnHeader.get('dimensions', [])
                    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
                    rows = report.get('data', {}).get('rows', [])
                  
                    is_product = False

                    for row in rows:   
                        dimensions = row.get('dimensions', [])
                        dateRangeValues = row.get('metrics', [])

                        for header, dimension in zip(dimensionHeaders, dimensions):
                            if '/products/' in dimension:
                                is_product = True
                                f.write('https://iroza.jp' + dimension + self.token)
                        if is_product == True:
                            is_product = False 
                            for i, values in enumerate(dateRangeValues):
                            #    f.write('Date range (' + str(i) + ')'+'\r\n')
                                for metricHeader, value in zip(metricHeaders, values.get('values')):
                                #           print(metricHeader.get('name') + ': ' + value)
                                    f.write(metricHeader.get('name') + ': ' + value+'\r\n')                                       
        else:
            print('No results found')

    def _change_date_format(self, month, day):
        if day < 10:    str_day = '0'+str(day)
        else:           str_day = str(day)        

        return month + '-' + str_day

    def get_page_views_month(self, month):
        days = 0
        m = int(month.split('-')[1])

        if m == 1:  days = 31
        if m == 2:  days = 28
        if m == 3:  days = 31
        if m == 4:  days = 30
        if m == 5:  days = 31
        if m == 6:  days = 30
        if m == 7:  days = 31
        if m == 8:  days = 31
        if m == 9:  days = 30
        if m == 10: days = 31
        if m == 11: days = 30
        if m == 12: days = 31

        for i in range(1,days):
            today = i
            tomorrow = i+1

            str_today = self._change_date_format(month, today)
            str_tomorrow = self._change_date_format(month, tomorrow)
            print ('%s -- %s'%(str_today, str_tomorrow))
            self.get_page_views(month, str_today, str_tomorrow)

    def get_page_views_year(self, year):
        for i in range(1, 13):
            if i < 10:  str_month = '0' + str(i)
            else:       str_month = str(i)            
            month = year + '-' + str_month
            self.get_page_views_month(month)

    def _save_url(self, url):
        page = urllib.urlopen(url)
        html = page.read()
        with open("temp.txt","w") as f:
            f.write(html)
        return html

    def get_one_image_url(self, url):
        html = self._save_url(url)
        with open("temp.txt","r") as f:
            while True:
                line = f.readline()
                if line:
                    if 'detail-img-wrap' in line:   # 提取图片url
                        res = line.split('href="')[1]
                        res = res.split('"')[0]
                        print (res)
                        break
                    if 'twitter:description' in line:
                        name = line.split('content="')[1]
                        name = name.split(' | ドリーアンドモリー | 色でアイテムを探せるセレクトショップIROZA(イロザ)')[0]
                        print (name)
                    #    os.remove("temp.txt")
                else:
                    break

    def get_month_image_url(self, month):
        with open(month,"r") as f:
            while True:
                line = f.readline()
                if line:
                    url = line.split(self.token)[0]
                    self.get_one_image_url(url)
                else:
                    break

ga = Ga()
#ga.get_page_views('2017-07', '2017-07-01', '2017-07-02')
#ga.get_page_views_month('2016-10')
#ga.get_page_views_year('2016')
ga.get_month_image_url('./data/2017-09.txt')


