# -*- coding: utf-8 -*-
"""
天命明鏡 (천명명경) | 2인 사주 정밀 궁합(宮合) & 현허도인 직설 공수 엔진
- 4대 관계 유형: 짝사랑(crush), 썸/연애(dating), 부부(married), 업무/동업(business)
- 명리학 일간 천간합충, 지지 육합/삼합/육충/원진살 정밀 대조
- 상호 오행 보완도(Complementarity) 수치화 (0~100점)
- 자미두수 명궁 주성 케미 결합
- 현허도인의 촌철살인 관계별 공수 및 개운 처방
"""

# 천간합 (5합)
CHEONGAN_HAP = {
    ("갑", "기"): "중정지합 (中正之合) - 서로의 부족함을 채우는 신뢰의 결합",
    ("기", "갑"): "중정지합 (中正之合) - 서로의 부족함을 채우는 신뢰의 결합",
    ("을", "경"): "인의지합 (仁義之合) - 다정함과 결단력이 조화를 이루는 결합",
    ("경", "을"): "인의지합 (仁義之合) - 다정함과 결단력이 조화를 이루는 결합",
    ("병", "신"): "위엄지합 (威嚴之合) - 열정과 냉철함이 불꽃을 튀기는 결합",
    ("신", "병"): "위엄지합 (威嚴之合) - 열정과 냉철함이 불꽃을 튀기는 결합",
    ("정", "임"): "음덕지합 (陰德之合) - 깊은 무의식과 본능적 끌림이 통하는 결합",
    ("임", "정"): "음덕지합 (陰德之合) - 깊은 무의식과 본능적 끌림이 통하는 결합",
    ("무", "계"): "무정지합 (無情之合) - 현실적 이해와 실리를 바탕으로 한 결합",
    ("계", "무"): "무정지합 (無情之合) - 현실적 이해와 실리를 바탕으로 한 결합"
}

# 천간충 (7충)
CHEONGAN_CHUNG = [
    {"갑", "경"}, {"을", "신"}, {"병", "임"}, {"정", "계"}
]

# 지지 육합 (6합)
JIJI_YUKHAP = {
    ("자", "축"): "자축합토 (子丑合土) - 은밀하고 끈끈한 현실적 결속",
    ("인", "해"): "인해합목 (寅亥合木) - 서로의 성장을 북돋아주는 생명력",
    ("묘", "술"): "묘술합화 (卯戌合火) - 봄과 가을의 불꽃같은 열정",
    ("진", "유"): "진유합금 (辰酉合金) - 굳건하고 단단한 신의",
    ("사", "신"): "사신합수 (巳申合水) - 유연하고 지혜로운 임기응변",
    ("오", "미"): "오미합화 (午未合火) - 따뜻하고 화려한 영혼의 조화"
}

# 지지 육충 (6충)
JIJI_CHUNG = [
    {"자", "오"}, {"축", "미"}, {"인", "신"}, {"묘", "유"}, {"진", "술"}, {"사", "해"}
]

# 원진살 (6쌍)
WONJIN_PAIRS = [
    {"자", "미"}, {"축", "오"}, {"인", "유"}, {"묘", "신"}, {"진", "해"}, {"사", "술"}
]

# 삼합 그룹
SAMHAP_GROUPS = [
    {"신", "자", "진"}, # 수국
    {"인", "오", "술"}, # 화국
    {"사", "유", "축"}, # 금국
    {"해", "묘", "미"}  # 목국
]

# 오행 상생/상극
OHENG_SANGSAENG = {
    "목": "화", "화": "토", "토": "금", "금": "수", "수": "목"
}
OHENG_SANGGEUK = {
    "목": "토", "토": "수", "수": "화", "화": "금", "금": "목"
}

RELATION_NAMES = {
    "crush": ("짝사랑", "💘 닿을 듯 말 듯한 마음의 진실과 상대방의 속내"),
    "dating": ("썸/연애", "💞 불타오르는 감정의 온도와 미래의 결실"),
    "married": ("부부", "💍 백년해로의 길과 가정을 지키는 현실적 궁합"),
    "business": ("업무/동업", "🤝 돈과 권력, 사업적 성패를 가르는 동업의 합")
}

