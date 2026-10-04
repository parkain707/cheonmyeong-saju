# -*- coding: utf-8 -*-
import urllib.request
import re
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

target_chunks = ["2ybeke5n-s44l.js", "319jkq75kdhw4.js"]

for c in target_chunks:
    url = f"https://cheongwoldang.com/_next/static/immutable/chunks/{c}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        text = resp.read().decode('utf-8', errors='ignore')
        print(f"\n=================== {c} 분석 ({len(text):,} bytes) ===================")
        with open(f"analyzed_{c}", "w", encoding="utf-8") as f:
            f.write(text)
            
        # API 경로 모두 추출
        routes = re.findall(r'["\'`](/(?:api|v[0-9]|b|order[0-9]?|product[s]?|page[s]?|auth|user|coupon)[a-zA-Z0-9_\-\?\/]+)["\'`]', text)
        print("발견된 API 라우트:")
        for r in sorted(list(set(routes))):
            print("  ->", r)
            
        # api.cheongwoldang.com 관련 호출 문맥
        matches = [m.start() for m in re.finditer(r'api\.cheongwoldang\.com', text)]
        for idx in matches:
            snippet = text[max(0, idx - 150):min(len(text), idx + 250)]
            print("\n[api.cheongwoldang.com 문맥 스니펫]:")
            print(snippet)
            print("-" * 50)
