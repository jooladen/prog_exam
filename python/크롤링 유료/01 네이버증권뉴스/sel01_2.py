from selenium import webdriver
from selenium.webdriver.common.by import By

searchWord = input("검색할 단어를 입력하세요.")
#searchWord = "빵"

driver = webdriver.Chrome()
#driver.get(f"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query={searchWord}")
driver.get("https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=" + searchWord)
