from bs4 import BeautifulSoup
import requests

# 네이버 검색 결과 페이지 요청 (예시: '크롤링')
query = "크롤링"
url = f"https://search.naver.com/search.naver?query={query}"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# 게시글 제목만 추출 (VIEW 탭에서)
#title_spans = soup.select("a.fds-comps-right-image-text-title span")
#title_spans = soup.select('a.fds-comps-right-image-text-title')
title_spans = soup.select('[data-meta-area="ugB_b1R"] .fds-comps-right-image-text-title')

print(f"\n🔍 네이버 VIEW 탭 '{query}' 검색 결과 제목 목록:")
for idx, span in enumerate(title_spans, 1):
    print(f"{idx}. {span.get_text(strip=True)}")
