# -*- coding: utf-8 -*-
import re
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 27zpvgk82zhdg.js 집중 분석
chunk_name = "27zpvgk82zhdg.js"
url = f"https://cheongwoldang.com/_next/static/immutable/chunks/{chunk_name}"

import urllib.request
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    data = resp.read().decode('utf-8', errors='ignore')

print(f"27zpvgk82zhdg.js 크기: {len(data):,} bytes")

# 1. API 주소 및 백엔드 도메인 검색
domains = set(re.findall(r'https?://[a-zA-Z0-9\-\._]+(?:\.[a-zA-Z]{2,})[^\s"\'`<>]*', data))
print("\n=== 발견된 외부 URL / API 도메인 ===")
for d in sorted(domains):
    if any(k in d for k in ['cheong', 'fortune', 'api', 'rocket', 'backend', 'toss', 'mzshaman']):
        print(" •", d)

# 2. API 경로 패턴 (/api/..., /v1/..., /b/...)
api_paths = set(re.findall(r'["\'`](/(?:api|v[0-9]|b|products?|pages?|orders?|payments?)[a-zA-Z0-9_\-\?\/]+)["\'`]', data))
print("\n=== 발견된 API 엔드포인트 경로 ===")
for p in sorted(api_paths):
    print(" •", p)

# 3. MZ무당 시아 / 팩폭점사 / 질문 구조 검색
print("\n=== 점사/무당/질문지 관련 구조 검색 ===")
shaman_texts = re.findall(r'["\']([^"\']*(?:무당|시아|팩폭|점사|신점|사주|신령|동자|방울|부적|도령|신내림|오방기|화기|칼|작두)[^"\']*)["\']', data)
for txt in sorted(list(set(shaman_texts)))[:40]:
    if 5 < len(txt) < 80:
        print(" -", txt)

# 4. 결제/상품 가격 및 쿠폰 구조
print("\n=== 상품/가격/결제 관련 패턴 ===")
payment_patterns = re.findall(r'["\']([^"\']*(?:할인|원|결제|쿠폰|포인트|토스|주문|가격)[^"\']*)["\']', data)
for pp in sorted(list(set(payment_patterns)))[:30]:
    if 4 < len(pp) < 50:
        print(" $", pp)
