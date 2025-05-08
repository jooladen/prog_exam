# ─── API 인증 관련 설정 ───
import time, hashlib, hmac, base64, requests
from urllib.parse import urlencode

BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000c6d85b711847dd9cc75fd8a871b12eb61c9d23bf8aa12e998a6eb618b77ffd55'
SECRET_KEY = 'AQAAAACUIl5duGI+KnLo1dWvs+hThAJz7k28wJRLE+XUuy3/KQ=='
CUSTOMER_ID = '3455835'



# def generate_signature(timestamp, method, uri, secret_key):
#     msg = f"{timestamp}.{method}.{uri}"
#     sig = hmac.new(secret_key.encode(), msg.encode(), hashlib.sha256).digest()
#     return base64.b64encode(sig).decode()

class Signature:

    @staticmethod
    def generate_signature(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)

        hash.hexdigest()
        return base64.b64encode(hash.digest())

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = Signature.generate_signature(timestamp, method, uri, secret_key)
    
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 
            'X-API-KEY': api_key, 'X-Customer': str(customer_id), 'X-Signature': signature}

def get_monthly_search_volume(keyword):
    method, uri = "GET", "/keywordstool"
    # #timestamp = str(int(time.time() * 1000))
    # timestamp = str(round(time.time() * 1000))
    # #sig = generate_signature(timestamp, method, uri, SECRET_KEY)
    # sig = Signature.generate_signature(timestamp, method, uri, SECRET_KEY)
    # headers = {
    #     'Content-Type': 'application/json; charset=UTF-8',
    #     "X-Timestamp": timestamp,
    #     "X-API-KEY": API_KEY,
    #     "X-CUSTOMER": str(CUSTOMER_ID),
    #     "X-Signature": sig
    # }

    #params = {"hintKeywords": keyword, "showDetail": 1}
    params = {"hintKeywords": 'chatgpt', "showDetail": 1}
    #res = requests.get(BASE_URL + uri, headers=headers, params=params)
    #res = requests.get(BASE_URL + uri, params=params, headers=headers)
    res = requests.get(BASE_URL + uri, params=params, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    print("res >>> ", res)
    data = res.json()
    if isinstance(data, list) and data:
        pc = int(data[0].get('monthlyPcQcCnt', 0))
        mob = int(data[0].get('monthlyMobileQcCnt', 0))
        return pc + mob
    return 0


# ─── Selenium 웹 자동화로 연관검색어 + 블로그 발행량 크롤링 ───
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def get_driver():
    options = Options()
    options.add_experimental_option("detach", True)
    #opts.add_argument("--headless=new")
    #opts.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)

def get_related_keywords(main_keyword):
    driver = get_driver()
    driver.get(f"https://search.naver.com/search.naver?query={main_keyword}")
    time.sleep(2)
    try:
        #elems = driver.find_elements(By.CSS_SELECTOR, ".lst_related_srch a")
        elems = driver.find_elements(By.CSS_SELECTOR, ".title_area")
        print("elems >>> ", elems)
        keywords = [e.text.strip() for e in elems if e.text.strip()]
    except:
        keywords = []
    driver.quit()
    return keywords

def get_blog_post_count(keyword):
    driver = get_driver()
    driver.get(f"https://search.naver.com/search.naver?where=post&query={keyword}&nso=so:r,p:1m,a:all")
    time.sleep(2)
    try:
        text = driver.find_element(By.CSS_SELECTOR, "div.title_desc span").text
        return int(text.replace(",", "").split("건")[0].strip())
    except:
        return 0
    finally:
        driver.quit()


# ─── 실행부 ───
def main():
    base_keyword = "ChatGPT API"
    related = get_related_keywords(base_keyword)
    results = []
    print("related >>>> ", related)
    for kw in related:
        try:
            sv = get_monthly_search_volume(kw)
            if 500 <= sv <= 1000:
                bc = get_blog_post_count(kw)
                if bc <= sv * 0.3:
                    results.append({"키워드": kw, "검색량": sv, "발행량": bc})
        except Exception as e:
            print(f"[{kw}] 오류 발생: {e}")
    print("\n✅ 최종 결과:")
    for r in results:
        print(r)

if __name__ == "__main__":
    main()
