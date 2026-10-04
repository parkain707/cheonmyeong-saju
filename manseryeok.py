# -*- coding: utf-8 -*-
"""
정밀 만세력 계산 코어 엔진 (Manseryeok Engine)
- 24절기 절입 시각 계산 (Astronomical Solar Terms)
- 60갑자 사주팔자(년주, 월주, 일주, 시주) 정밀 산출
- 십성(육친), 지장간, 12운성
- 특수 신살: 귀문관살, 공망, 백호대살, 천라지망, 괴강살, 도화살, 역마살, 화개살, 천을귀인 등
- 60갑자 납음오행 (納音五行)
- 음양 체질 5단계 및 육감 6대 지표(직감, 영감, 꿈선명도, 귀신감지, 전생기억, 주술친화) 스코어링
"""

import math
from datetime import datetime, date, time

# 천간 및 지지
CHEONGAN = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
CHEONGAN_HANJA = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

JIJI = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]
JIJI_HANJA = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 오행 및 음양
OHENG_CHEONGAN = {
    "갑": ("목", "양"), "을": ("목", "음"),
    "병": ("화", "양"), "정": ("화", "음"),
    "무": ("토", "양"), "기": ("토", "음"),
    "경": ("금", "양"), "신": ("금", "음"),
    "임": ("수", "양"), "계": ("수", "음"),
}

OHENG_JIJI = {
    "자": ("수", "음"), "축": ("토", "음"),
    "인": ("목", "양"), "묘": ("목", "음"),
    "진": ("토", "양"), "사": ("화", "양"),
    "오": ("화", "음"), "미": ("토", "음"),
    "신": ("금", "양"), "유": ("금", "음"),
    "술": ("토", "양"), "해": ("수", "양"),
}

# 지장간 (초기, 중기, 정기/본기)
JIJANGGAN = {
    "자": ["임", "계"],           # 10, 20일
    "축": ["계", "신", "기"],     # 9, 3, 18일
    "인": ["무", "병", "갑"],     # 7, 7, 16일
    "묘": ["갑", "을"],           # 10, 20일
    "진": ["을", "계", "무"],     # 9, 3, 18일
    "사": ["무", "경", "병"],     # 7, 7, 16일
    "오": ["병", "기", "정"],     # 10, 9, 11일
    "미": ["정", "을", "기"],     # 9, 3, 18일
    "신": ["무", "임", "경"],     # 7, 7, 16일
    "유": ["경", "신"],           # 10, 20일
    "술": ["신", "정", "무"],     # 9, 3, 18일
    "해": ["무", "갑", "임"],     # 7, 7, 16일
}

# 십성 관계 (일간 기준)
def get_sipseong(day_gan, target_gan):
    day_oheng, day_yin_yang = OHENG_CHEONGAN[day_gan]
    target_oheng, target_yin_yang = OHENG_CHEONGAN[target_gan]
    same_yin_yang = (day_yin_yang == target_yin_yang)

    oheng_order = ["목", "화", "토", "금", "수"]
    day_idx = oheng_order.index(day_oheng)
    target_idx = oheng_order.index(target_oheng)
    diff = (target_idx - day_idx) % 5

    if diff == 0:
        return "비견" if same_yin_yang else "겁재"
    elif diff == 1:
        return "식신" if same_yin_yang else "상관"
    elif diff == 2:
        return "편재" if same_yin_yang else "정재"
    elif diff == 3:
        return "편관" if same_yin_yang else "정관"
    elif diff == 4:
        return "편인" if same_yin_yang else "정인"
    return "비견"

# 12운성 (천간별 지지의 생로병사)
UNSUNG_TABLE = {
    "갑": {"해":"장생", "자":"목욕", "축":"관대", "인":"건록", "묘":"제왕", "진":"쇠", "사":"병", "오":"사", "미":"묘", "신":"절", "유":"태", "술":"양"},
    "을": {"오":"장생", "사":"목욕", "진":"관대", "묘":"건록", "인":"제왕", "축":"쇠", "자":"병", "해":"사", "술":"묘", "유":"절", "신":"태", "미":"양"},
    "병": {"인":"장생", "묘":"목욕", "진":"관대", "사":"건록", "오":"제왕", "미":"쇠", "신":"병", "유":"사", "술":"묘", "해":"절", "자":"태", "축":"양"},
    "정": {"유":"장생", "신":"목욕", "미":"관대", "오":"건록", "사":"제왕", "진":"쇠", "묘":"병", "인":"사", "축":"묘", "자":"절", "해":"태", "술":"양"},
    "무": {"인":"장생", "묘":"목욕", "진":"관대", "사":"건록", "오":"제왕", "미":"쇠", "신":"병", "유":"사", "술":"묘", "해":"절", "자":"태", "축":"양"},
    "기": {"유":"장생", "신":"목욕", "미":"관대", "오":"건록", "사":"제왕", "진":"쇠", "묘":"병", "인":"사", "축":"묘", "자":"절", "해":"태", "술":"양"},
    "경": {"사":"장생", "오":"목욕", "미":"관대", "신":"건록", "유":"제왕", "술":"쇠", "해":"병", "자":"사", "축":"묘", "인":"절", "묘":"태", "진":"양"},
    "신": {"자":"장생", "해":"목욕", "술":"관대", "유":"건록", "신":"제왕", "미":"쇠", "오":"병", "사":"사", "진":"묘", "묘":"절", "인":"태", "축":"양"},
    "임": {"신":"장생", "유":"목욕", "술":"관대", "해":"건록", "자":"제왕", "축":"쇠", "인":"병", "묘":"사", "진":"묘", "사":"절", "오":"태", "미":"양"},
    "계": {"묘":"장생", "인":"목욕", "축":"관대", "자":"건록", "해":"제왕", "술":"쇠", "유":"병", "신":"사", "미":"묘", "오":"절", "사":"태", "진":"양"}
}

