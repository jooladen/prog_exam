import time
import requests

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
#params['hintKeywords']='과자'
#params['hintKeywords']='chatgpt'
params['hintKeywords']='CHATGPT' 
params['showDetail']=1

res = requests.get(BASE_URL + uri, params=params, 
                     headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

total_count = 0       # 전체 항목 수
matched_count = 0     # total이 500~600 사이인 키워드 수
removed_count = 0     # '< 10' 포함으로 제거된 항목 수

# 설정: 출력 대상 total 범위 지정
min_total = 500
max_total = 600

def safe_int(value):
    return int(value) if value != '< 10' else None  # '< 10'이면 None 반환

for keyword_info in res.json()['keywordList']:
    total_count += 1
    pc_cnt_raw = keyword_info['monthlyPcQcCnt']
    mobile_cnt_raw = keyword_info['monthlyMobileQcCnt']

    # 둘 중 하나라도 '< 10'이면 제외
    if pc_cnt_raw == '< 10' or mobile_cnt_raw == '< 10':
        removed_count += 1
        continue

    keyword = keyword_info['relKeyword']
    pc_cnt = safe_int(pc_cnt_raw)
    mobile_cnt = safe_int(mobile_cnt_raw)
    total = pc_cnt + mobile_cnt

    # total > 500이면 출력 제외
    if min_total <= total <= max_total:
        print(f"키워드: {keyword}")
        print(f"PC 검색량: {pc_cnt}")
        print(f"모바일 검색량: {mobile_cnt}")
        print(f"총합: {total}")
        print('-' * 30)
        matched_count += 1

print(f"\n총 키워드 수: {total_count}건")
print(f"제거된 키워드 수 (pc에든 mobile에든 '< 10'가 있다면): {removed_count}건")
print(f"총합이 {min_total} ~ {max_total} 사이인 키워드 수: {matched_count}건")





