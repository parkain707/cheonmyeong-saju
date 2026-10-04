# -*- coding: utf-8 -*-
import urllib.request
import re
import os
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

chunks = [
    '3bt1hfkxa4im5.js', '2j_gigp463a87.js', '37431m5d7_cha.js', '3w3onxr_0_22j.js',
    '02t1bni4wmkjp.js', '1ll133tjbi-ni.js', '27zpvgk82zhdg.js', '3ocdb3t93kqf_.js',
    '2apkllv2-thy3.js', '1c-3xa5zwy2mt.js', '0uk4_a-nmt_lf.js'
]

print("=== 청월당 번들 JS 분석 시작 ===")
all_endpoints = set()
shaman_keywords = []

for c in chunks:
    url = f"https://cheongwoldang.com/_next/static/immutable/chunks/{c}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req) as resp:
            text = resp.read().decode('utf-8', errors='ignore')
            print(f"[{c}] 다운로드 완료 ({len(text):,} bytes)")
            
            # API 엔드포인트 탐색
            endpoints = re.findall(r'["\'`](/(?:api|v[0-9]|b)/[a-zA-Z0-9_\-\?\/]+)["\'`]', text)
            for ep in endpoints:
                if not ep.endswith('.js') and not ep.endswith('.css'):
                    all_endpoints.add(ep)
            
            # 무당/시아/점사/사주 관련 핵심 키워드/문구 탐색
            matches = re.findall(r'["\']([^"\']*(?:무당|시아|팩폭|점사|신점|사주|신령|동자|방울|부적|도령|신내림|오방기|화기|칼|작두)[^"\']*)["\']', text)
            for m in matches[:15]:
                if len(m) > 4 and len(m) < 80:
                    shaman_keywords.append(m)
                    
    except Exception as e:
        print(f"[{c}] 실패: {e}")

print("\n=== 발견된 API 엔드포인트 ===")
for ep in sorted(all_endpoints):
    print(" -", ep)

print("\n=== 발견된 점사/무당 핵심 텍스트 및 UI 카피 ===")
for kw in set(shaman_keywords)[:30]:
    print(" •", kw)