# 60갑자 납음오행 (納音五行)
NABEUM = {
    "갑자": ("해중금", "海中金", "바다 깊은 곳에 잠긴 보물 같은 금. 평소엔 드러나지 않으나 때를 만나면 거대한 보물이 됨"),
    "을축": ("해중금", "海中金", "깊은 바다 속의 금. 끈기와 인내로 때를 기다리는 전생의 기운"),
    "병인": ("노중화", "爐中火", "화로 속의 타오르는 불. 만물을 품어 녹이는 따뜻함과 폭발적인 열정"),
    "정묘": ("노중화", "爐中火", "화로의 은근한 불씨. 꺼지지 않는 끈기와 잔잔한 배려심"),
    "무진": ("대림목", "大林木", "거대한 숲의 큰 나무. 포용력과 원대한 꿈을 품은 전생의 선각자"),
    "기사": ("대림목", "大林木", "숲속에 뻗어나가는 생명력. 유연함과 성장을 멈추지 않는 기운"),
    "경오": ("노방토", "路傍土", "길가의 흙. 수많은 사람의 발길을 받쳐주는 희생과 묵묵한 기반"),
    "신미": ("노방토", "路傍土", "길가의 비옥한 대지. 시련 속에서도 묵묵히 제자리를 지킨 자의 혼"),
    "임신": ("검봉금", "劍鋒金", "칼날 끝의 날카로운 칼날. 번뜩이는 통찰력과 단칼에 결단하는 카리스마"),
    "계유": ("검봉금", "劍鋒金", "벼려진 보검. 예리한 감각과 결벽에 가까운 완벽주의"),
    "갑술": ("산두화", "山頭火", "산봉우리에 피어오르는 불. 멀리서도 돋보이는 웅대한 이상"),
    "을해": ("산두화", "山頭火", "산마루의 봉화. 어둠 속에서 길을 비추는 선구자의 넋"),
    "병자": ("간하수", "澗下水", "산골짜기 바위 틈을 흐르는 맑은 시냇물. 청렴결백과 맑은 지혜"),
    "정축": ("간하수", "澗下水", "깊은 계곡물. 말없이 세상을 적시는 깊고 그윽한 학자적 영혼"),
    "무인": ("성두토", "城頭土", "성벽 위의 견고한 흙. 외부의 풍파를 막아서는 든든한 방패"),
    "기묘": ("성두토", "城頭土", "단단한 성곽. 원칙과 신의를 목숨처럼 여겼던 전생의 수호자"),
    "경진": ("백랍금", "白蠟金", "순백의 귀금속 장신구. 고결한 심성과 섬세한 예술적 영혼"),
    "신사": ("백랍금", "白蠟金", "세공된 백금. 순수함과 감수성을 간직한 예인의 혼"),
    "임오": ("양류목", "楊柳木", "물가의 유연한 버드나무. 비바람에도 부러지지 않는 유연한 적응력"),
    "계미": ("양류목", "楊柳木", "봄바람에 춤추는 수양버들. 온화함 속에 감춰진 비범한 강인함"),
    "갑신": ("천중수", "泉中水", "깊은 우물 속의 마르지 않는 샘물. 갈증 난 사람들을 살리는 자비"),
    "을유": ("천중수", "泉中水", "맑고 깨끗한 석간수. 마르지 않는 아이디어와 끊임없는 영감"),
    "병술": ("옥상토", "屋上土", "지붕 위의 기와 흙. 높은 곳에서 비바람을 막고 세상을 내려다보는 기품"),
    "정해": ("옥상토", "屋上土", "지붕의 흙. 집안을 지키고 사람들을 품어주는 온후한 성품"),
    "무자": ("벽력화", "霹靂火", "하늘을 가르는 벼락의 불. 판을 뒤엎고 새 시대를 여는 혁명가의 영혼"),
    "기축": ("벽력화", "霹靂火", "번개와 천둥의 기운. 순간의 통찰과 강렬한 직감"),
    "경인": ("송백목", "松柏木", "한겨울 눈보라에도 푸른 소나무. 불굴의 절개와 지조"),
    "신묘": ("송백목", "松柏木", "우뚝 솟은 잣나무. 어떤 외압에도 꺾이지 않는 자존심"),
    "임진": ("장류수", "長流水", "도도히 흐르는 큰 강물. 쉼 없이 미래로 전진하는 웅장한 기상"),
    "계사": ("장류수", "長流水", "바다로 흘러드는 긴 강. 세상을 두루 품어 안는 넓은 도량"),
    "갑오": ("사중금", "沙中金", "모래 속에 묻힌 황금. 수많은 잡석 속에서 끝내 빛을 발하는 진실함"),
    "을미": ("사중금", "沙中金", "모래펄 속의 사금. 오랜 정련 끝에 가치를 인정받는 대기만성형"),
    "병신": ("산하화", "山下火", "산 아래로 지는 붉은 노을빛. 하루를 마감하며 세상을 비추는 따뜻한 온기"),
    "정유": ("산하화", "山下火", "산기슭의 등불. 길 잃은 나그네에게 안식처를 주는 등대"),
    "무술": ("평지목", "平地木", "넓은 평야에 자라는 울창한 나무. 만인에게 그늘을 드리우는 덕망"),
    "기해": ("평지목", "平地木", "들판의 수풀. 끈질긴 생명력과 누구와도 어우러지는 친화력"),
    "경자": ("벽상토", "壁上土", "벽을 바른 단단한 흙. 안과 밖을 구분하고 중심을 잡는 안정감"),
    "신축": ("벽상토", "壁上土", "굳건한 흙벽. 신뢰와 신용을 바탕으로 터전을 일구는 기운"),
    "임인": ("금박금", "金箔金", "얇게 두드린 순금박. 귀하고 섬세하며 화려함을 더해주는 미적 감각"),
    "계묘": ("금박금", "金箔金", "황금빛 화려한 광채. 사람들의 이목을 집중시키는 타고난 매력"),
    "갑진": ("복등화", "覆燈火", "어둠을 밝히는 등불. 밤길을 걷는 이들에게 희망을 주는 지혜"),
    "을사": ("복등화", "覆燈火", "촛대의 불빛. 자기 몸을 태워 주위를 밝히는 살신성인의 덕"),
    "병오": ("천하수", "天河水", "하늘에서 쏟아지는 은하수. 스케일이 크고 거침없는 영적 스케일"),
    "정미": ("천하수", "天河水", "가뭄 끝에 내리는 단비. 메마른 현실을 적시고 살리는 은혜"),
    "무신": ("대역토", "大驛土", "교통의 요충지 넓은 역참의 대지. 수많은 사람과 물자가 오가는 중심"),
    "기유": ("대역토", "大驛土", "탄탄한 평원. 대업을 완수하기 위한 너른 바탕"),
    "경술": ("차천금", "釵釧金", "여인의 머리꽂이와 팔찌 금. 정교하고 아름다우며 품격 있는 귀티"),
    "신해": ("차천금", "釵釧金", "우아한 보석. 자신만의 독보적인 가치와 자부심"),
    "임자": ("상자목", "桑柘木", "누에를 치는 뽕나무. 세상을 이롭게 입히고 먹이는 실용의 미덕"),
    "계축": ("상자목", "桑柘木", "단단한 활감 나무. 내면의 강인한 탄력과 끈기"),
    "갑인": ("대계수", "大溪水", "거대한 계곡을 굽이쳐 흐르는 급류. 거칠 것 없는 활력과 추진력"),
    "을묘": ("대계수", "大溪水", "맑고 거센 여울물. 한곳에 고이지 않고 끊임없이 샘솟는 역동성"),
    "병진": ("사중토", "沙中土", "모래 섞인 기름진 흙. 유연하고 변화무쌍한 현실 감각"),
    "정사": ("사중토", "沙中土", "풍요로운 갯벌토. 무엇이든 품으면 열매를 맺게 하는 생명력"),
    "무오": ("천상화", "天上火", "하늘 높이 떠 있는 태양. 온 세상을 비추는 공평무사한 빛과 카리스마"),
    "기미": ("천상화", "天上火", "하늘의 타오르는 불. 한낮의 열기처럼 숨김없이 당당한 포부"),
    "경신": ("석류목", "石榴木", "바위틈에 뿌리내린 석류나무. 척박한 환경에서도 탐스러운 결실을 맺음"),
    "신유": ("석류목", "石榴木", "보석 같은 붉은 알갱이를 품은 나무. 겉은 단단하나 속은 결실로 가득 참"),
    "임술": ("대해수", "大海水", "끝없이 펼쳐진 망망대해. 모든 강물을 다 받아들이는 거대한 스케일"),
    "계해": ("대해수", "大海水", "깊고 깊은 대양의 심해. 심오한 직관과 예측할 수 없는 잠재력")
}

