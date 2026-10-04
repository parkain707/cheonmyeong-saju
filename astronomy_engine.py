# -*- coding: utf-8 -*-
"""
天命明鏡 (천명명경) | 칼 융의 공시성(Synchronicity) 천문 연산 코어 엔진
- 접속 순간(찰나)의 정확한 12시진(時辰)과 8각(刻) 계산
- 실시간 달의 위상(Lunar Phase: 삭·초승·상현·만월·하현·그믐) 정밀 연산
- 현재 찰나의 우주적 천간지지(년·월·일·시 4주 8자) 실시간 동기화
- 방문자가 문을 두드린 순간의 '천문학적 공시성 서두' 생성
"""

import math
from datetime import datetime
from manseryeok import calculate_saju

# 12시진 명칭 및 영적 의미
SHIJIN_INFO = {
    "자": ("자시 (子時)", "23:30~01:29", "하늘이 비로소 열리는 천개우자(天開於子)의 심야"),
    "축": ("축시 (丑時)", "01:30~03:29", "대지가 침묵 속에 굳어지는 지벽어축(地闢於丑)의 고요"),
    "인": ("인시 (寅時)", "03:30~05:29", "만물이 잠에서 깨어나 생명이 약동하는 인생어인(人生於寅)의 여명"),
    "묘": ("묘시 (卯時)", "05:30~07:29", "동방의 붉은 태양이 솟구치며 새 날이 밝아오는 아침"),
    "진": ("진시 (辰時)", "07:30~09:29", "청룡이 구름을 헤치며 승천을 준비하는 활기의 시간"),
    "사": ("사시 (巳時)", "09:30~11:29", "대지의 만물이 왕성하게 기운을 뿜어내는 정오의 문턱"),
    "오": ("오시 (午時)", "11:30~13:29", "태양이 중천에 우뚝 솟아 양기(陽氣)가 극에 달하는 대낮"),
    "미": ("미시 (未時)", "13:30~15:29", "한낮의 뜨거운 열기가 서서히 대지에 스며드는 완숙의 시간"),
    "신": ("신시 (申時)", "15:30~17:29", "석양이 서산으로 기울며 그림자가 길어지는 황혼의 문턱"),
    "유": ("유시 (酉時)", "17:30~19:29", "어둠이 내리고 촛불을 밝히며 영혼을 정화하는 저녁"),
    "술": ("술시 (戌時)", "19:30~21:29", "세상의 소음이 잦아들고 안식의 문을 닫는 밤"),
    "해": ("해시 (亥時)", "21:30~23:29", "만물이 깊은 명상과 영적 평온에 빠져드는 심야")
}

