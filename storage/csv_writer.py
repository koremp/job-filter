"""수집 결과를 CSV로 저장하는 유틸."""

import csv
import os

import config


def save_to_csv(rows: list, filename: str):
    if not rows:
        print("저장할 데이터가 없습니다.")
        return

    os.makedirs(config.DATA_DIR, exist_ok=True)
    filepath = os.path.join(config.DATA_DIR, filename)

    keys = rows[0].keys()
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)

    print(f"{len(rows)}건을 {filepath} 에 저장했습니다.")
