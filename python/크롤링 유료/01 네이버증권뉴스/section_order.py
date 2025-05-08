import requests
from bs4 import BeautifulSoup
import re
import json
import urllib.parse

# 섹션 코드와 의미 매핑
SECTION_MAP = {
    "pwl_nop": "파워링크 광고",
    "sit_4po": "사이트 섹션",
    "ugN_gnC": "VIEW - 일반 블로그/카페",
    "ugB_b1R": "VIEW - 전문가형 블로그",
    "ugB_qpR": "VIEW - 일반 블로그형",
    "ugB_b2R": "VIEW - 카페형",
    "kwX_rqT": "지식백과",
    "ldc_btm": "뉴스(또는 기타)",
    "kin": "지식인 (지식iN)",
    "img": "이미지",
    "web_gen": "웹사이트 일반 영역 (웹문서)",
    "biz_nop": "비즈니스 프로필"
}

def get_section_order(keyword):
    enc_keyword = urllib.parse.quote(keyword)
    url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&query={enc_keyword}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    script_tags = soup.find_all("script")

    for tag in script_tags:
        if 'nx_cr_area_info' in tag.text:
            match = re.search(r'nx_cr_area_info\s*=\s*(\[[^\]]+\])', tag.text)
            if match:
                try:
                    area_list = json.loads(match.group(1))
                    print(f"\n검색어: {keyword}\n\n[네이버 검색 섹션 순서]")
                    for item in area_list:
                        code = item['n']
                        desc = SECTION_MAP.get(code, f"기타({code})")
                        print(f"{item['r']}. {desc} ({code})")
                    return
                except Exception as e:
                    print("JSON 파싱 실패:", e)
                    return

    print("섹션 정보를 찾을 수 없습니다.")

# 예제 실행
get_section_order("크롤링")
