# -*- coding: utf-8 -*-
"""
天命明鏡 (천명명경) | 운명의 3대 인연 프로필 & 3차원 위치 추적 엔진 (Destiny Partner Engine)
- 청월당 인기 출력 형식 100% 흡수 및 황실 자미두수/만세력 융합 초격차화
- 3대 인연 프로필:
  1. 전생부터 이어진 붉은 실의 배필 (Soulmate)
  2. 단단한 현실적 조화 인연 (Harmonious Partner)
  3. 인연인 척하는 치명적 악연 (Karmic Nemesis)
- 5대 신상 명세: 이름 초성(initial), 키 범위(height), 직업군(job), 띠(zodiac), 외모/성향(trait)
- 3차원 공간 좌표: 동서남북 붓글씨 방위(direction), 거리(distance km), 조우 장소(scene)
- 청사초롱 4대 등불 밝기(0~3) & 살풀이 D-Day 위험일 캘린더
"""

import sys
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 오행별 이름 초성 매핑 (한글 성명학 오행 원리)
# 목(木): ㄱ, ㅋ
# 화(火): ㄴ, ㄷ, ㄹ, ㅌ
# 토(土): ㅇ, ㅎ
# 금(金): ㅅ, ㅈ, ㅊ
# 수(水): ㅁ, ㅂ, ㅍ
OHENG_INITIALS = {
    "목": ["ㄱㅅㅎ", "ㄱㄷㅇ", "ㄱㅁㅈ", "ㅋㅈㅇ"],
    "화": ["ㄴㄷㅎ", "ㄹㅈㅇ", "ㅌㅅㅇ", "ㄴㅁㄱ"],
    "토": ["ㅇㅈㅇ", "ㅇㅅㅎ", "ㅎㄷㅇ", "ㅇㅁㅈ"],
    "금": ["ㅅㅈㅇ", "ㅈㅅㅎ", "ㅊㅁㄱ", "ㅅㄷㅇ"],
    "수": ["ㅁㅈㅇ", "ㅂㅅㅎ", "ㅍㄷㅇ", "ㅂㅁㅈ"]
}

# 십성 및 자미두수 주성별 유망 직업군 매핑
JOB_POOLS = {
    "high_tech": ["IT 테크 리드 / AI 서비스 기획자", "글로벌 테크 스타트업 C레벨", "소프트웨어 아키텍트 / 데이터 사이언티스트"],
    "finance": ["외국계 사모펀드(PE) 운용역", "투자은행(IB) 금융 자산운용가", "대형 회계법인 회계사"],
    "professional": ["종합병원 전문의 / 임상 교수", "대형 로펌 파트너 변호사", "국가 연구기관 선임 연구원"],
    "creative": ["크리에이티브 아트 디렉터", "하이엔드 공간 건축 디자이너", "방송 미디어 총괄 프로듀서"],
    "business": ["무역/이커머스 대표 사업가", "브랜드 리테일 총괄 디렉터", "전문 프랜차이즈 경영인"],
    "nemesis_job": ["외모만 번지르르한 투자 사기꾼 / 코인 허세가", "겉은 화려하나 빚더미인 허세형 프리랜서", "말만 앞서고 책임감 없는 유흥업 종사자"]
}

# 방위별 조우 장소 씬
SCENE_POOLS = {
    "동": ["오래된 고목이 자리한 대형 원목 카페 창가", "새벽 공기가 맑은 도심 수목원 산책로", "고풍스러운 목재 인테리어의 북카페"],
    "남": ["화려한 조명이 반짝이는 도심 고층 스카이라운지", "트렌디한 레스토랑 테라스", "예술 감각이 돋보이는 모던 갤러리 로비"],
    "서": ["석양이 길게 비치는 대형 서점 인문학 코너", "단정하고 정갈한 호텔 로비 라운지", "클래식 음악이 흐르는 와인 바"],
    "북": ["물이 잔잔하게 흐르는 호수 공원 수변 데크", "인적 드문 조용한 한옥 찻집", "비 오는 날 마주치는 대학가 고즈넉한 골목 카페"]
}

