# -*- coding: utf-8 -*-
"""
세계적 영성 융합 엔진 (Global Spiritual Synthesis Engine)
- 1. 칼 융(Carl Jung)의 동시성(Synchronicity), 12대 원형(Archetypes), 그림자(Shadow Self)
- 2. 인도 베다 7대 차크라(7 Chakras) 및 오라(Aura) 에너지 센터 진단
- 3. 주역(I-Ching) 64괘 찰나 영동(靈動) 괘상 도출
- 4. 일일 신점(Daily Spiritual Fortune) & 피해야 할 방위/살(煞)
- 5. 바이럴 황금 부적(Spiritual Amulet) 생성 알고리즘
"""

from datetime import datetime
import hashlib

# 칼 융 12대 원형과 사주 십성 매핑
JUNG_ARCHETYPES = {
    "비견": ("영웅 (The Hero)", "스스로의 힘으로 난관을 돌파하고 주체성을 증명하려는 강력한 투사", "고립과 인정 욕구, 지는 것을 참지 못하는 패배 공포"),
    "겁재": ("반역자 (The Rebel)", "기존 질서를 뒤흔들고 혁신을 꾀하는 카리스마 넘치는 승부사", "파괴적 충동, 질투심, 모든 것을 잃을 수 있는 무리수"),
    "식신": ("창조자 (The Creator)", "새로운 가치와 예술, 생명을 잉태하고 세상에 풍요를 베푸는 예술가", "완벽주의에 대한 강박, 현실 감각의 결여"),
    "상관": ("마술사 (The Magician)", "언변과 재치로 판을 뒤바꾸고 사람의 마음을 홀리는 변혁가", "오만함, 냉소주의, 말로써 남의 가슴에 비수를 꽂는 업보"),
    "편재": ("탐험가 (The Explorer)", "미지의 영역과 거대한 기회를 향해 거침없이 뛰어드는 모험가", "방황, 안주하지 못하는 조급증, 공허한 허상 쫓기"),
    "정재": ("통치자 (The Ruler)", "안정과 질서, 현실적인 기반을 튼튼히 일구는 든든한 설계자", "통제 강박, 인색함, 변화에 대한 병적인 두려움"),
    "편관": ("전사 (The Warrior)", "자신을 극한으로 몰아붙이며 대의를 위해 칼을 뽑는 의인", "자신과 타인을 학대하는 엄격함, 내면의 분노 폭발"),
    "정관": ("현자 (The Sage)", "원칙과 명예, 법도를 지키며 만인에게 귀감이 되는 지도자", "교조주의, 체면치레, 위선과 융통성 상실"),
    "편인": ("신비가 (The Mystic)", "보이지 않는 영계와 형이상학적 진리를 꿰뚫어보는 은둔자", "세상과의 단절, 편집증, 음산한 망상과 의심"),
    "정인": ("수호자 (The Caregiver)", "만인을 품어 안고 지혜와 자비를 베푸는 대모/대부의 영혼", "의존성, 희생에 대한 억울함, 현실 도피")
}

# 7대 차크라와 오행 매핑
CHAKRAS = [
    {"name": "물라다라 (뿌리 차크라)", "sanskrit": "Muladhara", "element": "수", "color": "루비 레드 / 흑단", "meaning": "생존, 현실 감각, 생명력의 뿌리"},
    {"name": "스와디스타나 (천골 차크라)", "sanskrit": "Svadhisthana", "element": "수", "color": "주황", "meaning": "감정, 창조성, 성(性) 에너지"},
    {"name": "마니푸라 (태양신경총 차크라)", "sanskrit": "Manipura", "element": "화", "color": "황금빛 옐로우", "meaning": "의지력, 자존감, 주체적 힘"},
    {"name": "아나하타 (심장 차크라)", "sanskrit": "Anahata", "element": "목", "color": "에메랄드 그린", "meaning": "사랑, 연민, 용서와 치유"},
    {"name": "비슈다 (목 차크라)", "sanskrit": "Vishuddha", "element": "금", "color": "청록빛 블루", "meaning": "표현, 소통, 진실의 발성"},
    {"name": "아즈나 (제3의 눈 차크라)", "sanskrit": "Ajna", "element": "화", "color": "인디고 남색", "meaning": "직관, 투시, 영적 통찰력"},
    {"name": "사하스라라 (크라운 차크라)", "sanskrit": "Sahasrara", "element": "금", "color": "바이올렛 / 순백", "meaning": "우주 의식과의 합일, 초월적 지혜"}
]

