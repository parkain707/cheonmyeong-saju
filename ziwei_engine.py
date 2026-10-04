# -*- coding: utf-8 -*-
"""
天命明鏡 (천명명경) | 황실 비전 자미두수(紫微斗數) 정통 성반 연산 코어 엔진
- 12궁(命宮·兄弟宮·夫妻宮·子女宮·財帛宮·疾厄宮·遷移宮·奴僕宮·官祿宮·田宅宮·福德宮·父母宮) 입체 좌표 산출
- 오호돈결(五虎遁訣) 및 납음오행 기반 오행국(수이국~화육국) 도출
- 14대 주성(자미·천기·태양·무곡·천동·염정·천부·태음·탐랑·거문·천상·천량·칠살·파군) 정확한 안성(安星)
- 10간 생년 사화(四化: 化祿, 化權, 化科, 化忌) 및 흉성(화기) 적중 분석
- 명궁 주성 및 삼방사정(명궁·재백궁·관록궁·천이궁) 종합 운명도 도출
"""

from datetime import datetime

# 12지지 순서 (인덱스: 0=자, 1=축, 2=인, 3=묘, 4=진, 5=사, 6=오, 7=미, 8=신, 9=유, 10=술, 11=해)
JI_NAMES = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]
JI_HANJA = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 12궁 명칭 (명궁에서 출발하여 반시계방향 역행 배치)
PALACE_NAMES = [
    ("명궁", "命宮", "타고난 천명과 자아, 인격의 핵, 생애 총운"),
    ("형제궁", "兄弟宮", "형제자매, 친밀한 동료, 협력자와의 연대"),
    ("부처궁", "夫妻宮", "배우자와 연인, 애정의 본질과 부부 인연"),
    ("자녀궁", "子女宮", "자손, 후배, 제자, 부하 직원과의 인연"),
    ("재백궁", "財帛宮", "재물 운용, 현금 흐름, 부의 획득 방식"),
    ("질액궁", "疾厄宮", "체질적 약점, 신체 장기, 잠재 질환"),
    ("천이궁", "遷移宮", "대외 활동, 출장, 이사, 사회적 이미지와 무대"),
    ("노복궁", "奴僕宮", "친구, 지인, 사회적 인맥과 교우 관계"),
    ("관록궁", "官祿宮", "직업 소명, 사회적 명예, 성취와 출세"),
    ("전택궁", "田宅宮", "부동산, 가택 운, 종잣돈 저축과 고정 자산"),
    ("복덕궁", "福德宮", "정신적 안식, 무의식, 내면의 평온과 심미안"),
    ("부모궁", "父母宮", "부모님, 가문의 은덕, 직장 상사 및 스승")
]

