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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_PATH = "relkeywordmount.ui"

class Signature:

    @staticmethod
    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)

        hash.hexdigest()
        return base64.b64encode(hash.digest())

def get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID):
    timestamp = str(round(time.time() * 1000))
    signature = Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(os.path.join(BASE_DIR, UI_PATH), self)
        self.start.clicked.connect(self.start_function)
        
    def start_function(self):
        BASE_URL = 'https://api.searchad.naver.com'
        API_KEY = "본인코드 입력"
        SECRET_KEY = "본인코드 입력"
        CUSTOMER_ID = "본인코드 입력"
        keyword = self.key.text()

        uri = '/keywordstool'
        method = 'GET'
        r = requests.get(BASE_URL + uri, params={'showDetail': '1', 'hintKeywords' : keyword}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

        response = r.json()

        print(response)

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

        if len(data_list) < 10:
            for i in range(0, len(data_list)):
                keyword_lists.append(data_list[i]['relKeyword'])
                PC_mount.append(data_list[i]['monthlyPcQcCnt'])
                MO_mount.append(data_list[i]['monthlyMobileQcCnt'])
                print("키워드: " + str(data_list[i]['relKeyword']) + " , PC검색량: " + str(data_list[i]['monthlyPcQcCnt']) + "건, MO검색량: " + str(data_list[i]['monthlyMobileQcCnt']) + "건")

                client_id = "본인코드 입력"
                client_secret = "본인코드 입력"
                encText = urllib.parse.quote(data_list[i]['relKeyword'])
                url = "https://openapi.naver.com/v1/search/blog?query=" + encText # JSON 결과
                 # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id",client_id)
                request.add_header("X-Naver-Client-Secret",client_secret)
                response = urllib.request.urlopen(request)
                rescode = response.getcode()
                if(rescode==200):
                    response_body = response.read()

                    result = json.loads(response_body.decode('utf-8'))
                    print(result)
                    search_result_mount.append(result['total'])
                else:
                    print("Error Code:" + rescode)


        else:
            for i in range(0, 10):
                keyword_lists.append(data_list[i]['relKeyword'])
                PC_mount.append(data_list[i]['monthlyPcQcCnt'])
                MO_mount.append(data_list[i]['monthlyMobileQcCnt'])
                print("키워드: " + str(data_list[i]['relKeyword']) + " , PC검색량: " + str(data_list[i]['monthlyPcQcCnt']) + "건, MO검색량: " + str(data_list[i]['monthlyMobileQcCnt']) + "건")

                client_id = "본인코드 입력"
                client_secret = "본인코드 입력"
                encText = urllib.parse.quote(data_list[i]['relKeyword'])
                url = "https://openapi.naver.com/v1/search/blog?query=" + encText # JSON 결과
                # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id",client_id)
                request.add_header("X-Naver-Client-Secret",client_secret)
                response = urllib.request.urlopen(request)
                rescode = response.getcode()
                if(rescode==200):
                    response_body = response.read()
        
                    result = json.loads(response_body.decode('utf-8'))
                    print(result)
                    search_result_mount.append(result['total'])
                else:
                    print("Error Code:" + rescode)

# ## 검색 경쟁강도 계산

        for n in range(0, len(keyword_lists)):
            try:
                search_per_result_ratio.append(search_result_mount[n]/(PC_mount[n] + MO_mount[n]))
            except:
                search_per_result_ratio.append(0)

## 출력값 도출

        for t in range(0, len(keyword_lists)):
            block1 = block1 + keyword_lists[t] + "\n"
            block2 = block2 + str(PC_mount[t]) + "\n"
            block3 = block3 + str(MO_mount[t]) + "\n"
            block4 = block4 + str(search_result_mount[t]) + "\n"

            try:
                cal = search_result_mount[t]/(PC_mount[n] + MO_mount[t])
                if cal > 20:
                    block5 = block5 + "경쟁강도 높음" + "\n"
                else:
                    block5 = block5 + "경쟁강도 낮음" + "\n"

            except:
                block5 = block5 + "경쟁강도 낮음" + "\n"
        

        self.relkeyresult.setPlainText(block1)
        self.pcm.setPlainText(block2)
        self.mom.setPlainText(block3)
        self.resultnum.setPlainText(block4)
        self.res.setPlainText(block5)

QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())
