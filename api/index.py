# -*- coding: utf-8 -*-
"""
Vercel Serverless Python Handler for 天命明鏡 (천명명경)
- Vercel 환경에서 /api/saju, /api/gunghap, /api/qa, /api/version 등을 처리하는 진입점
"""

import sys
import os
import json
from http.server import BaseHTTPRequestHandler

# 프로젝트 루트 디렉토리를 파이썬 모듈 검색 경로에 추가
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from manseryeok import calculate_saju
from guija_engine import generate_guija_reading
from smart_parser import parse_free_text_saju, estimate_hour_from_three_pillars
from lunar_converter import lunar_to_solar
from spirit_engine import analyze_shamanic_vision
from global_spirit import analyze_global_spirituality
from ziwei_engine import calculate_ziwei_from_saju
from gunghap_engine import analyze_gunghap
from qa_engine import generate_shaman_answer
from destiny_partner_engine import (
    calculate_destiny_partners,
    calculate_destiny_place,
    calculate_lantern_fortune,
    calculate_caution_calendar
)
from mz_saju_engine import get_mz_comprehensive_analysis

class handler(BaseHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path.startswith('/api/health'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "service": "天命明鏡 (천명명경) Vercel Serverless"}, ensure_ascii=False).encode('utf-8'))
            return
        if self.path.startswith('/api/version'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"version": "20261001_v7_vercel", "platform": "Vercel Serverless"}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b""

        # /api/saju
        if self.path.endswith('/saju'):
            try:
                params = json.loads(post_data.decode('utf-8')) if post_data else {}
                free_text = str(params.get('free_text', '')).strip()
                raw_name = str(params.get('name', '')).strip()
                name = raw_name if (raw_name and raw_name != '자네') else '그대'

                gender_raw = str(params.get('gender', 'male')).lower().strip()
                gender = 'female' if gender_raw in ['female', 'f', '여', '여자', '여성'] else 'male'

                obanggi_raw = str(params.get('obanggi', '황')).strip()
                obanggi_map = {
                    '청': '청', '적': '적', '황': '황', '백': '백', '흑': '흑'
                }
                obanggi_choice = obanggi_map.get(obanggi_raw, '황')

                concern_raw = str(params.get('concern', 'career')).strip()
                concern_map = {
                    '직업': 'career', '이직': 'career', 'career': 'career',
                    '애정': 'love', '연애': 'love', '인연': 'love', 'love': 'love',
                    '재물': 'wealth', '돈': 'wealth', '투자': 'wealth', 'wealth': 'wealth',
                    '시기': 'timing', '대운': 'timing', 'timing': 'timing'
                }
                concern = concern_map.get(concern_raw, 'career')

                parser_notes = []

                if free_text:
                    parsed = parse_free_text_saju(free_text)
                    solar_year = parsed["solar_year"]
                    solar_month = parsed["solar_month"]
                    solar_day = parsed["solar_day"]
                    hour = parsed["hour"]
                    minute = parsed["minute"]
                    is_lunar = parsed["is_lunar"]
                    is_leap = parsed["is_leap"]
                    if parsed.get("name") and parsed["name"] != "그대":
                        name = parsed["name"]
                    if parsed.get("gender"):
                        gender = parsed["gender"]
                    parser_notes = parsed.get("notes", [])
                else:
                    year = int(params.get('year', 1993))
                    month = int(params.get('month', 8))
                    day = int(params.get('day', 17))
                    hour = int(params.get('hour', 18))
                    minute = int(params.get('minute', 0))
                    calendar_type = params.get('calendar_type', 'solar')
                    is_leap = bool(params.get('is_leap', False))
                    is_lunar = (calendar_type == 'lunar')

                    if is_lunar:
                        solar_year, solar_month, solar_day = lunar_to_solar(year, month, day, is_leap)
                        parser_notes.append(f"음력 {year}년 {month}월 {day}일 ({'윤달' if is_leap else '평달'}) -> 양력 {solar_year}년 {solar_month}월 {solar_day}일로 천문 변환 완료")
                    else:
                        solar_year, solar_month, solar_day = year, month, day

                if hour < 0:
                    est = estimate_hour_from_three_pillars(solar_year, solar_month, solar_day)
                    hour = est["estimated_hour"]
                    minute = est["estimated_minute"]
                    parser_notes.append(f"출생 시간 미입력: 일간의 균형을 돕는 {est['reason']} ({hour:02d}:{minute:02d})로 천문 역추론 보정 완료")

                # 사주팔자 계산
                saju_result = calculate_saju(solar_year, solar_month, solar_day, hour, minute, gender=gender)
                saju_result["korean_age"] = 2026 - solar_year + 1
                ziwei_chart = calculate_ziwei_from_saju(
                    saju_result,
                    is_lunar=is_lunar,
                    original_year=year if 'year' in locals() else None,
                    original_month=month if 'month' in locals() else None,
                    original_day=day if 'day' in locals() else None
                )
                spirit_vision = analyze_shamanic_vision(saju_result, obanggi_choice, concern, name=name, ziwei_data=ziwei_chart)
                global_spirit = analyze_global_spirituality(saju_result)

                reading_result = generate_guija_reading(
                    saju_result,
                    name=name,
                    gender=gender,
                    concern=concern
                )

                # 100% 무료 배포: 11개 전 챕터 전면 잠금 해제
                sections = reading_result["sections"]
                is_unlocked = True
                for sec in sections:
                    sec["is_locked"] = False
                    sec["locked_preview"] = ""

                # 청월당 4대 점사
                destiny_partners = calculate_destiny_partners(saju_result, ziwei_chart, gender)
                destiny_place = calculate_destiny_place(saju_result)
                lantern_fortune = calculate_lantern_fortune(saju_result)
                caution_calendar = calculate_caution_calendar(saju_result)

                # 2030 바이럴 인텔리전스
                mz_insight = get_mz_comprehensive_analysis(saju_result, name)

                response_data = {
                    "status": "success",
                    "saju": saju_result,
                    "reading": reading_result,
                    "spirit_vision": spirit_vision,
                    "global_spirit": global_spirit,
                    "ziwei": ziwei_chart,
                    "destiny_partners": destiny_partners,
                    "destiny_place": destiny_place,
                    "lantern_fortune": lantern_fortune,
                    "caution_calendar": caution_calendar,
                    "mz_insight": mz_insight,
                    "notes": parser_notes,
                    "is_unlocked": is_unlocked
                }

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))

            except Exception as e:
                import traceback
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                err_resp = {"status": "error", "message": f"연산 오류: {str(e)}", "trace": traceback.format_exc()}
                self.wfile.write(json.dumps(err_resp, ensure_ascii=False).encode('utf-8'))

        # /api/gunghap
        elif self.path.endswith('/gunghap'):
            try:
                params = json.loads(post_data.decode('utf-8')) if post_data else {}
                relation = params.get('relation', 'dating')

                # Person 1
                p1_raw = params.get('person1', {})
                p1_cal = p1_raw.get('calendar_type', 'solar')
                p1_leap = bool(p1_raw.get('is_leap', False))
                p1_y, p1_m, p1_d = int(p1_raw.get('year', 1993)), int(p1_raw.get('month', 8)), int(p1_raw.get('day', 17))
                if p1_cal == 'lunar':
                    p1_sy, p1_sm, p1_sd = lunar_to_solar(p1_y, p1_m, p1_d, p1_leap)
                else:
                    p1_sy, p1_sm, p1_sd = p1_y, p1_m, p1_d
                p1_h = int(p1_raw.get('hour', 18))
                if p1_h < 0:
                    p1_h = estimate_hour_from_three_pillars(p1_sy, p1_sm, p1_sd)['estimated_hour']
                saju1 = calculate_saju(p1_sy, p1_sm, p1_sd, p1_h, gender=p1_raw.get('gender', 'male'))

                # Person 2
                p2_raw = params.get('person2', {})
                p2_cal = p2_raw.get('calendar_type', 'solar')
                p2_leap = bool(p2_raw.get('is_leap', False))
                p2_y, p2_m, p2_d = int(p2_raw.get('year', 1995)), int(p2_raw.get('month', 10)), int(p2_raw.get('day', 24))
                if p2_cal == 'lunar':
                    p2_sy, p2_sm, p2_sd = lunar_to_solar(p2_y, p2_m, p2_d, p2_leap)
                else:
                    p2_sy, p2_sm, p2_sd = p2_y, p2_m, p2_d
                p2_h = int(p2_raw.get('hour', 14))
                if p2_h < 0:
                    p2_h = estimate_hour_from_three_pillars(p2_sy, p2_sm, p2_sd)['estimated_hour']
                saju2 = calculate_saju(p2_sy, p2_sm, p2_sd, p2_h, gender=p2_raw.get('gender', 'female'))

                name1 = p1_raw.get('name', '그대')
                name2 = p2_raw.get('name', '상대방')
                gunghap_result = analyze_gunghap(saju1, saju2, name1=name1, name2=name2, relation=relation)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "gunghap": gunghap_result}, ensure_ascii=False).encode('utf-8'))
            except Exception as ge:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(ge)}, ensure_ascii=False).encode('utf-8'))

        # /api/qa
        elif self.path.endswith('/qa'):
            try:
                params = json.loads(post_data.decode('utf-8')) if post_data else {}
                question = str(params.get('question', '')).strip()
                mode = params.get('mode', 'single')
                history = params.get('history', [])
                person = params.get('person', {})

                py = int(person.get('year', 1993))
                pm = int(person.get('month', 8))
                pd = int(person.get('day', 17))
                ph = int(person.get('hour', 18))
                pg = person.get('gender', 'male')
                pname = person.get('name', '질문자')

                saju = calculate_saju(py, pm, pd, ph, gender=pg)
                ziwei = calculate_ziwei_from_saju(saju)

                qa_resp = generate_shaman_answer(question, mode=mode, history=history, saju_data=saju, ziwei_data=ziwei, name=pname)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(qa_resp, ensure_ascii=False).encode('utf-8'))
            except Exception as qe:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(qe)}, ensure_ascii=False).encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()
