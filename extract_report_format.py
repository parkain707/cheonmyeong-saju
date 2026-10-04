# -*- coding: utf-8 -*-
import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open("chunk_27zpvgk82zhdg.js", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

print("파일 크기:", len(text))

# 1. 블록 컴포넌트 경로 (/components/blocks/... 또는 blocks/) 추출
block_paths = set(re.findall(r'["\'](/[^"\']*blocks/[^"\']*)["\']', text))
print(f"\n=== 발견된 블록/컴포넌트 리소스 경로 ({len(block_paths)}개) ===")
for bp in sorted(block_paths):
    print(" 🧱", bp)

# 2. 렌더링 카드/박스 구조 (예: className 또는 타이틀/구조체)
# shamantotal 관련 블록 클래스나 옵션 찾기
shaman_blocks = re.findall(r'["\']([a-zA-Z0-9_\-]+shamantotal[a-zA-Z0-9_\-/]*)["\']', text)
print(f"\n=== 발견된 shamantotal 전용 컴포넌트/경로 ===")
for sb in set(shaman_blocks):
    print(" 🔮", sb)

# 3. 출력 형식 템플릿 (카피 구조)
# "인연", "방위", "장소", "프로필", "나이", "외모", "직업", "성격" 등이 결합된 템플릿 찾기
profile_templates = re.findall(r'(\{[^{}]*?(?:상대|인연|배필|악연)[^{}]*?(?:외모|직업|나이|만남|특징|장소)[^{}]*?\})', text)
print(f"\n=== 발견된 인연 프로필 출력 템플릿 ({len(profile_templates)}개) ===")
for pt in profile_templates[:10]:
    print(" 👤", pt[:120])

# 4. 결과지 섹션 순서 (목차 레이아웃)
sections = re.findall(r'["\']([0-9]+\.\s*[^"\']+|제[0-9]+장[^"\']+|Chapter\s*[0-9]+[^"\']*)["\']', text)
print(f"\n=== 발견된 챕터/섹션 순서 레이아웃 ===")
for s in sorted(list(set(sections)))[:20]:
    print(" 📑", s)
