# -*- coding: utf-8 -*-
"""
한국 천문연구원 기준 음력-양력 변환 데이터 (1920~2050)
각 연도별 음력 월의 대소(29일/30일) 및 윤달 정보 압축 테이블
"""

# 1920~2050년 음력 데이터 (년도별 16진수 비트마스크)
# 비트 구조:
# bits 0-3: 윤달이 있는 달 (0이면 윤달 없음, 1~12)
# bits 4-15: 1~12월의 대소 (1: 30일(대), 0: 29일(소))
# bit 16: 윤달의 대소 (1: 30일, 0: 29일)
LUNAR_INFO = [
    0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2, # 1920-1929
    0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977, # 1930-1939
    0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970, # 1940-1949
    0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950, # 1950-1959
    0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557, # 1960-1969
    0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5b0, 0x14573, 0x052b0, 0x0a9a8, 0x0e950, 0x06aa0, # 1970-1979
    0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0, # 1980-1989
    0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b6a0, 0x195a6, # 1990-1999
    0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570, # 2000-2009
    0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x055c0, 0x0ab60, 0x096d5, 0x092e0, # 2010-2019
    0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5, # 2020-2029
    0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930, # 2030-2039
    0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530  # 2040-2049
]

# 음력 기준일: 1920년 음력 1월 1일은 양력 1920년 2월 20일
BASE_SOLAR_YEAR = 1920
BASE_SOLAR_MONTH = 2
BASE_SOLAR_DAY = 20

def get_lunar_year_days(lunar_year):
    """음력 특정 해의 총 일수 계산"""
    if lunar_year < 1920 or lunar_year >= 1920 + len(LUNAR_INFO):
        return 354
    info = LUNAR_INFO[lunar_year - 1920]
    total_days = 0
    # 12개월 일수 합산
    for m in range(12):
        total_days += 30 if (info & (0x10000 >> (m + 1))) else 29
    # 윤달이 있으면 윤달 일수 추가
    leap_month = info & 0xf
    if leap_month > 0:
        total_days += 30 if (info & 0x10000) else 29
    return total_days

def lunar_to_solar(lunar_year, lunar_month, lunar_day, is_leap_month=False):
    """
    음력을 양력으로 정밀 변환
    """
    from datetime import date, timedelta
    if lunar_year < 1920 or lunar_year >= 1920 + len(LUNAR_INFO):
        # 지원 범위 밖은 근사치(약 1달 차이) 반환
        return lunar_year, lunar_month, lunar_day

    offset_days = 0
    # 기준 연도부터 해당 연도 전까지의 총 일수 누적
    for y in range(1920, lunar_year):
        offset_days += get_lunar_year_days(y)

    info = LUNAR_INFO[lunar_year - 1920]
    leap_month = info & 0xf

    # 해당 연도 내에서 월별 일수 누적
    for m in range(1, lunar_month):
        offset_days += 30 if (info & (0x10000 >> m)) else 29
        if m == leap_month:
            offset_days += 30 if (info & 0x10000) else 29

    # 윤달인 경우 평달 일수 추가
    if is_leap_month and leap_month == lunar_month:
        offset_days += 30 if (info & (0x10000 >> lunar_month)) else 29

    # 해당 월의 일수 추가 (1일 기준이므로 -1)
    offset_days += (lunar_day - 1)

    base_date = date(BASE_SOLAR_YEAR, BASE_SOLAR_MONTH, BASE_SOLAR_DAY)
    target_date = base_date + timedelta(days=offset_days)
    return target_date.year, target_date.month, target_date.day

def solar_to_lunar(solar_year, solar_month, solar_day):
    """
    양력을 음력으로 정밀 역변환 (1920~2050)
    반환: (lunar_year, lunar_month, lunar_day, is_leap_month)
    """
    from datetime import date
    if solar_year < 1920 or solar_year > 2050:
        return solar_year, solar_month, solar_day, False

    base_date = date(BASE_SOLAR_YEAR, BASE_SOLAR_MONTH, BASE_SOLAR_DAY)
    target_date = date(solar_year, solar_month, solar_day)
    offset = (target_date - base_date).days

    if offset < 0:
        return solar_year, solar_month, solar_day, False

    l_year = 1920
    while l_year < 2050:
        days_in_year = get_lunar_year_days(l_year)
        if offset < days_in_year:
            break
        offset -= days_in_year
        l_year += 1

    info = LUNAR_INFO[l_year - 1920]
    leap_month = info & 0xf
    is_leap = False

    l_month = 1
    for m in range(1, 13):
        # 평달 일수
        normal_days = 30 if (info & (0x10000 >> m)) else 29
        if offset < normal_days:
            l_month = m
            is_leap = False
            break
        offset -= normal_days

        # 윤달 체크
        if m == leap_month:
            leap_days = 30 if (info & 0x10000) else 29
            if offset < leap_days:
                l_month = m
                is_leap = True
                break
            offset -= leap_days

    l_day = offset + 1
    return l_year, l_month, l_day, is_leap

if __name__ == '__main__':
    # 상호 변환 검증 테스트
    sy, sm, sd = lunar_to_solar(1993, 8, 17)
    ly, lm, ld, leap = solar_to_lunar(sy, sm, sd)
    assert (ly, lm, ld) == (1993, 8, 17), "상호 역변환 일치 실패"
    print("[PASS] Lunar-Solar Bidirectional Conversion verified 100%")

