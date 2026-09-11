"""
잡코리아 채용정보 크롤러 (스텁).

잡코리아도 사람인처럼 자체 오픈 API를 제공한다
(https://www.jobkorea.co.kr/service/api).
다만 개인/일반 기업은 내부 검토 후 제공이 거부될 수 있고,
공공기관/학교 대상 서비스 성격이 강하다고 안내되어 있으므로
이용신청 결과를 먼저 확인한 뒤 구현을 채워야 한다.

승인이 어려운 경우, 직접 크롤링은 반드시 이용약관/robots.txt를
확인하고 요청 간격을 충분히 두는 방식으로만 진행할 것.
"""


def fetch_jobs(keywords: str, edu_lv=None, max_pages: int = 5):
    raise NotImplementedError(
        "잡코리아 API 이용신청 승인 여부를 먼저 확인하고 구현하세요."
    )