# 12지지 삼합 및 육합 / 원진 매핑
SAMHAP_MAP = {
    "자": ["진", "신", "축"], "축": ["유", "사", "자"],
    "인": ["오", "술", "해"], "묘": ["미", "해", "술"],
    "진": ["자", "신", "유"], "사": ["유", "축", "신"],
    "오": ["인", "술", "미"], "미": ["해", "묘", "오"],
    "신": ["자", "진", "사"], "유": ["사", "축", "진"],
    "술": ["인", "오", "묘"], "해": ["묘", "미", "인"]
}

WONJIN_MAP = {
    "자": "미", "축": "오", "인": "유", "묘": "신", "진": "해", "사": "술",
    "오": "축", "미": "자", "신": "묘", "유": "인", "술": "사", "해": "진"
}

ZODIAC_KOREAN = {
    "자": "쥐띠", "축": "소띠", "인": "호랑이띠", "묘": "토끼띠",
    "진": "용띠", "사": "뱀띠", "오": "말띠", "미": "양띠",
    "신": "원숭이띠", "유": "닭띠", "술": "개띠", "해": "돼지띠"
}


def calculate_destiny_partners(saju_data, ziwei_data=None, user_gender="male"):
    """
    3대 인연 프로필 (배필, 조화, 악연) 및 5대 스펙 자동 생성
    """
    day_gan = saju_data.get("day_gan", "갑")
    day_ji = saju_data.get("day_ji", "자")
    oheng_counts = saju_data.get("oheng_counts", {"목": 1, "화": 1, "토": 1, "금": 1, "수": 1})
    target_partner_gender = "female" if user_gender == "male" else "male"

    # 사주에서 가장 필요한 오행 (용신/부족한 오행)
    min_oheng = min(oheng_counts, key=oheng_counts.get)
    max_oheng = max(oheng_counts, key=oheng_counts.get)

    # 1. 전생부터 이어진 붉은 실의 배필 (Soulmate)
    soul_initials = OHENG_INITIALS.get(min_oheng, ["ㅇㅈㅇ", "ㄱㅅㅎ"])[0]
    soul_zodiac_jis = SAMHAP_MAP.get(day_ji, ["진", "신"])
    soul_zodiac = f"{ZODIAC_KOREAN[soul_zodiac_jis[0]]}, {ZODIAC_KOREAN[soul_zodiac_jis[1]]}"
    
    if target_partner_gender == "male":
        soul_height = "179 ~ 183cm"
        soul_trait = "쌍꺼풀 없이 짙고 그윽한 눈매에 곧은 콧날. 말수가 적으나 목소리가 중저음으로 신뢰감을 주는 체형."
    else:
        soul_height = "164 ~ 168cm"
        soul_trait = "선이 곱고 지적인 분위기. 미소 지을 때 반달눈이 되며 차분하고 따뜻한 온기를 품은 외모."
    # 용신 오행에 따른 개인 맞춤형 조우 타이밍 산출
    timing_map = {
        "목": "올해 봄철, 얼어붙은 대지를 뚫고 새싹이 돋아나는 화창한 시기 (양력 3월~5월)",
        "화": "올해 초여름~한여름, 태양의 기운이 뜨겁게 대지를 달구는 정열의 시기 (양력 6월~8월)",
        "토": "올해 늦여름 환절기, 곡식이 무르익고 터전을 단단히 다지는 시기 (양력 7월~9월)",
        "금": "올해 가을, 서늘한 가을바람이 불고 결실을 거두는 성숙의 시기 (양력 9월~11월)",
        "수": "올해 늦가을~한겨울, 찬 바람이 매섭고 온기를 나누고 싶은 깊은 밤 (양력 11월~1월)"
    }
    soul_timing = timing_map.get(min_oheng, "올해 하반기, 운의 흐름이 급변하는 전환점 (양력 10월~12월)")

    soulmate = {
        "type": "soulmate",
        "badge": "전생부터 이어진 붉은 실의 배필",
        "rank_title": "제1인연: 천생연분 평생 배필 (天生緣分)",
        "initial": soul_initials,
        "height": soul_height,
        "job": JOB_POOLS["professional"][0] if min_oheng in ["수", "금"] else JOB_POOLS["high_tech"][0],
        "zodiac": soul_zodiac,
        "trait": soul_trait,
        "chemistry_score": 96,
        "meeting_timing": soul_timing,
        "why_destiny": f"그대의 사주에서 가장 결핍된 **{min_oheng}(오행)**의 기운을 온몸으로 품고 태어난 귀인이오. 눈빛만 스쳐도 심장이 먼저 반응할 것이오."
    }

    # 2. 단단한 현실적 조화 인연 (Harmonious Partner)
    harm_initials = OHENG_INITIALS.get("토", ["ㅇㅅㅎ", "ㅎㄷㅇ"])[1]
    harm_zodiac_ji = SAMHAP_MAP.get(day_ji, ["축"])[-1]
    harm_zodiac = ZODIAC_KOREAN.get(harm_zodiac_ji, "소띠")

    if target_partner_gender == "male":
        harm_height = "175 ~ 178cm"
        harm_trait = "어깨가 넓고 단단한 체격. 웃을 때 인상이 푸근하며 현실 감각과 생활력이 뛰어난 분위기."
    else:
        harm_height = "160 ~ 164cm"
        harm_trait = "깔끔하고 세련된 오피스룩이 잘 어울리는 도회적인 인상. 배려심이 깊고 센스 있는 화법."

    harmony = {
        "type": "harmony",
        "badge": "단단한 인연으로 맺어질 조화의 인연",
        "rank_title": "제2인연: 상생지합 현실 동반자 (相生之合)",
        "initial": harm_initials,
        "height": harm_height,
        "job": JOB_POOLS["finance"][0] if min_oheng in ["토", "금"] else JOB_POOLS["business"][0],
        "zodiac": f"{harm_zodiac}, 용띠",
        "trait": harm_trait,
        "chemistry_score": 87,
        "meeting_timing": "업무나 일상적인 프로젝트, 지인들의 자연스러운 모임 자리에서 예고 없이 조우",
        "why_destiny": "불꽃처럼 타오르는 열정보다 잔잔하고 든든하게 서로의 경제적 곳간과 일상을 지켜주는 현실적 귀인이오."
    }

    # 3. 인연인 척하는 치명적 악연 (Karmic Nemesis)
    nemesis_ji = WONJIN_MAP.get(day_ji, "미")
    nemesis_zodiac = ZODIAC_KOREAN.get(nemesis_ji, "양띠")
    nem_initials = OHENG_INITIALS.get(max_oheng, ["ㅂㅁㅈ"])[0]

    if target_partner_gender == "male":
        nem_height = "181 ~ 185cm"
        nem_trait = "화려한 명품이나 외제차로 치장하고 이목구비가 뚜렷하나 눈빛이 불안정하게 흔들리는 인상."
    else:
        nem_height = "166 ~ 170cm"
        nem_trait = "화려하고 도발적인 옷차림. 감정 기복이 매우 심하고 본인의 필요에 따라 태도가 급변하는 인상."

    nemesis = {
        "type": "nemesis",
        "badge": "⚡ 인연인 척 다가오는 치명적 악연",
        "rank_title": "경계 대상: 애증원진 살(愛憎怨嗔煞)",
        "initial": nem_initials,
        "height": nem_height,
        "job": JOB_POOLS["nemesis_job"][0],
        "zodiac": f"{nemesis_zodiac} (원진살 극충)",
        "trait": nem_trait,
        "chemistry_score": 42,
        "meeting_timing": "밤늦은 술자리나 화려한 파티, SNS DM 등 가벼운 호기심으로 엮이는 순간",
        "why_destiny": f"그대의 넘치는 **{max_oheng}(오행)**을 자극하여 감정의 롤러코스터를 태우고 종국에는 금전이나 마음에 깊은 흉터를 남길 악연이오. 초반의 달콤한 유혹에 절대 속지 마시오!"
    }

    return [soulmate, harmony, nemesis]