# 14대 주성 정보 (성격, 상징, 기운)
MAJOR_STARS = {
    "자미": {
        "hanja": "紫微", "type": "제왕성 (帝王星)", "element": "토 (土)",
        "keyword": "지배력, 품격, 자존심, 제왕적 리더십",
        "desc": "북극성을 상징하는 최고의 황제성. 매사에 품격을 잃지 않으며 남의 지배를 받기 싫어하는 강한 자존심과 통솔력을 발휘합니다."
    },
    "천기": {
        "hanja": "天機", "type": "지혜책사성 (智慧星)", "element": "목 (木)",
        "keyword": "기획력, 번뜩이는 지략, 변화, 민첩함",
        "desc": "천상의 지혜와 전략을 담당하는 책사의 별. 뛰어난 두뇌 회전과 임기응변, 창의적 기획으로 난세를 돌파합니다."
    },
    "태양": {
        "hanja": "太陽", "type": "광명명예성 (光明星)", "element": "화 (火)",
        "keyword": "공명정대, 명예, 추진력, 만인 구제",
        "desc": "온 세상을 골고루 비추는 태양의 별. 뒤끝이 없고 호탕하며, 남을 위해 헌신하고 명예를 최고의 가치로 삼습니다."
    },
    "무곡": {
        "hanja": "武曲", "type": "재무장군성 (財帛星)", "element": "금 (金)",
        "keyword": "실행력, 결단력, 강직함, 재물 집행",
        "desc": "손에 보검과 황금을 쥔 강직한 장군의 별. 말이 앞서기보다 행동으로 증명하며, 악착같이 부를 쌓아 올리는 실무적 천재입니다."
    },
    "천동": {
        "hanja": "天同", "type": "복덕안식성 (福星)", "element": "수 (水)",
        "keyword": "유순함, 평화, 감수성, 낙천성",
        "desc": "온화하고 맑은 어린아이의 심성을 지닌 복성. 모나지 않고 유연하여 인복이 넘치며, 삶의 여유와 예술을 즐깁니다."
    },
    "염정": {
        "hanja": "廉貞", "type": "승부정치성 (囚星)", "element": "화 (火)",
        "keyword": "승부사, 카리스마, 치밀함, 도화",
        "desc": "불꽃같은 승부욕과 강렬한 매력을 뿜어내는 정치가의 별. 호불호가 극명하며 목표를 위해 끝까지 밀어붙이는 돌파력이 있습니다."
    },
    "천부": {
        "hanja": "天府", "type": "황금금고성 (財庫星)", "element": "토 (土)",
        "keyword": "포용력, 곳간 수호, 안정성, 신중함",
        "desc": "남두칠성의 우두머리로 하늘의 보물창고를 관장하는 별. 스케일이 크고 포용력이 넘치며, 어떤 풍파에도 재산을 지켜냅니다."
    },
    "태음": {
        "hanja": "太陰", "type": "정결모성성 (月星)", "element": "수 (水)",
        "keyword": "섬세함, 자애로움, 부동산, 은근한 인내",
        "desc": "밤하늘을 은은히 비추는 달의 여신. 심성이 곱고 디테일에 강하며, 계획성 있게 부동산과 알짜 자산을 불려 나갑니다."
    },
    "탐랑": {
        "hanja": "貪狼", "type": "욕망도화성 (桃花星)", "element": "목/수 (木水)",
        "keyword": "다재다능, 사교술, 기회포착, 예술성",
        "desc": "인간의 모든 욕망과 재능을 집약한 만능 엔터테이너의 별. 사람의 마음을 홀리는 천부적 매력과 탁월한 기회 포착 능력을 지녔습니다."
    },
    "거문": {
        "hanja": "巨門", "type": "언변탐구성 (暗星)", "element": "수 (水)",
        "keyword": "달변, 비판적 분석력, 전문지식, 진실 규명",
        "desc": "거대한 문을 열고 진실을 파헤치는 학자이자 달변가의 별. 날카로운 논리와 비판 정신으로 가짜를 가려내며 말과 글로 천하를 움직입니다."
    },
    "천상": {
        "hanja": "天相", "type": "재상옥새성 (印星)", "element": "수 (水)",
        "keyword": "신뢰, 조율자, 공정함, 의리",
        "desc": "황제의 옥새를 손에 쥔 믿음직한 재상의 별. 품행이 단정하고 정의감이 투철하며, 양쪽의 갈등을 평화롭게 조율하는 최고의 참모입니다."
    },
    "천량": {
        "hanja": "天梁", "type": "청렴어른성 (蔭星)", "element": "토 (土)",
        "keyword": "선비정신, 위기해결, 멘토, 직관",
        "desc": "풍파를 만나면 오히려 더 큰 기적을 일으키는 큰어른의 별. 청렴결백하며 남의 억울함을 풀어주고 액운을 소멸시키는 영험한 수호성입니다."
    },
    "칠살": {
        "hanja": "七殺", "type": "독보적 돌파장군 (將星)", "element": "금/화 (金火)",
        "keyword": "독립심, 결사항전, 파괴적 혁신, 영웅호걸",
        "desc": "전쟁터의 선봉에 서서 적진을 베어버리는 무적의 장군성. 남에게 기대지 않고 혼자 힘으로 황무지를 개척하여 새 역사를 씁니다."
    },
    "파군": {
        "hanja": "破軍", "type": "개척선봉성 (耗星)", "element": "수 (水)",
        "keyword": "기존 판 파괴, 혁신, 반골 기질, 새판 짜기",
        "desc": "낡은 판을 가차 없이 뒤엎고 새로운 세상을 여는 혁명가의 별. 안주함을 거부하고 끊임없이 변화를 시도하여 불가능을 가능으로 바꿉니다."
    }
}

