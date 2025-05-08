# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# # 셀레니움 드라이버 설정
# driver = webdriver.Chrome()

# # 네이버 지도 'SKT 대리점' 검색 결과 페이지 접속
# search_query = "SKT 대리점"
# driver.get(f"https://map.naver.com/p/search/{search_query}")

# # 프레임 전환 (네이버지도는 iframe 안에 검색결과가 뜸)
# time.sleep(3)
# driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe#searchIframe"))

# # 결과 스크롤을 위해 반복
# store_names = []
# store_addresses = []

# for _ in range(5):  # 필요시 스크롤 횟수 조정
#     stores = driver.find_elements(By.CSS_SELECTOR, "div.UEzoS")  # 매장정보 블록
    
#     for store in stores:
#         try:
#             name = store.find_element(By.CSS_SELECTOR, "span.YwYLL").text
#             address = store.find_element(By.CSS_SELECTOR, "span._3Apve").text
#             if name not in store_names:  # 중복 방지
#                 store_names.append(name)
#                 store_addresses.append(address)
#         except:
#             continue
    
#     # 스크롤 내려서 추가 로딩
#     driver.execute_script("window.scrollBy(0, 500)")
#     time.sleep(2)

# # 결과 출력
# for idx, (name, addr) in enumerate(zip(store_names, store_addresses), 1):
#     print(f"{idx}. {name} - {addr}")

# # 브라우저 종료
# driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

search_query = "SKT 대리점"
driver.get(f"https://map.naver.com/p/search/{search_query}")

time.sleep(3)
driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe#searchIframe"))

store_names = []
store_addresses = []

for _ in range(5):
    stores = driver.find_elements(By.CSS_SELECTOR, "div.UEzoS")
    for store in stores:
        try:
            name = store.find_element(By.CSS_SELECTOR, "span.YwYLL").text
            address = store.find_element(By.CSS_SELECTOR, "span._3Apve").text
            if name not in store_names:
                store_names.append(name)
                store_addresses.append(address)
        except:
            continue
    driver.execute_script("window.scrollBy(0, 500)")
    time.sleep(2)

for idx, (name, addr) in enumerate(zip(store_names, store_addresses), 1):
    print(f"{idx}. {name} - {addr}")

driver.quit()
