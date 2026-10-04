# -*- coding: utf-8 -*-
import urllib.request
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://cheongwoldang.com/b/mzshamantotal',
    'Origin': 'https://cheongwoldang.com',
    'Accept': 'application/json, text/plain, */*'
}

for ep in ['pages/free', 'pages/resolve', 'pages/preview', 'pages']:
    u = f'https://api.cheongwoldang.com/products/basic/mzshamantotal/{ep}'
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = resp.read().decode('utf-8')
            print(f"[OK] {ep}: Status {resp.status} ({len(data)} bytes)")
            with open(f"cheongwoldang_{ep.replace('/', '_')}.json", "w", encoding="utf-8") as f:
                f.write(data)
            print(data[:300])
    except urllib.error.HTTPError as e:
        print(f"[HTTP {e.code}] {ep}: {e.read().decode('utf-8', errors='ignore')[:150]}")
    except Exception as e:
        print(f"[ERR] {ep}: {e}")
