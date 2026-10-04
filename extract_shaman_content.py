# -*- coding: utf-8 -*-
import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open("chunk_27zpvgk82zhdg.js", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

print("파일 크기:", len(text))

# 1. '시아' 또는 '무당' 관련 한국어 문장 모두 수집
sentences = re.findall(r'["\']([^"\']*(?:시아|무당|점사|팩폭|방울|부적|오방기|신령|작두|동자|할매)[^"\']*)["\']', text)
clean_sentences = []
for s in sentences:
    s = s.strip()
    if 5 <= len(s) <= 200 and not s.startswith("http") and not s.endswith(".webp") and not s.endswith(".png"):
        clean_sentences.append(s)

unique_sentences = sorted(list(set(clean_sentences)))
print(f"\n발견된 무당/시아 관련 문구: {len(unique_sentences)}개")
for s in unique_sentences[:40]:
    print(" 🔮", s)

# 2. 질문/폼 관련 텍스트 (사주 입력 항목)
form_texts = re.findall(r'["\']([^"\']*(?:태어난|생년월일|양력|음력|태어난 시간|성별|이름을 입력|고민|질문)[^"\']*)["\']', text)
clean_forms = []
for ft in form_texts:
    ft = ft.strip()
    if 4 <= len(ft) <= 100:
        clean_forms.append(ft)

print(f"\n발견된 사주 입력 폼 문구: {len(clean_forms)}개")
for ft in sorted(list(set(clean_forms)))[:25]:
    print(" 📝", ft)

# 3. 점사 결과 리포트 섹션/챕터 타이틀 (예: 1장, 2장, 챕터, 총운, 연애운, 재물운 등)
report_sections = re.findall(r'["\']([^"\']*(?:총운|재물운|연애운|직업운|인연|대운|세운|오행|십성|신살|격국|용신|희신|기신|구신|한신)[^"\']*)["\']', text)
print(f"\n발견된 명리학/점사 분석 섹션: {len(report_sections)}개")
for rs in sorted(list(set(report_sections)))[:30]:
    if 4 <= len(rs) <= 80:
        print(" 📜", rs)
