# -*- coding: utf-8 -*-
import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open("chunk_27zpvgk82zhdg.js", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# job, initial, zodiac, height, trait 주변 스니펫 찾기
pos = text.find('initial:"이름 초성"')
if pos == -1:
    pos = text.find('initial:')

if pos != -1:
    snippet = text[max(0, pos - 400):min(len(text), pos + 1200)]
    print("=== 인연 프로필 렌더링 스니펫 ===")
    print(snippet)
else:
    print("initial 키워드를 못 찾았습니다.")

# shamantotal 관련 블록 컴포넌트 렌더러 찾기
shaman_pos = [m.start() for m in re.finditer(r'shamantotal', text)]
print(f"\nshamantotal 출현 횟수: {len(shaman_pos)}개")
for p in shaman_pos[:5]:
    print("--- shamantotal 문맥 ---")
    print(text[max(0, p - 100):min(len(text), p + 300)])
    print("-" * 50)
