# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from manseryeok import calculate_saju

benchmark_dates = [
    (2000, 1, 1, 12, "기묘", "병자", "무오"),
    (2026, 10, 4, 12, "병오", "정유", "신해"),
    (1988, 9, 17, 12, "무진", "신유", "정사"),
    (2002, 5, 31, 12, "임오", "을사", "기축"),
    (1950, 6, 25, 12, "경인", "임오", "신유"),
    (1945, 8, 15, 12, "을유", "갑신", "병자"),
    (2010, 1, 1, 12, "기축", "병자", "계미"),
    (2020, 1, 1, 12, "기해", "병자", "계해")
]

for y, m, d, h, exp_y, exp_m, exp_d in benchmark_dates:
    res = calculate_saju(y, m, d, h, 0)
    p = res['pillars']
    py = p['year']['pillar']
    pm = p['month']['pillar']
    pd = p['day']['pillar']
    print(f"{y}-{m:02d}-{d:02d}:")
    print(f"  계산: {py}년 {pm}월 {pd}일")
    print(f"  기대: {exp_y}년 {exp_m}월 {exp_d}일")
    print(f"  일치: 연({py==exp_y}) 월({pm==exp_m}) 일({pd==exp_d})")
