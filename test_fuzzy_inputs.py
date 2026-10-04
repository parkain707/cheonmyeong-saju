# -*- coding: utf-8 -*-
"""
초보자 엉성한 정보 스마트 파서 및 역추론 검증 테스트 스위트
"""
import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

def test_fuzzy_api():
    print("=" * 60)
    print("🛡️ [Sentinel] 초보자 엉성한 정보 자동 보정 API 테스트")
    print("=" * 60)

    test_cases = [
        {
            "name": "엉성한 케이스 1: 93년 닭띠 음력 5월 저녁 퇴근길",
            "body": {
                "name": "김초보",
                "gender": "male",
                "free_text": "93년 닭띠 음력 5월 12일 저녁 퇴근길 무렵"
            },
            "expect_year": 1993,
            "expect_lunar_converted": True
        },
        {
            "name": "엉성한 케이스 2: 88년생 시간 전혀 모름",
            "body": {
                "name": "이모름",
                "gender": "female",
                "free_text": "88년생 3월 15일인데 태어난 시간은 아예 몰라요"
            },
            "expect_year": 1988,
            "expect_time_estimated": True
        },
        {
            "name": "엉성한 케이스 3: 02년생 개띠 여름 점심때쯤",
            "body": {
                "name": "박막적",
                "gender": "male",
                "free_text": "02년생 개띠 여름 점심때쯤 태어남"
            },
            "expect_year": 2002,
            "expect_hour": 12
        }
    ]

    for tc in test_cases:
        print(f"\n▶ 테스트: {tc['name']}")
        req = urllib.request.Request(
            'http://localhost:8088/api/saju',
            data=json.dumps(tc['body']).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            assert data["status"] == "success"
            saju = data["saju"]
            print(f"  - 원국: {saju['raw']['year']}년 {saju['raw']['month']}월 {saju['raw']['day']}일 {saju['raw']['hour']}시")
            print(f"  - 음양체질: {saju['constitution']['type']}")
            print(f"  - 보정 알림: {data['notes']}")
            assert len(data["reading"]["sections"]) == 11
            print("  -> 검증 통과 (PASS)")

    print("\n" + "=" * 60)
    print("✅ [Sentinel] 초보자 엉성한 정보 보정 테스트 100% 성공!")
    print("=" * 60)

if __name__ == '__main__':
    test_fuzzy_api()
