# 네이버 검색광고 API 연동을 위한 전체 코드 생성 (API 키는 사용자가 별도로 입력)
# 주의: 이 코드는 키를 직접 입력해야 하며, 실제 검색량을 불러옵니다.

import time
import hashlib
import hmac
import base64
import requests
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 사용자 입력 필요: 네이버 검색광고 API 인증 정보
BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000c6d85b711847dd9cc75fd8a871b12eb61c9d23bf8aa12e998a6eb618b77ffd55'
SECRET_KEY = 'AQAAAACUIl5duGI+KnLo1dWvs+hThAJz7k28wJRLE+XUuy3/KQ=='
CUSTOMER_ID = '3455835'

# HMAC SHA256 서명 생성
def generate_signature(timestamp, method, uri, secret_key):
    message = f"{timestamp}.{method}.{uri}"
    signing_key = bytes(secret_key, 'utf-8')
    message = bytes(message, 'utf-8')
    signature = hmac.new(signing_key, message, digestmod=hashlib.sha256).digest()
    return base64.b64encode(signature).decode()

# 검색량 조회 함수 (API)
def get_monthly_search_volume(keyword):
    method = "GET"
    uri = "/keywordstool"
    timestamp = str(int(time.time() * 1000))
    signature = generate_signature(timestamp, method, uri, SECRET_KEY)

    headers = {
        "Content-Type": "application/json",
        "X-Timestamp": timestamp,
        "X-API-KEY": API_KEY,
        "X-CUSTOMER": CUSTOMER_ID,
        "X-Signature": signature
    }

    params = {
        "hintKeywords": keyword,
        "showDetail": 1
    }

    response = requests.get(BASE_URL + uri, headers=headers, params=params)
    data = response.json()

    if isinstance(data, list) and data:
        return int(data[0].get('monthlyPcQcCnt', 0)) + int(data[0].get('monthlyMobileQcCnt', 0))
    return 0

# Selenium 드라이버 설정
def get_driver():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    return driver

# 연관검색어 추출
def get_related_keywords(main_keyword):
    driver = get_driver()
    driver.get(f"https://search.naver.com/search.naver?query={main_keyword}")
    time.sleep(2)
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, ".lst_related_srch a")
        keywords = [el.text.strip() for el in elements if el.text.strip()]
    except:
        keywords = []
    driver.quit()
    return keywords

# 블로그 발행량 크롤링
def get_blog_post_count(keyword):
    driver = get_driver()
    driver.get(f"https://search.naver.com/search.naver?where=post&query={keyword}&nso=so:r,p:1m,a:all")
    time.sleep(2)
    try:
        text = driver.find_element(By.CSS_SELECTOR, "div.title_desc span").text
        count = int(text.replace(",", "").split("건")[0].strip())
    except:
        count = 0
    driver.quit()
    return count

# 전체 실행
def main():
    main_keyword = "ChatGPT API"
    related_keywords = get_related_keywords(main_keyword)
    result = []

    for kw in related_keywords:
        try:
            search_volume = get_monthly_search_volume(kw)
            if 500 <= search_volume <= 1000:
                blog_count = get_blog_post_count(kw)
                if blog_count <= search_volume * 0.3:
                    result.append({
                        "키워드": kw,
                        "검색량": search_volume,
                        "발행량": blog_count
                    })
        except Exception as e:
            print(f"[{kw}] 오류 발생: {e}")
    
    # 결과 출력
    for item in result:
        print(item)

# main() 함수는 사용자가 직접 API 키 입력 후 실행하세요.
