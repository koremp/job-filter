"""사람인 오픈 API 채용공고 크롤러."""

import time
import requests

import config

BASE_URL = "https://oapi.saramin.co.kr/job-search"


def fetch_jobs(keywords: str, edu_lv: str, max_pages: int = 5, page_size: int = 110):
    """
    사람인 Open API로 채용공고를 검색한다.

    keywords: 검색 키워드 (예: '프론트엔드')
    edu_lv: 학력 코드 (예: '0,1,6')
    """
    results = []
    call_count = 0

    for page in range(max_pages):
        if call_count >= config.SARAMIN_DAILY_CALL_LIMIT:
            print("[saramin] 일일 호출 한도에 도달해 중단합니다.")
            break

        params = {
            "access-key": config.SARAMIN_ACCESS_KEY,
            "keywords": keywords,
            "edu_lv": edu_lv,
            "start": page,
            "count": page_size,
            "sort": "pd",
        }
        headers = {"Accept": "application/json"}

        resp = requests.get(BASE_URL, params=params, headers=headers, timeout=10)
        call_count += 1
        time.sleep(config.API_CALL_INTERVAL_SEC)

        if resp.status_code != 200:
            print(f"[saramin] HTTP 오류: {resp.status_code}")
            break

        data = resp.json()

        if "code" in data:
            print(f"[saramin] API 오류: {data.get('message')}")
            break

        jobs_block = data.get("jobs", {})
        total = int(jobs_block.get("total", 0))
        job_list = jobs_block.get("job", [])

        if isinstance(job_list, dict):
            job_list = [job_list]

        if not job_list:
            break

        for job in job_list:
            position = job.get("position", {})
            edu = position.get("required-education-level", {})
            company = job.get("company", {}).get("detail", {})

            results.append({
                "source": "saramin",
                "id": job.get("id"),
                "company": company.get("name"),
                "title": position.get("title"),
                "location": position.get("location", {}).get("name"),
                "job_type": position.get("job-type", {}).get("name"),
                "education": edu.get("name"),
                "education_code": edu.get("code"),
                "salary": job.get("salary", {}).get("name"),
                "url": job.get("url"),
                "posting_date": job.get("posting-date"),
            })

        print(f"[saramin][page {page}] {len(job_list)}건 수집 (누적 {len(results)} / 전체 {total})")

        if (page + 1) * page_size >= total:
            break

    return results
