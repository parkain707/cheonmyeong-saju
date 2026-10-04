# -*- coding: utf-8 -*-
import urllib.request
import json

payload = {
    "year": 1993,
    "month": 8,
    "day": 17,
    "hour": 18,
    "gender": "male",
    "concern": "career",
    "obanggi": "청",
    "prev_visit": {
        "timestamp": "2026년 9월 28일",
        "concern": "career",
        "obanggi": "황"
    }
}

req = urllib.request.Request(
    'http://localhost:8088/api/saju',
    data=json.dumps(payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    print("Status:", data.get("status"))
    sv = data.get("spirit_vision", {})
    zw = data.get("ziwei", {})
    
    print("\n--- [1] Zi Wei Dou Shu Verification ---")
    print("Has Ziwei Data:", bool(zw))
    print("Bureau:", zw.get("bureau", {}).get("name"))
    print("Ming Palace:", zw.get("ming_palace", {}).get("ji_hanja"), "Stars:", [s["name"] for s in zw.get("ming_palace", {}).get("stars", [])])
    print("Sihua Hua-Yi (화기):", zw.get("sihua", {}).get("기", {}).get("star"), "->", zw.get("sihua", {}).get("기", {}).get("palace"))
    
    print("\n--- [2] Shamanic Speech Ziwei Integration ---")
    speech = sv.get("shamanic_speech", "")
    has_ziwei_in_speech = ("자미두수" in speech) or ("명궁" in speech)
    print("Ziwei in Shamanic Speech:", has_ziwei_in_speech)
    print("Speech snippet mentioning Ziwei:")
    for line in speech.split("\n"):
        if "자미두수" in line or "명궁" in line or "화기" in line:
            print("  >", line[:100])
            
    assert bool(zw), "FAIL: ziwei 데이터 누락"
    assert has_ziwei_in_speech, "FAIL: 신점 공수에 자미두수 결합 누락"
    print("\n[ALL PASS] Server Zi Wei Dou Shu HTTP Integration Verified 100%!")
