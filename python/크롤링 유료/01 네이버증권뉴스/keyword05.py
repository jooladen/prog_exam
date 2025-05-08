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
#params['hintKeywords']='CHATGPT' 
params['hintKeywords']='CHATGPT개발'
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

import datetime

#def analyze_keyword_density(result, base_search_volume=200):
def analyze_keyword_density(result, monthly_search_volume):
    print("월검색수 >>> ", monthly_search_volume)
    if not result["items"]:
        return None, "데이터 없음"

    # 마지막 포스팅 정보
    last_posting = result["items"][-1]
    last_postdate = last_posting["postdate"]
    print("last_postdate >>> ", last_postdate)

    # 날짜 문자열을 datetime 객체로 변환
    last_year = int(last_postdate[:4])
    last_month = int(last_postdate[4:6])
    last_day = int(last_postdate[6:])
    last_date = datetime.datetime(last_year, last_month, last_day)

    # 오늘 날짜와의 차이 계산
    today = datetime.datetime.today()
    date_difference = today - last_date
    days = date_difference.days
    print("경과일 >>> ", days)
    # 0일 경과: 과포화
    if days == 0:  #하루도 안됬는데 100건
         return None, None 

    # 발행량 계산
    daily_post = 100 / days
    print("일 발행량 >>> ", daily_post)
    monthly_post = daily_post * 30
    print("월 발행량 >>> ", monthly_post)
    percentage = (monthly_post / monthly_search_volume) * 100
    rounded_percent = round(percentage, 1)

    # 메시지 판단
    if (days <= 3 and percentage <= 5) or (days <= 10 and percentage <= 1.0):
        message = "신규 트렌드 / 단기 과열 주의"   
    elif percentage >= 100:
        message = "과포화 (100% 이상)"
    elif 90 <= percentage < 100:
        message = "포화도 90%"
    elif 80 <= percentage < 90:
        message = "포화도 80%"
    elif 70 <= percentage < 80:
        message = "포화도 70%"
    elif 60 <= percentage < 70:
        message = "포화도 60%"
    elif 50 <= percentage < 60:
        message = "포화도 50%"
    elif 40 <= percentage < 50:
        message = "포화도 40%"
    elif 30 <= percentage < 40:
        message = "포화도 30%"
    elif 20 <= percentage < 30:
        message = "포화도 20%"
    elif 10 <= percentage < 20:
        # 날짜 조건도 만족해야 베스트로 인정
        if 11 <= days <= 20:
            message = "베스트 진입 구간"
        else:
            message = "포화도 10%"
    else:
        message = "글감 부족 / 주제 탐색 필요"

    
    if not (15.0 <= percentage <= 25.0):
          return None, None 
    else:
        return f"{rounded_percent}%", message 



display = 100
sort = 'date'

print("len(data_list) >>> ", len(data_list))
for i in range(0, len(data_list)):
#for i in range(0, len(keyword_lists)):    
    #print(i)
    pcCnt = data_list[i]['monthlyPcQcCnt']
    mobileCnt = data_list[i]['monthlyMobileQcCnt']
    # 둘 중 하나라도 '< 10'이면 제외
    if pcCnt == '< 10' or mobileCnt == '< 10':
        continue

    pcCnt = int(pcCnt)
    mobileCnt = int(mobileCnt)

    # PC 검색량이 200 이상 300 이하일 때만 처리
    if not (200 <= pcCnt + mobileCnt <= 300):
        continue

    keyword_lists.append(data_list[i]['relKeyword'])
    PC_mount.append(pcCnt)
    MO_mount.append(mobileCnt)
    print("키워드: " + str(data_list[i]['relKeyword']) + " , PC검색량: " + str(pcCnt) + "건, MO검색량: " + str(mobileCnt) + "건")

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
        # print(" result >>> ", result)
        # print("count >>> ", len(result))
        # print("count___ >>> ", len(result['items']))
        # print(result)
        search_result_mount.append(result['total'])

        #테스트용
        # for j in range(0, len(result['items'])):
        #     print(f"{j}번째 글")
        #     print("postdate >>> ", result['items'][j]['postdate'])
        #     print("title >>> ", result['items'][j]['title'])

        # 포화도
        #percent, status = analyze_keyword_density(result, data_list[1]['monthlyPcQcCnt'] + data_list[1]['monthlyMobileQcCnt'])
        percent, statusMsg = analyze_keyword_density(result, pcCnt + mobileCnt)
        if percent is None:
            continue 

        print("포화도:", percent)
        print("판단:", statusMsg)
        print("\n" + "-" * 50)
    else:
        print("Error Code:" + rescode)


    
            


