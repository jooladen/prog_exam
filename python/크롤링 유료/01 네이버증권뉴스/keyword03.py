from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import os

import requests
import hmac
import time

## 네이버 디벨로퍼스
import urllib.request
import json

import hashlib
import hmac
import base64

class Signature:

    @staticmethod
    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)

        hash.hexdigest()
        return base64.b64encode(hash.digest())

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = Signature.generate(timestamp, method, uri, secret_key)
    
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 
            'X-API-KEY': api_key, 'X-Customer': str(customer_id), 'X-Signature': signature}

#BASE_URL = 'https://api.searchad.naver.com'
BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000c6d85b711847dd9cc75fd8a871b12eb61c9d23bf8aa12e998a6eb618b77ffd55'
SECRET_KEY = 'AQAAAACUIl5duGI+KnLo1dWvs+hThAJz7k28wJRLE+XUuy3/KQ=='
CUSTOMER_ID = '3455835'

uri = '/keywordstool'
method = 'GET'

params={}
params['hintKeywords']='CHATGPT' 
params['showDetail']=1

r = requests.get(BASE_URL + uri, params=params, 
                 headers = get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

response = r.json()

#print(response)

data_list = response['keywordList']

# 연관키워드 / 검색량 결과 저장공간간
keyword_lists = []
PC_mount = []
MO_mount = []

## 검색건수
search_result_mount = []

## 검색량/검색건수 비율 
search_per_result_ratio = []

block1 = ""
block2 = ""
block3 = ""
block4 = ""
block5 = ""

# if len(data_list) < 10:
#     for i in range(0, len(data_list)):
#         keyword_lists.append(data_list[i]['relKeyword'])
#         PC_mount.append(data_list[i]['monthlyPcQcCnt'])
#         MO_mount.append(data_list[i]['monthlyMobileQcCnt'])
#         print("키워드: " + str(data_list[i]['relKeyword']) + " , "
#               "PC검색량: " + str(data_list[i]['monthlyPcQcCnt']) + "건, "
#               "MO검색량: " + str(data_list[i]['monthlyMobileQcCnt']) + "건")

#         client_id = "OOOwOkFmGACcqwV269OU"
#         client_secret = "lbJwq0cr3d"
#         encText = urllib.parse.quote(data_list[i]['relKeyword'])
#         url = "https://openapi.naver.com/v1/search/blog?query=" + encText # JSON 결과
#             # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
#         request = urllib.request.Request(url)
#         request.add_header("X-Naver-Client-Id",client_id)
#         request.add_header("X-Naver-Client-Secret",client_secret)
#         response = urllib.request.urlopen(request)
#         rescode = response.getcode()
#         if(rescode==200):
#             response_body = response.read()

#             result = json.loads(response_body.decode('utf-8'))
#             print(" >>> ", result)
#             search_result_mount.append(result['total'])
#         else:
#             print("Error Code:" + rescode)


display = 15
sort = 'date'


for i in range(0, 1):
#for i in range(0, len(keyword_lists)):    
    
    keyword_lists.append(data_list[i]['relKeyword'])
    PC_mount.append(data_list[i]['monthlyPcQcCnt'])
    MO_mount.append(data_list[i]['monthlyMobileQcCnt'])
    print("키워드: " + str(data_list[i]['relKeyword']) + " , PC검색량: " + str(data_list[i]['monthlyPcQcCnt']) + "건, MO검색량: " + str(data_list[i]['monthlyMobileQcCnt']) + "건")

    client_id = "OOOwOkFmGACcqwV269OU"
    client_secret = "lbJwq0cr3d"

    print('0번 >>>', data_list[i]['relKeyword'])

    encText = urllib.parse.quote(data_list[i]['relKeyword'])
    #encText = urllib.parse.quote('인터스트리뉴스')
    print("encText >>> ", encText, data_list[i]['relKeyword'])
    #url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "&display=" + str(display) + "&sort=" + sort # JSON 결과
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "&display=" + str(display) + "&sort=" + sort # JSON 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        

        result = json.loads(response_body.decode('utf-8'))
        print(" result >>> ", result)
        print("count >>> ", len(result))
        print("count___ >>> ", len(result['items']))
        print(result)
        search_result_mount.append(result['total'])
        #lastPosting = result['items'][display - 1]
        #print('postdate >>> ', lastPosting['postdate'])
        for j in range(0, len(result['items'])):
            print(f"{j}번째 글")
            print("postdate >>> ", result['items'][j]['postdate'])
            print("title >>> ", result['items'][j]['title'])
    else:
        print("Error Code:" + rescode)



        


