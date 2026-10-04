# -*- coding: utf-8 -*-
import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

ids_in_js = re.findall(r'document\.getElementById\("([^"]+)"\)', js)
ids_in_js += re.findall(r"document\.getElementById\('([^']+)'\)", js)

missing = []
for id_name in sorted(set(ids_in_js)):
    if f'id="{id_name}"' not in html and f"id='{id_name}'" not in html:
        missing.append(id_name)

print("Total getElementById searched:", len(set(ids_in_js)))
print("MISSING IDS:", missing)
