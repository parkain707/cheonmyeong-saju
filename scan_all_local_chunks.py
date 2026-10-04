# -*- coding: utf-8 -*-
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

chunk_files = [f for f in os.listdir(".") if f.startswith("chunk_") and f.endswith(".js")]
print(f"로컬 청크 파일 {len(chunk_files)}개 전수 분석...")

all_korean = []
shaman_cards = []

for cf in chunk_files:
    with open(cf, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    # 한국어 문자열 추출
    found = re.findall(r'["\']([^"\']*[가-힣]{3,}[^"\']*)["\']', content)
    for txt in found:
        txt = txt.strip()
        if 8 <= len(txt) <= 120:
            if any(k in txt for k in ["무당", "시아", "점사", "인연", "오방기", "부적", "용신", "기신", "살풀이", "복채", "흉살", "백호", "도화", "원진", "대운", "거리", "방위"]):
                shaman_cards.append((cf, txt))

print(f"\n핵심 점사/무속 텍스트 {len(shaman_cards)}개 발견!")
for cf, txt in sorted(list(set(shaman_cards)))[:60]:
    print(f" • [{cf[:15]}] {txt}")