# 주역 64괘 주요 대표 괘 (시점 영동 추출)
ICHING_TRIGRAMS = [
    ("지천태 (地天泰)", "하늘과 땅이 사귀어 만물이 통달하고 평화가 깃드는 최고의 태평성대 괘"),
    ("화천대유 (火天大有)", "하늘 높이 타오르는 태양처럼 천하의 모든 부와 사람을 한 손에 거머쥐는 대길 괘"),
    ("수천수 (水天需)", "구름이 하늘에 가득 차 비를 기다리듯, 조급함을 버리고 때를 기다리면 크게 얻는 괘"),
    ("천화동인 (天火同人)", "뜻을 같이하는 귀인들이 모여 천하를 도모하는 대화합의 괘"),
    ("풍뢰익 (風雷益)", "바람과 우레가 서로를 북돋아 만물이 번창하고 비약적으로 성장하는 괘"),
    ("화풍정 (火風鼎)", "새로운 솥을 걸어 묵은 것을 갈아엎고 신분과 격을 혁신하는 개혁의 괘"),
    ("수뢰준 (水雷屯)", "새싹이 두터운 얼음 땅을 뚫고 솟아오르듯, 초기의 고난을 딛고 거목으로 자라나는 괘"),
    ("산화비 (山火賁)", "노을이 산을 곱게 물들이듯, 내면의 품격과 외면의 명예가 찬란하게 빛나는 괘")
]

