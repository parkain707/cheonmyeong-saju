# -*- coding: utf-8 -*-
"""
天命明鏡 (천명명경) | 현허도인의 천기 신점사주 웹 애플리케이션 로컬 서버
- Python 표준 내장 라이브러리(http.server) 기반 단독 실행
- REST API:
  - POST /api/saju: 스마트 자연어 파싱, 음력 변환, 시주 역추론, 신점 영안 투시, 세계 영성(융/차크라/주역) 통합
  - POST /api/unlock: 연 10억 수익화를 위한 VIP 프리미엄 리포트 잠금 해제 (결제 시뮬레이션)
- 정적 웹 UI 서빙
"""

import http.server
import socketserver
import json
import os
import sys

if sys.stdout is None:
    sys.stdout = open(os.devnull, "w", encoding="utf-8")
else:
    sys.stdout.reconfigure(encoding='utf-8')

if sys.stderr is None:
    sys.stderr = open(os.devnull, "w", encoding="utf-8")
else:
    sys.stderr.reconfigure(encoding='utf-8')



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

PORT = 8088
WEB_DIR = os.path.dirname(os.path.abspath(__file__))

class SajuRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self):
        if self.path.startswith('/api/health'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "service": "天命明鏡 (천명명경) API"}, ensure_ascii=False).encode('utf-8'))
            return
        if self.path.startswith('/api/version'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            ver_info = {
                "version": "20261001_v6_stable",
                "mtime": os.path.getmtime(os.path.join(WEB_DIR, "index.html"))
            }
            self.wfile.write(json.dumps(ver_info).encode('utf-8'))
            return
        super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b""

        if self.path == '/api/saju':
            try:
                if not post_data:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "code": "EMPTY_BODY", "message": "요청 본문이 비어있습니다."}, ensure_ascii=False).encode('utf-8'))
                    return

                try:
                    params = json.loads(post_data.decode('utf-8'))
                except Exception as je:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "code": "INVALID_JSON", "message": f"유효한 JSON 형식이 아닙니다: {str(je)}"}, ensure_ascii=False).encode('utf-8'))
                    return

                free_text = str(params.get('free_text', '')).strip()
                raw_name = str(params.get('name', '')).strip()
                name = raw_name if (raw_name and raw_name != '자네') else '그대'

                # 성별 정규화
                gender_raw = str(params.get('gender', 'male')).lower().strip()
                gender = 'female' if gender_raw in ['female', 'f', '여', '여자', '여성'] else 'male'

                # 오방기 정규화
                obanggi_raw = str(params.get('obanggi', '황')).strip()
                obanggi_map = {
                    '청': '청', 'blue': '청', '청룡': '청',
                    '적': '적', 'red': '적', '주작': '적',
                    '황': '황', 'yellow': '황', '황제': '황',
                    '백': '백', 'white': '백', '백호': '백',
                    '흑': '흑', 'black': '흑', '현무': '흑'
                }
                obanggi_choice = obanggi_map.get(obanggi_raw, '황')

                # 고민 영역 정규화
                concern_raw = str(params.get('concern', 'career')).strip()
                concern_map = {
                    '직업': 'career', '이직': 'career', 'career': 'career', 'job': 'career',
                    '애정': 'love', '연애': 'love', '인연': 'love', 'love': 'love',
                    '재물': 'wealth', '돈': 'wealth', '투자': 'wealth', 'wealth': 'wealth', 'money': 'wealth',
                    '시기': 'timing', '대운': 'timing', 'timing': 'timing', 'time': 'timing'
                }
                concern = concern_map.get(concern_raw, 'career')
                is_unlocked = bool(params.get('is_unlocked', False)) # VIP 결제 여부
                
                import calendar

                # 1. 자연어 자유 텍스트 스마트 파싱
                if free_text:
                    parsed = parse_free_text_saju(free_text)
                    solar_year = parsed["solar_year"]
                    solar_month = parsed["solar_month"]
                    solar_day = parsed["solar_day"]
                    hour = parsed["hour"]
                    is_lunar = parsed["is_lunar"]
                    parser_notes = parsed["notes"]
                else:
                    try:
                        year = int(params.get('year', 1990))
                    except (ValueError, TypeError):
                        year = 1990
                    try:
                        month = int(params.get('month', 1))
                    except (ValueError, TypeError):
                        month = 1
                    try:
                        day = int(params.get('day', 1))
                    except (ValueError, TypeError):
                        day = 1
                    try:
                        hour = int(params.get('hour', 12))
                    except (ValueError, TypeError):
                        hour = 12

                    is_lunar = (params.get('calendar_type') == 'lunar')
                    is_leap = bool(params.get('is_leap', False))
                    parser_notes = []

                    # 연월일 안전 범위 클램핑 (1920 ~ 2050)
                    year = max(1920, min(2050, year))
                    month = max(1, min(12, month))
                    max_day = calendar.monthrange(year, month)[1]
                    day = max(1, min(max_day, day))
                    if hour != -1:
                        hour = max(0, min(23, hour))

                    if is_lunar:
                        solar_year, solar_month, solar_day = lunar_to_solar(year, month, day, is_leap)
                        parser_notes.append(f"음력 {year}년 {month}월 {day}일을 양력 {solar_year}년 {solar_month}월 {solar_day}일로 자동 변환했습니다.")
                    else:
                        solar_year, solar_month, solar_day = year, month, day

                # 2. 시간을 전혀 모를 때의 지능적 시주 역추론
                time_estimated = False
                time_estimate_desc = ""
                if hour < 0:
                    time_estimated = True
                    temp_saju = calculate_saju(solar_year, solar_month, solar_day, 12, 0, gender)
                    hour, time_estimate_desc = estimate_hour_from_three_pillars(temp_saju)
                    parser_notes.append(f"태어난 시간을 모름에 따라 삼주(三柱) 오행 균형을 정밀 분석하여 '{time_estimate_desc}'로 역추론하여 보정했습니다.")

                # 3. 만세력 정밀 계산
                saju_result = calculate_saju(solar_year, solar_month, solar_day, hour, 0, gender)
                saju_result["time_estimated"] = time_estimated
                saju_result["time_estimate_desc"] = time_estimate_desc
                saju_result["parser_notes"] = parser_notes
                saju_result["solar_year"] = solar_year
                saju_result["solar_month"] = solar_month
                saju_result["solar_day"] = solar_day
                saju_result["solar_hour"] = hour
                saju_result["gender"] = gender
                saju_result["concern"] = concern
                saju_result["korean_age"] = 2026 - solar_year + 1

                # 4. 현허도인 천기 사주 풀이 생성
                reading_result = generate_guija_reading(saju_result, name, gender, concern)

                # 5. 신점 영안 투시 공수 생성
                prev_visit = params.get('prev_visit', None)
                spirit_vision = analyze_shamanic_vision(saju_result, obanggi_choice, concern, name, prev_visit=prev_visit)

                # 6. 세계적 영성(융 원형, 차크라 오라, 주역 64괘) 통합 분석
                global_spirit = analyze_global_spirituality(saju_result)

                # 6.5 황실 비전 자미두수(紫微斗數) 12궁 성반 연산
                ziwei_chart = calculate_ziwei_from_saju(
                    saju_result,
                    is_lunar=is_lunar,
                    original_year=year if 'year' in locals() else None,
                    original_month=month if 'month' in locals() else None,
                    original_day=day if 'day' in locals() else None
                )

                # 7. [오픈 기념 100% 전면 무료 배포]
                # 2030 폭발적 바이럴 유입 및 시장 선점을 위해 11개 전 챕터 100% 완전 무료 무제한 개방
                sections = reading_result["sections"]
                is_unlocked = True  # 100% 무료 배포
                for sec in sections:
                    sec["is_locked"] = False
                    sec["locked_preview"] = ""

                # 7. 청월당 4대 점사 출력 포맷 (운명의 3대 인연, 3차원 위치 좌표, 청사초롱 등불, 위험일 캘린더)
                gender_val = params.get('gender', 'male')
                destiny_partners = calculate_destiny_partners(saju_result, ziwei_chart, gender_val)
                destiny_place = calculate_destiny_place(saju_result)
                lantern_fortune = calculate_lantern_fortune(saju_result)
                caution_calendar = calculate_caution_calendar(saju_result)

                # 8. 2030 바이럴 인텔리전스 (60갑자 캐릭터 카드, 애착유형, 직장 번아웃, 이직 골든타임, 바이럴 공유 텍스트)
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
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
                
            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                sys.stderr.write(f"❌ [API ERROR]: {tb}\n")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                err_resp = {"status": "error", "code": "SERVER_EXCEPTION", "message": f"서버 연산 중 오류가 발생했습니다: {str(e)}"}
                self.wfile.write(json.dumps(err_resp, ensure_ascii=False).encode('utf-8'))

        elif self.path == '/api/unlock':
            # VIP 결제 시뮬레이션 및 잠금 해제
            try:
                params = json.loads(post_data.decode('utf-8'))
                order_id = params.get('order_id', 'ORDER-20261001-SUCCESS')
                print(f"💰 [결제 성공 알림] 주문번호: {order_id} (19,800원 결제 완료)")
                
                resp_data = {
                    "status": "success",
                    "message": "VIP 평생 열람 권한이 성공적으로 활성화되었습니다.",
                    "order_id": order_id
                }
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(resp_data, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

        elif self.path == '/api/gunghap':
            # 2인 사주 정밀 궁합 API
            try:
                params = json.loads(post_data.decode('utf-8'))
                pA = params.get('personA', {})
                pB = params.get('personB', {})
                rel_type = params.get('relation_type', 'dating')

                # 사주 A 계산
                syA, smA, sdA = int(pA.get('year', 1993)), int(pA.get('month', 8)), int(pA.get('day', 17))
                if pA.get('is_lunar'):
                    syA, smA, sdA = lunar_to_solar(syA, smA, sdA)
                shA = int(pA.get('hour', 12)) if pA.get('hour') is not None else 12
                sajuA = calculate_saju(syA, smA, sdA, shA, 0)

                # 사주 B 계산
                syB, smB, sdB = int(pB.get('year', 1995)), int(pB.get('month', 5)), int(pB.get('day', 20))
                if pB.get('is_lunar'):
                    syB, smB, sdB = lunar_to_solar(syB, smB, sdB)
                shB = int(pB.get('hour', 12)) if pB.get('hour') is not None else 12
                sajuB = calculate_saju(syB, smB, sdB, shB, 0)

                gunghap_res = analyze_gunghap(sajuA, sajuB, rel_type, pA.get('name', '본인'), pB.get('name', '상대방'))

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "gunghap": gunghap_res, "sajuA": sajuA, "sajuB": sajuB}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False).encode('utf-8'))

        elif self.path == '/api/qa':
            # 현허도인 1:1 천기 심층 문답 API
            try:
                params = json.loads(post_data.decode('utf-8'))
                question = str(params.get('question', '')).strip()
                mode = params.get('mode', 'single')
                name = params.get('name', '그대')
                history = params.get('history', [])
                saju_obj = params.get('saju', None)
                ziwei_obj = params.get('ziwei', None)

                if not saju_obj:
                    y = int(params.get('year', 1993))
                    m = int(params.get('month', 8))
                    d = int(params.get('day', 17))
                    h = int(params.get('hour', 12)) if params.get('hour') is not None else 12
                    saju_obj = calculate_saju(y, m, d, h, 0)
                if not ziwei_obj:
                    ziwei_obj = calculate_ziwei_from_saju(saju_obj)

                qa_res = generate_shaman_answer(saju_obj, ziwei_obj, question, mode, history, name)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(qa_res, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server():
    import webbrowser
    import threading

    def open_browser():
        try:
            webbrowser.open(f"http://localhost:{PORT}")
        except Exception:
            pass

    socketserver.ThreadingTCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.ThreadingTCPServer(("", PORT), SajuRequestHandler)
    except OSError:
        # 포트가 이미 사용 중인 경우 즉시 브라우저만 띄움
        print(f"==================================================")
        print(f"🔮 天命明鏡 (천명명경) | 서버가 이미 포트 {PORT}에서 실행 중입니다.")
        print(f"👉 브라우저를 즉시 실행합니다: http://localhost:{PORT}")
        print(f"==================================================")
        open_browser()
        return

    with httpd:
        print(f"==================================================")
        print(f"🔮 天命明鏡 (천명명경) | 현허도인의 천기 신점사주 서버 가동 중")
        print(f"👉 브라우저 자동 연결: http://localhost:{PORT}")
        print(f"==================================================")
        
        # 0.8초 후 브라우저 자동 오픈
        threading.Timer(0.8, open_browser).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n서버를 종료합니다.")
            httpd.server_close()

if __name__ == '__main__':
    run_server()
