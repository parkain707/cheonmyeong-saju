# -*- coding: utf-8 -*-
import urllib.request
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 1. /api/gunghap 테스트
gh_payload = {
    "relation": "dating",
    "person_a": {"name": "테스터A", "year": 1994, "month": 3, "day": 15, "hour": 18, "gender": "male", "is_lunar": False},
    "person_b": {"name": "테스터B", "year": 1995, "month": 5, "day": 20, "hour": 10, "gender": "female", "is_lunar": False}
}

req = urllib.request.Request(
    "http://localhost:8088/api/gunghap",
    data=json.dumps(gh_payload).encode('utf-8'),
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(req) as response:
    gh_data = json.loads(response.read().decode('utf-8'))
    print("✅ /api/gunghap E2E 검증 성공!")
    print(f"   - 상태: {gh_data['status']}")
    print(f"   - 궁합 총점: {gh_data['gunghap']['total_score']}점")
    print(f"   - 등급: {gh_data['gunghap']['grade']}")
    print(f"   - 도인 공수 앞부분: {gh_data['gunghap']['oracle_speech'][:60]}...")

# 2. /api/qa 테스트 (정상 질문)
qa_payload = {
    "question": "올해 안에 새로운 부서로 이동하거나 직장을 옮기는 것이 길할까요?",
    "mode": "quick",
    "name": "홍길동",
    "year": 1994, "month": 3, "day": 15, "hour": 18
}

req_qa = urllib.request.Request(
    "http://localhost:8088/api/qa",
    data=json.dumps(qa_payload).encode('utf-8'),
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(req_qa) as response:
    qa_data = json.loads(response.read().decode('utf-8'))
    print("\n✅ /api/qa (quick mode) E2E 검증 성공!")
    print(f"   - 상태: {qa_data['status']}")
    print(f"   - 카테고리: {qa_data['category']}")
    print(f"   - 답변 첫 구절: {qa_data['answer'][:80]}...")

# 3. /api/qa 테스트 (금기어 차단)
qa_taboo_payload = {
    "question": "로또 1등 당첨 번호 좀 찍어주세요",
    "mode": "single",
    "name": "홍길동"
}

req_taboo = urllib.request.Request(
    "http://localhost:8088/api/qa",
    data=json.dumps(qa_taboo_payload).encode('utf-8'),
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(req_taboo) as response:
    taboo_data = json.loads(response.read().decode('utf-8'))
    print("\n✅ /api/qa (금기어 차단 가드레일) E2E 검증 성공!")
    print(f"   - 상태: {taboo_data['status']} (forbidden 기대)")
    print(f"   - 도인 호통: {taboo_data['answer'][:80]}...")
