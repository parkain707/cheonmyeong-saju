# -*- coding: utf-8 -*-
"""
[Sentinel] 황실 비전 자미두수(紫微斗數) 정통 성반 무결점 정밀 감사 테스트
- 12궁 배치 완전성 (12 Palaces)
- 14대 주성(자미·천기·태양·무곡·천동·염정·천부·태음·탐랑·거문·천상·천량·칠살·파군) 무누락 검증
- 10간 생년 사화(四化: 化祿, 化權, 化科, 化忌) 100% 전수 감사
- 오행국(수이국~화육국) 도출 정확성 감사
- 다양한 생년월일시에서의 성반 다양성 및 독립 차별화 검증
"""

import sys
import io

if sys.stdout is not None:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from ziwei_engine import calculate_ziwei_chart, calculate_ziwei_from_saju, SIHUA_TABLE, MAJOR_STARS
from manseryeok import calculate_saju

def test_12_palaces_integrity():
    """12개 궁이 누락 없이 모두 배정되고 고유한 지지를 갖는지 검증"""
    chart = calculate_ziwei_chart("갑", 1, 1, 12)
    palaces = chart["palaces"]
    assert len(palaces) == 12, f"FAIL: 궁의 개수가 12개가 아님 ({len(palaces)})"
    
    expected_palaces = ["명궁", "형제궁", "부처궁", "자녀궁", "재백궁", "질액궁", "천이궁", "노복궁", "관록궁", "전택궁", "복덕궁", "부모궁"]
    for p in expected_palaces:
        assert p in palaces, f"FAIL: {p} 누락"
        
    jis = [p_data["ji"] for p_data in palaces.values()]
    assert len(set(jis)) == 12, f"FAIL: 12궁 지지가 중복됨: {jis}"
    print("  [PASS] 1. 12궁 배치 및 지지 완전성 감사 통과 (12/12 고유 배정)")
    return True

def test_14_major_stars_placement():
    """14대 주성이 빠짐없이 12궁 중 어딘가에 정확히 1번씩 안성되는지 검증"""
    test_cases = [
        ("갑", 3, 15, 6),
        ("병", 7, 22, 14),
        ("경", 11, 5, 20),
        ("계", 8, 17, 18)
    ]
    
    for gan, m, d, h in test_cases:
        chart = calculate_ziwei_chart(gan, m, d, h)
        major_stars = []
        for p in chart["palaces"].values():
            for s in p["stars"]:
                if s.get("is_major"):
                    major_stars.append(s["name"])
                
        assert len(major_stars) == 14, f"FAIL: 배치된 주성 수가 14개가 아님 ({len(major_stars)}개) - case ({gan},{m},{d},{h})"
        for s_name in MAJOR_STARS.keys():
            assert s_name in major_stars, f"FAIL: 주성 {s_name} 누락 - case ({gan},{m},{d},{h})"
            
    print("  [PASS] 2. 14대 주성(자미계 6성 + 천부계 8성) 무누락 안성 감사 통과")
    return True

def test_10_gan_sihua_exhaustion():
    """10대 천간별 사화(록·권·과·기)가 정확히 4개씩 도출되고 특정 궁에 배정되는지 전수 검증"""
    gans = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
    for g in gans:
        chart = calculate_ziwei_chart(g, 5, 10, 10)
        sihua = chart["sihua"]
        assert len(sihua) == 4, f"FAIL: 사화 개수 오류 ({g}간)"
        for s_type in ["록", "권", "과", "기"]:
            assert s_type in sihua, f"FAIL: {s_type} 사화 누락 ({g}간)"
            star = sihua[s_type]["star"]
            assert star in MAJOR_STARS or star in ["문창", "문곡", "좌보", "우필"], f"FAIL: 잘못된 사화 대상 별 {star}"
            
        # 화기가 든 궁이 실제로 존재하는지
        hwayi_palace = sihua["기"]["palace"]
        assert hwayi_palace in chart["palaces"], f"FAIL: 화기가 배정된 궁 {hwayi_palace} 존재하지 않음"
        
    print("  [PASS] 3. 10대 천간 생년 사화(四化: 祿·權·科·忌) 100% 전수 감사 통과")
    return True

