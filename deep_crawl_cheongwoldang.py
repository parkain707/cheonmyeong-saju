# -*- coding: utf-8 -*-
import urllib.request
import re
import os
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 1. 청월당 API 및 데이터 구조 추적
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

api_candidates = [
    "https://cheongwoldang.com/api/products/mzshamantotal",
    "https://cheongwoldang.com/api/products/130",
    "https://cheongwoldang.com/api/pages/690",
    "https://cheongwoldang.com/api/products/130/preview",
    "https://cheongwoldang.com/api/b/mzshamantotal",
    "https://api.cheongwoldang.com/products/130",
    "https://api.cheongwoldang.com/pages/690"
]

print("=== 청월당 백엔드 API 후보 프로빙 ===")
for u in api_candidates:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode('utf-8', errors='ignore')
            print(f"✅ [SUCCESS] {u} -> Status {resp.status} ({len(body):,} bytes)")
            with open(f"api_{os.path.basename(u)}.json", "w", encoding="utf-8") as f:
                f.write(body)
    except urllib.error.HTTPError as e:
        print(f"❌ [HTTP {e.code}] {u}")
    except Exception as e:
        print(f"⚠️ [ERR] {u}: {e}")

# 2. 27zpvgk82zhdg.js 번들에서 FreeView 및 페이지 렌더링 로직 정밀 분석
chunk_path = "chunk_27zpvgk82zhdg.js"
if not os.path.exists(chunk_path):
    print("다운로드 중: 27zpvgk82zhdg.js...")
    req = urllib.request.Request("https://cheongwoldang.com/_next/static/immutable/chunks/27zpvgk82zhdg.js", headers=headers)
    with urllib.request.urlopen(req) as resp:
        with open(chunk_path, "wb") as f:
            f.write(resp.read())

with open(chunk_path, "r", encoding="utf-8", errors="ignore") as f:
    js_content = f.read()

print(f"\n번들 파일 크기: {len(js_content):,} bytes")

# FreeView 컴포넌트 위치 찾기
pos_freeview = js_content.find("FreeView")
print("FreeView 키워드 위치:", pos_freeview)
if pos_freeview != -1:
    snippet = js_content[max(0, pos_freeview - 500):min(len(js_content), pos_freeview + 1500)]
    print("\n--- FreeView 스니펫 ---")
    print(snippet[:600])

# mzshamantotal 또는 sia 관련 함수/데이터 탐색
pos_shaman = js_content.find("mzshamantotal")
print("\nmzshamantotal 키워드 위치:", pos_shaman)

# 챕터/목차 구조 패턴 찾기 (예: chapter, title, subtitle, order, sections)
chapters = re.findall(r'(\{[^{}]*?"title"[^{}]*?"description"[^{}]*?\})', js_content)
print(f"발견된 title-description 오브젝트: {len(chapters)}개")
for c in chapters[:5]:
    print(" •", c[:150])

# MZ무당 시아 대화체 및 팩폭 스크립트 탐색
dialogues = re.findall(r'["\']([^"\']*(?:했잖아|했어|말해줄게|맞지|보이지|들어봐|팩폭|거든|알려줄게)[^"\']*)["\']', js_content)
print(f"\n발견된 무당 시아 특유 화법 문장: {len(dialogues)}개")
for d in dialogues[:20]:
    if len(d) > 8:
        print(" 🔮", d)