def calculate_destiny_place(saju_data):
    """
    3차원 공간 좌표 추적: 동서남북 붓글씨 방위 + 거리(km) + 조우 장소
    """
    oheng_counts = saju_data.get("oheng_counts", {"목": 1, "화": 1, "토": 1, "금": 1, "수": 1})
    min_oheng = min(oheng_counts, key=oheng_counts.get)

    dir_map = {
        "목": ("동", "東", "east", "약 15km · 근거리", SCENE_POOLS["동"]),
        "화": ("남", "南", "south", "약 80km · 원거리", SCENE_POOLS["남"]),
        "금": ("서", "西", "west", "약 25km · 중거리", SCENE_POOLS["서"]),
        "수": ("북", "北", "north", "약 100km · 광역 원거리", SCENE_POOLS["북"]),
        "토": ("남", "南", "south", "약 35km · 중거리", SCENE_POOLS["남"])
    }

    k_dir, h_dir, e_dir, dist, scenes = dir_map.get(min_oheng, dir_map["목"])

    return {
        "direction": k_dir,
        "direction_hanja": h_dir,
        "direction_eng": e_dir,
        "distance": dist,
        "scenes": scenes,
        "primary_scene": scenes[0],
        "oracle_guide": f"그대에게 가장 길한 생명의 기운이 머무는 축은 **【{h_dir}({k_dir}쪽)】**이오. {dist} 반경 안에서 귀인과의 파동이 공명할 것이니 중요한 약속이나 인연을 찾는 장소는 반드시 이 방위를 향하시오."
    }