def analyze_global_spirituality(saju_data):
    raw = saju_data["raw"]
    day_gan = saju_data["day_gan"]
    pillars = saju_data["pillars"]
    oheng = saju_data["oheng_counts"]
    shinsal = saju_data["shinsal"]
    
    # 1. 칼 융 원형 및 그림자(Shadow)
    day_sipseong = pillars["month"]["gan_sipseong"] # 월간 십성 = 사회적 원형
    if day_sipseong == "일원(나)": day_sipseong = "비견"
    archetype_info = JUNG_ARCHETYPES.get(day_sipseong, JUNG_ARCHETYPES["비견"])
    
    # 그림자 자아: 사주에서 가장 결핍되거나 억압된 오행에서 발생
    weakest_oheng = min(oheng, key=oheng.get)
    shadow_map = {
        "목": ("자라지 못하는 나무의 슬픔", "새로운 도전을 두려워하고 패배의식에 갇혀 제자리에 맴도는 무의식"),
        "화": ("차가운 어둠 속의 분노", "열정을 억누르고 차가운 척하다가 홧김에 폭발해 모든 것을 태우는 무의식"),
        "토": ("발밑이 꺼지는 공포", "믿을 곳이 없어 끝없이 불안해하며 사람을 집착하고 의심하는 무의식"),
        "금": ("무뎌진 칼날의 자괴감", "단호하게 결단하지 못하고 우유부단하게 끌려다니며 자책하는 무의식"),
        "수": ("메마른 우물의 갈증", "감정이 메말라 타인과 깊은 교감을 나누지 못하고 고독에 떠는 무의식")
    }
    shadow_info = shadow_map.get(weakest_oheng, shadow_map["토"])

    # 2. 7대 차크라 에너지 오라 진단
    chakra_diagnoses = []
    for c in CHAKRAS:
        elem = c["element"]
        count = oheng.get(elem, 0)
        if count == 0:
            status = "차단됨 (Blocked)"
            desc = f"{elem}({elem}) 기운의 결핍으로 인해 {c['name']}가 닫혀 있어 에너지가 정체되어 있습니다."
        elif count >= 3:
            status = "과열됨 (Overactive)"
            desc = f"{elem}({elem}) 기운의 과다로 인해 에너지가 통제되지 않고 불안정하게 분출됩니다."
        else:
            status = "균형 (Balanced)"
            desc = f"안정적인 에너지 흐름을 유지하고 있습니다."
        chakra_diagnoses.append({
            "name": c["name"],
            "sanskrit": c["sanskrit"],
            "color": c["color"],
            "meaning": c["meaning"],
            "status": status,
            "desc": desc
        })

    # 오라 컬러 판정 (가장 강한 오행 기준)
    strongest_oheng = max(oheng, key=oheng.get)
    aura_colors = {
        "목": ("에메랄드 그린 (Emerald Aura)", "생명력과 치유, 타인을 살리고 성장시키는 성장의 오라"),
        "화": ("루비 골드 (Ruby Gold Aura)", "열정과 카리스마, 무대를 장악하고 사람을 이끄는 지배자의 오라"),
        "토": ("엠버 옐로우 (Amber Gold Aura)", "흔들리지 않는 대지처럼 포용력과 신뢰를 풍기는 황금빛 오라"),
        "금": ("다이아몬드 화이트 (Diamond Silver Aura)", "순백의 칼날처럼 결벽과 고결함, 날카로운 통찰을 품은 오라"),
        "수": ("딥 사파이어 (Deep Indigo Aura)", "깊은 심해처럼 신비롭고 영적인 통찰과 무한한 잠재력을 품은 오라")
    }
    aura_info = aura_colors.get(strongest_oheng, aura_colors["토"])

    # 3. 주역 64괘 찰나 영동 괘상
    now = datetime.now()
    hash_val = int(hashlib.md5(f"{raw['year']}{raw['month']}{raw['day']}{now.second}".encode()).hexdigest(), 16)
    iching_idx = hash_val % len(ICHING_TRIGRAMS)
    iching_result = ICHING_TRIGRAMS[iching_idx]

    # 4. 일일 신점(Daily Spiritual Fortune)
    daily_fortunes = [
        "오늘은 동북방에서 귀인이 들어오니 낯선 사람의 제안을 경청하라. 다만 보증이나 금전 차용은 절대 금물이다.",
        "오후 2시부터 4시 사이에 말실수로 인한 구설이 따르니 입을 무겁게 하고 비밀을 지켜라.",
        "묵혀뒀던 골칫거리가 단칼에 해결되는 운이다. 미루던 계약이나 결단이 있다면 오늘 해치워라.",
        "밤 기운이 서늘하니 일찍 귀가하여 따뜻한 물로 샤워하고 몸의 음기를 씻어내라. 밤길 시비를 피하라."
    ]
    daily_fortune = daily_fortunes[hash_val % len(daily_fortunes)]

    # 5. 맞춤형 황금 부적 (Amulet) 생성
    amulet_names = {
        "목": "청룡벽사 만사여의부 (靑龍萬事如意符)",
        "화": "주작초재 천하대길부 (朱雀天下大吉符)",
        "토": "황제진택 무병안녕부 (黃帝無病安寧符)",
        "금": "백호단살 파사현정부 (白虎破邪顯正符)",
        "수": "현무수복 만복귀래부 (玄武萬福歸來符)"
    }
    amulet_name = amulet_names.get(weakest_oheng, "천지감응 만사대길부")
    amulet_desc = f"사주에 부족한 {weakest_oheng}({weakest_oheng})의 기운을 보완하고, 액운을 쳐내며 천운을 당겨오는 현허도인의 맞춤 천기 황금 부적"

    return {
        "archetype": {
            "title": archetype_info[0],
            "light": archetype_info[1],
            "dark": archetype_info[2]
        },
        "shadow": {
            "title": shadow_info[0],
            "desc": shadow_info[1]
        },
        "aura": {
            "name": aura_info[0],
            "desc": aura_info[1]
        },
        "chakras": chakra_diagnoses,
        "iching": {
            "hexagram": iching_result[0],
            "meaning": iching_result[1]
        },
        "daily_fortune": daily_fortune,
        "amulet": {
            "name": amulet_name,
            "desc": amulet_desc,
            "element": weakest_oheng
        }
    }

if __name__ == '__main__':
    from manseryeok import calculate_saju
    saju = calculate_saju(1993, 7, 1, 18, 0)
    res = analyze_global_spirituality(saju)
    print("융 원형:", res["archetype"]["title"])
    print("에너지 오라:", res["aura"]["name"])
    print("주역 괘상:", res["iching"]["hexagram"])
    print("부적:", res["amulet"]["name"])
