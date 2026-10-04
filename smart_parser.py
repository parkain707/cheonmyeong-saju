# -*- coding: utf-8 -*-
"""
초보자를 위한 사주 정보 스마트 파서 및 보정기 (Smart Parser & Fallback Estimator)
- "93년 닭띠 여름 저녁", "1988.3.15 새벽", "음력 90년 5월 점심" 등 자연어 자유 텍스트 정밀 파싱
- 일상 언어 기반 시간대(새벽, 아침, 점심, 저녁, 밤 등) 12시진 자동 변환
- 12간지(띠) 기반 연도 추론
- 시간을 전혀 모를 때의 삼주(三柱) 기반 '조후 및 억부' 시주 역추론 알고리즘
"""

import re
from datetime import datetime
from lunar_converter import lunar_to_solar

# 12간지 띠 매핑 (1920 ~ 2030)
ZODIAC_ANIMALS = ["쥐", "소", "호랑이", "범", "토끼", "용", "뱀", "말", "양", "원숭이", "잔나비", "닭", "개", "돼지"]
ZODIAC_JI = {
    "쥐": "자", "소": "축", "호랑이": "인", "범": "인", "토끼": "묘",
    "용": "진", "뱀": "사", "말": "오", "양": "미",
    "원숭이": "신", "잔나비": "신", "닭": "유", "개": "술", "돼지": "해"
}
JI_ORDER = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# 일상 생활 시간대 매핑
TIME_DESCRIPTIONS = [
    (re.compile(r'(깊은\s*밤|한밤중|자정|야밤|밤열두시|밤\s*12|새벽\s*1|새벽\s*0)'), 0, "자시 (23:30~01:29, 깊은 밤)"),
    (re.compile(r'(닭\s*울\s*때|첫닭|새벽\s*[23]|새벽녘)'), 2, "축시 (01:30~03:29, 새벽닭 울 무렵)"),
    (re.compile(r'(새벽\s*[45]|동틀\s*무렵|여명|새벽운동)'), 4, "인시 (03:30~05:29, 동틀 무렵)"),
    (re.compile(r'(아침\s*[67]|해뜰\s*무렵|등교|출근길)'), 6, "묘시 (05:30~07:29, 해 뜰 무렵)"),
    (re.compile(r'(아침\s*[89]|아침밥|오전\s*[89])'), 8, "진시 (07:30~09:29, 아침 식사 시간)"),
    (re.compile(r'(오전\s*1[01]|새참|점심전)'), 10, "사시 (09:30~11:29, 햇살 완연한 오전)"),
    (re.compile(r'(정오|점심|낮\s*12|한낮|점심밥|오후\s*1)'), 12, "오시 (11:30~13:29, 정오 한낮)"),
    (re.compile(r'(오후\s*[23]|나른할\s*때|늦은\s*점심)'), 14, "미시 (13:30~15:29, 나른한 오후)"),
    (re.compile(r'(오후\s*[45]|해질\s*무렵\s*전|장볼\s*때)'), 16, "신시 (15:30~17:29, 늦은 오후)"),
    (re.compile(r'(해질녘|노을|퇴근|저녁\s*[67])'), 18, "유시 (17:30~19:29, 해질녘 퇴근 시간)"),
    (re.compile(r'(저녁\s*[89]|초저녁|저녁밥|뉴스볼\s*때)'), 20, "술시 (19:30~21:29, 초저녁)"),
    (re.compile(r'(밤\s*1[01]|잠들\s*때|취침|야식)'), 22, "해시 (21:30~23:29, 잠자리에 들 무렵)")
]

