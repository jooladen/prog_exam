from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options


# Chrome 옵션 설정
chrome_options = Options()


# ChromeDriver 경로 설정
chrome_driver_path = "C:/Users/jooladen/Desktop/prog dev exam/python/chromedriver.exe"

# 브라우저 실행
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

try:
    driver.execute_cdp_cmd(
        "Network.setUserAgentOverride",
        {"userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"},
    )
    # 로그인할 사이트 접속
    driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")
                
    time.sleep(2)  # 페이지 로드 대기
    
    # 이메일 입력
    email_input = driver.find_element(By.ID, "id")
    email_input.send_keys("21thjojo")
    email_input.send_keys(Keys.RETURN)
    time.sleep(2)  # 다음 페이지 로드 대기
    
    # 비밀번호 입력
    password_input = driver.find_element(By.NAME, "pw")
    password_input.send_keys("977VIPER9746")
    password_input.send_keys(Keys.RETURN)
    time.sleep(3)  # 로그인 완료 대기
    
    print("로그인 완료")
finally:
    # 브라우저 닫기
    driver.quit()