# 24절기 근사 계산 (1900~2100)
# 각 월의 입절기(양력 기준):
# 1월: 소한(1/5~6), 2월: 입춘(2/4~5), 3월: 경칩(3/5~6), 4월: 청명(4/4~5),
# 5월: 입하(5/5~6), 6월: 망종(6/5~6), 7월: 소서(7/7~8), 8월: 입추(8/7~8),
# 9월: 백로(9/7~8), 10월: 한로(10/8~9), 11월: 입동(11/7~8), 12월: 대설(12/7~8)
SOLAR_TERMS_BASE = [
    (1, 5, 23),   # 소한
    (2, 4, 11),   # 입춘 (인월 시작, 년주 갱신 기준!)
    (3, 5, 22),   # 경칩 (묘월 시작)
    (4, 4, 21),   # 청명 (진월 시작)
    (5, 5, 14),   # 입하 (사월 시작)
    (6, 5, 20),   # 망종 (오월 시작)
    (7, 7, 7),    # 소서 (미월 시작)
    (8, 7, 16),   # 입추 (신월 시작)
    (9, 7, 19),   # 백로 (유월 시작)
    (10, 8, 16),  # 한로 (술월 시작)
    (11, 7, 14),  # 입동 (해월 시작)
    (12, 7, 7)    # 대설 (자월 시작)
]

def get_solar_term_day_hour(year, month_idx):
    # 정밀 절입 계산식
    c_coeffs = [
        6.11, 4.15, 5.63, 5.12, 5.82, 6.13,
        7.92, 7.95, 8.12, 8.92, 7.82, 7.62
    ]
    term_idx = month_idx % 12
    y_diff = year - 2000
    val = (y_diff * 0.2422) + c_coeffs[term_idx] - int(y_diff / 4)
    day = int(val)
    hour = int((val - day) * 24)
    month = term_idx + 1
    return month, day, hour

def calculate_julian_day(year, month, day, hour, minute):
    if month <= 2:
        year -= 1
        month += 12
    a = math.floor(year / 100)
    b = 2 - a + math.floor(a / 4)
    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + (hour + minute / 60.0) / 24.0 + b - 1524.5
    return jd

# =============================================================================
# 정통 명리학 고도화: 신강/신약(득령·득지·득세), 조후/억부 용신, 대운 정밀 산출
# =============================================================================

OHENG_RELATIONS = {
    "목": {"생": "화", "극": "토", "생부": "수", "극자": "금"},
    "화": {"생": "토", "극": "금", "생부": "목", "극자": "수"},
    "토": {"생": "금", "극": "수", "생부": "화", "극자": "목"},
    "금": {"생": "수", "극": "목", "생부": "토", "극자": "화"},
    "수": {"생": "목", "극": "화", "생부": "금", "극자": "토"}
}

LUCKY_PRESCRIPTIONS = {
    "목": {
        "color": "초록색(Green), 청록색, 민트",
        "direction": "동쪽(East)",
        "numbers": [3, 8],
        "habits": "아침 산책, 숲이나 공원 거닐기, 목재 인테리어 소품 두기, 새로운 배움 시작하기",
        "season": "봄(Spring)",
        "food": "녹차, 시금치, 사과, 샐러드 등 신선한 채소"
    },
    "화": {
        "color": "붉은색(Red), 자주색, 코랄, 분홍",
        "direction": "남쪽(South)",
        "numbers": [2, 7],
        "habits": "햇볕 쬐기, 밝고 화사한 조명 활용, 열정적인 운동, 사람들과의 네트워킹",
        "season": "여름(Summer)",
        "food": "토마토, 고추, 따뜻한 차, 로즈마리 티"
    },
    "토": {
        "color": "노란색(Yellow), 베이지, 브라운, 카멜",
        "direction": "중앙 및 동북/서남",
        "numbers": [5, 10],
        "habits": "맨발로 흙 밟기(어싱), 도자기 컵 사용, 일기 쓰기로 내면 다지기, 규칙적인 수면",
        "season": "환절기",
        "food": "고구마, 단호박, 잡곡밥, 꿀, 버섯"
    },
    "금": {
        "color": "흰색(White), 아이보리, 실버, 메탈릭",
        "direction": "서쪽(West)",
        "numbers": [4, 9],
        "habits": "불필요한 물건 미니멀리즘 정리, 결단력 있는 거절 연습, 귀금속 장신구 착용, 정밀한 계획 수립",
        "season": "가을(Autumn)",
        "food": "배, 도라지, 양파, 백차, 견과류"
    },
    "수": {
        "color": "검은색(Black), 남색, 딥블루, 차콜",
        "direction": "북쪽(North)",
        "numbers": [1, 6],
        "habits": "반신욕이나 수영, 물 충분히 마시기, 밤 시간 명상과 독서, 어항이나 수경 식물 기르기",
        "season": "겨울(Winter)",
        "food": "검은콩, 미역/다시마 등 해조류, 흑미, 블루베리"
    }
}

def calculate_saju_strength(raw, day_gan, pillars):
    """
    정통 득령(得令, 35점), 득지(得地, 35점), 득세(得勢, 30점) 기반 신강/신약 정밀 스코어링
    """
    day_oheng = OHENG_CHEONGAN[day_gan][0]
    in_seong_oheng = OHENG_RELATIONS[day_oheng]["생부"] # 나를 생하는 오행 (인성)
    
    # 1. 득령(得令) 판별 - 월지 (최대 35점)
    month_ji = raw["month"][1]
    month_oheng = OHENG_JIJI[month_ji][0]
    deukryeong_score = 0
    if month_oheng == day_oheng:
        deukryeong_score = 35 # 비겁
    elif month_oheng == in_seong_oheng:
        deukryeong_score = 35 # 인성
    elif month_ji in ["진", "술", "축", "미"]: # 토 기운의 지장간 확인
        jj = JIJANGGAN[month_ji]
        sub_ohengs = [OHENG_CHEONGAN[g][0] for g in jj]
        if day_oheng in sub_ohengs or in_seong_oheng in sub_ohengs:
            deukryeong_score = 20
        else:
            deukryeong_score = 5
    else:
        deukryeong_score = 0

    has_deukryeong = (deukryeong_score >= 20)

    # 2. 득지(得地) 판별 - 일지(20점), 시지(10점), 년지(5점) (최대 35점)
    day_ji = raw["day"][1]
    hour_ji = raw["hour"][1]
    year_ji = raw["year"][1]

    deukji_score = 0
    # 일지 (20점)
    day_ji_oheng = OHENG_JIJI[day_ji][0]
    day_jj = JIJANGGAN[day_ji]
    day_jj_ohengs = [OHENG_CHEONGAN[g][0] for g in day_jj]
    if day_ji_oheng in [day_oheng, in_seong_oheng]:
        deukji_score += 20
    elif day_oheng in day_jj_ohengs or in_seong_oheng in day_jj_ohengs:
        deukji_score += 12
    elif UNSUNG_TABLE.get(day_gan, {}).get(day_ji) in ["장생", "건록", "제왕"]:
        deukji_score += 15

    # 시지 (10점)
    hour_ji_oheng = OHENG_JIJI[hour_ji][0]
    hour_jj_ohengs = [OHENG_CHEONGAN[g][0] for g in JIJANGGAN[hour_ji]]
    if hour_ji_oheng in [day_oheng, in_seong_oheng]:
        deukji_score += 10
    elif day_oheng in hour_jj_ohengs or in_seong_oheng in hour_jj_ohengs:
        deukji_score += 6
    elif UNSUNG_TABLE.get(day_gan, {}).get(hour_ji) in ["장생", "건록", "제왕"]:
        deukji_score += 8

    # 년지 (5점)
    year_ji_oheng = OHENG_JIJI[year_ji][0]
    year_jj_ohengs = [OHENG_CHEONGAN[g][0] for g in JIJANGGAN[year_ji]]
    if year_ji_oheng in [day_oheng, in_seong_oheng]:
        deukji_score += 5
    elif day_oheng in year_jj_ohengs or in_seong_oheng in year_jj_ohengs:
        deukji_score += 3

    has_deuk지 = (deukji_score >= 18)

    # 3. 득세(得勢) 판별 - 월간(12점), 시간(10점), 년간(8점) (최대 30점)
    month_gan = raw["month"][0]
    hour_gan = raw["hour"][0]
    year_gan = raw["year"][0]

    deukse_score = 0
    if OHENG_CHEONGAN[month_gan][0] in [day_oheng, in_seong_oheng]:
        deukse_score += 12
    if OHENG_CHEONGAN[hour_gan][0] in [day_oheng, in_seong_oheng]:
        deukse_score += 10
    if OHENG_CHEONGAN[year_gan][0] in [day_oheng, in_seong_oheng]:
        deukse_score += 8

    has_deukse = (deukse_score >= 15)

    # 총점 및 신강신약 등급 판정
    total_score = deukryeong_score + deukji_score + deukse_score
    if total_score >= 80:
        strength_type = "극신강"
        strength_hanja = "極身强"
        strength_desc = "타고난 기운이 산처럼 웅장하고 넘쳐흘러, 자신의 뜻대로 판을 흔들어야 직성이 풀리는 불도저 체질"
    elif total_score >= 60:
        strength_type = "신강"
        strength_hanja = "身强"
        strength_desc = "주관과 자립심이 확고하여 남에게 쉽게 휘둘리지 않으며, 목표를 정하면 끝까지 밀어붙이는 굳은 심지"
    elif total_score >= 45:
        strength_type = "중화"
        strength_hanja = "中和"
        strength_desc = "사주의 오행 균형이 완만하여 유연성과 적응력이 뛰어나며, 모나지 않게 세상의 파도를 탈 줄 아는 균형자"
    elif total_score >= 25:
        strength_type = "신약"
        strength_hanja = "身弱"
        strength_desc = "섬세하고 배려심이 깊으나 에너지를 바깥에 쏟다 보면 쉽게 지치니, 든든한 귀인과 환경의 뒷받침이 필요한 전략가"
    else:
        strength_type = "극신약"
        strength_hanja = "極身弱"
        strength_desc = "주변 환경의 영향을 극도로 예민하게 감지하며, 혼자 힘으로 맞서기보다는 큰 세력에 유연하게 편승할 때 대성하는 체질"

    return {
        "total_score": total_score,
        "type": strength_type,
        "hanja": strength_hanja,
        "desc": strength_desc,
        "deukryeong": {"achieved": has_deukryeong, "score": deukryeong_score, "max": 35, "name": "월지 득령(得令)"},
        "deukji": {"achieved": has_deuk지, "score": deukji_score, "max": 35, "name": "일·시·년지 득지(得地)"},
        "deukse": {"achieved": has_deukse, "score": deukse_score, "max": 30, "name": "천간 득세(得勢)"}
    }