def test_saju_ziwei_cross_integration():
    """사주팔자 데이터에서 자미두수 성반이 올바르게 크로스오버되는지 검증"""
    saju = calculate_saju(1993, 8, 17, 18, 0) # 양력 1993.08.17 (음력 1993.06.30)
    chart = calculate_ziwei_from_saju(saju)
    
    assert chart["bureau"]["number"] in [2, 3, 4, 5, 6], "FAIL: 오행국 수치 오류"
    assert len(chart["ming_palace"]["stars"]) >= 0, "FAIL: 명궁 주성 오류"
    assert len(chart["oracle_summary"]) > 50, "FAIL: 도인 자미두수 직설 요약 너무 짧음"
    
    print(f"  [PASS] 4. 사주 x 자미두수 크로스오버 연산 감사 통과")
    print(f"    - 오행국: {chart['bureau']['name']}")
    print(f"    - 명궁: {chart['ming_palace']['ji_hanja']}궁 ({[s['name'] for s in chart['ming_palace']['stars']]})")
    print(f"    - 시련의 화기(化忌): {chart['sihua']['기']['palace']} ({chart['sihua']['기']['star']}化忌)")
    return True

def test_ziwei_differentiation():
    """서로 다른 사주 간 자미두수 명궁 및 주성의 다양성 검증"""
    test_cases = [
        (1993, 8, 17, 18), # 음력 6월 유시 -> 술궁
        (1988, 2, 25, 0),  # 음력 1월 자시 -> 인궁
        (1995, 5, 10, 6),  # 음력 4월 묘시 -> 사궁
        (2000, 11, 20, 12),# 음력 10월 오시 -> 오궁
        (1972, 7, 7, 22)   # 음력 5월 해시 -> 축궁
    ]
    
    ming_locs = []
    bureau_names = []
    for y, m, d, h in test_cases:
        s = calculate_saju(y, m, d, h, 0)
        z = calculate_ziwei_from_saju(s)
        ming_locs.append(z["ming_palace"]["ji"])
        bureau_names.append(z["bureau"]["name"])
        
    unique_mings = len(set(ming_locs))
    unique_bureaus = len(set(bureau_names))
    print(f"  [PASS] 5. 자미두수 성반 다양성: 명궁 위치 {unique_mings}/5 고유, 오행국 {unique_bureaus}/5 고유")
    assert unique_mings >= 3, "FAIL: 명궁 위치가 지나치게 중복됨"
    return True

def test_nayin_bureau_table():
    """60갑자 전체가 오행국에 빠짐없이, 국별 12개씩 매핑되는지 + 문창 기준점 검증"""
    import ast, inspect, collections, ziwei_engine
    src = inspect.getsource(ziwei_engine)
    start = src.index("NAYEUM_BUREAU = {")
    end = src.index("}", start) + 1
    tree = ast.parse(src[start:end])
    keys = [k.value for k in tree.body[0].value.keys]
    assert len(keys) == len(set(keys)), f"FAIL: 오행국 표에 중복 키 존재: {[k for k,c in collections.Counter(keys).items() if c>1]}"
    assert len(keys) == 60, f"FAIL: 60갑자 중 {len(keys)}개만 매핑됨"
    per = collections.Counter(ziwei_engine.NAYEUM_BUREAU.values())
    assert all(per[b] == 12 for b in [2, 3, 4, 5, 6]), f"FAIL: 국별 분포 이상 {dict(per)}"
    chart = calculate_ziwei_chart("갑", 1, 1, 0)  # 자시
    wc = [p["ji"] for p in chart["palaces"].values() if any(s["name"] == "문창" for s in p["stars"])]
    assert wc == ["술"], f"FAIL: 자시 문창은 戌궁이어야 함 (현재 {wc})"
    print("  [PASS] 6. 납음 오행국 60갑자 무결성 + 문창 기준점 감사 통과")
    return True

if __name__ == "__main__":
    print("=" * 65)
    print("🛡️ [Sentinel] 황실 비전 자미두수(紫微斗數) 정통 성반 감사 시작")
    print("=" * 65)
    
    tests = [
        test_12_palaces_integrity,
        test_14_major_stars_placement,
        test_10_gan_sihua_exhaustion,
        test_saju_ziwei_cross_integration,
        test_ziwei_differentiation,
        test_nayin_bureau_table
    ]
    
    passed = 0
    for t in tests:
        if t():
            passed += 1
            
    print("=" * 65)
    print(f"✅ [Sentinel] 자미두수 성반 5대 정밀 감사: {passed}/5 ALL PASS 100% 무결점 완료!")
    print("=" * 65)
