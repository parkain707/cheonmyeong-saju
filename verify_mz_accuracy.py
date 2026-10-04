# -*- coding: utf-8 -*-
import urllib.request
import json
import sys

test_cases = [
    {
        'desc': '1993-08-17 18:00 남성 (경오일주)',
        'payload': {'year': 1993, 'month': 8, 'day': 17, 'hour': 18, 'gender': 'male', 'name': '김철수', 'concern': 'career'}
    },
    {
        'desc': '1995-10-24 14:30 여성 (무자일주)',
        'payload': {'year': 1995, 'month': 10, 'day': 24, 'hour': 14, 'gender': 'female', 'name': '이영희', 'concern': 'love'}
    },
    {
        'desc': '자연어: 1990년 5월 21일 오후 2시 30분 남자',
        'payload': {'free_text': '1990년 5월 21일 오후 2시 30분 남자', 'name': '박도윤', 'concern': 'wealth'}
    }
]

for idx, tc in enumerate(test_cases, 1):
    req = urllib.request.Request(
        'http://localhost:8088/api/saju',
        data=json.dumps(tc['payload']).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        if resp.status != 200:
            print(f"[FAIL] HTTP Status {resp.status}")
            sys.exit(1)
        body = json.loads(resp.read().decode('utf-8'))
        if body['status'] != 'success':
            print(f"[FAIL] Response status not success")
            sys.exit(1)

        saju = body['saju']
        mz = body['mz_insight']

        assert 'strength' in saju
        assert 'yongsin' in saju
        assert 'daeun' in saju
        assert 'persona' in mz
        assert 'attachment' in mz
        assert 'career' in mz
        assert 'wealth' in mz
        assert 'viral_share_text' in mz

        print(f"[{idx}/3 PASS] {tc['desc']}")
        print(f"   -> 일주: {saju['raw']['day']} | 신강약: {saju['strength']['type']}({saju['strength']['total_score']}점)")
        print(f"   -> 용신: {saju['yongsin']['title']} {saju['yongsin']['main']} | 황금기: {saju['daeun']['golden_age_str']}")
        print(f"   -> MZ본캐: {mz['persona']['title']}")
        print(f"   -> 애착: {mz['attachment']['style']} | 번아웃: {mz['career']['burnout_score']}%")

print("=== ALL SENTINEL VERIFICATION TESTS PASSED (100% SUCCESS) ===")
