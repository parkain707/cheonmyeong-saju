# -*- coding: utf-8 -*-
import urllib.request
import re
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# HTML에서 모든 Next.js 청크 JS URL 수집
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
req = urllib.request.Request("https://cheongwoldang.com/b/mzshamantotal", headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

chunk_urls = re.findall(r'/_next/static/immutable/chunks/[a-zA-Z0-9_\-\.]+\.js', html)
chunk_urls = sorted(list(set(chunk_urls)))
print(f"발견된 Next.js 청크 수: {len(chunk_urls)}개")

api_patterns = set()
auth_headers = []
found_routes = set()

for c_url in chunk_urls:
    full_url = f"https://cheongwoldang.com{c_url}"
    fname = os.path.basename(c_url)
    try:
        r = urllib.request.Request(full_url, headers=headers)
        with urllib.request.urlopen(r) as res:
            text = res.read().decode('utf-8', errors='ignore')
            
            # API 관련 URL 및 설정 탐색
            if "api.cheongwoldang.com" in text or "NEXT_PUBLIC" in text:
                print(f"⭐ [핵심 청크 발견] {fname} ({len(text):,} bytes)")
                
            # axios / fetch 헤더, authorization 탐색
            matches = re.findall(r'["\'](Bearer [^"\']+|Authorization|x-[a-zA-Z\-]+)["\']', text)
            if matches:
                auth_headers.extend(matches)
                
            # /api/ 또는 v1, v2 엔드포인트
            endpoints = re.findall(r'["\'`](/(?:api|v[0-9]|auth|products|pages|orders|user)[a-zA-Z0-9_\-\?\/]+)["\'`]', text)
            for ep in endpoints:
                if not ep.endswith('.js') and not ep.endswith('.css'):
                    found_routes.add(ep)
                    
            # 텍스트 내 API 호스트 정의
            hosts = re.findall(r'https?://[a-zA-Z0-9\-\.]*(?:cheongwoldang|rocketai|aifortunedoctor)[a-zA-Z0-9\-\.\:/]*', text)
            for h in hosts:
                api_patterns.add(h)
    except Exception as e:
        print(f"Error {fname}: {e}")

print("\n=== 발견된 API 베이스 호스트 ===")
for h in sorted(api_patterns):
    print(" •", h)

print("\n=== 발견된 헤더 패턴 ===")
for ah in set(auth_headers)[:15]:
    print(" •", ah)

print("\n=== 발견된 내부 라우트/엔드포인트 ===")
for r in sorted(found_routes)[:40]:
    print(" •", r)
