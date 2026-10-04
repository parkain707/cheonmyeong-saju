# -*- coding: utf-8 -*-
import urllib.request
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://cheongwoldang.com/b/mzshamantotal',
    'Origin': 'https://cheongwoldang.com',
    'Accept': 'application/json, text/plain, */*'
}

# 1. 기본 상품 전체 정보 조회
url = 'https://api.cheongwoldang.com/products/basic/mzshamantotal'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    data_str = resp.read().decode('utf-8')
    with open('cheongwoldang_product_full.json', 'w', encoding='utf-8') as f:
        f.write(data_str)
    product_obj = json.loads(data_str)
    print("✅ 상품 기본 정보 수신 성공!")
    print(json.dumps(product_obj, ensure_ascii=False, indent=2)[:1000])

# 2. 페이지 프리뷰 조회 시도
initial_page_id = product_obj.get("product", {}).get("initialPageId", 690)
page_url = f'https://api.cheongwoldang.com/products/basic/mzshamantotal/pages/preview?pageId={initial_page_id}'
try:
    req_page = urllib.request.Request(page_url, headers=headers)
    with urllib.request.urlopen(req_page) as resp_page:
        page_str = resp_page.read().decode('utf-8')
        with open(f'cheongwoldang_page_{initial_page_id}.json', 'w', encoding='utf-8') as f:
            f.write(page_str)
        page_obj = json.loads(page_str)
        print(f"\n✅ 프리뷰 페이지 ({initial_page_id}) 수신 성공!")
        print(json.dumps(page_obj, ensure_ascii=False, indent=2)[:1500])
except Exception as e:
    print(f"\n❌ 프리뷰 페이지 ({initial_page_id}) 실패:", e)

# 3. 다른 연관 엔드포인트 테스트 (featured, recommend, package)
for sub in ["featured", "recommend", "package"]:
    try:
        sub_url = f'https://api.cheongwoldang.com/products/{sub}'
        r = urllib.request.Request(sub_url, headers=headers)
        with urllib.request.urlopen(r) as res:
            res_str = res.read().decode('utf-8')
            with open(f'cheongwoldang_{sub}.json', 'w', encoding='utf-8') as f:
                f.write(res_str)
            print(f"✅ /products/{sub} 수신 완료 ({len(res_str):,} bytes)")
    except Exception as e:
        print(f"❌ /products/{sub} 에러:", e)
