# -*- coding: utf-8 -*-
"""
천명명경 (天命明鏡) | 청월당 흡수 기능 무결성 감사 테스트
- 대상: destiny_partner_engine.py
- 감사자: 🛠️ Agent 4 (Sentinel / QA Auditor)
"""

import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from manseryeok import calculate_saju
from destiny_partner_engine import (
    calculate_destiny_partners,
    calculate_destiny_place,
    calculate_lantern_fortune,
    calculate_caution_calendar
)


class TestDestinyPartnerEngine(unittest.TestCase):
    def setUp(self):
        # 다양한 사주 샘플
        self.samples = [
            (1994, 3, 15, 18, "male"),    # 갑술년 정묘월 신해일 정유시
            (1988, 8, 8, 12, "female"),   # 무진년 경신월 무자일 무오시
            (2001, 12, 25, 6, "male"),    # 신사년 경자월 임술일 계묘시
            (1975, 5, 20, 23, "female"),  # 을묘년 신사월 정미일 경자시
            (1965, 11, 3, 0, "male"),     # 을사년 병술월 계축일 임자시
        ]

    def test_calculate_destiny_partners_structure(self):
        """3대 인연 프로필과 5대 스펙 무결성 검증"""
        for y, m, d, h, gender in self.samples:
            saju = calculate_saju(y, m, d, h, 0, gender=gender)
            partners = calculate_destiny_partners(saju, user_gender=gender)

            self.assertEqual(len(partners), 3, "반드시 3대 인연(배필, 조화, 악연)이 산출되어야 함")
            types = [p["type"] for p in partners]
            self.assertEqual(types, ["soulmate", "harmony", "nemesis"])

            for p in partners:
                # 5대 스펙 필수 필드 검증
                self.assertIn("initial", p, "초성 누락")
                self.assertTrue(len(p["initial"]) >= 2, "초성은 2글자 이상이어야 함")
                self.assertIn("height", p, "키 누락")
                self.assertIn("cm", p["height"], "키에는 cm 단위가 포함되어야 함")
                self.assertIn("job", p, "직업 누락")
                self.assertTrue(len(p["job"]) > 2, "직업명이 유효해야 함")
                self.assertIn("zodiac", p, "띠 누락")
                self.assertIn("띠", p["zodiac"], "띠 표기가 유효해야 함")
                self.assertIn("trait", p, "외모/성향 누락")
                self.assertTrue(len(p["trait"]) > 5, "외모 묘사가 풍부해야 함")

                # 부가 필수 필드
                self.assertIn("chemistry_score", p)
                self.assertTrue(0 <= p["chemistry_score"] <= 100)
                self.assertIn("meeting_timing", p)
                self.assertIn("why_destiny", p)

    def test_calculate_destiny_place(self):
        """동서남북 붓글씨 방위 및 3차원 위치 좌표 검증"""
        valid_hanja = ["東", "西", "南", "北"]
        valid_dirs = ["동", "서", "남", "북"]

        for y, m, d, h, gender in self.samples:
            saju = calculate_saju(y, m, d, h, 0, gender=gender)
            place = calculate_destiny_place(saju)

            self.assertIn(place["direction_hanja"], valid_hanja)
            self.assertIn(place["direction"], valid_dirs)
            self.assertIn("km", place["distance"])
            self.assertTrue(len(place["scenes"]) >= 1)
            self.assertTrue(len(place["primary_scene"]) > 5)
            self.assertTrue(len(place["oracle_guide"]) > 10)

    def test_calculate_lantern_fortune(self):
        """청사초롱 5색 기운 등불 진단 검증"""
        for y, m, d, h, gender in self.samples:
            saju = calculate_saju(y, m, d, h, 0, gender=gender)
            lantern = calculate_lantern_fortune(saju)

            self.assertTrue(1 <= lantern["overall_level"] <= 3)
            self.assertIn("metrics", lantern)
            for k in ["wealth", "love", "health"]:
                metric = lantern["metrics"][k]
                self.assertTrue(1 <= metric["level"] <= 3)
                self.assertTrue(len(metric["title"]) > 0)
                self.assertTrue(len(metric["desc"]) > 5)

    def test_calculate_caution_calendar(self):
        """위험일 캘린더 및 살풀이 D-Day 검증"""
        for y, m, d, h, gender in self.samples:
            saju = calculate_saju(y, m, d, h, 0, gender=gender)
            caution = calculate_caution_calendar(saju)

            self.assertEqual(caution["salpuri_dday"], 7)
            self.assertTrue(len(caution["schedule"]) >= 3)
            for s in caution["schedule"]:
                self.assertTrue(1 <= s["month"] <= 12)
                self.assertTrue(len(s["days"]) >= 2)
                self.assertTrue(len(s["reason"]) > 5)


if __name__ == '__main__':
    unittest.main()
