# -*- coding: utf-8 -*-
from manseryeok import calculate_saju, CHEONGAN, JIJI

test_cases = [
    (1993, 8, 17, 18, 0, "1993년 8월 17일 18:00 (기본 프리셋)"),
    (2000, 1, 1, 12, 0, "2000년 1월 1일 12:00 (밀레니엄 기준)"),
    (2026, 10, 4, 12, 0, "2026년 10월 4일 12:00 (오늘 현재)"),
    (1988, 3, 15, 6, 0, "1988년 3월 15일 06:00 (올림픽 해)"),
    (2002, 6, 15, 14, 0, "2002년 6월 15일 14:00 (월드컵 해)")
]

for y, m, d, h, mn, desc in test_cases:
    res = calculate_saju(y, m, d, h, mn)
    p = res["pillars"]
    print("=" * 40)
    print(desc)
    print(f"  년주: {p['year']['pillar']} (십성: {p['year']['gan_sipseong']})")
    print(f"  월주: {p['month']['pillar']} (십성: {p['month']['gan_sipseong']})")
    print(f"  일주: {p['day']['pillar']} (일간/일원: {p['day']['gan']})")
    print(f"  시주: {p['hour']['pillar']} (십성: {p['hour']['gan_sipseong']})")
    print(f"  오행분포: {res['oheng_counts']}")
    print(f"  신살: {[k for k, v in res['shinsal'].items() if v]}")