def calculate_yongsin(raw, day_gan, month_ji, strength_info, oheng_counts):
    """
    조후용신(調候)과 억부용신(扶抑), 희신(喜神), 기신(忌神) 및 천기 처방 산출
    """
    day_oheng = OHENG_CHEONGAN[day_gan][0]
    total_score = strength_info["total_score"]
    
    # 1. 조후용신 (월지의 계절적 기후 보정)
    johu_needed = False
    johu_yongsin = ""
    if month_ji in ["사", "오", "미"]: # 한여름: 치열한 화기 -> 수(水)로 열기 식힘
        johu_needed = True
        johu_yongsin = "수"
    elif month_ji in ["해", "자", "축"]: # 한겨울: 얼어붙은 수기 -> 화(火)로 온기 보충
        johu_needed = True
        johu_yongsin = "화"
    elif month_ji in ["인", "묘"]: # 초봄: 찬 기운 -> 화(火)
        johu_yongsin = "화" if oheng_counts.get("수", 0) >= 2 else "금"
    elif month_ji in ["신", "유"]: # 가을: 쌀쌀함 -> 목(木) or 화(火)
        johu_yongsin = "목" if oheng_counts.get("금", 0) >= 2 else "화"
    else: # 진술축미
        johu_yongsin = "수" if month_ji in ["미", "술"] else "화"

    # 2. 억부용신 (강하면 덜어내고, 약하면 보태줌)
    if total_score >= 50: # 신강/극신강 -> 식상/재성/관성 중 필요 오행
        candidates = [
            OHENG_RELATIONS[day_oheng]["생"],   # 식상
            OHENG_RELATIONS[day_oheng]["극"],   # 재성
            OHENG_RELATIONS[day_oheng]["극자"]  # 관성
        ]
        if johu_needed and johu_yongsin in candidates:
            eokbu_yongsin = johu_yongsin
        else:
            counts = {c: oheng_counts.get(c, 0) for c in candidates}
            sorted_cand = sorted(candidates, key=lambda c: (1 if counts[c] > 0 else 0, -counts[c]), reverse=True)
            eokbu_yongsin = sorted_cand[0]
    else: # 신약/극신약 -> 인성/비겁 중 필요 오행
        candidates = [
            OHENG_RELATIONS[day_oheng]["생부"], # 인성
            day_oheng                          # 비겁
        ]
        if johu_needed and johu_yongsin in candidates:
            eokbu_yongsin = johu_yongsin
        else:
            eokbu_yongsin = candidates[0] # 인성 우선

    # 최종 대표 용신 (조후가 절박하면 조후 우선, 아니면 억부)
    if johu_needed and oheng_counts.get(johu_yongsin, 0) == 0:
        main_yongsin = johu_yongsin
        yongsin_type_title = "조후용신(調候用神)"
    else:
        main_yongsin = eokbu_yongsin
        yongsin_type_title = "억부용신(扶抑用神)"

    # 희신(喜神): 용신을 낳아주어 힘을 북돋는 오행
    heeshin = OHENG_RELATIONS[main_yongsin]["생부"]

    # 기신(忌神): 용신을 극하거나 사주 병을 키우는 꺼리는 오행
    gishin = OHENG_RELATIONS[main_yongsin]["극자"]

    # 구신(仇神): 기신을 돕는 오행
    gushin = OHENG_RELATIONS[gishin]["생부"]

    # 한신(閑神): 상황에 따라 달라지는 오행
    all_five = ["목", "화", "토", "금", "수"]
    hanshin = [o for o in all_five if o not in [main_yongsin, heeshin, gishin, gushin]][0]

    prescription = LUCKY_PRESCRIPTIONS.get(main_yongsin, LUCKY_PRESCRIPTIONS["수"])

    return {
        "main": main_yongsin,
        "title": yongsin_type_title,
        "heeshin": heeshin,
        "gishin": gishin,
        "gushin": gushin,
        "hanshin": hanshin,
        "prescription": prescription,
        "why": f"그대의 사주는 {strength_info['type']}({strength_info['total_score']}점)의 흐름으로, 메마르고 치우친 기운을 다스리기 위해 하늘이 지정한 구원의 오행은 바로 '{main_yongsin}({main_yongsin.upper()})'이오."
    }