# 4대 핵심 보좌길성 (문창·문곡·좌보·우필 - 사화와 직결)
ASSISTANT_STARS = {
    "문창": {
        "hanja": "文昌", "type": "학문시험성 (文星)", "element": "금 (金)",
        "keyword": "학문, 정통 시험 합격, 문학적 재능, 명예",
        "desc": "정통 과거 급제와 국가 공인 시험, 정갈한 문장력을 주관하는 문성의 대표별입니다."
    },
    "문곡": {
        "hanja": "文曲", "type": "재능예술성 (藝星)", "element": "수 (水)",
        "keyword": "순발력, 예술, 언변, 임기응변",
        "desc": "번뜩이는 창의성과 예술적 감각, 대중을 사로잡는 말솜씨와 다재다능함을 주관하는 별입니다."
    },
    "좌보": {
        "hanja": "左輔", "type": "조력협력성 (輔星)", "element": "토 (土)",
        "keyword": "귀인의 도움, 충직한 파트너, 조화, 포용",
        "desc": "위기 때마다 나를 돕는 귀인을 보내주고 든든한 조력자가 되어주는 대표적 보좌길성입니다."
    },
    "우필": {
        "hanja": "右弼", "type": "지혜조력성 (弼星)", "element": "수 (水)",
        "keyword": "지략적 보좌, 유연함, 해결사, 후원자",
        "desc": "지혜와 유연함으로 뒤에서 궂은일을 해결해주고 판을 매끄럽게 조율하는 최고의 참모성입니다."
    }
}

# 10간 생년 사화(四化: 化祿, 化權, 化科, 化忌) 조견표
SIHUA_TABLE = {
    "갑": {"록": "염정", "권": "파군", "과": "무곡", "기": "태양"},
    "을": {"록": "천기", "권": "천량", "과": "자미", "기": "태음"},
    "병": {"록": "천동", "권": "천기", "과": "문창", "기": "염정"},
    "정": {"록": "태음", "권": "천동", "과": "천기", "기": "거문"},
    "무": {"록": "탐랑", "권": "태음", "과": "우필", "기": "천기"},
    "기": {"록": "무곡", "권": "탐랑", "과": "천량", "기": "문곡"},
    "경": {"록": "태양", "권": "무곡", "과": "태음", "기": "천동"},
    "신": {"록": "거문", "권": "태양", "과": "문곡", "기": "문창"},
    "임": {"록": "천량", "권": "자미", "과": "좌보", "기": "무곡"},
    "계": {"록": "파군", "권": "거문", "과": "태음", "기": "탐랑"}
}

# 납음오행 기반 오행국 조견표 (명궁 간지 기준)
NAYEUM_BUREAU = {
    # 수이국 (2)
    "갑인": 2, "을묘": 2, "임술": 2, "계해": 2, "병자": 2, "정축": 2, "갑신": 2, "을유": 2, "임진": 2, "계사": 2, "병오": 2, "정미": 2,
    # 목삼국 (3) - 양류목·송백목·대림목·상자목·석류목·평지목
    "임오": 3, "계미": 3, "경인": 3, "신묘": 3, "무진": 3, "기사": 3, "임자": 3, "계축": 3, "경신": 3, "신유": 3, "무술": 3, "기해": 3,
    # 금사국 (4)
    "갑자": 4, "을축": 4, "임신": 4, "계유": 4, "경진": 4, "신사": 4, "갑오": 4, "을미": 4, "임인": 4, "계묘": 4, "경술": 4, "신해": 4,
    # 토오국 (5)
    "경오": 5, "신미": 5, "무인": 5, "기묘": 5, "병술": 5, "정해": 5, "경자": 5, "신축": 5, "무신": 5, "기유": 5, "병진": 5, "정사": 5,
    # 화육국 (6)
    "병인": 6, "정묘": 6, "갑술": 6, "을해": 6, "무자": 6, "기축": 6, "병신": 6, "정유": 6, "갑진": 6, "을사": 6, "무오": 6, "기미": 6
}

