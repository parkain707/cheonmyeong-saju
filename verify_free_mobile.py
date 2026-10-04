# -*- coding: utf-8 -*-
import urllib.request
import json
import sys

# 1. API 테스트 (100% 무료 전면 개방 검증)
payload = {'year': 1993, 'month': 8, 'day': 17, 'hour': 18, 'gender': 'male', 'name': '김철수'}
req = urllib.request.Request('http://localhost:8088/api/saju', data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    assert data['status'] == 'success'
    assert data['is_unlocked'] == True
    sections = data['reading']['sections']
    assert len(sections) == 11, f'Sections count: {len(sections)}'
    for idx, sec in enumerate(sections, 1):
        assert sec['is_locked'] == False, f'Chapter {idx} is locked!'
    print(f"[PASS] 11개 챕터 전편 100% 무료 완전 개방 확인! (총 {len(sections)}개 장 모두 잠금 해제)")

# 2. PWA manifest.json 서빙 확인
with urllib.request.urlopen('http://localhost:8088/manifest.json') as resp:
    assert resp.status == 200
    manifest = json.loads(resp.read().decode('utf-8'))
    name = manifest['short_name']
    print(f"[PASS] PWA manifest.json 서빙 정상 확인: {name}")

# 3. PWA sw.js 서빙 확인
with urllib.request.urlopen('http://localhost:8088/sw.js') as resp:
    assert resp.status == 200
    sw_code = resp.read().decode('utf-8')
    assert 'cheonmyeong-cache' in sw_code
    print("[PASS] PWA Service Worker (sw.js) 서빙 정상 확인")

print("=== 100% 무료 배포 & 모바일 초최적화 검증 100% 완벽 통과 ===")