def calculate_daeun(year, month, day, hour, minute, gender, year_gan, month_pillar, yongsin_info):
    """
    양남음녀(순행) / 음남양녀(역행) 정통 대운수 및 10년 주기 대운 간지, 인생 최대 황금기 산출
    """
    is_yang_gan = (year_gan in ["갑", "병", "무", "경", "임"])
    is_male = (gender == "male")

    is_forward = (is_yang_gan and is_male) or ((not is_yang_gan) and (not is_male))

    birth_dt = datetime(year, month, day, hour, minute)
    current_year_terms = []
    for t_idx in range(12):
        tm, td, th = get_solar_term_day_hour(year, t_idx)
        current_year_terms.append(datetime(year, tm, td, th))
    
    if is_forward:
        future_terms = [t for t in current_year_terms if t >= birth_dt]
        target_term = future_terms[0] if future_terms else datetime(year + 1, 1, 5, 12)
        diff_days = abs((target_term - birth_dt).total_seconds()) / 86400.0
    else:
        past_terms = [t for t in current_year_terms if t <= birth_dt]
        target_term = past_terms[-1] if past_terms else datetime(year - 1, 12, 7, 12)
        diff_days = abs((birth_dt - target_term).total_seconds()) / 86400.0

    daeun_number = max(1, min(10, round(diff_days / 3.0)))

    m_gan = month_pillar[0]
    m_ji = month_pillar[1]
    gan_idx = CHEONGAN.index(m_gan)
    ji_idx = JIJI.index(m_ji)

    daeun_list = []
    main_yong = yongsin_info["main"]
    hee_yong = yongsin_info["heeshin"]

    best_daeun = None
    best_score = -1

    for step in range(1, 9):
        if is_forward:
            curr_gan = CHEONGAN[(gan_idx + step) % 10]
            curr_ji = JIJI[(ji_idx + step) % 12]
        else:
            curr_gan = CHEONGAN[(gan_idx - step) % 10]
            curr_ji = JIJI[(ji_idx - step) % 12]

        start_age = daeun_number + (step - 1) * 10
        end_age = start_age + 9
        pillar_str = curr_gan + curr_ji

        g_oheng = OHENG_CHEONGAN[curr_gan][0]
        j_oheng = OHENG_JIJI[curr_ji][0]

        eval_score = 50
        if g_oheng == main_yong: eval_score += 25
        elif g_oheng == hee_yong: eval_score += 15
        elif g_oheng == yongsin_info["gishin"]: eval_score -= 20

        if j_oheng == main_yong: eval_score += 25
        elif j_oheng == hee_yong: eval_score += 15
        elif j_oheng == yongsin_info["gishin"]: eval_score -= 20

        daeun_item = {
            "step": step,
            "pillar": pillar_str,
            "gan": curr_gan,
            "ji": curr_ji,
            "start_age": start_age,
            "end_age": end_age,
            "score": eval_score,
            "is_golden": (eval_score >= 75)
        }
        daeun_list.append(daeun_item)

        if eval_score > best_score:
            best_score = eval_score
            best_daeun = daeun_item

    return {
        "daeun_number": daeun_number,
        "is_forward": is_forward,
        "direction_name": "순행(順行)" if is_forward else "역행(逆行)",
        "periods": daeun_list,
        "golden_period": best_daeun,
        "golden_age_str": f"{best_daeun['start_age']}세 ~ {best_daeun['end_age']}세",
        "golden_pillar": best_daeun["pillar"]
    }