BUREAU_NAMES = {
    2: ("수이국 (水二局)", "유연하고 지혜로우며 막힘없이 도도하게 흐르는 물의 본질"),
    3: ("목삼국 (木三局)", "굳은 땅을 뚫고 하늘 높이 솟구쳐 오르는 거목의 생명력"),
    4: ("금사국 (金四局)", "단단하게 벼려진 보검처럼 결단력 있고 서슬 퍼런 칼날의 기운"),
    5: ("토오국 (土五局)", "만물을 품어 안고 기름지게 키워내는 광활한 대지의 중심"),
    6: ("화육국 (火六局)", "온 세상을 환히 비추고 열정으로 만인을 이끄는 불꽃의 힘")
}

def calculate_ziwei_chart(lunar_year_gan, lunar_month, lunar_day, birth_hour, gender="male"):
    """
    정통 자미두수 12궁 성반 및 14주성 연산
    - lunar_year_gan: 생년 천간 ("갑"~"계")
    - lunar_month: 음력 월 (1~12)
    - lunar_day: 음력 일 (1~30)
    - birth_hour: 태어난 시 (0~23)
    """
    # 1. 생시 지지 인덱스 산출 (자=0, 축=1, 인=2, ..., 해=11)
    # 자시는 23:00~00:59 -> 0
    hour_idx = ((birth_hour + 1) % 24) // 2

    # 2. 명궁(命宮) & 신궁(身宮) 위치 산출
    # 인궁(index 2)에서 출발 -> 월만큼 순행(+ M - 1) -> 시만큼 역행(- H)
    ming_idx = (2 + (lunar_month - 1) - hour_idx) % 12
    # 신궁: 인궁(index 2)에서 출발 -> 월만큼 순행(+ M - 1) -> 시만큼 순행(+ H)
    shen_idx = (2 + (lunar_month - 1) + hour_idx) % 12

    # 3. 12궁 지지 배정 (명궁부터 반시계방향 역행)
    palaces = {}
    for i, (p_name, p_hanja, p_desc) in enumerate(PALACE_NAMES):
        p_ji_idx = (ming_idx - i) % 12
        palaces[p_name] = {
            "name": p_name,
            "hanja": p_hanja,
            "desc": p_desc,
            "ji": JI_NAMES[p_ji_idx],
            "ji_hanja": JI_HANJA[p_ji_idx],
            "ji_idx": p_ji_idx,
            "stars": [],
            "sihua": []
        }

    # 4. 명궁 천간 도출 (오호돈결)
    gan_list = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
    in_gan_map = {"갑": 2, "기": 2, "을": 4, "경": 4, "병": 6, "신": 6, "정": 8, "임": 8, "무": 0, "계": 0}
    in_start_gan = in_gan_map.get(lunar_year_gan, 2)
    
    # 인궁(2)부터 명궁 지지(ming_idx)까지 순행
    dist_from_in = (ming_idx - 2) % 12
    ming_gan_idx = (in_start_gan + dist_from_in) % 10
    ming_gan = gan_list[ming_gan_idx]
    ming_ganji = ming_gan + JI_NAMES[ming_idx]

    # 5. 오행국 산출
    bureau_num = NAYEUM_BUREAU.get(ming_ganji, 2)
    bureau_info = BUREAU_NAMES.get(bureau_num, BUREAU_NAMES[2])

    # 6. 자미성(紫微星) 위치 산출
    d = lunar_day
    b = bureau_num
    if d % b == 0:
        q = d // b
        rem = 0
    else:
        # 부족한 수(x)를 더해 배수로 만듦
        rem = b - (d % b)
        q = (d + rem) // b

    if rem == 0:
        ziwei_idx = (2 + q - 1) % 12
    elif rem % 2 == 0: # 짝수 보수 -> 순행
        ziwei_idx = (2 + q - 1 + rem) % 12
    else: # 홀수 보수 -> 역행
        ziwei_idx = (2 + q - 1 - rem) % 12

    # 7. 천부성(天府星) 위치 산출 (자미성과 인-신 축 대칭)
    tianfu_idx = (4 - ziwei_idx) % 12

    # 8. 14대 주성 위치 계산
    # [자미성계 6성 - 역행 배치]
    star_positions = {
        "자미": ziwei_idx,
        "천기": (ziwei_idx - 1) % 12,
        "태양": (ziwei_idx - 3) % 12,
        "무곡": (ziwei_idx - 4) % 12,
        "천동": (ziwei_idx - 5) % 12,
        "염정": (ziwei_idx - 8) % 12,
        # [천부성계 8성 - 순행 배치]
        "천부": tianfu_idx,
        "태음": (tianfu_idx + 1) % 12,
        "탐랑": (tianfu_idx + 2) % 12,
        "거문": (tianfu_idx + 3) % 12,
        "천상": (tianfu_idx + 4) % 12,
        "천량": (tianfu_idx + 5) % 12,
        "칠살": (tianfu_idx + 6) % 12,
        "파군": (tianfu_idx + 10) % 12
    }

    # 8-1. 보좌 4대 길성 (문창, 문곡, 좌보, 우필) 위치 계산
    assist_positions = {
        "문창": (10 - hour_idx) % 12,
        "문곡": (4 + hour_idx) % 12,
        "좌보": (4 + (lunar_month - 1)) % 12,
        "우필": (10 - (lunar_month - 1)) % 12
    }

    # 9. 각 궁에 14대 주성 배정
    for star_name, star_pos in star_positions.items():
        for p_name, p_data in palaces.items():
            if p_data["ji_idx"] == star_pos:
                s_info = MAJOR_STARS[star_name]
                p_data["stars"].append({
                    "name": star_name,
                    "hanja": s_info["hanja"],
                    "type": s_info["type"],
                    "element": s_info["element"],
                    "keyword": s_info["keyword"],
                    "desc": s_info["desc"],
                    "is_major": True
                })

    # 9-1. 각 궁에 보좌길성 배정
    for star_name, star_pos in assist_positions.items():
        for p_name, p_data in palaces.items():
            if p_data["ji_idx"] == star_pos:
                a_info = ASSISTANT_STARS[star_name]
                p_data["stars"].append({
                    "name": star_name,
                    "hanja": a_info["hanja"],
                    "type": a_info["type"],
                    "element": a_info["element"],
                    "keyword": a_info["keyword"],
                    "desc": a_info["desc"],
                    "is_major": False
                })

    # 10. 생년 사화(四化: 祿·權·科·忌) 배정
    sihua_map = SIHUA_TABLE.get(lunar_year_gan, SIHUA_TABLE["갑"])
    sihua_types = [("록", "化祿", "재물과 풍요, 기운의 결실과 시작"),
                   ("권", "化權", "권력과 장악력, 전문성과 돌파력"),
                   ("과", "化科", "명예와 학문, 시험 합격과 귀인의 가호"),
                   ("기", "化忌", "집착과 번민, 액운과 파괴, 반드시 넘어야 할 시련")]

    sihua_results = {}
    for s_key, s_hanja, s_desc in sihua_types:
        target_star = sihua_map.get(s_key, "")
        sihua_results[s_key] = {
            "type": s_key,
            "hanja": s_hanja,
            "star": target_star,
            "desc": s_desc,
            "palace": "미배정"
        }
        # 해당 별이 위치한 궁에 사화 표기 추가
        for p_name, p_data in palaces.items():
            for s in p_data["stars"]:
                if s["name"] == target_star:
                    p_data["sihua"].append(f"{s_hanja}({target_star})")
                    sihua_results[s_key]["palace"] = p_name

    # 11. 핵심 궁 (명궁, 관록궁, 재백궁, 천이궁) 분석 요약
    ming_palace = palaces["명궁"]
    guan_palace = palaces["관록궁"]
    cai_palace = palaces["재백궁"]
    qian_palace = palaces["천이궁"]
    fuqi_palace = palaces["부처궁"]

    # 명궁 주성 요약
    ming_stars = [s["name"] for s in ming_palace["stars"]]
    ming_star_str = "·".join(ming_stars) if ming_stars else "명궁 무주성 (대궁 천이궁 기운 차용)"

    # 관록궁/재백궁 주성 요약
    guan_stars = [s["name"] for s in guan_palace["stars"]]
    cai_stars = [s["name"] for s in cai_palace["stars"]]

    # 화기(化忌)가 머무는 궁 - 인생의 가장 뼈아픈 시련이자 숙명
    hwayi_palace = sihua_results["기"]["palace"]
    hwayi_star = sihua_results["기"]["star"]

    # 도인의 자미두수 황실 비전 해설 요약
    oracle_summary = (
        f"황실 비전 자미두수 성반을 펼쳐보니, 그대의 명궁(命宮)은 **{ming_palace['ji_hanja']}궁({ming_palace['ji']})**에 자리하고 "
        f"**{bureau_info[0]}**의 천기를 타고났소. "
        f"명궁에 **[{ming_star_str}]**이 좌정하여 {ming_palace['stars'][0]['keyword'] if ming_palace['stars'] else '주변의 파동을 흡수하는 비범함'}을 떨칠 그릇이오. "
        f"단, 하늘의 엄정한 시련을 뜻하는 **화기(化忌: {hwayi_star})**가 **{hwayi_palace}**에 박혀 있으니, "
        f"인생의 성패는 바로 이 {hwayi_palace}의 덫을 어떻게 돌파하느냐에 달려 있소!"
    )

    return {
        "bureau": {
            "number": bureau_num,
            "name": bureau_info[0],
            "desc": bureau_info[1]
        },
        "ming_palace": {
            "ji": ming_palace["ji"],
            "ji_hanja": ming_palace["ji_hanja"],
            "ganji": ming_ganji,
            "stars": ming_palace["stars"],
            "sihua": ming_palace["sihua"]
        },
        "shen_palace": {
            "ji": JI_NAMES[shen_idx],
            "ji_hanja": JI_HANJA[shen_idx]
        },
        "palaces": palaces,
        "sihua": sihua_results,
        "oracle_summary": oracle_summary,
        "core_three_four": {
            "ming": {"name": "명궁", "stars": [s["name"] for s in ming_palace["stars"]], "sihua": ming_palace["sihua"]},
            "guan": {"name": "관록궁", "stars": [s["name"] for s in guan_palace["stars"]], "sihua": guan_palace["sihua"]},
            "cai": {"name": "재백궁", "stars": [s["name"] for s in cai_palace["stars"]], "sihua": cai_palace["sihua"]},
            "qian": {"name": "천이궁", "stars": [s["name"] for s in qian_palace["stars"]], "sihua": qian_palace["sihua"]},
            "fuqi": {"name": "부처궁", "stars": [s["name"] for s in fuqi_palace["stars"]], "sihua": fuqi_palace["sihua"]}
        }
    }

