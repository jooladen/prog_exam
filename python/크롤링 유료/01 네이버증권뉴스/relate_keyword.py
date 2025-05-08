import time
import requests
import hashlib
import hmac
import base64
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import os

# UI 파일 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_PATH = "lecturetest.ui"

# 인증 서명 생성 클래스
class Signature:
    @staticmethod
    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)
        return base64.b64encode(hash.digest())

# 요청 헤더 구성 함수
def get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID):
    timestamp = str(round(time.time() * 1000))
    signature = Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Timestamp': timestamp,
        'X-API-KEY': API_KEY,
        'X-Customer': str(CUSTOMER_ID),
        'X-Signature': signature
    }

# 메인 GUI 클래스
class MainDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(BASE_DIR, UI_PATH), self)
        self.startbutton.clicked.connect(self.start)

    def start(self):
        #################### 입력값 정리 ####################
        BASE_URL = 'https://api.searchad.naver.com'
        API_KEY = self.apikey.text()
        SECRET_KEY = self.secretkey.text()
        CUSTOMER_ID = self.customer_key.text()
        keyword = self.keyword.text()

        #################### API 요청 ####################
        uri = '/keywordstool'
        method = 'GET'
        r = requests.get(
            BASE_URL + uri,
            params={'showDetail': '1', 'hintKeywords': keyword},
            headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID)
        )

        response = r.json()
        data_list = response['keywordList']

        #################### 데이터 가공 ####################
        keyword_result = []
        PC_mount = []
        MO_mount = []

        for i in range(0, len(data_list)):
            if data_list[i]['monthlyPcQcCnt'] == "< 10" or data_list[i]['monthlyMobileQcCnt'] == "< 10":
                continue
            elif int(data_list[i]['monthlyPcQcCnt']) >= 200 and int(data_list[i]['monthlyMobileQcCnt']) >= 1000:
                keyword_result.append(data_list[i]['relKeyword'])
                PC_mount.append(data_list[i]['monthlyPcQcCnt'])
                MO_mount.append(data_list[i]['monthlyMobileQcCnt'])

        #################### 결과 출력 ####################
        for i in range(0, len(keyword_result)):
            self.result_browser.append(
                "키워드: " + str(keyword_result[i]) +
                ", PC 검색량: " + str(PC_mount[i]) + "건, MO 검색량: " + str(MO_mount[i]) + "건" + "\n"
            )

# 앱 실행
QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())
