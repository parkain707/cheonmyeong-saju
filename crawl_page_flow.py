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

visited_pages = []
next_page_id = 690

print("=== 청월당 'MZ무당 시아의 팩폭점사' 전체 페이지 플로우 크롤링 시작 ===")

while next_page_id and next_page_id not in [p['id'] for p in visited_pages]:
    url = f"https://api.cheongwoldang.com/products/basic/mzshamantotal/pages/resolve?pageId={next_page_id}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            page = data.get("page", {})
            p_id = page.get("id")
            title = page.get("title")
            stage = page.get("stage")
            blocks = page.get("blocks", [])
            
            print(f"\n[PAGE {p_id}] {title} (Stage: {stage}) | 블록 {len(blocks)}개")
            
            # 블록 내용 분석
            next_id_from_blocks = None
            for b in blocks:
                b_name = b.get("name")
                opts = b.get("options", {})
                print(f"  - Block: {b_name}")
                if "title" in opts:
                    print(f"    • Title: {opts['title']}")
                if "question" in opts:
                    print(f"    • Question: {opts['question']}")
                if "content" in opts:
                    print(f"    • Content: {str(opts['content'])[:100]}...")
                if "buttonText" in opts:
                    print(f"    • Button: {opts['buttonText']} (goToPageId: {opts.get('goToPageId')})")
                    if opts.get("goToPageId"):
                        next_id_from_blocks = opts.get("goToPageId")
                if "description" in opts:
                    print(f"    • Desc: {str(opts['description'])[:100]}...")
            
            visited_pages.append({
                "id": p_id,
                "title": title,
                "stage": stage,
                "blocks": blocks,
                "nextPageId": next_id_from_blocks
            })
            
            next_page_id = next_id_from_blocks
            if not next_page_id:
                break
                
    except Exception as e:
        print(f"❌ Page {next_page_id} 조회 에러:", e)
        break

with open("cheongwoldang_all_pages_flow.json", "w", encoding="utf-8") as f:
    json.dump(visited_pages, f, ensure_ascii=False, indent=2)

print(f"\n총 {len(visited_pages)}개 페이지 수집 완료! (cheongwoldang_all_pages_flow.json 저장)")
