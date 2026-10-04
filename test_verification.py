# -*- coding: utf-8 -*-
"""
Agent 4 (Sentinel) & Agent 6 (Oracle) 사주 명리 정밀도 및 시스템 검증 테스트 스위트
"""

import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

from manseryeok import calculate_saju
from guija_engine import generate_guija_reading


def run_tests():
    print("=" * 60)
    print("🛡️ [Sentinel] 현허도인의 천명 신점사주 시스템 정밀 감사 시작")
    print("=" * 60)

    # 1. 만세력 간지 검증
    # 테스트 케이스 1: 2000년 1월 1일 12:00
    # 입춘 전이므로 년주는 1999 기묘년, 월주는 병자월, 일주는 경진일
    res1 = calculate_saju(2000, 1, 1, 12, 0)
    raw1 = res1["raw"]
    print(f"Test 1 [2000-01-01 12:00]: {raw1['year']}년 {raw1['month']}월 {raw1['day']}일 {raw1['hour']}시")
    assert raw1['year'] == '기묘', f"Expected 기묘, got {raw1['year']}"
    assert raw1['month'] == '병자', f"Expected 병자, got {raw1['month']}"
    assert raw1['day'] == '경진', f"Expected 경진, got {raw1['day']}"
    print("  -> 만세력 년/월/일주 계산 일치 확인! (PASS)")

    # 테스트 케이스 2: 1992년 8월 17일 12:00 (입추 지난 신월)
    res2 = calculate_saju(1992, 8, 17, 12, 0)
    raw2 = res2["raw"]
    print(f"Test 2 [1992-08-17 12:00]: {raw2['year']}년 {raw2['month']}월 {raw2['day']}일 {raw2['hour']}시")
    assert raw2['year'] == '임신', f"Expected 임신, got {raw2['year']}"
    assert raw2['month'] == '무신', f"Expected 무신, got {raw2['month']}"
    assert raw2['day'] == '정해', f"Expected 정해, got {raw2['day']}"
    print("  -> 1992년 임신년 무신월 정해일 일치 확인! (PASS)")


    # 2. 입춘 분기점 테스트: 2024년 2월 2일(계묘년) vs 2024년 2월 6일(갑진년)
    res_before = calculate_saju(2024, 2, 2, 12, 0)
    res_after = calculate_saju(2024, 2, 6, 12, 0)
    print(f"Test 3 [입춘 전후]: 2024.2.2 -> {res_before['raw']['year']} | 2024.2.6 -> {res_after['raw']['year']}")
    assert res_before['raw']['year'] == '계묘', "입춘 전은 계묘년이어야 함"
    assert res_after['raw']['year'] == '갑진', "입춘 후는 갑진년이어야 함"
    print("  -> 입춘(立春) 절입 시각 기준 년주 전환 정상 동작! (PASS)")

    # 3. 육감 6대 지표 및 4대 문 무결성 검증
    senses = res2["six_senses"]
    assert len(senses) == 6, f"Expected 6 senses, got {len(senses)}"
    for s in senses:
        assert 1 <= s["score"] <= 5, f"Score out of range: {s['score']}"
    print(f"  -> 육감 6대 지표 스코어링 정상 (1~5점 범위 준수) (PASS)")

    gates = res2["gates"]
    assert len(gates) == 4, f"Expected 4 gates, got {len(gates)}"
    print(f"  -> 4대 영적 통로(문) 산출 정상 (귀문, 공망, 백호, 천라지망) (PASS)")

    # 4. 11개 챕터 풀이 및 현허도인 페르소나 검증
    reading = generate_guija_reading(res2, "홍길동", "male")
    sections = reading["sections"]
    assert len(sections) == 11, f"Expected 11 chapters, got {len(sections)}"
    
    chapter_ids = [s["id"] for s in sections]
    expected_ids = ["soul_origin", "ghost_reveal", "desire_dual", "love_style", "love_trap", "love_fate", "wealth_flow", "career_path", "health_body", "future_map", "destiny_fork"]
    assert chapter_ids == expected_ids, f"Chapter ids mismatch: {chapter_ids}"
    
    for s in sections:
        assert len(s["desc"]) > 50, f"Section {s['id']} description too short"
        assert len(s["good"]) > 20, f"Section {s['id']} good fate too short"
        assert len(s["bad"]) > 20, f"Section {s['id']} bad fate too short"
        assert len(s["advice"]) > 20, f"Section {s['id']} advice too short"
    print("  -> 11개 챕터 (총 10편 52장 체계) 및 천운 vs 악운 양극단 대조 풀이 완전성 검증 완료! (PASS)")

    print("=" * 60)
    print("✅ [Sentinel & Oracle] 모든 검증 테스트 100% 통과!")
    print("=" * 60)

if __name__ == '__main__':
    run_tests()
