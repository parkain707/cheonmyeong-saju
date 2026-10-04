# -*- coding: utf-8 -*-
import urllib.request
import re
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# HTML에서 모든 청크 스크립트 태그 추출
req = urllib.request.Request("https://cheongwoldang.com/b/mzshamantotal", headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

all_chunks = re.findall(r'/_next/static/immutable/chunks/([a-zA-Z0-9_\-\.]+\.js)', html)
all_chunks = sorted(list(set(all_chunks)))

print(f"총 {len(all_chunks)}개 청크 정밀 스캔 시작...")

queries = set()
api_calls = []

for c in all_chunks:
    url = f"https://cheongwoldang.com/_next/static/immutable/chunks/{c}"
    try:
        r = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(r) as res:
            text = res.read().decode('utf-8', errors='ignore')
            
            # queryKey 검색
            qkeys = re.findall(r'queryKey:\s*\[([^\]]+)\]', text)
            for qk in qkeys:
                queries.add(qk.strip())
                
            # axios.get / fetch / post 호출 패턴 검색
            calls = re.findall(r'(?:get|post|put|delete)\s*\(\s*[`"\']([^`"\']*(?:/|api|products|order)[^`"\']*)[`"\']', text)
            for call in calls:
                if len(call) < 100:
                    api_calls.append((c, call))
                    
    except Exception as e:
        pass

print("\n=== 발견된 React Query queryKeys ===")
for q in sorted(queries):
    print(" 🔑", q)

print("\n=== 발견된 API 호출 경로 ===")
for c, call in set(api_calls):
    print(f" 📡 [{c}] -> {call}")
