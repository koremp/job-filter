"""프로젝트 공통 설정."""

import os
from dotenv import load_dotenv

load_dotenv()

# --- 사람인 Open API ---
SARAMIN_ACCESS_KEY = os.getenv("SARAMIN_ACCESS_KEY", "")
SARAMIN_DAILY_CALL_LIMIT = 500

# 학력 코드 (근무형태/학력/연봉 코드표 기준)
# 0: 학력무관 1: 고졸 2: 전문학사(2,3년) 3: 학사(4년)
# 4: 석사 5: 박사 6: 고졸이상 7: 전문학사이상 8: 학사이상 9: 석사이상
EDU_LEVEL_HIGH_SCHOOL = "0,1,6"
EDU_LEVEL_BACHELOR_UP = "3,8"

# --- 검색 키워드 (직무 필터) ---
SEARCH_KEYWORDS = ["프론트엔드", "웹퍼블리셔", "React"]

# --- 상세페이지 텍스트 검증용 제외 키워드 ---
EXCLUDE_PHRASES = [
    "대졸 이상", "대졸이상", "학사 이상", "학사이상",
    "대학교 졸업 이상", "4년제 대학교", "대졸자 우대", "학사학위 소지자",
]

# --- 요청 간 딜레이 (서버 부담 최소화) ---
API_CALL_INTERVAL_SEC = 0.5
DETAIL_FETCH_INTERVAL_SEC = 1.0

# --- OpenAI API (선택: 상세페이지 2차 검증에 LLM 판단 보조) ---
# OPENAI_API_KEY가 없으면 키워드 매칭(EXCLUDE_PHRASES)만으로 검증한다.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL = "gpt-4o-mini"
USE_LLM_VERIFICATION = bool(OPENAI_API_KEY)

# --- 출력 경로 ---
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
