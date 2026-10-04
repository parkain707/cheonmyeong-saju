# -*- coding: utf-8 -*-
"""
Pillar 1~3 통합 검증 테스트
- 공시성 엔진 (Synchronicity)
- 영혼 지속성 기억 (Soul Memory / Reunion)
- 무의식 그림자 투시 (Shadow Archetype)
"""
from manseryeok import calculate_saju
from spirit_engine import analyze_shamanic_vision

def test_first_visit():
    """첫 방문: 공시성 + 그림자가 출력되고, reunion은 False"""
    saju = calculate_saju(1993, 8, 17, 18, 0)
    result = analyze_shamanic_vision(saju, "청", "career", "홍길동")
    
    assert "synchronicity" in result, "FAIL: synchronicity 필드 누락"
    assert "unconscious_shadow" in result, "FAIL: unconscious_shadow 필드 누락"
    assert result["is_reunion"] == False, "FAIL: 첫 방문인데 is_reunion=True"
    
    sync = result["synchronicity"]
    assert "shijin" in sync and "name" in sync["shijin"], f"FAIL: shijin.name 누락. keys={list(sync.keys())}"
    assert "lunar" in sync and "title" in sync["lunar"], f"FAIL: lunar.title 누락"
    assert "synchronicity_speech" in sync, f"FAIL: synchronicity_speech 누락"
    assert len(sync["synchronicity_speech"]) > 20, f"FAIL: 공시성 공수가 너무 짧음: {sync['synchronicity_speech'][:50]}"
    
    shadow = result["unconscious_shadow"]
    assert "type" in shadow, "FAIL: shadow type 누락"
    assert "insight" in shadow, "FAIL: shadow insight 누락"
    assert len(shadow["insight"]) > 30, f"FAIL: 그림자 통찰이 너무 짧음"
    
    # shamanic_speech에 공시성 문구 포함 확인
    speech = result["shamanic_speech"]
    assert sync["shijin"]["name"] in speech or "시" in speech or "현허도인" in speech, \
        f"FAIL: 공시성이 shamanic_speech에 미반영"
    assert shadow["type"] in speech, f"FAIL: 그림자 유형이 shamanic_speech에 미반영"
    
    print(f"  [OK] 첫 방문 테스트 통과")
    print(f"    - 공시성: {sync['shijin']['name']} / 달: {sync['lunar']['title']}")
    print(f"    - 그림자: {shadow['type']}")
    print(f"    - reunion: {result['is_reunion']}")
    return True

def test_reunion_visit():
    """재방문: reunion_prefix가 shamanic_speech에 포함"""
    saju = calculate_saju(1985, 5, 22, 10, 0)
    prev = {
        "timestamp": "2026년 9월 28일",
        "concern": "career",
        "obanggi": "청"
    }
    result = analyze_shamanic_vision(saju, "적", "wealth", "김철수", prev_visit=prev)
    
    assert result["is_reunion"] == True, "FAIL: 재방문인데 is_reunion=False"
    speech = result["shamanic_speech"]
    assert "그대구려" in speech, f"FAIL: 재방문 인사 '그대구려' 미포함"
    assert "9월 28일" in speech, f"FAIL: 이전 방문 날짜 미반영"
    assert "직업과 이직의 절벽" in speech, f"FAIL: 이전 고민 영역 미반영"
    assert "청" in speech, f"FAIL: 이전 오방기 미반영"
    
    print(f"  [OK] 재방문 테스트 통과")
    print(f"    - is_reunion: {result['is_reunion']}")
    print(f"    - 재방문 인사 포함: 확인")
    return True

def test_different_shadows():
    """서로 다른 사주는 다른 그림자 유형을 생성하는 경우가 있어야 함"""
    test_cases = [
        (1993, 8, 17, 18, 0, "청", "career", "A"),
        (1982, 3, 10, 8, 30, "적", "wealth", "B"),
        (1975, 12, 3, 2, 0, "황", "love", "C"),
        (2000, 1, 15, 14, 0, "백", "timing", "D"),
        (1968, 7, 7, 22, 0, "흑", "career", "E"),
    ]
    shadows = []
    for y, m, d, h, mi, o, c, label in test_cases:
        saju = calculate_saju(y, m, d, h, mi)
        result = analyze_shamanic_vision(saju, o, c, f"테스트{label}")
        shadows.append(result["unconscious_shadow"]["type"])
        print(f"    {label}: {result['unconscious_shadow']['type']}")
    
    unique_count = len(set(shadows))
    print(f"  [OK] 그림자 다양성: {unique_count}/{len(shadows)} 유형 분화")
    assert unique_count >= 2, f"FAIL: 모든 사주가 동일한 그림자 유형 ({shadows[0]})"
    return True

def test_speech_contains_all_elements():
    """공수 전문에 모든 핵심 요소가 포함되는지 검증"""
    saju = calculate_saju(1990, 6, 15, 6, 0)
    result = analyze_shamanic_vision(saju, "황", "love", "박영희")
    speech = result["shamanic_speech"]
    
    checks = {
        "신체 통증": result["body_pain"] in speech,
        "과거 환란": result["recent_shock"] in speech,
        "비밀 속마음": result["secret_mind"] in speech,
        "수호 영체": result["spirit_name"] in speech,
        "오방기 신탁": result["obanggi"]["oracle"] in speech,
        "그림자 유형": result["unconscious_shadow"]["type"] in speech,
        "그림자 통찰": result["unconscious_shadow"]["insight"] in speech,
    }
    
    all_pass = True
    for name, ok in checks.items():
        status = "OK" if ok else "FAIL"
        if not ok:
            all_pass = False
        print(f"    [{status}] {name}")
    
    assert all_pass, "FAIL: 일부 요소가 공수에 미포함"
    print(f"  [OK] 공수 전문 완전성 검증 통과")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("天命明鏡 | Pillar 1~3 통합 검증")
    print("=" * 60)
    
    tests = [
        ("1. 첫 방문 (공시성+그림자)", test_first_visit),
        ("2. 재방문 (영혼 지속성 기억)", test_reunion_visit),
        ("3. 그림자 다양성 분화", test_different_shadows),
        ("4. 공수 전문 완전성", test_speech_contains_all_elements),
    ]
    
    passed = 0
    failed = 0
    for title, func in tests:
        print(f"\n[TEST] {title}")
        try:
            func()
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {e}")
            failed += 1
    
    print(f"\n{'=' * 60}")
    print(f"결과: {passed} passed / {failed} failed")
    print(f"{'=' * 60}")
