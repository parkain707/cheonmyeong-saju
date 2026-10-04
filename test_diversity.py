# -*- coding: utf-8 -*-
"""
Agent 4 (Sentinel) 사주별 풀이 차별화 및 다양성(Diversity) 정밀 감사 스크립트
- 3대 완전 분기 사주 (병화 식상, 을목 재성, 경금 관성)의 11개 챕터 및 신점 공수를 비교 분석
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from manseryeok import calculate_saju
from guija_engine import generate_guija_reading
from spirit_engine import analyze_shamanic_vision

def calculate_similarity(text1, text2):
    # Jaccard similarity of 3-grams
    ngrams1 = set(text1[i:i+3] for i in range(len(text1)-2))
    ngrams2 = set(text2[i:i+3] for i in range(len(text2)-2))
    if not ngrams1 or not ngrams2:
        return 0.0
    intersection = len(ngrams1 & ngrams2)
    union = len(ngrams1 | ngrams2)
    return intersection / union

def run_diversity_audit():
    print("=" * 70)
    print("🛡️ [Sentinel] 서로 다른 사주 간 풀이 차별화 및 독립성 감사 시작")
    print("=" * 70)

    # 케이스 1: 1991년 5월 4일 14:00 (병신일주, 남, 36세, 식상 격국, 직업 고민, 청기)
    saju1 = calculate_saju(1991, 5, 4, 14, 0, "male")
    saju1["korean_age"] = 36
    read1 = generate_guija_reading(saju1, "김태양", "male", "career")
    spir1 = analyze_shamanic_vision(saju1, "청", "career", "김태양")

    # 케이스 2: 1998년 7월 15일 10:00 (을유일주, 여, 29세, 재성 격국, 재물 고민, 적기)
    saju2 = calculate_saju(1998, 7, 15, 10, 0, "female")
    saju2["korean_age"] = 29
    read2 = generate_guija_reading(saju2, "이지은", "female", "wealth")
    spir2 = analyze_shamanic_vision(saju2, "적", "wealth", "이지은")

    # 케이스 3: 1997년 6월 5일 21:00 (경자일주, 남, 30세, 관성 격국, 연애 고민, 백기)
    saju3 = calculate_saju(1997, 6, 5, 21, 0, "male")
    saju3["korean_age"] = 30
    read3 = generate_guija_reading(saju3, "박철민", "male", "love")
    spir3 = analyze_shamanic_vision(saju3, "백", "love", "박철민")

    # 1. 신점 공수 유사도 검사
    sim_spir_1_2 = calculate_similarity(spir1["shamanic_speech"], spir2["shamanic_speech"])
    sim_spir_1_3 = calculate_similarity(spir1["shamanic_speech"], spir3["shamanic_speech"])
    sim_spir_2_3 = calculate_similarity(spir2["shamanic_speech"], spir3["shamanic_speech"])
    avg_spir_sim = (sim_spir_1_2 + sim_spir_1_3 + sim_spir_2_3) / 3

    print(f"🔮 신점 공수 유사도 [사주1 vs 사주2]: {sim_spir_1_2*100:.1f}%")
    print(f"🔮 신점 공수 유사도 [사주1 vs 사주3]: {sim_spir_1_3*100:.1f}%")
    print(f"🔮 신점 공수 유사도 [사주2 vs 사주3]: {sim_spir_2_3*100:.1f}%")
    print(f"✨ 신점 공수 평균 유사도: {avg_spir_sim*100:.1f}% (독립성: {100-avg_spir_sim*100:.1f}%)")
    assert avg_spir_sim < 0.35, f"신점 공수가 너무 유사함! ({avg_spir_sim})"

    # 2. 11개 챕터별 유사도 및 차별성 검사
    print("\n📜 11개 챕터별 텍스트 고유성 검증:")
    total_sim = 0
    for idx in range(11):
        c1 = read1["sections"][idx]
        c2 = read2["sections"][idx]
        c3 = read3["sections"][idx]
        
        sim12 = calculate_similarity(c1["desc"], c2["desc"])
        sim13 = calculate_similarity(c1["desc"], c3["desc"])
        sim23 = calculate_similarity(c2["desc"], c3["desc"])
        avg_sim = (sim12 + sim13 + sim23) / 3
        total_sim += avg_sim
        
        print(f"  [제{idx+1:02d}장 {c1['hanja']}] {c1['title']}: 평균 유사도 {avg_sim*100:.1f}% (독립성: {100-avg_sim*100:.1f}%) [1-2:{sim12*100:.1f}%, 1-3:{sim13*100:.1f}%, 2-3:{sim23*100:.1f}%]")
        assert avg_sim < 0.40, f"제{idx+1}장 내용이 다른 사주와 너무 흡사함! (유사도: {avg_sim})"

    overall_avg_sim = (total_sim / 11) * 100
    print("\n" + "=" * 70)
    print(f"✅ [감사 완벽 통과] 11개 챕터 전체 평균 유사도: {overall_avg_sim:.1f}%")
    print(f"🎉 각 사주 간 고유 차별화 지수(Differentiation Index): {100-overall_avg_sim:.1f}% 달성!")
    print("=" * 70)

if __name__ == '__main__':
    run_diversity_audit()
