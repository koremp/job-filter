"""
프론트엔드 신입/고졸 채용공고 수집 프로젝트 - 실행 진입점.

현재는 사람인만 구현되어 있음. 잡코리아/원티드/랠릿/잡플래닛은
crawlers/ 아래 스텁을 확인하고 하나씩 채워나갈 것.
"""

import config
from crawlers import saramin
from filters import education
from storage import csv_writer, json_writer


def run_saramin_pipeline():
    all_candidates = []
    for keyword in config.SEARCH_KEYWORDS:
        print(f"\n=== '{keyword}' 검색 중 (사람인) ===")
        jobs = saramin.fetch_jobs(
            keywords=keyword,
            edu_lv=config.EDU_LEVEL_HIGH_SCHOOL,
            max_pages=5,
        )
        all_candidates.extend(jobs)

    print(f"\n총 {len(all_candidates)}건의 1차 후보 공고를 상세 검증합니다...")
    verified = education.verify_jobs(all_candidates)

    csv_writer.save_to_csv(verified, "saramin_high_school_eligible_jobs.csv")
    json_writer.save_to_json(verified, "jobs.json")

    eligible_count = sum(1 for j in verified if j["actually_eligible"])
    print(f"\n최종 결과: 전체 {len(verified)}건 중 실제 지원 가능 {eligible_count}건")


if __name__ == "__main__":
    if not config.SARAMIN_ACCESS_KEY:
        print("SARAMIN_ACCESS_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
    else:
        run_saramin_pipeline()
