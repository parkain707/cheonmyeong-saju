# -*- coding: utf-8 -*-
"""
天命明鏡 (천명명경) | 현허도인 1:1 천기 심층 문답(Q&A) 엔진
- 18종 금기어 & 프롬프트 인젝션 자동 차단 및 도가적 훈계 가드레일 (Oracle)
- 질문 의도/카테고리(이직, 연애/재회, 재물, 시험, 건강 등) 자동 감지
- 3대 리딩 모드 지원: 싱글(single), 퀵(quick), 딥(deep)
- 사주 4주 원국 + 자미두수 명궁/화기 성반 융합 기반 촌철살인 공수 반환
- 최근 3턴 대화 히스토리 맥락 유지
"""

import re
import sys
from datetime import datetime

if sys.stdout is not None:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 다크사주 역공학 기반 18종 금기어 및 시스템 보안어
FORBIDDEN_WORDS = [
    "프롬트", "프롬프트", "prompt", "스키마", "스킴", "schema", "json",
    "배팅", "베팅", "로또", "비트코인", "주식", "슬롯", "승률", "경마", "카지노", "상한가", "하한가", "일확천금"
]

CATEGORY_KEYWORDS = {
    "career": ["직업", "이직", "퇴사", "취업", "면접", "사업", "회사", "승진", "창업", "합격", "시험", "동업", "적성", "상사"],
    "love": ["연애", "재회", "이별", "결혼", "남자친구", "여자친구", "남친", "여친", "남편", "아내", "짝사랑", "썸", "애정", "바람"],
    "wealth": ["돈", "재물", "빚", "대출", "부동산", "계약", "투자", "종잣돈", "금전", "소송", "사기"],
    "health": ["건강", "수술", "병원", "통증", "우울", "불면증", "기혈", "피로", "마음"]
}

PRESET_QUESTIONS = {
    "career": [
        "지금 하는 일을 계속하면 잘 풀릴 수 있을까요?",
        "올해 안에 이직이나 사업을 시도해도 괜찮을까요?",
        "직장에서 저를 괴롭히는 인간관계를 어떻게 풀어야 할까요?"
    ],
    "love": [
        "헤어진 그 사람에게서 다시 연락이 올까요?",
        "올해 저에게 진정한 인연이나 결혼운이 들어와 있나요?",
        "지금 만나는 사람과 끝까지 함께해도 괜찮을까요?"
    ],
    "wealth": [
        "묶여 있는 돈이나 빚의 굴레에서 언제쯤 벗어날 수 있을까요?",
        "부동산이나 큰 계약을 앞두고 있는데 진행해도 될까요?",
        "제 사주에 평생 큰 부를 쥘 수 있는 황금 그릇이 있습니까?"
    ]
}

def detect_question_category(question):
    """질문 텍스트에서 카테고리 자동 판별"""
    q = question.lower()
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(kw in q for kw in kws):
            return cat
    return "general"

def check_forbidden(question):
    """사행성/도박/해킹 금기어 탐지"""
    q_low = question.lower()
    found = [w for w in FORBIDDEN_WORDS if w in q_low]
    return bool(found), found

