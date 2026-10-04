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
    print("Is Reunion:", sv.get("is_reunion"))
    print("Has Synchronicity:", "synchronicity" in sv)
    print("Has Unconscious Shadow:", "unconscious_shadow" in sv)
    print("Shadow Type:", sv.get("unconscious_shadow", {}).get("type"))
    print("\n--- Speech Intro ---")
    print(sv.get("shamanic_speech", "")[:300])
