# -*- coding: utf-8 -*-
import urllib.request
import json

url = 'http://localhost:8088/api/saju'
cases = [
    ('방문자 A [직업/이직 + 청기]', {'year': 1991, 'month': 5, 'day': 4, 'hour': 14, 'gender': 'male', 'concern': 'career', 'obanggi': '청'}),
    ('방문자 B [애정/인연 + 백기]', {'year': 1991, 'month': 5, 'day': 4, 'hour': 14, 'gender': 'male', 'concern': 'love', 'obanggi': '백'}),
    ('방문자 C [재물/투자 + 황기]', {'year': 1991, 'month': 5, 'day': 4, 'hour': 14, 'gender': 'male', 'concern': 'wealth', 'obanggi': '황'})
]

with open('comparison_result.txt', 'w', encoding='utf-8') as out:
    for label, data in cases:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        res = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
        sv = res['spirit_vision']
        rd = res['reading']
        out.write(f'==================================================\n')
        out.write(f'📌 {label}\n')
        out.write(f'  • [신탁 첫마디]: {sv["shamanic_speech"].split(chr(10)+chr(10))[1][:110]}...\n')
        out.write(f'  • [신체 통증 투시]: {sv["body_pain"]}\n')
        out.write(f'  • [과거 환란 적중]: {sv["recent_shock"]}\n')
        out.write(f'  • [은밀한 속마음]: {sv["secret_mind"][:100]}...\n')
        out.write(f'  • [오방기 신탁]: {sv["obanggi"]["color"]} -> "{sv["obanggi"]["oracle"]}"\n')
        out.write(f'  • [도인 천기 프리뷰]: {rd["preview_text"]}\n\n')

print('Comparison finished successfully.')
