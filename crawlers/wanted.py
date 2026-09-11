"""
원티드 채용정보 크롤러 (스텁).

원티드는 공개 채용검색 오픈 API를 제공하지 않는 것으로 보임.
사이트가 SPA(동적 렌더링) 구조라 단순 HTTP 요청만으로는 데이터를
가져올 수 없고, Playwright 등 헤드리스 브라우저가 필요할 가능성이 큼.

구현 전 반드시:
1) robots.txt 확인 (https://www.wanted.co.kr/robots.txt)
2) 이용약관에서 크롤링/데이터 수집 관련 조항 확인
3) 요청 간격을 충분히 둘 것 (예: 2~3초 이상)
"""


def fetch_jobs(keywords: str, edu_lv=None, max_pages: int = 5):
    raise NotImplementedError(
        "robots.txt/이용약관 확인 후 Playwright 기반으로 구현하세요."
    )