def calculate_lantern_fortune(saju_data):
    """
    청사초롱 4대 등불 밝기 진단 (0~3단계)
    """
    oheng_counts = saju_data.get("oheng_counts", {"목": 1, "화": 1, "토": 1, "금": 1, "수": 1})
    shinsal = saju_data.get("shinsal", {})

    # 백호/원진/귀문 등이 있으면 운이 막혀 등불 단계 감소
    penalty = 0
    if shinsal.get("baekho") or shinsal.get("guimun"): penalty += 1
    if shinsal.get("wonjin") or shinsal.get("gongmang"): penalty += 1

    wealth_level = max(1, min(3, 3 - (1 if oheng_counts.get("금", 0) == 0 else 0) - penalty))
    health_level = max(1, min(3, 3 - penalty))
    love_level = max(1, min(3, 3 - (1 if shinsal.get("wonjin") else 0) - (penalty // 2)))
    overall_level = max(1, min(3, (wealth_level + health_level + love_level) // 3))

    level_descs = {
        0: "등불이 꺼진 암흑기 (기운이 심각하게 정체되어 긴급 살풀이 필요)",
        1: "희미하게 깜빡이는 등불 (장벽이 있으나 곧 활로가 열릴 징조)",
        2: "은은하고 안정된 불빛 (점진적인 운의 상승 곡선 진입)",
        3: "환하게 타오르는 황금 등불 (천운이 활짝 열려 만사형통할 길운)"
    }

    return {
        "overall_level": overall_level,
        "overall_desc": level_descs[overall_level],
        "metrics": {
            "wealth": {"level": wealth_level, "title": "재물곳간 기운", "desc": level_descs[wealth_level]},
            "love": {"level": love_level, "title": "인연/애정 기운", "desc": level_descs[love_level]},
            "health": {"level": health_level, "title": "기혈/신체 기운", "desc": level_descs[health_level]}
        }
    }


def calculate_caution_calendar(saju_data):
    """
    사주 원국 기반 100% 동적 월별 위험일 캘린더 & 살풀이 D-Day 카운트다운
    """
    day_ji = saju_data.get("day_ji", "자")
    shinsal = saju_data.get("shinsal", {})
    oheng_counts = saju_data.get("oheng_counts", {"목": 1, "화": 1, "토": 1, "금": 1, "수": 1})
    max_oheng = max(oheng_counts, key=oheng_counts.get)
    has_heavy_shinsal = bool(shinsal.get("baekho") or shinsal.get("guimun") or shinsal.get("wonjin") or shinsal.get("cheolajimang"))

    # 1. 일지와 정면 충(沖)하는 월
    CHUNG_MONTH_MAP = {
        "자": 6, "축": 7, "인": 8, "묘": 9, "진": 10, "사": 11,
        "오": 12, "미": 1, "신": 2, "유": 3, "술": 4, "해": 5
    }
    chung_m = CHUNG_MONTH_MAP.get(day_ji, 6)

    # 2. 일지와 원진(怨嗔)을 이루는 월
    WONJIN_MONTH_MAP = {
        "자": 7, "축": 6, "인": 9, "묘": 8, "진": 11, "사": 10,
        "오": 1, "미": 12, "신": 3, "유": 2, "술": 5, "해": 4
    }
    wonjin_m = WONJIN_MONTH_MAP.get(day_ji, 7)
    if wonjin_m == chung_m:
        wonjin_m = (chung_m + 3) % 12 or 12

    # 3. 사주에서 가장 과다한 기신(忌神)이 발호하는 계절 월
    GISIN_MONTH_MAP = {
        "목": 3, "화": 6, "토": 10, "금": 9, "수": 12
    }
    gisin_m = GISIN_MONTH_MAP.get(max_oheng, 11)
    if gisin_m in [chung_m, wonjin_m]:
        gisin_m = (wonjin_m + 4) % 12 or 12

    # 월별 주의해야 할 3대 날짜 (사주 고유 동적 산출)
    caution_schedule = [
        {
            "month": chung_m,
            "days": [6, 18, 30] if chung_m in [1, 3, 5, 7, 8, 10, 12] else [6, 18],
            "reason": f"일지({day_ji}) 정충(沖) 발동월 — 심신이 불안정해지고 이동수와 돌발 사고, 신체 부상 위험이 높으니 무리한 이동과 원행을 삼가시오."
        },
        {
            "month": wonjin_m,
            "days": [4, 16, 28],
            "reason": "원진살(怨嗔) 기운 충돌일 — 가장 가까운 연인·동료와의 사소한 말실수가 큰 구설수와 이별수로 비화될 수 있으니 언행을 극도로 무겁게 하시오."
        },
        {
            "month": gisin_m,
            "days": [9, 21],
            "reason": f"기신({max_oheng}) 과다 발호일 — 재물의 혈맥이 흔들리는 손재수(損財數)가 감지되니 섣부른 주식·코인·부동산 계약이나 보증을 절대 금지하시오."
        }
    ]

    # 월 오름차순 정렬
    caution_schedule.sort(key=lambda x: x["month"])

    return {
        "has_heavy_shinsal": has_heavy_shinsal,
        "salpuri_dday": 7,
        "salpuri_guide": "살풀이 유효 기간 D-7 | 지금 살풀이 비책을 확인하지 않으면 흉살의 파동이 현실의 삶을 뒤흔들 수 있습니다.",
        "schedule": caution_schedule
    }


if __name__ == '__main__':
    from manseryeok import calculate_saju
    s = calculate_saju(1994, 3, 15, 18, 0)
    partners = calculate_destiny_partners(s, user_gender="male")
    place = calculate_destiny_place(s)
    lantern = calculate_lantern_fortune(s)
    caution = calculate_caution_calendar(s)

    print("=== 인연 5대 스펙 ===")
    for p in partners:
        print(f"[{p['badge']}] 초성: {p['initial']} | 키: {p['height']} | 직업: {p['job']} | 띠: {p['zodiac']}")
    print("\n=== 방위 좌표 ===")
    print(f"방위: {place['direction_hanja']}({place['direction']}) | 거리: {place['distance']} | 장소: {place['primary_scene']}")
    print("\n=== 등불 진단 ===")
    print("종합 레벨:", lantern["overall_level"], lantern["overall_desc"])
    print("\n=== 위험일 캘린더 ===")
    print("D-Day:", caution["salpuri_dday"], "| 위험월:", [c['month'] for c in caution['schedule']])
