from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 수집할 상품 링크 3개
# urls = [
#     "https://smartstore.naver.com/dogipet/products/11558221245",
#     "https://smartstore.naver.com/dogipet/products/11395005491",
#     "https://smartstore.naver.com/dogipet/products/4601120472"
# ]

urls = [
    #"https://smartstore.naver.com/dogipet/products/11558221245",
    #"https://smartstore.naver.com/dogipet/products/4601120472",
    "https://brand.naver.com/knollostore/products/10973935207",
    "https://brand.naver.com/cargillpetfood/products/8325214479"
]


options = Options()

options.add_experimental_option("detach", True)

# options.add_argument("disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
# options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 표시 제거
# options.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 기능 사용 안 함
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")




# 크롬 드라이버 연결 (드라이버 경로는 필요시 수정)
driver = webdriver.Chrome(options=options)
#driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


for url in urls:
    driver.get(url)
    time.sleep(3)  # 충분한 로딩 대기

    try:
        # 상품명
        #title = driver.find_element(By.CSS_SELECTOR, "div._1eddNbiU1H h3").text
        title = driver.find_element(By.CSS_SELECTOR, "div._1eddO7u4UC h3").text
                                                      
        # title = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "div._1eddO7u4UC h3"))
        # ).text

        # 가격
        price = driver.find_element(By.CSS_SELECTOR, "strong span._1LY7DqCnwR").text

        # 리뷰 수 (선택 사항, 없으면 건너뜀)
        try:
            #review = driver.find_element(By.CSS_SELECTOR, "a._2pgHN-ntx6 span._2ZqVnU3gaN").text
            review = driver.find_element(By.CSS_SELECTOR, "a strong._2pgHN-ntx6").text
            
        except:
            review = "리뷰 없음"

        print("상품명:", title)
        print("가격:", price)
        print("리뷰 수:", review)
        print("-" * 40)

    except Exception as e:
        print("데이터 수집 실패:", e)

driver.quit()