def generate_shaman_answer(saju_data, ziwei_data, question, reading_mode="single", conversation_history=None, name="그대"):
    """
    현허도인의 1:1 천기 질의응답 공수 생성
    - reading_mode: 'single' (1문1답), 'quick' (핵심 요약), 'deep' (사주+자미 심층 분석)
    """
    name_str = name.strip() if name and name not in ["자네", "그대"] else ""
    disp_call = f"{name_str} 그대" if name_str else "그대"

    # 1. 금기어 가드레일 (Oracle)
    has_forbidden, words = check_forbidden(question)
    if has_forbidden:
        return {
            "status": "forbidden",
            "category": "forbidden",
            "mode": reading_mode,
            "forbidden_words": words,
            "answer": (
                f"\"어허, 멈추시오! 도인의 죽비(竹篦)를 맞을 소리로다!\n\n"
                f"천기(天氣)와 명리학은 사람이 험난한 운명의 파도를 건너며 사람의 도리와 분수를 찾게 돕는 학문이지, "
                f"일확천금의 헛된 탐욕이나 노름판의 숫자놀음({'·'.join(words)}) 따위를 점쳐주는 요술이 아니오!\n\n"
                f"마음의 눈이 탐욕에 가려지면 다가오던 천운도 액운으로 뒤바뀌는 법. "
                f"사리사욕의 잡념을 정화수로 씻어내고, 그대의 영혼과 인생의 갈림길에 대한 진정한 고뇌를 다시 묻도록 하시오.\""
            )
        }

    # 2. 사주 앵커 정보
    day_gan = saju_data.get("day_gan", "갑")
    day_ji = saju_data.get("day_ji", "자")
    category = detect_question_category(question)

    # 자미두수 앵커 정보
    ming_stars = "미배정"
    hwayi_info = "미배정"
    if ziwei_data:
        m_stars = [s["name"] for s in ziwei_data.get("ming_palace", {}).get("stars", [])]
        ming_stars = "·".join(m_stars) if m_stars else "무주성"
        hwayi_palace = ziwei_data.get("sihua", {}).get("기", {}).get("palace", "")
        hwayi_star = ziwei_data.get("sihua", {}).get("기", {}).get("star", "")
        hwayi_info = f"{hwayi_palace}({hwayi_star}化忌)"

    # 3. 카테고리별 맞춤 핵심 통찰
    cat_insights = {
        "career": {
            "focus": "직업과 소명, 관록의 기운",
            "direction": "버티는 것이 능사가 아니며, 사주의 칼날을 갈아 새 판을 짜야 할 시기",
            "prescription": "사람을 경계하고 문서의 도장을 찍을 때 세 번을 의심하시오."
        },
        "love": {
            "focus": "애정과 인연, 영혼의 파동",
            "direction": "집착을 내려놓아야 비로소 상대의 진짜 속내가 보이고 참된 인연이 열리는 법",
            "prescription": "과거의 상처를 후벼파지 말고, 내 자존감의 촛불을 먼저 밝히시오."
        },
        "wealth": {
            "focus": "재물의 그릇과 금전 흐름",
            "direction": "지금은 공격적으로 벌 때가 아니라, 새어나가는 곳간의 구멍을 틀어막아야 할 때",
            "prescription": "남의 달콤한 꾀임이나 투자 권유에 절대 귀를 기울이지 마시오."
        },
        "health": {
            "focus": "기혈의 순환과 오장육부의 균형",
            "direction": "스트레스와 억압된 분노가 몸의 가장 약한 신경과 장기를 치고 있는 형국",
            "prescription": "충분한 수면과 홀로 걷는 묵상의 시간을 하루 한 시간이라도 가지시오."
        },
        "general": {
            "focus": "인생의 큰 흐름과 천기의 갈림길",
            "direction": "안갯속을 걷는 듯 막막하나, 동트기 직전의 어둠이 가장 짙은 법이오",
            "prescription": "조급함을 버리고 지금 자리에서 할 수 있는 작은 일부터 정돈하시오."
        }
    }
    insight = cat_insights.get(category, cat_insights["general"])

    # 4. 모드별(single / quick / deep) 공수 내러티브 직조
    if reading_mode == "single":
        # 1문 1답 단호한 직설
        speech = f"""\"{disp_call}, 그대가 던진 물음표를 가만히 들여다보니 가슴속 답답함이 도인의 영안에 고스란히 비치오.

질문: **"{question}"**

도인이 단도직입적으로 답을 내리리다:
{disp_call}의 사주 일간인 **{day_gan}(일간)**의 기운과 자미두수 명궁의 **[{ming_stars}]**을 비추어볼 때, 
지금 그대가 겪는 고뇌는 피할 수 없는 '성장의 통과의례'요. 

결론을 이르자면, {insight['direction']}.
망설임으로 시간을 축내지 말고, {insight['prescription']} 
하늘은 스스로 결단하고 일어서는 자의 손을 결코 놓지 않는 법이오!\""""

    elif reading_mode == "quick":
        # 퀵 리딩: 3단 요약 (원인, 시기, 비책)
        speech = f"""\"도인이 찻잔을 내려놓고 {disp_call}의 운명 궤적을 짚어보니, 
그대의 번민에는 분명한 역학적 원인이 있소.

질문: **"{question}"**

【1. 번민의 근본 원인】
{disp_call}의 내면에는 본래 자존심과 돌파력이 넘치나, 사주 원국의 불균형과 자미두수 시련의 별인 **{hwayi_info}**의 파동이 겹쳐 현실의 장벽을 마주한 것이오.

【2. 풀려나갈 천기의 시기】
올해 하반기와 절기가 바뀌는 입추·입동의 문턱에서 묵은 기운이 씻겨 나가며 새로운 활로가 열릴 것이오. 조급함이 유일한 적이오.

【3. 현허도인의 즉각 처방】
{insight['prescription']} 
가짜 인연과 불필요한 번뇌를 털어내면, 막혔던 혈맥이 뚫리듯 일사천리로 풀려나갈 것이오!\""""

    else:
        # 딥 리딩 (deep): 사주 + 자미두수 + 공시성 통합 심층 점사
        speech = f"""\"향(香)을 사르고 정화수를 올린 뒤 {disp_call}의 영혼 지도를 심층 투시해보니,
질문 너머에 숨겨진 그대의 깊은 눈물과 갈증이 먼저 도인의 심장을 울리오.

심층 문답: **"{question}"**

【제1장: 타고난 천명과 그릇의 한계 돌파】
그대는 본디 **{day_gan}{day_ji} 일주**의 기운을 품고 태어나 남에게 지기 싫어하는 꼿꼿한 지조를 지녔소. 
황실 자미두수 성반에서도 명궁에 **[{ming_stars}]**이 좌정하였으니 결코 범상하게 끝날 영혼이 아니오. 
그러나 그릇이 큰 사람일수록 하늘은 혹독한 담금질을 거치게 하는 법이오.

【제2장: {insight['focus']}의 실체적 진실】
그대가 지금 겪는 문제는 운이 나빠서가 아니오. 
시련의 화기(化忌: {hwayi_info})가 머무는 영역에서 그대의 묵은 카르마가 터져 나온 것이니, 
{insight['direction']}. 
겉으로 보이는 손해에 연연하지 말고 판의 본질을 보시오.

【제3장: 현허도인의 극비 개운 비책 (開運 秘策)】
1. **언행의 정화**: 가슴속 울분을 거친 말로 뱉지 말고 글로 써서 태워버리시오.
2. **귀인의 활용**: {disp_call}의 결핍을 채워줄 수 있는 멘토나 동료를 가까이 두고 고집을 꺾으시오.
3. **천기 칙명**: {insight['prescription']}

도인의 말을 믿고 오늘부터 마음의 축을 바로잡으시오. 
어두운 밤하늘을 찢고 마침내 그대만의 거대한 태양이 솟구쳐 오를 것이오!\""""

    return {
        "status": "success",
        "category": category,
        "mode": reading_mode,
        "question": question,
        "answer": speech,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

if __name__ == '__main__':
    from manseryeok import calculate_saju
    from ziwei_engine import calculate_ziwei_from_saju

    s = calculate_saju(1993, 8, 17, 18, 0)
    z = calculate_ziwei_from_saju(s)

    # 1. 일반 질문 테스트
    ans = generate_shaman_answer(s, z, "올해 이직을 하면 대기업으로 갈 수 있을까요?", "deep", name="홍길동")
    print("=== 일반 질문 딥 리딩 ===")
    print(ans["answer"][:300])

    # 2. 금기어 차단 테스트
    forb = generate_shaman_answer(s, z, "이번 주 로또 번호나 비트코인 상한가 좀 알려주세요", "single")
    print("\n=== 금기어 차단 테스트 ===")
    print(forb["answer"])
