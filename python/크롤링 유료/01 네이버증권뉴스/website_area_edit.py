import requests
from bs4 import BeautifulSoup

keyword = ["네이버카페", "네이버블로그", "티스토리"]
n = 1

for i in keyword:
    response = requests.get("https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=" + i)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup_lists = soup.select(".api_subject_bx")
    found = False

    for soup_list in soup_lists:
        title_lists = soup_list.select(".total_tit")
        if len(title_lists) != 0:
            found = True
            break

    if found:
        print(i + " 검색 순서는: " + str(n) + "번째 입니다.")
    n = n + 1