def analyze_gunghap(sajuA, sajuB, relation_type="dating", nameA="본인", nameB="상대방"):
    """
    2인 사주(A, B) 간의 정밀 궁합 분석 및 현허도인 직설 공수 생성
    """
    rel_info = RELATION_NAMES.get(relation_type, RELATION_NAMES["dating"])
    nameA = nameA.strip() if nameA else "본인"
    nameB = nameB.strip() if nameB else "상대방"

    dayA_gan = sajuA["day_gan"]
    dayA_ji = sajuA["day_ji"]
    yearA_ji = sajuA["raw"]["year"][1]
    ohengA = sajuA.get("oheng_counts", {"목": 0, "화": 0, "토": 0, "금": 0, "수": 0})

    dayB_gan = sajuB["day_gan"]
    dayB_ji = sajuB["day_ji"]
    yearB_ji = sajuB["raw"]["year"][1]
    ohengB = sajuB.get("oheng_counts", {"목": 0, "화": 0, "토": 0, "금": 0, "수": 0})

    # 1. 일간(정신적/본질적 케미) 분석 (최대 30점)
    gan_score = 15
    gan_relation = ""
    is_gan_hap = (dayA_gan, dayB_gan) in CHEONGAN_HAP or (dayB_gan, dayA_gan) in CHEONGAN_HAP
    is_gan_chung = {dayA_gan, dayB_gan} in CHEONGAN_CHUNG

    if is_gan_hap:
        gan_score = 30
        hap_desc = CHEONGAN_HAP.get((dayA_gan, dayB_gan), CHEONGAN_HAP.get((dayB_gan, dayA_gan), "천간합"))
        gan_relation = f"하늘이 맺어준 천간합(天干合) - {hap_desc}"
    elif OHENG_SANGSAENG.get(sajuA["pillars"]["day"]["gan_oheng"][0]) == sajuB["pillars"]["day"]["gan_oheng"][0]:
        gan_score = 25
        gan_relation = f"{nameA}의 기운이 {nameB}를 낳고 기르는 수려한 상생(相生)"
    elif OHENG_SANGSAENG.get(sajuB["pillars"]["day"]["gan_oheng"][0]) == sajuA["pillars"]["day"]["gan_oheng"][0]:
        gan_score = 25
        gan_relation = f"{nameB}의 기운이 {nameA}를 포근히 감싸고 보듬어주는 상생(相生)"
    elif sajuA["pillars"]["day"]["gan_oheng"][0] == sajuB["pillars"]["day"]["gan_oheng"][0]:
        gan_score = 20
        gan_relation = "동일한 오행의 만남 - 오랜 친구처럼 편안하나 고집의 대립 주의"
    elif is_gan_chung:
        gan_score = 8
        gan_relation = "서로의 칼날이 부딪치는 천간충(天干沖) - 강렬한 자극이자 마찰"
    else:
        gan_score = 14
        gan_relation = "서로 다른 결의 기운 - 조율과 존중이 필요한 관계"

    # 2. 일지(속궁합 및 현실적/감정적 밀착도) 분석 (최대 30점)
    ji_score = 15
    ji_relation = ""
    is_ji_yukhap = (dayA_ji, dayB_ji) in JIJI_YUKHAP or (dayB_ji, dayA_ji) in JIJI_YUKHAP
    is_ji_chung = {dayA_ji, dayB_ji} in JIJI_CHUNG
    is_ji_wonjin = {dayA_ji, dayB_ji} in WONJIN_PAIRS
    is_ji_samhap = any(dayA_ji in g and dayB_ji in g for g in SAMHAP_GROUPS)

    if is_ji_yukhap:
        ji_score = 30
        hap_desc = JIJI_YUKHAP.get((dayA_ji, dayB_ji), JIJI_YUKHAP.get((dayB_ji, dayA_ji), "지지육합"))
        ji_relation = f"몸과 마음이 자석처럼 달라붙는 육합(六合) - {hap_desc}"
    elif is_ji_samhap:
        ji_score = 26
        ji_relation = "같은 꿈과 지향점을 바라보는 지지삼합(三合) - 흔들리지 않는 가치관 공유"
    elif is_ji_wonjin:
        ji_score = 5
        ji_relation = "마주보면 원망스럽고 돌아서면 보고픈 원진살(怨嗔煞)의 애증"
    elif is_ji_chung:
        ji_score = 8
        ji_relation = "생활 습관과 가치관의 정면 충돌 지지육충(六沖) - 마찰 극복 비책 필수"
    else:
        ji_score = 18
        ji_relation = "무합무충의 평온한 결합 - 큰 풍파 없이 잔잔하게 유지되는 터전"

    # 3. 상호 오행 보완도 (결핍 채워주기) (최대 25점)
    elem_score = 10
    complement_insights = []
    for elem in ["목", "화", "토", "금", "수"]:
        if ohengA.get(elem, 0) == 0 and ohengB.get(elem, 0) >= 2:
            elem_score += 7
            complement_insights.append(f"{nameA}에게 절실히 마른 **{elem}(오행)**을 {nameB}가 넉넉히 채워줌")
        if ohengB.get(elem, 0) == 0 and ohengA.get(elem, 0) >= 2:
            elem_score += 7
            complement_insights.append(f"{nameB}에게 부족한 **{elem}(오행)**의 결핍을 {nameA}가 든든하게 받쳐줌")
    elem_score = min(25, max(5, elem_score))
    elem_summary = " · ".join(complement_insights) if complement_insights else "서로의 오행이 비교적 고르게 분배되어 균형을 이룸"

    # 4. 겉궁합(년지/띠 조화) (최대 15점)
    year_score = 10
    is_year_samhap = any(yearA_ji in g and yearB_ji in g for g in SAMHAP_GROUPS)
    is_year_chung = {yearA_ji, yearB_ji} in JIJI_CHUNG
    is_year_wonjin = {yearA_ji, yearB_ji} in WONJIN_PAIRS

    if is_year_samhap:
        year_score = 15
        year_relation = f"띠의 기운이 하나로 엮이는 삼합(三合) - 세상 사람들 앞에서도 보기 좋은 천생연분"
    elif is_year_wonjin:
        year_score = 5
        year_relation = f"초반 인상에서 이유 없는 경계심이나 편견이 생길 수 있는 띠의 원진"
    elif is_year_chung:
        year_score = 6
        year_relation = f"서로 다른 배경과 환경에서 자라나 초반 기싸움이 팽팽한 띠의 충돌"
    else:
        year_score = 11
        year_relation = f"무난하고 자연스럽게 어우러지는 사회적 관계의 띠 조화"

    # 총점 산출 (0~100)
    total_score = min(100, max(20, gan_score + ji_score + elem_score + year_score))

    # 등급 분류
    if total_score >= 88:
        grade = "천생연분 (天生緣分)"
        grade_desc = "하늘이 천년에 한 번 맺어주는 기적 같은 합. 서로의 영혼과 현실이 완벽하게 맞물리는 최상의 궁합입니다."
    elif total_score >= 75:
        grade = "찰떡궁합 (相生之合)"
        grade_desc = "서로의 부족함을 너그럽게 품어주고 함께 있을 때 더 큰 부와 행복을 끌어당기는 길한 인연입니다."
    elif total_score >= 60:
        grade = "밀당연분 (調和之緣)"
        grade_desc = "호기심과 매력은 넘치나 가끔씩 찾아오는 감정의 엇갈림을 대화와 배려로 조율해야 하는 관계입니다."
    elif total_score >= 45:
        grade = "애증원진 (愛憎之煞)"
        grade_desc = "강렬하게 끌리면서도 돌아서면 상처를 주기 쉬운 애증의 고리. 집착을 내려놓아야 편안해집니다."
    else:
        grade = "풍파주의 (克沖之緣)"
        grade_desc = "기운의 충돌과 엇갈림이 잦아 서로의 독립적인 영역을 반드시 존중해야 관계를 유지할 수 있습니다."

    # 현허도인의 4대 관계별 촌철살인 직설 공수
    speech_intro = f"도인이 양손에 {nameA}와 {nameB} 두 사람의 명식을 올려두고 영안을 열어 천기를 관조해보니...\n\n"
    
    if relation_type == "crush": # 짝사랑
        oracle_speech = f"""{speech_intro}이것은 단순한 스쳐 지나가는 호기심이 아니오.
{nameA} 그대가 홀로 가슴앓이하며 잠 못 이루는 까닭은, 그대의 사주에서 결핍된 기운을 {nameB}가 온몸으로 뿜어내고 있기 때문이오.

두 사람의 천기 궁합은 **【{grade} - {total_score}점】**이오.
{gan_relation}이며, {ji_relation}이니 결코 닿을 수 없는 허상은 아니오.

하지만 똑똑히 들으시오. {nameB}의 속마음은 지금 당장 문을 활짝 열어둔 상태가 아니오. 
조급하게 마음을 들이대면 상대의 {dayB_ji} 지지 기운이 도망치거나 방어막을 칠 것이니,
{elem_summary}의 기운을 활용하여 '자연스러운 조력자'의 모습으로 먼저 다가가야만 기어이 그 사람의 마음을 훔칠 수 있소!"""

    elif relation_type == "dating": # 썸/연애
        oracle_speech = f"""{speech_intro}두 영혼의 파동이 얽혀드는 불꽃을 투시해보니,
서로를 향한 이끌림은 거짓이 아니나 연애의 온도차에서 오는 마찰이 감지되는구려.

두 사람의 애정 궁합 지수는 **【{grade} - {total_score}점】**이오.
정신적 호흡은 {gan_relation}의 성향을 띠고 있으며, 일상의 케미는 {ji_relation}의 형국이오.

{nameA}와 {nameB}가 오래도록 예쁜 사랑을 이어가려면 반드시 명심하시오:
한쪽이 불처럼 타오를 때 다른 한쪽은 차가운 물로 식혀주는 유연함이 필요하오.
{elem_summary}를 기억하고, 사소한 자존심 싸움으로 서로의 가슴에 비수를 꽂지 마시오.
이 고비만 넘기면 두 사람은 둘도 없는 인생의 동반자로 승화될 것이오!"""

    elif relation_type == "married": # 부부
        oracle_speech = f"""{speech_intro}한 지붕 아래서 밥숟가락을 맞대고 살아가는 부부의 연은 전생의 삼천 겁(劫)의 인연이 쌓여야 열리는 법이오.

두 사람의 백년해로 궁합은 **【{grade} - {total_score}점】**이오.
가정의 기둥을 이루는 천기는 {gan_relation}이며, 안방의 속궁합과 정서는 {ji_relation}이오.

부부궁에서 경계해야 할 것은 '익숙함에 속아 서로를 당연하게 여기는 오만함'이오.
{elem_summary}의 상호 보완을 인정하고, 가계의 재물권과 집안 대소사의 결정권을 각자의 장점에 맞추어 나누어 맡으시오.
서로를 귀인으로 섬길 때 이 집안에 마르지 않는 재물과 자손의 번영이 깃들 것이오!"""

    else: # business (업무/동업)
        oracle_speech = f"""{speech_intro}돈과 명예, 생업의 전선에서 손을 잡는 동업은 부부의 연보다 더 냉철하고 서슬 퍼런 잣대가 필요하오.

두 사람의 사업적 시너지 궁합은 **【{grade} - {total_score}점】**이오.
아이디어와 비전의 합은 {gan_relation}이며, 실제 자금 집행과 실행의 조화는 {ji_relation}이오.

동업에서 망하는 첫 번째 길은 돈 계산이 흐릿한 것이요, 두 번째는 역할의 월권이오.
{elem_summary}의 이점을 철저히 극대화하시오.
영업과 대외 활동은 더 능숙한 사람에게 일임하고, 내부 곳간과 금전 관리는 꼼꼼한 이가 도맡아야만
중간에 배신수로 갈라서지 않고 막대한 천하의 부를 함께 나눌 수 있소!"""

    return {
        "relation_type": relation_type,
        "relation_name": rel_info[0],
        "relation_desc": rel_info[1],
        "total_score": total_score,
        "grade": grade,
        "grade_desc": grade_desc,
        "scores": {
            "spirit_chemistry": gan_score * 100 // 30, # 정신/영혼 케미 %
            "reality_chemistry": ji_score * 100 // 30, # 현실/속궁합 케미 %
            "element_balance": elem_score * 100 // 25,  # 오행 상호 보완도 %
            "social_harmony": year_score * 100 // 15   # 겉궁합/사회적 조화 %
        },
        "details": {
            "gan_chemistry": {"score": gan_score * 100 // 30, "title": "정신적/본질적 교감", "relation": gan_relation},
            "ji_chemistry": {"score": ji_score * 100 // 30, "title": "현실적/속궁합 밀착도", "relation": ji_relation},
            "elem_balance": {"score": elem_score * 100 // 25, "title": "오행 상호 보완", "relation": elem_summary},
            "year_chemistry": {"score": year_score * 100 // 15, "title": "사회적 조화 (띠궁합)", "relation": year_relation},
            "gan_relation": gan_relation,
            "ji_relation": ji_relation,
            "element_summary": elem_summary,
            "year_relation": year_relation
        },
        "oracle_speech": oracle_speech,
        "personA": {"name": nameA, "day_gan": dayA_gan, "day_ji": dayA_ji, "year_ji": yearA_ji},
        "personB": {"name": nameB, "day_gan": dayB_gan, "day_ji": dayB_ji, "year_ji": yearB_ji}
    }

if __name__ == '__main__':
    from manseryeok import calculate_saju
    s1 = calculate_saju(1993, 8, 17, 18, 0)
    s2 = calculate_saju(1995, 5, 20, 10, 0)
    res = analyze_gunghap(s1, s2, "dating", "홍길동", "성춘향")
    print("=== 궁합 테스트 ===")
    print("총점:", res["total_score"], res["grade"])
    print("공수 요약:\n", res["oracle_speech"][:200])