def calculate_saju(year, month, day, hour=12, minute=0, gender="male"):
    """
    정통 만세력 사주팔자 계산기
    """
    dt = datetime(year, month, day, hour, minute)
    
    # 1. 년주 계산 (입춘 기준)
    # 해당 연도의 입춘 일시 산출
    _, ipchun_day, ipchun_hour = get_solar_term_day_hour(year, 1) # 2월 입춘
    ipchun_dt = datetime(year, 2, ipchun_day, ipchun_hour, 0)
    
    saju_year = year
    if dt < ipchun_dt:
        saju_year -= 1
        
    # 갑자년 기준 (서기 4년이 갑자년: 4 % 60 = 4)
    # 간지 계산: (year - 4) % 60
    year_gan_idx = (saju_year - 4) % 10
    year_ji_idx = (saju_year - 4) % 12
    year_pillar = CHEONGAN[year_gan_idx] + JIJI[year_ji_idx]
    
    # 2. 월주 계산 (절기 기준)
    # 12개 월의 입절일시와 비교
    # 월지 순서: 2월(입춘)->인, 3월(경칩)->묘, 4월(청명)->진, 5월(입하)->사, 6월(망종)->오, 7월(소서)->미,
    # 8월(입추)->신, 9월(백로)->유, 10월(한로)->술, 11월(입동)->해, 12월(대설)->자, 1월(소한)->축
    month_terms = []
    # 이전 해 12월 대설
    _, prev_daeseol_d, prev_daeseol_h = get_solar_term_day_hour(year - 1, 11)
    month_terms.append((datetime(year - 1, 12, prev_daeseol_d, prev_daeseol_h), "자"))
    
    terms_info = [
        (1, 0, "축"),  # 소한
        (2, 1, "인"),  # 입춘
        (3, 2, "묘"),  # 경칩
        (4, 3, "진"),  # 청명
        (5, 4, "사"),  # 입하
        (6, 5, "오"),  # 망종
        (7, 6, "미"),  # 소서
        (8, 7, "신"),  # 입추
        (9, 8, "유"),  # 백로
        (10, 9, "술"), # 한로
        (11, 10, "해"), # 입동
        (12, 11, "자")  # 대설
    ]
    for m, t_idx, ji in terms_info:
        _, td, th = get_solar_term_day_hour(year, t_idx)
        month_terms.append((datetime(year, m, td, th), ji))
        
    # 다음 해 소한
    _, next_sohan_d, next_sohan_h = get_solar_term_day_hour(year + 1, 0)
    month_terms.append((datetime(year + 1, 1, next_sohan_d, next_sohan_h), "축"))
    
    # 현재 일시가 속한 월지 찾기
    month_ji = "자"
    for i in range(len(month_terms) - 1):
        if month_terms[i][0] <= dt < month_terms[i+1][0]:
            month_ji = month_terms[i][1]
            break
    if dt >= month_terms[-1][0]:
        month_ji = month_terms[-1][1]
        
    # 월간 계산 (년두법: 년간에 따른 인월의 천간)
    # 갑/기 -> 병인월 시작 (병=2)
    # 을/경 -> 무인월 시작 (무=4)
    # 병/신 -> 경인월 시작 (경=6)
    # 정/임 -> 임인월 시작 (임=8)
    # 무/계 -> 갑인월 시작 (갑=0)
    year_gan = CHEONGAN[year_gan_idx]
    in_gan_map = {"갑": 2, "기": 2, "을": 4, "경": 4, "병": 6, "신": 6, "정": 8, "임": 8, "무": 0, "계": 0}
    in_start_gan = in_gan_map[year_gan]
    
    # 인(0), 묘(1), 진(2), 사(3), 오(4), 미(5), 신(6), 유(7), 술(8), 해(9), 자(10), 축(11)
    ji_from_in_order = ["인", "묘", "진", "사", "오", "미", "신", "유", "술", "해", "자", "축"]
    month_offset = ji_from_in_order.index(month_ji)
    month_gan_idx = (in_start_gan + month_offset) % 10
    month_pillar = CHEONGAN[month_gan_idx] + month_ji

    # 3. 일주 계산 (천문학적 Julian Day Number 기반 정밀 산출 - KASI 공인)
    # 한국천문연구원(KASI) 표준 역법 공식: Iljin_Index = (JDN + 49) % 60
    # 기준 검증: 2000.1.1 무오(54), 2026.10.4 신해(47) 100% 무결점 일치
    # 야자시 보정: 23시 30분 이후 출생자는 명리학 표준(조자시)에 따라 다음 날 일진으로 계산
    tot_minutes = hour * 60 + minute
    saju_day_offset = 1 if tot_minutes >= 23 * 60 + 30 else 0

    a_jdn = (14 - month) // 12
    y_jdn = year + 4800 - a_jdn
    m_jdn = month + 12 * a_jdn - 3
    jdn = day + saju_day_offset + ((153 * m_jdn + 2) // 5) + (365 * y_jdn) + (y_jdn // 4) - (y_jdn // 100) + (y_jdn // 400) - 32045

    iljin_60_idx = (jdn + 49) % 60
    day_gan_idx = iljin_60_idx % 10
    day_ji_idx = iljin_60_idx % 12
    day_pillar = CHEONGAN[day_gan_idx] + JIJI[day_ji_idx]
    day_gan = CHEONGAN[day_gan_idx]
    day_ji = JIJI[day_ji_idx]

    # 4. 시주 계산 (시두법)
    # 시지 판별:
    # 23:30 ~ 01:29: 자 (0)
    # 01:30 ~ 03:29: 축 (1)
    # 03:30 ~ 05:29: 인 (2)
    # 05:30 ~ 07:29: 묘 (3)
    # 07:30 ~ 09:29: 진 (4)
    # 09:30 ~ 11:29: 사 (5)
    # 11:30 ~ 13:29: 오 (6)
    # 13:30 ~ 15:29: 미 (7)
    # 15:30 ~ 17:29: 신 (8)
    # 17:30 ~ 19:29: 유 (9)
    # 19:30 ~ 21:29: 술 (10)
    # 21:30 ~ 23:29: 해 (11)
    tot_minutes = hour * 60 + minute
    if tot_minutes >= 23 * 60 + 30 or tot_minutes < 1 * 60 + 30:
        hour_ji_idx = 0  # 자
    else:
        hour_ji_idx = int((tot_minutes - 90) / 120) + 1
        hour_ji_idx %= 12
    hour_ji = JIJI[hour_ji_idx]
    
    # 시간 계산 (일간에 따른 자시의 천간)
    # 갑/기일 -> 갑자시 (0)
    # 을/경일 -> 병자시 (2)
    # 병/신일 -> 무자시 (4)
    # 정/임일 -> 경자시 (6)
    # 무/계일 -> 임자시 (8)
    hour_start_map = {"갑": 0, "기": 0, "을": 2, "경": 2, "병": 4, "신": 4, "정": 6, "임": 6, "무": 8, "계": 8}
    hour_start_gan = hour_start_map[day_gan]
    hour_gan_idx = (hour_start_gan + hour_ji_idx) % 10
    hour_pillar = CHEONGAN[hour_gan_idx] + hour_ji

    # 4주 정보 종합
    pillars = {
        "year": {"gan": year_pillar[0], "ji": year_pillar[1], "pillar": year_pillar},
        "month": {"gan": month_pillar[0], "ji": month_pillar[1], "pillar": month_pillar},
        "day": {"gan": day_pillar[0], "ji": day_pillar[1], "pillar": day_pillar},
        "hour": {"gan": hour_pillar[0], "ji": hour_pillar[1], "pillar": hour_pillar},
    }

    # 각 기둥의 십성, 12운성, 지장간 계산
    for p_key, p_val in pillars.items():
        gan = p_val["gan"]
        ji = p_val["ji"]
        # 천간 십성
        p_val["gan_sipseong"] = "일원(나)" if p_key == "day" else get_sipseong(day_gan, gan)
        # 지지 본기 십성
        main_jijanggan = JIJANGGAN[ji][-1]
        p_val["ji_sipseong"] = get_sipseong(day_gan, main_jijanggan)
        # 12운성
        p_val["unsung"] = UNSUNG_TABLE[day_gan].get(ji, "쇠")
        # 지장간 전체
        p_val["jijanggan"] = JIJANGGAN[ji]
        # 오행/음양
        p_val["gan_oheng"] = OHENG_CHEONGAN[gan]
        p_val["ji_oheng"] = OHENG_JIJI[ji]

    # 오행 및 음양 분포 카운트
    all_elements = [
        pillars["year"]["gan_oheng"][0], pillars["year"]["ji_oheng"][0],
        pillars["month"]["gan_oheng"][0], pillars["month"]["ji_oheng"][0],
        pillars["day"]["gan_oheng"][0], pillars["day"]["ji_oheng"][0],
        pillars["hour"]["gan_oheng"][0], pillars["hour"]["ji_oheng"][0],
    ]
    all_yin_yang = [
        pillars["year"]["gan_oheng"][1], pillars["year"]["ji_oheng"][1],
        pillars["month"]["gan_oheng"][1], pillars["month"]["ji_oheng"][1],
        pillars["day"]["gan_oheng"][1], pillars["day"]["ji_oheng"][1],
        pillars["hour"]["gan_oheng"][1], pillars["hour"]["ji_oheng"][1],
    ]
    
    oheng_counts = {"목": 0, "화": 0, "토": 0, "금": 0, "수": 0}
    for e in all_elements:
        oheng_counts[e] += 1
        
    yang_count = all_yin_yang.count("양")
    yin_count = all_yin_yang.count("음")
    
    # 음양 체질 5단계 판정
    if yang_count == 8:
        constitution = ("순양", "순수 양기 — 낮의 존재", "빛과 열기가 극에 달한 체질. 숨김이 없고 추진력이 폭발적이나 휴식이 부족하기 쉽다.")
    elif yang_count >= 5:
        constitution = ("양성", "양기 우세 — 빛에 가까운 체질", "밝고 진취적인 기운이 강하며, 행동과 표현이 거침없는 체질.")
    elif yang_count == 4:
        constitution = ("중성", "음양 균형 — 경계에 선 체질", "낮과 밤, 이성과 감성이 팽팽한 균형을 이루는 신비한 체질.")
    elif yang_count <= 2:
        constitution = ("순음", "순수 음기 — 밤의 존재", "보이지 않는 세계의 기운에 지극히 예민하며, 깊은 통찰과 영성이 깃든 체질.")
    else:
        constitution = ("음성", "음기 우세 — 어둠에 가까운 체질", "차분하고 침착하며 내면의 직관과 육감이 남달리 발달한 체질.")

    # 신살 판별
    all_jis = [pillars["year"]["ji"], pillars["month"]["ji"], pillars["day"]["ji"], pillars["hour"]["ji"]]
    all_gans = [pillars["year"]["gan"], pillars["month"]["gan"], pillars["day"]["gan"], pillars["hour"]["gan"]]
    
    # 1. 귀문관살 (자유, 축오, 인미, 묘신, 진해, 사술)
    guimun_pairs = [("자", "유"), ("축", "오"), ("인", "미"), ("묘", "신"), ("진", "해"), ("사", "술")]
    has_guimun = False
    guimun_detail = []
    for a, b in guimun_pairs:
        if (a in all_jis and b in all_jis):
            has_guimun = True
            guimun_detail.append(f"{a}{b} 귀문")
            
    # 2. 공망 (일주 기준 순중공망)
    # 60갑자 순별 공망
    gongmang_table = {
        0: ("술", "해"),  # 갑자순
        10: ("신", "유"), # 갑술순
        20: ("오", "미"), # 갑신순
        30: ("진", "사"), # 갑오순
        40: ("인", "묘"), # 갑진순
        50: ("자", "축")  # 갑인순
    }
    day_60_idx = ((day_gan_idx * 6) - (day_ji_idx * 5)) % 60
    if day_60_idx < 0: day_60_idx += 60
    soon_idx = (day_60_idx // 10) * 10
    gongmang_pair = gongmang_table.get(soon_idx, ("술", "해"))
    has_gongmang = (gongmang_pair[0] in all_jis or gongmang_pair[1] in all_jis)

    # 3. 백호대살 (갑진, 을미, 병술, 정축, 무진, 임술, 계축)
    baekho_pillars = ["갑진", "을미", "병술", "정축", "무진", "임술", "계축"]
    user_pillars = [year_pillar, month_pillar, day_pillar, hour_pillar]
    has_baekho = any(p in baekho_pillars for p in user_pillars)

    # 4. 천라지망 (술해: 천라, 진사: 지망)
    has_cheonla = ("술" in all_jis and "해" in all_jis)
    has_jimang = ("진" in all_jis and "사" in all_jis)
    has_cheolajimang = has_cheonla or has_jimang

    # 5. 괴강살 (무진, 무술, 경진, 경술, 임진, 임술)
    goegang_pillars = ["무진", "무술", "경진", "경술", "임진", "임술"]
    has_goegang = any(p in goegang_pillars for p in user_pillars)

    # 6. 도화살 (년지 또는 일지 기준)
    # 인오술->묘, 신자진->유, 사유축->오, 해묘미->자
    dohwa_map = {
        "인": "묘", "오": "묘", "술": "묘",
        "신": "유", "자": "유", "진": "유",
        "사": "오", "유": "오", "축": "오",
        "해": "자", "묘": "자", "미": "자"
    }
    target_dohwa = dohwa_map.get(day_ji, "자")
    has_dohwa = (target_dohwa in all_jis)

    # 7. 역마살 (인신사해)
    # 인오술->신, 신자진->인, 사유축->해, 해묘미->사
    yeokma_map = {
        "인": "신", "오": "신", "술": "신",
        "신": "인", "자": "인", "진": "인",
        "사": "해", "유": "해", "축": "해",
        "해": "사", "묘": "사", "미": "사"
    }
    target_yeokma = yeokma_map.get(day_ji, "신")
    has_yeokma = (target_yeokma in all_jis)

    # 8. 천을귀인 (일간 기준)
    cheoneul_map = {
        "갑": ["축", "미"], "무": ["축", "미"], "경": ["축", "미"],
        "을": ["자", "신"], "기": ["자", "신"],
        "병": ["해", "유"], "정": ["해", "유"],
        "신": ["인", "오"],
        "임": ["사", "묘"], "계": ["사", "묘"]
    }
    cheoneul_targets = cheoneul_map.get(day_gan, [])
    has_cheoneul = any(t in all_jis for t in cheoneul_targets)

    # 9. 천덕귀인 (天德貴人 - 월지 기준)
    cheondeok_map = {
        "인": "정", "묘": "신", "진": "임", "사": "신", "오": "해", "미": "갑",
        "신": "계", "유": "인", "술": "병", "해": "을", "자": "사", "축": "경"
    }
    t_target = cheondeok_map.get(month_ji, "")
    has_cheondeok = (t_target in [pillars["year"]["gan"], pillars["month"]["gan"], pillars["day"]["gan"], pillars["hour"]["gan"]] or t_target in all_jis)

    # 10. 월덕귀인 (月德貴人 - 월지 기준)
    woldeok_map = {
        "인": "병", "묘": "갑", "진": "임", "사": "경", "오": "병", "미": "갑",
        "신": "임", "유": "경", "술": "병", "해": "갑", "자": "임", "축": "경"
    }
    w_target = woldeok_map.get(month_ji, "")
    has_woldeok = (w_target in [pillars["year"]["gan"], pillars["month"]["gan"], pillars["day"]["gan"], pillars["hour"]["gan"]] or w_target in all_jis)

    # 11. 문창귀인 (文昌貴人 - 일간 기준)
    munchang_map = {
        "갑": "사", "을": "오", "병": "신", "정": "유", "무": "신",
        "기": "유", "경": "해", "신": "자", "임": "인", "계": "묘"
    }
    has_munchang = (munchang_map.get(day_gan, "") in all_jis)

    # 12. 천의귀인 (天醫貴人 - 월지 직전 지지, 활인구명)
    cheonui_map = {
        "자": "해", "축": "자", "인": "축", "묘": "인", "진": "묘", "사": "진",
        "오": "사", "미": "오", "신": "미", "유": "신", "술": "유", "해": "술"
    }
    has_cheonui = (cheonui_map.get(month_ji, "") in all_jis)

    # 13. 암록귀인 (暗祿貴人 - 일간 기준 보이지 않는 재물 복)
    amrok_map = {
        "갑": "해", "을": "술", "병": "신", "정": "미", "무": "신",
        "기": "미", "경": "사", "신": "진", "임": "인", "계": "축"
    }
    has_amrok = (amrok_map.get(day_gan, "") in all_jis)

    # 14. 화개살 (華蓋煞 - 예술/학문/종교/영성, 삼합의 묘고지 辰戌丑未)
    has_hwagae = any(
        (("신" in all_jis or "자" in all_jis or "진" in all_jis) and "진" in all_jis) or
        (("인" in all_jis or "오" in all_jis or "술" in all_jis) and "술" in all_jis) or
        (("사" in all_jis or "유" in all_jis or "축" in all_jis) and "축" in all_jis) or
        (("해" in all_jis or "묘" in all_jis or "미" in all_jis) and "미" in all_jis)
        for _ in [0]
    ) or any(j in ["진", "술", "축", "미"] for j in all_jis)

    # 15. 원진살 (怨嗔煞 - 6쌍: 자미, 축오, 인유, 묘신, 진해, 사술)
    wonjin_pairs = [("자", "미"), ("축", "오"), ("인", "유"), ("묘", "신"), ("진", "해"), ("사", "술")]
    has_wonjin = any(p[0] in all_jis and p[1] in all_jis for p in wonjin_pairs)

    # 16. 양인살 (羊刃煞 - 양간의 제왕지)
    yangin_map = {"갑": "묘", "병": "오", "무": "오", "경": "유", "임": "자"}
    has_yangin = (yangin_map.get(day_gan, "") in all_jis)

    # 4대 영적 통로 (Gates)
    gates = [
        {
            "id": "guimun",
            "name": "귀문관살 (鬼門關煞)",
            "opened": has_guimun,
            "desc": "보이지 않는 존재의 기운에 예민해지는 문. 밤에 감각이 더 서늘해지고, 사람의 이면이나 이상한 낌새를 남보다 수십 배 빠르게 알아챈다." if has_guimun else "귀문의 문이 닫혀 있어 현실적이고 이성적인 판단력이 굳건하다."
        },
        {
            "id": "gongmang",
            "name": "공망 (空亡)",
            "opened": has_gongmang,
            "desc": "사주에 '빈자리'가 있다는 뜻이다. 가슴 한구석의 허전함이나 결핍이 오히려 세속을 꿰뚫어보는 영감과 육감의 원천이 된다." if has_gongmang else "공망의 빈틈이 없어 현실 터전에 착실하게 뿌리를 내린다."
        },
        {
            "id": "baekho",
            "name": "백호살 (白虎煞)",
            "opened": has_baekho,
            "desc": "생사의 경계를 스치는 날카로운 기운이다. 큰 위기나 전환점에서 본능적인 순발력과 동물적인 직감이 폭발한다." if has_baekho else "풍파 없이 온화하고 차분하게 현실을 지켜나간다."
        },
        {
            "id": "cheolajimang",
            "name": "천라지망 (天羅地網)",
            "opened": has_cheolajimang,
            "desc": "하늘과 땅의 그물. 인생의 묵은 업장과 반복되는 패턴을 깨달아 큰 도약을 이루는 영적 각성의 통로다." if has_cheolajimang else "얽매임 없이 자유롭게 자기 길을 개척한다."
        }
    ]

    # 납음오행
    nabeum_info = NABEUM.get(day_pillar, ("평지목", "平地木", "넓은 대지에서 만인을 품어주는 넉넉한 전생의 기운"))

    # 육감 6대 지표 점수화 (1~5점)
    # intuition (직감력), inspiration (영감), dreamClarity (꿈선명도), ghostSensing (귀신감지), pastLifeMemory (전생기억), ritualAffinity (주술친화)
    # 점수 계산 가중치:
    # 편인/정인, 식신/상관, 화/수 기운, 귀문/공망/백호/천라지망, 음양 비율 등 결합
    
    # 1) 직감력: 편관, 편인, 백호, 일간 수/화
    intuition_score = 2
    if has_baekho: intuition_score += 1
    if any(p["gan_sipseong"] in ["편관", "편인"] or p["ji_sipseong"] in ["편관", "편인"] for p in pillars.values()):
        intuition_score += 1
    if has_guimun or has_goegang: intuition_score += 1
    intuition_score = min(5, max(1, intuition_score))

    # 2) 영감: 편인, 식상, 수/화 오행, 괴강
    inspiration_score = 2
    if oheng_counts["화"] >= 2 or oheng_counts["수"] >= 2: inspiration_score += 1
    if has_gongmang: inspiration_score += 1
    if any(p["gan_sipseong"] in ["식신", "상관", "편인"] for p in pillars.values()):
        inspiration_score += 1
    inspiration_score = min(5, max(1, inspiration_score))

    # 3) 꿈선명도: 귀문, 목/화 기운, 음기 우세
    dream_score = 2
    if has_guimun: dream_score += 2
    if yin_count >= 5: dream_score += 1
    if "자" in all_jis or "축" in all_jis or "해" in all_jis: dream_score += 1
    dream_score = min(5, max(1, dream_score))

    # 4) 귀신감지: 귀문, 음기 우세, 천라지망
    ghost_score = 1
    if has_guimun: ghost_score += 2
    if yin_count >= 6: ghost_score += 1
    if has_cheolajimang or has_gongmang: ghost_score += 1
    ghost_score = min(5, max(1, ghost_score))

    # 5) 전생기억: 납음오행 깊이, 화개살(진술축미 2개 이상), 공망
    past_score = 2
    hwagae_count = sum(1 for j in all_jis if j in ["진", "술", "축", "미"])
    if hwagae_count >= 2: past_score += 1
    if has_gongmang: past_score += 1
    if has_cheolajimang: past_score += 1
    past_score = min(5, max(1, past_score))

    # 6) 주술친화: 화개살, 천을귀인, 편인, 목 기운
    ritual_score = 2
    if hwagae_count >= 1: ritual_score += 1
    if has_cheoneul: ritual_score += 1
    if any(p["ji_sipseong"] in ["편인", "정인"] for p in pillars.values()): ritual_score += 1
    ritual_score = min(5, max(1, ritual_score))

    six_senses = [
        {
            "key": "intuition",
            "label": "직감력",
            "hanja": "直感力",
            "score": intuition_score,
            "desc": "사람을 처음 만났을 때 낌새를 채거나 중요한 결정에서 본능적으로 승부수를 띄우는 촉이다."
        },
        {
            "key": "inspiration",
            "label": "영감",
            "hanja": "靈感",
            "score": inspiration_score,
            "desc": "머리로 계산하지 않아도 무의식에서 번뜩이는 발상과 아이디어가 솟아나는 능력이다."
        },
        {
            "key": "dreamClarity",
            "label": "꿈선명도",
            "hanja": "夢鮮明度",
            "score": dream_score,
            "desc": "꿈이 얼마나 또렷하고 생생하게 현실의 신호나 예지적 복선으로 이어지는지의 척도다."
        },
        {
            "key": "ghostSensing",
            "label": "귀신감지",
            "hanja": "鬼神感知",
            "score": ghost_score,
            "desc": "터가 센 곳이나 음산한 기운, 보이지 않는 존재의 분위기를 몸이 먼저 알아채고 소름이나 한기로 반응하는 체질이다."
        },
        {
            "key": "pastLifeMemory",
            "label": "전생기억",
            "hanja": "前生記憶",
            "score": past_score,
            "desc": "처음 가본 곳이 낯익거나 특정 문화에 까닭 없이 끌리는 등 납음오행에 아로새겨진 전생의 미련과 잔향이다."
        },
        {
            "key": "ritualAffinity",
            "label": "주술친화",
            "hanja": "呪術親和",
            "score": ritual_score,
            "desc": "절이나 명산, 조용한 사찰에 가면 마음이 씻기듯 편안해지고 정성을 들이면 감응이 빠른 정도다."
        }
    ]

    # 정통 명리학 고도화 연산: 신강/신약, 용신/희신/기신, 대운
    raw_saju = {
        "year": year_pillar,
        "month": month_pillar,
        "day": day_pillar,
        "hour": hour_pillar,
    }
    strength_info = calculate_saju_strength(raw_saju, day_gan, pillars)
    yongsin_info = calculate_yongsin(raw_saju, day_gan, month_ji, strength_info, oheng_counts)
    daeun_info = calculate_daeun(year, month, day, hour, minute, gender, raw_saju["year"][0], raw_saju["month"], yongsin_info)

    now_year = datetime.now().year
    korean_age = now_year - year + 1

    return {
        "pillars": pillars,
        "raw": raw_saju,
        "day_gan": day_gan,
        "day_ji": day_ji,
        "oheng_counts": oheng_counts,
        "yin_yang": {"yang": yang_count, "yin": yin_count},
        "constitution": {
            "type": constitution[0],
            "title": constitution[1],
            "desc": constitution[2],
        },
        "gates": gates,
        "opened_gates_count": sum(1 for g in gates if g["opened"]),
        "nabeum": {
            "name": nabeum_info[0],
            "hanja": nabeum_info[1],
            "desc": nabeum_info[2]
        },
        "shinsal": {
            "guimun": has_guimun,
            "gongmang": has_gongmang,
            "baekho": has_baekho,
            "cheolajimang": has_cheolajimang,
            "goegang": has_goegang,
            "dohwa": has_dohwa,
            "yeokma": has_yeokma,
            "cheoneul": has_cheoneul,
            "cheondeok": has_cheondeok,
            "woldeok": has_woldeok,
            "munchang": has_munchang,
            "cheonui": has_cheonui,
            "amrok": has_amrok,
            "hwagae": has_hwagae,
            "wonjin": has_wonjin,
            "yangin": has_yangin
        },
        "strength": strength_info,
        "yongsin": yongsin_info,
        "daeun": daeun_info,
        "korean_age": korean_age,
        "six_senses": six_senses,
        "solar_year": year,
        "solar_month": month,
        "solar_day": day,
        "solar_hour": hour
    }


if __name__ == "__main__":
    # Test sample
    result = calculate_saju(1990, 5, 21, 14, 30)
    print("사주팔자:", result["raw"])
    print("음양체질:", result["constitution"]["type"])
    print("열린 문 개수:", result["opened_gates_count"])
    print("육감 지표:", [(s["label"], s["score"]) for s in result["six_senses"]])
