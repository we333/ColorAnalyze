#!/usr/bin/env python
# -- coding: utf-8 --

import argparse

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2

def show_page_views(service):
    results = service.reports().batchGet(
        body={
            'reportRequests': [
                {
                 #   'viewId': '119302976',
                    'viewId': '100411459',
                    'pageSize': '100000',
                    'dateRanges': [{'startDate': '2017-06-01', 'endDate': '2017-09-25'}],
                    'dimensions': [
                        {
                            'name': 'ga:pagePath',
                        }
                    ],
                    'metrics': [{'expression': 'ga:pageviews',}
                    ] 
                }
            ]
        }
    ).execute()
      
    if results:
        with open('result.txt','w') as f:
            for report in results.get('reports', []):
                columnHeader = report.get('columnHeader', {})
                dimensionHeaders = columnHeader.get('dimensions', [])
                metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
                rows = report.get('data', {}).get('rows', [])
              
                for row in rows:
                  
                    dimensions = row.get('dimensions', [])
                    dateRangeValues = row.get('metrics', [])

                    for header, dimension in zip(dimensionHeaders, dimensions):
                        f.write(header + ':' + dimension +'~~')
                        for i, values in enumerate(dateRangeValues):
                            for metricHeader, value in zip(metricHeaders, values.get('values')):
                                f.write(metricHeader.get('name') + ':' + value+'\r\n')      
    else:
        print('No results found')

if __name__ == '__main__':
    scope = ['https://www.googleapis.com/auth/analytics.readonly']
    discoveryURI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
    email = 'miyabi@miyabi-mix.iam.gserviceaccount.com'
    key = './client_secrets.p12'
    password = 'notasecret'
    credentials = ServiceAccountCredentials.from_p12_keyfile(email, key, private_key_password=password, scopes=scope)
    http = credentials.authorize(httplib2.Http())

    api_name = 'analytics'
    api_version = 'v4'
    service = build(api_name, api_version, http=http, discoveryServiceUrl=discoveryURI)

    show_page_views(service)