def calculate_ziwei_from_saju(saju_data, is_lunar=False, original_year=None, original_month=None, original_day=None):
    """
    사주 결과(saju_data) 및 입력 정보를 바탕으로 자미두수 성반 도출
    """
    from lunar_converter import solar_to_lunar

    # 사주의 년천간 (갑~계)
    year_gan = saju_data["raw"]["year"][0]
    hour = saju_data.get("solar_hour", 12)
    gender = saju_data.get("gender", "male")

    if is_lunar and original_year and original_month and original_day:
        l_year = original_year
        l_month = original_month
        l_day = original_day
    else:
        # 양력 -> 음력 변환
        s_year = saju_data.get("solar_year", 1990)
        s_month = saju_data.get("solar_month", 1)
        s_day = saju_data.get("solar_day", 1)
        l_year, l_month, l_day, is_leap = solar_to_lunar(s_year, s_month, s_day)

    # 자미두수는 입춘이 아닌 음력 설날 기준 년간을 사용
    gan_list = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
    year_gan = gan_list[(l_year - 4) % 10]

    return calculate_ziwei_chart(year_gan, l_month, l_day, hour, gender)

if __name__ == '__main__':
    # 테스트 실행 (1993년 계유년 음력 8월 17일 18시 유시)
    chart = calculate_ziwei_chart("계", 8, 17, 18)
    print("=== 자미두수 성반 연산 테스트 ===")
    print("오행국:", chart["bureau"]["name"])
    print("명궁 위치:", chart["ming_palace"]["ji_hanja"], "주성:", [s["name"] for s in chart["ming_palace"]["stars"]])
    print("신궁 위치:", chart["shen_palace"]["ji_hanja"])
    print("사화 배치:", {k: f"{v['star']}({v['palace']})" for k, v in chart["sihua"].items()})
    print("\n[도인의 자미두수 직설]")
    print(chart["oracle_summary"])
