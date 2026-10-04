# -*- coding: utf-8 -*-
import urllib.request
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://cheongwoldang.com/b/mzshamantotal',
    'Origin': 'https://cheongwoldang.com',
    'Accept': 'application/json, text/plain, */*'
}

print("=== 청월당 페이지 ID 연속 스캔 (730 ~ 750, 690 ~ 710) ===")
found_pages = []

for pid in list(range(730, 755)) + list(range(690, 705)):
    url = f"https://api.cheongwoldang.com/products/basic/mzshamantotal/pages/resolve?pageId={pid}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            page = data.get("page", {})
            title = page.get("title")
            stage = page.get("stage")
            blocks = [b.get("name") for b in page.get("blocks", [])]
            print(f"[{pid}] {title} (Stage: {stage}) -> 블록: {', '.join(blocks[:4])}")
            found_pages.append(page)
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"[{pid}] HTTP {e.code}")
    except Exception as e:
        pass

with open("cheongwoldang_scanned_pages.json", "w", encoding="utf-8") as f:
    json.dump(found_pages, f, ensure_ascii=False, indent=2)

print(f"\n총 {len(found_pages)}개 유효 페이지 발견!")