def parse_free_text_saju(text):
    """
    초보자의 자유 텍스트 입력을 지능적으로 분석하여 정형 데이터로 변환
    예: "93년 닭띠 음력 5월 12일 저녁 퇴근길"
    """
    res = {
        "year": None,
        "month": None,
        "day": None,
        "hour": None,
        "is_lunar": False,
        "is_leap": False,
        "time_desc": "",
        "notes": []
    }

    # 1. 음력 / 윤달 감지
    if re.search(r'(음력|음|달력|음력생)', text):
        res["is_lunar"] = True
        res["notes"].append("음력 생일로 인식되었습니다.")
    if re.search(r'(윤달|윤월|윤)', text):
        res["is_leap"] = True
        res["notes"].append("윤달(閏月)로 인식되었습니다.")

    # 2. 연도 감지
    # 4자리 연도: 1988년, 2002 등
    m_year4 = re.search(r'(19\d\d|20\d\d)', text)
    if m_year4:
        res["year"] = int(m_year4.group(1))
    else:
        # 2자리 연도: 93년, 88년생, 05년 등
        m_year2 = re.search(r'(\d{2})\s*(년|년생|학번)?', text)
        if m_year2:
            val = int(m_year2.group(1))
            res["year"] = (2000 + val) if val <= 30 else (1900 + val)
            res["notes"].append(f"연도를 {res['year']}년으로 자동 보정했습니다.")

    # 띠 감지 (연도가 없을 경우 또는 연도 교차 검증)
    for animal, ji in ZODIAC_JI.items():
        if animal + "띠" in text or animal in text:
            target_idx = JI_ORDER.index(ji)
            # 만약 연도가 없으면 가장 유력한 1980~2010 사이 연도 추론
            if not res["year"]:
                # 4년이 자년이므로 (year - 4) % 12 == target_idx
                for y in range(1990, 2015):
                    if (y - 4) % 12 == target_idx:
                        res["year"] = y
                        res["notes"].append(f"{animal}띠를 바탕으로 {y}년생으로 추정했습니다.")
                        break
            break

    # 3. 월/일 감지
    # 형식 1: 1988.03.15, 1988-3-15, 1988/3/15
    m_date = re.search(r'(\d{1,2})[\.\-\/](\d{1,2})', text)
    if m_date:
        res["month"] = int(m_date.group(1))
        res["day"] = int(m_date.group(2))
    else:
        # 형식 2: 5월 12일, 5월12일
        m_md = re.search(r'(\d{1,2})\s*월\s*(\d{1,2})\s*일?', text)
        if m_md:
            res["month"] = int(m_md.group(1))
            res["day"] = int(m_md.group(2))
        else:
            # 계절 힌트만 있는 경우
            if re.search(r'(봄|새봄|초봄)', text):
                res["month"] = 4; res["day"] = 15; res["notes"].append("봄 생일(4월 15일)로 기본 보정했습니다.")
            elif re.search(r'(여름|한여름|초여름)', text):
                res["month"] = 7; res["day"] = 15; res["notes"].append("여름 생일(7월 15일)로 기본 보정했습니다.")
            elif re.search(r'(가을|늦가을|초가을)', text):
                res["month"] = 10; res["day"] = 15; res["notes"].append("가을 생일(10월 15일)로 기본 보정했습니다.")
            elif re.search(r'(겨울|한겨울|초겨울)', text):
                res["month"] = 1; res["day"] = 15; res["notes"].append("겨울 생일(1월 15일)로 기본 보정했습니다.")

    # 4. 시간 감지
    # 형식 1: 구체적 시간 (14시, 오후 3시, 15:30 등)
    m_exact_time = re.search(r'(오전|오후|새벽|밤)?\s*(\d{1,2})\s*(시|:\d{2})', text)
    if m_exact_time:
        ampm = m_exact_time.group(1) or ""
        h = int(m_exact_time.group(2))
        if ampm in ["오후", "저녁", "밤"] and h < 12:
            h += 12
        elif ampm in ["오전", "새벽"] and h == 12:
            h = 0
        res["hour"] = h
        res["time_desc"] = f"{h}시경"
    else:
        # 형식 2: 일상 표현 (닭 울 때, 점심, 퇴근길 등)
        for pattern, h_val, desc in TIME_DESCRIPTIONS:
            if pattern.search(text):
                res["hour"] = h_val
                res["time_desc"] = desc
                res["notes"].append(f"시간대를 '{desc}'로 감지했습니다.")
                break

    # 기본값 보정 (연도 없으면 1992, 월일 없으면 5월 5일, 시간 없으면 -1)
    if not res["year"]: res["year"] = 1992; res["notes"].append("연도 미입력으로 1992년 기본 설정")
    if not res["month"]: res["month"] = 5
    if not res["day"]: res["day"] = 5
    if res["hour"] is None: res["hour"] = -1

    # 음력이면 양력으로 자동 정밀 변환
    if res["is_lunar"]:
        sy, sm, sd = lunar_to_solar(res["year"], res["month"], res["day"], res["is_leap"])
        res["solar_year"] = sy
        res["solar_month"] = sm
        res["solar_day"] = sd
        res["notes"].append(f"음력 {res['year']}년 {res['month']}월 {res['day']}일을 양력 {sy}년 {sm}월 {sd}일로 자동 변환했습니다.")
    else:
        res["solar_year"] = res["year"]
        res["solar_month"] = res["month"]
        res["solar_day"] = res["day"]

    return res

def estimate_hour_from_three_pillars(saju_data, user_preference="balanced"):
    """
    태어난 시간을 전혀 모를 때, 삼주(년·월·일주)의 오행 균형을 분석하여
    사주의 치우침을 바로잡아주는 최적의 시주(調候/用神 時柱)를 역추론
    """
    oheng = saju_data["oheng_counts"]
    day_gan = saju_data["day_gan"]
    
    # 부족한 오행 찾기
    min_element = min(oheng, key=oheng.get)
    
    # 각 오행을 보충해주는 대표 시진
    element_to_hours = {
        "목": (4, "인시 (03:30~05:29) — 부족한 목(木) 기운을 채워 생명력과 추진력을 불어넣는 시간"),
        "화": (12, "오시 (11:30~13:29) — 부족한 화(火) 기운을 채워 밝은 온기와 활력을 더하는 시간"),
        "토": (8, "진시 (07:30~09:29) — 부족한 토(土) 기운을 채워 안정감과 포용력을 다지는 시간"),
        "금": (16, "신시 (15:30~17:29) — 부족한 금(金) 기운을 채워 단단한 결단력과 실속을 세우는 시간"),
        "수": (0, "자시 (23:30~01:29) — 부족한 수(水) 기운을 채워 깊은 지혜와 유연성을 더하는 시간")
    }
    
    estimated_hour, explanation = element_to_hours.get(min_element, (12, "오시 (정오)"))
    return estimated_hour, explanation

if __name__ == '__main__':
    sample = "93년 닭띠 음력 5월 12일 저녁 퇴근길에 태어났어요"
    parsed = parse_free_text_saju(sample)
    print("분석 결과:", parsed)
