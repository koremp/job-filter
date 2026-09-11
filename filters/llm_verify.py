"""OpenAI API를 이용한 상세페이지 2차 검증 (선택 기능).

EXCLUDE_PHRASES 키워드 매칭으로는 걸러지지 않는, 표현이 다르게 된
"사실상 대졸 이상만 가능" 공고를 잡기 위한 보조 검증.
config.OPENAI_API_KEY가 설정된 경우에만 동작한다.
"""

from pydantic import BaseModel

import config

_client = None


def _get_client():
    global _client
    if _client is None:
        import openai
        _client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
    return _client


class EligibilityResult(BaseModel):
    eligible: bool
    reason: str


def verify_with_llm(title: str, detail_text: str) -> tuple[bool, str]:
    """상세페이지 본문을 OpenAI에 보내 고졸 지원 가능 여부를 재확인한다.

    반환값: (실제로 고졸 지원 가능한지, 판단 근거)
    호출 실패/거부 시에는 판단 보류로 (True, "") 를 반환한다.
    """
    try:
        client = _get_client()
        completion = client.chat.completions.parse(
            model=config.LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "너는 채용공고 본문을 읽고 고등학교 졸업자가 실제로 "
                        "지원 가능한지 판단하는 도우미다. '대졸 이상', '학사 "
                        "이상' 등 사실상 고졸 지원을 막는 문구나 우대사항이 "
                        "있으면 eligible=false로 판단해라. 그런 문구가 없다면 "
                        "eligible=true로 판단해라. reason에는 판단 근거를 "
                        "한 문장으로 적어라."
                    ),
                },
                {
                    "role": "user",
                    "content": f"공고 제목: {title}\n\n본문:\n{detail_text[:4000]}",
                },
            ],
            response_format=EligibilityResult,
        )
        message = completion.choices[0].message
        if message.parsed is None:
            print(f"[llm-verify] 응답 거부, 판단 보류: {message.refusal}")
            return True, ""
        return message.parsed.eligible, message.parsed.reason
    except Exception as e:
        print(f"[llm-verify] 호출 실패, 판단 보류: {e}")
        return True, ""
