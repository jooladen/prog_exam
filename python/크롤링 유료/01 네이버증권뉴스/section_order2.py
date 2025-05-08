import requests
from bs4 import BeautifulSoup
import re
import json
import urllib.parse

# 섹션 코드와 설명
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

# 콘텐츠 CSS 선택자 (섹션 코드별)
CONTENT_SELECTOR_MAP = {
    "pwl_nop": "#power_link_body.nad_area ul.lst_type > li",  # 광고 링크
    "sit_4po": "a.total_wrap",           # 사이트 블록
    "ugN_gnC": "a.api_txt_lines.total_tit",  # VIEW 블로그/카페 공통
    "ugB_b1R": "[data-meta-area='ugB_b1R'] .fds-comps-right-image-text-title",
    "ugB_qpR": "a.api_txt_lines.total_tit",
    "ugB_b2R": "a.api_txt_lines.total_tit",
    "kwX_rqT": "a.total_tit",            # 지식백과
    "ldc_btm": "a.news_tit",             # 뉴스
    "kin": "a.api_txt_lines.total_tit",  # 지식인
    "img": "div.img_area",               # 이미지 썸네일
    "web_gen": "a.total_tit",            # 웹사이트
    "biz_nop": "a"                        # 비즈 프로필
}

def get_section_and_content_counts(keyword):
    enc_keyword = urllib.parse.quote(keyword)
    url = f"https://search.naver.com/search.naver?query={enc_keyword}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    script_tags = soup.find_all("script")
    print(f"\n🔍 검색어: {keyword}\n")
    print("[네이버 검색 섹션 순서 및 콘텐츠 수]")

    found = False

    for tag in script_tags:
        if 'nx_cr_area_info' in tag.text:
            match = re.search(r'nx_cr_area_info\s*=\s*(\[[^\]]+\])', tag.text)
            if match:
                try:
                    area_list = json.loads(match.group(1))
                    for item in area_list:
                        code = item["n"]
                        desc = SECTION_MAP.get(code, f"기타({code})")
                        selector = CONTENT_SELECTOR_MAP.get(code)
                        if selector:
                            count = len(soup.select(selector))
                            print(f"{item['r']:>2}. {desc} ({code}) - 콘텐츠 {count}개")
                        else:
                            print(f"{item['r']:>2}. {desc} ({code}) - 콘텐츠 수 미지원")
                    found = True
                except Exception as e:
                    print("⚠️ JSON 파싱 실패:", e)
                break

    if not found:
        print("❌ 섹션 정보를 찾을 수 없습니다.")

# ✅ 실행
get_section_and_content_counts("크롤링")
