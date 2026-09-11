"""
구조화된 edu_lv 코드만으로는 걸러지지 않는 경우를 잡기 위한
2차 검증 필터.

예: edu_lv가 '고졸이상(6)'으로 등록돼 있어도, 본문 우대사항에
"대졸 이상 지원 가능" 같은 문구가 있어 사실상 고졸 지원이
어려운 공고가 있음. 상세페이지 텍스트를 열어 이런 문구를 확인한다.
"""

import time
import requests
from bs4 import BeautifulSoup

import config


def is_actually_high_school_eligible(url: str, title: str = "") -> tuple[bool, str]:
    """
    반환값: (실제로 고졸 지원 가능한지, 발견된 제외 문구/판단 근거)
    요청 실패 시에는 판단 보류로 True를 반환하고 로그를 남김
    (별도로 수동 확인이 필요함을 의미).

    1차로 EXCLUDE_PHRASES 키워드 매칭을 수행하고, 걸리지 않은 경우에는
    config.USE_LLM_VERIFICATION이 켜져 있을 때 Claude로 보조 검증한다.
    """
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (personal research crawler)"},
            timeout=10,
        )
        if resp.status_code != 200:
            print(f"[education-filter] 상세페이지 요청 실패({resp.status_code}): {url}")
            return True, ""

        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

        for phrase in config.EXCLUDE_PHRASES:
            if phrase in text:
                return False, phrase

        if config.USE_LLM_VERIFICATION:
            from filters import llm_verify
            eligible, reason = llm_verify.verify_with_llm(title, text)
            if not eligible:
                return False, f"LLM 판단: {reason}"

        return True, ""
    except requests.RequestException as e:
        print(f"[education-filter] 상세페이지 요청 오류: {e}")
        return True, ""


def verify_jobs(jobs: list) -> list:
    """공고 목록을 순회하며 상세페이지 텍스트로 재검증한 결과를 덧붙인다."""
    verified = []
    for job in jobs:
        eligible, found_phrase = is_actually_high_school_eligible(job["url"], job["title"])
        job["actually_eligible"] = eligible
        job["exclude_reason"] = found_phrase
        verified.append(job)
        print(
            f"  - {job['title'][:30]:30s} "
            f"{'OK' if eligible else f'제외({found_phrase})'}"
        )
        time.sleep(config.DETAIL_FETCH_INTERVAL_SEC)
    return verified