def get_current_shijin(hour, minute):
    """현재 시/분에 따른 12시진 및 각(刻) 계산"""
    total_minutes = hour * 60 + minute
    # 자시는 23:30부터 다음날 01:29까지
    adjusted = (total_minutes + 30) % 1440
    shijin_index = adjusted // 120
    shijin_keys = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]
    key = shijin_keys[shijin_index]
    
    # 15분 단위 1각 (총 8각)
    minute_in_shijin = adjusted % 120
    gak = (minute_in_shijin // 15) + 1
    gak_name = f"{gak}각(刻)"
    
    info = SHIJIN_INFO[key]
    return {
        "key": key,
        "name": info[0],
        "range": info[1],
        "meaning": info[2],
        "gak": gak_name
    }

def calculate_lunar_phase(target_dt=None):
    """
    천문학적 달의 위상(Lunar Phase) 정밀 연산
    신월(기준일: 2000-01-06 18:14 UTC) 기준 삭망월 주기(29.53058867일) 계산
    """
    if target_dt is None:
        target_dt = datetime.now()

    # 줄리안 데이(Julian Date) 계산
    year = target_dt.year
    month = target_dt.month
    day = target_dt.day + (target_dt.hour + target_dt.minute / 60.0) / 24.0

    if month <= 2:
        year -= 1
        month += 12

    A = year // 100
    B = 2 - A + (A // 4)
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5

    # 2000년 1월 6일 신월 JD = 2451549.5
    days_since_new = jd - 2451549.5
    synodic_month = 29.53058867
    moon_age = days_since_new % synodic_month

    if moon_age < 1.8:
        phase_title = "삭(朔) - 어둠 속에서 새로운 씨앗을 품은 흑월(黑月)"
        phase_desc = "하늘의 달이 빛을 감추고 깊은 자궁 속에서 새로운 천지의 기운을 잉태하는 시간"
        phase_energy = "내면의 정화와 새로운 결단의 씨앗을 심기에 가장 엄정한 천기"
    elif moon_age < 6.5:
        phase_title = "초승달(新月) - 은빛 칼날처럼 차오르는 희망의 삭달"
        phase_desc = "어둠을 가르고 여린 은빛 손톱눈을 틔우며 힘차게 솟구쳐 오르는 기운"
        phase_energy = "새로운 길을 개척하고 판을 박차고 나아갈 때 하늘의 추동력을 받는 천기"
    elif moon_age < 10.0:
        phase_title = "상현달(上弦月) - 빛과 어둠이 완벽한 균형을 이루는 도약의 달"
        phase_desc = "반쪽의 빛이 차오르며 주저함을 단칼에 베어내고 전진하는 기운"
        phase_energy = "우유부단함을 끝내고 칼자루를 단단히 쥐어야 할 결단의 천기"
    elif moon_age < 14.0:
        phase_title = "차오르는 달(盈月) - 만월의 충만을 향해 팽창하는 번영의 달"
        phase_desc = "밤하늘을 풍요로운 금빛으로 채워가며 소망을 무르익히는 기운"
        phase_energy = "뿌려둔 씨앗이 싹을 틔워 억대 곳간으로 결실을 맺어가는 번영의 천기"
    elif moon_age < 16.5:
        phase_title = "만월(滿月) - 온 세상을 대낮처럼 환히 비추는 충만의 보름달"
        phase_desc = "음기가 극에 달해 모든 비밀과 가려진 진실이 거울처럼 낱낱이 드러나는 시간"
        phase_energy = "가식과 거짓이 벗겨지고 순수한 그대의 천명이 가장 눈부시게 폭발하는 천기"
    elif moon_age < 21.0:
        phase_title = "하현달(下弦月) - 결실을 거두고 칼날을 갈무리하는 성찰의 달"
        phase_desc = "차오른 열기를 차분히 가라앉히고 진짜와 가짜를 분별하는 시간"
        phase_energy = "썩은 인연을 미련 없이 정리하고 내실을 단단히 다져야 할 천기"
    elif moon_age < 26.0:
        phase_title = "그믐달(殘月) - 심해의 깊은 지혜로 침잠하는 정화의 달"
        phase_desc = "한 주기를 마무리하며 영혼의 먼지를 털어내고 고요히 때를 기다리는 시간"
        phase_energy = "조급증을 내려놓고 마음의 호수를 맑게 닦아 신탁을 기다리는 천기"
    else:
        phase_title = "회(晦) - 묵은 액운을 다 태우고 새벽을 준비하는 침묵"
        phase_desc = "가장 짙은 어둠 속에서 비로소 다음 새벽의 첫 불씨가 피어오르는 시간"
        phase_energy = "낡은 껍질을 완전히 벗어던지고 환골탈태를 완성하는 정화의 천기"

    return {
        "age": round(moon_age, 1),
        "title": phase_title,
        "desc": phase_desc,
        "energy": phase_energy
    }

def get_synchronicity_moment(target_dt=None):
    """
    현재 접속 찰나의 공시성(천문 간지 + 시진각 + 달의 위상) 종합 도출
    """
    if target_dt is None:
        target_dt = datetime.now()

    # 1. 찰나의 12시진 및 각
    shijin = get_current_shijin(target_dt.hour, target_dt.minute)
    
    # 2. 실시간 달의 위상
    lunar = calculate_lunar_phase(target_dt)
    
    # 3. 실시간 천간지지 4주 8자 (현재 시점 만세력)
    curr_saju = calculate_saju(target_dt.year, target_dt.month, target_dt.day, target_dt.hour, target_dt.minute)
    curr_pillars = curr_saju["raw"]
    
    moment_str = target_dt.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    
    # 4. 찰나의 천문 공시성 시적 서두
    synchronicity_speech = (
        f"천지간에 **{curr_pillars['year']}년 {curr_pillars['month']}월 {curr_pillars['day']}일 {curr_pillars['hour']}시**의 천기가 서리고, "
        f"하늘에는 **{lunar['title']}**이 걸려 있는 찰나이오. "
        f"{shijin['meaning']} 속에서, 그대는 마침내 때가 이르러 **{shijin['name']} {shijin['gak']}**에 이 도인의 문을 두드렸구려. "
        f"이것은 우연이 아니오. 칼 융이 말한 우주적 공시성(Synchronicity)이자, 천지신명이 그대의 발걸음을 필연으로 이끈 바로 그 순간이오."
    )

    return {
        "moment_timestamp": moment_str,
        "shijin": shijin,
        "lunar": lunar,
        "current_pillars": curr_pillars,
        "synchronicity_speech": synchronicity_speech
    }

if __name__ == '__main__':
    res = get_synchronicity_moment()
    print("=== 칼 융의 공시성 실시간 천문 연산 결과 ===")
    print("접속 시각:", res["moment_timestamp"])
    print("달의 위상:", res["lunar"]["title"])
    print("시진각:", res["shijin"]["name"], res["shijin"]["gak"])
    print("현재 만세력:", res["current_pillars"])
    print("\n[공시성 천문 서두]")
    print(res["synchronicity_speech"])
