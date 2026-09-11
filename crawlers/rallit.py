"""
랠릿(Rallit) 채용정보 크롤러 (스텁).

공개 오픈 API 제공 여부 확인이 필요함. 없다면 wanted.py와 동일한
원칙(robots.txt 확인, 헤드리스 브라우저, 요청 간격)을 적용할 것.
"""


def fetch_jobs(keywords: str, edu_lv=None, max_pages: int = 5):
    raise NotImplementedError(
        "오픈 API 여부 확인 후, 없다면 robots.txt 확인 후 구현하세요."
    )
