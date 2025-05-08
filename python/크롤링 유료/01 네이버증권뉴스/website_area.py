import requests
from bs4 import BeautifulSoup

#keyword = ["네이버카페", "네이버블로그", "티스토리"]
keyword = ["오토캐드 노트북 인텔"]
#keyword = ["게이밍 노트북 추천"]
n = 1
a = []

for i in keyword:
    response = requests.get("https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=" + i)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup_lists = soup.select(".api_subject_bx")
    print(soup_lists)
    for soup_list in soup_lists:
        title_lists = soup_list.select(".total_tit")
        if len(title_lists) != 0:
            a.append(n)
            n = n + 1
        else:
            n = n + 1

print(a)
print(i + " 검색 순서는: " + str(a[0]) + "번째 입니다.")
