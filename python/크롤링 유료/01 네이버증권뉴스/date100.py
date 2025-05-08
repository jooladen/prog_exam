from selenium import webdriver
from selenium.webdriver.common.by import By
import time

keyword = "GPT 사용법"
url = f"https://search.naver.com/search.naver?where=view&query={keyword}&sm=tab_opt&mode=normal&sort=0"

driver = webdriver.Chrome()
driver.get(url)

# 스크롤 반복 → 약 100개 글이 로딩될 때까지
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1.5)
    articles = driver.find_elements(By.CSS_SELECTOR, ".api_txt_lines.total_tit")
    if len(articles) >= 100:
        break

# 100번째 글의 날짜 요소 추출
dates = driver.find_elements(By.CSS_SELECTOR, ".sub_time")  # 날짜 클래스
date_100th = dates[99].text  # 인덱스 99는 100번째 글

print("100번째 글 날짜:", date_100th)
driver.quit()
