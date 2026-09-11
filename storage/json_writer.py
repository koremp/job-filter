"""수집 결과를 웹사이트용 JSON으로 저장하는 유틸."""

import json
import os
from datetime import datetime, timezone

import config


def save_to_json(rows: list, filename: str):
    os.makedirs(config.DATA_DIR, exist_ok=True)
    filepath = os.path.join(config.DATA_DIR, filename)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(rows),
        "eligible_total": sum(1 for r in rows if r.get("actually_eligible")),
        "jobs": rows,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"{len(rows)}건을 {filepath} 에 저장했습니다.")
