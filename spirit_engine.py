# -*- coding: utf-8 -*-
"""
天命明鏡 (천명명경) | 현허도인의 신점(神占) 영안 투시 코어 엔진 (Spirit Engine)
- 사주팔자 10대 일간, 5대 오행 편중, 신살, 고민, 오방기에 따른 100% 동적 영안 투시
- 사주가 다르면 공수의 첫마디부터 신체 통증, 과거 환란, 가슴속 비밀, 미래 예언까지 완전히 다른 공수 생성
"""

from datetime import datetime
from astronomy_engine import get_synchronicity_moment
from ziwei_engine import calculate_ziwei_from_saju

# 오방기(五方旗) 정의 및 신령 점사
OBANGGI = {
    "청": {
        "color": "청기 (靑旗 - 동방 청룡의 깃발)",
        "meaning": "새로운 천지 개벽과 돌파, 이동수와 승부수",
        "oracle": "눈앞에 새로운 대로(大路)가 활짝 열리려 하오! 과거의 썩은 껍질과 미련을 과감히 벗어던지고, 주저 없이 판을 박차고 날아오르시오. 망설임은 독이오!"
    },
    "적": {
        "color": "적기 (赤旗 - 남방 주작의 깃발)",
        "meaning": "불꽃같은 명예와 문서 취득, 폭발적 도약 (단, 구설 경계)",
        "oracle": "하늘의 불꽃이 그대의 길을 환히 비추고 있소! 조만간 손에 도장을 찍거나 큰 문서를 쥐게 될 천운이오. 단, 입을 무겁게 다물고 주변의 시기 질투를 경계하시오."
    },
    "황": {
        "color": "황기 (黃旗 - 중앙 황제의 깃발)",
        "meaning": "천지신명과 조상의 가호, 마르지 않는 재물 성취",
        "oracle": "가문의 선대 조상과 천지신명이 그대의 뒤를 든든히 지키고 섰소. 비바람이 몰아쳐도 그대의 뿌리는 흔들리지 않을 터이니, 본래의 소신대로 밀고 나가 만복을 거두시오."
    },
    "백": {
        "color": "백기 (白旗 - 서방 백호의 깃발)",
        "meaning": "서릿발 같은 결단, 부패한 인연과 고인 물의 단칼 절단",
        "oracle": "썩은 살점은 피를 흘리더라도 도려내야 새 살이 돋는 법이오. 그대의 발목을 잡던 곪아 터진 인간관계든 미련이든, 오늘 이 순간부로 미련 없이 단칼에 베어내시오!"
    },
    "흑": {
        "color": "흑기 (黑旗 - 북방 현무의 깃발)",
        "meaning": "심해의 깊은 지혜, 내실을 다져 봄을 준비하는 은인자중",
        "oracle": "지금은 밤이 가장 깊은 자정이오. 섣불리 밖으로 뛰쳐나가지 말고 동굴 속에서 칼날을 벼리시오. 긴 겨울을 견뎌낸 자만이 찬란한 봄날의 주인이 되는 법이오."
    }
}

# 8대 영적 수호파동 분류
SPIRIT_TYPES = {
    "청룡개척령": ("동방 청룡의 개척령 (靑龍 開拓靈)", "새로운 길을 개척하고자 하는 강렬한 영감과 번뜩이는 직관, 멈추지 않는 도전의 파동"),
    "조상수호령": ("선대 가문의 은덕 수호령 (先代 護身靈)", "보이지 않는 곳에서 큰 사고를 막아주고, 위기 때마다 귀인을 보내 가문을 지키는 자애로운 조상님의 수호 파동"),
    "백호결단령": ("서방 백호의 결단령 (白虎 決斷靈)", "우유부단함을 용납하지 않고, 썩은 인연과 고인 물을 과감하게 단칼에 정리하여 새 판을 짜는 엄정한 파동"),
    "재물선신령": ("황금 곳간의 재물선신령 (財物 仙神靈)", "일할 때는 악착같이 모으나, 베풀고 나누는 지혜를 배워야 마르지 않는 천지 곳간이 열리는 번영의 파동"),
    "지혜현무령": ("북방 현무의 지혜령 (玄武 智慧靈)", "어둠 속에서도 길을 잃지 않는 깊은 사색과 혜안, 차분하게 세상의 이치를 꿰뚫어 보는 정화의 파동"),
    "터주평안령": ("터줏대감의 터전 안식령 (基址 安息靈)", "내 보금자리와 일터의 기운을 다스려, 번민을 가라앉히고 편안한 뿌리를 내리게 돕는 대지 어머니의 파동"),
    "명경수도령": ("맑은 거울의 도가 수호령 (明鏡 修道靈)", "탁한 세상 속에서도 티끌 하나 묻히지 않는 청정한 영혼, 마음을 닦을수록 놀라운 혜안과 복이 쏟아지는 파동"),
    "주작열정령": ("남방 주작의 온기열정령 (朱雀 熱情靈)", "얼어붙은 마음을 녹이고 사람을 끌어당기는 따뜻한 매력과 예술적 감수성, 빛나는 명예의 파동")
}

def analyze_shamanic_vision(saju_data, obanggi_choice="황", concern="career", name="그대", prev_visit=None, target_dt=None, ziwei_data=None):
    name_str = name.strip() if name and name not in ["자네", "그대"] else ""
    disp_call = f"{name_str} 그대" if name_str else "그대"

    raw = saju_data["raw"]
    day_gan = saju_data["day_gan"]
    day_ji = saju_data["day_ji"]
    all_jis = [raw["year"][1], raw["month"][1], raw["day"][1], raw["hour"][1]]
    oheng = saju_data.get("oheng_counts", {"목": 0, "화": 0, "토": 0, "금": 0, "수": 0})
    shinsal = saju_data.get("shinsal", {})
    age = saju_data.get("korean_age", 34)
    now = target_dt if target_dt else datetime.now()

    # 0. 황실 자미두수 성반 연산 (제공되지 않았을 경우 자동 산출)
    if ziwei_data is None:
        try:
            ziwei_data = calculate_ziwei_from_saju(saju_data)
        except Exception:
            ziwei_data = None

    # 0. 찰나의 천문 공시성(Synchronicity) 연산
    synchro_data = get_synchronicity_moment(now)

    # 0-1. 영혼 지속성 기억(재방문자 인지)
    reunion_prefix = ""
    is_reunion = False
    if prev_visit and isinstance(prev_visit, dict) and prev_visit.get("timestamp"):
        is_reunion = True
        c_korean = {
            "career": "직업과 이직의 절벽",
            "love": "애정과 배신의 상처",
            "wealth": "재물과 묶인 종잣돈",
            "timing": "황금기 때의 갈증"
        }.get(prev_visit.get("concern", "career"), "가슴속 번민")
        p_flag = prev_visit.get("obanggi", "황")
        p_time = prev_visit.get("timestamp", "얼마 전")
        reunion_prefix = (
            f"\"어허, 그대구려! 지난 {p_time}에 도인을 찾아와 "
            f"'{c_korean}'으로 속을 태우며 {p_flag}기를 뽑고 돌아갔던 {disp_call}의 영혼 파동을 도인이 어찌 잊겠소.\n\n"
            f"계절이 흐르고 달이 차올라 다시 이 문을 두드린 것을 보니, "
            f"지난번 일러준 하늘의 칙명은 가슴에 품고 그 험난한 고비를 어찌 건너왔는가? "
            f"한층 깊어진 번뇌 속에서도 기어이 길을 찾고자 하는 그대의 투혼이 먼저 도인의 심장을 울리는구려.\"\n\n"
        )

    # 0-2. 칼 융의 무의식 심층 그림자(Shadow Archetype) 분석
    sipseongs = []
    for p_name in ["year", "month", "day", "hour"]:
        p = saju_data.get("pillars", {}).get(p_name, {})
        if p.get("gan_sipseong"): sipseongs.append(p["gan_sipseong"])
        if p.get("ji_sipseong"): sipseongs.append(p["ji_sipseong"])
    
    s_counts = {
        "비겁": sum(1 for s in sipseongs if "비" in s or "겁" in s),
        "식상": sum(1 for s in sipseongs if "식" in s or "상" in s),
        "재성": sum(1 for s in sipseongs if "재" in s),
        "관성": sum(1 for s in sipseongs if "관" in s),
        "인성": sum(1 for s in sipseongs if "인" in s),
    }

    if s_counts["인성"] == 0:
        shadow_type = "모성적 결핍과 인정 갈망 (The Orphan Shadow)"
        shadow_insight = f"{disp_call}의 영혼 밑바닥에는 '내가 쓸모를 증명하지 못하면 아무도 나를 돌봐주지 않고 버려질지 모른다'는 지독한 유기 불안이 똬리를 틀고 있소. 겉으로는 의연하고 독립적인 척하지만, 마음 한구석에는 무조건적으로 나를 품어줄 안식처를 향한 피눈물 나는 갈증이 숨어 있소."
    elif s_counts["관성"] >= 3:
        shadow_type = "가면 우울과 가혹한 초자아 (The Imposter Shadow)"
        shadow_insight = f"{disp_call}의 내면에는 스스로를 가혹하게 채찍질하는 엄격한 심판관이 서 있소. '남들에게 흐트러진 모습을 보여서는 안 된다, 완벽해야 한다'는 강박에 짓눌려, 칭찬을 들어도 '언제 내 밑천이 드러날까' 전전긍긍하는 사기꾼 증후군의 그림자가 그대를 갉아먹어왔소."
    elif s_counts["식상"] >= 3:
        shadow_type = "오해받는 천재의 냉소와 분노 (The Misfit Rebel)"
        shadow_insight = f"{disp_call}의 깊은 곳에는 '세상이 내 천재성과 진심을 감당하지 못한다'는 서늘한 냉소와 분노가 도사리고 있소. 남들이 멍청해 보이고 꽉 막힌 규율에 질식할 것 같아 폭발하려 하면서도, 정작 제 속을 온전히 털어놓지 못해 고독한 섬처럼 표류해온 것이오."
    elif s_counts["재성"] >= 3:
        shadow_type = "통제 강박과 공허한 탈진 (The Exhausted Achiever)"
        shadow_insight = f"{disp_call}의 무의식은 오직 손에 쥐어지는 숫자가 불어나야만 안도감을 느끼는 통제 강박에 사로잡혀 있소. 쉴 때조차 죄책감에 시달리며 끊임없이 무언가를 쫓아가지만, 정작 통장에 돈이 쌓여도 가슴은 텅 빈 폐허처럼 공허해지는 쳇바퀴에 갇혀 있지 않소?"
    elif s_counts["비겁"] >= 3:
        shadow_type = "자존심의 감옥과 지독한 고립 (The Solitary Ruler)"
        shadow_insight = f"{disp_call}의 무의식은 남에게 아쉬운 소리를 하거나 고개를 숙이느니 차라리 피를 흘리며 굶어 죽겠다는 극단적 오만과 자존심의 감옥에 갇혀 있소. 누구에게도 약점을 보이지 않으려다 결국 사방에 벽을 치고 고립되어 스스로를 학대해온 형국이오."
    else:
        shadow_type = "억압된 야망과 주저함 (The Dormant Sovereign)"
        shadow_insight = f"{disp_call}의 내면에는 남들의 기대와 평온한 일상 뒤에 숨겨둔 폭발적인 지배욕과 승부사 기질이 억눌려 있소. '착하고 무난한 사람'이라는 가면 뒤에서, 언제든 천하를 흔들 판을 뒤엎고 싶은 위험한 불꽃이 조용히 때를 벼리고 있소."
    
    # 1. 8대 수호 영적 기운 판별
    if shinsal.get("guimun"):
        spirit_key = "청룡개척령" if ("자" in all_jis and "유" in all_jis) else "명경수도령"
    elif shinsal.get("gongmang"):
        spirit_key = "조상수호령" if oheng.get("토", 0) >= 2 else "재물선신령"
    elif shinsal.get("baekho"):
        spirit_key = "백호결단령"
    elif shinsal.get("cheolajimang"):
        spirit_key = "지혜현무령"
    elif oheng.get("수", 0) >= 3 or oheng.get("화", 0) == 0:
        spirit_key = "주작열정령"
    elif oheng.get("목", 0) >= 3 or oheng.get("금", 0) == 0:
        spirit_key = "터주평안령"
    else:
        spirit_key = "명경수도령"
        
    spirit_info = SPIRIT_TYPES.get(spirit_key, SPIRIT_TYPES["명경수도령"])

    # 2. 일간 및 문점(고민)별 오프닝 연출 및 기운 투시
    elem_pair = "갑을" if day_gan in ["갑", "을"] else ("병정" if day_gan in ["병", "정"] else ("무기" if day_gan in ["무", "기"] else ("경신" if day_gan in ["경", "신"] else "임계")))

    concern_openings = {
        "career": {
            "갑을": f"어서 오시오. 큰 숲을 일굴 재목으로 태어났으나, 썩은 조직의 그늘에 가려 칼자루를 빼앗기고 청춘을 좀먹혀온 {disp_call}의 다급한 숨소리가 들리오. 지금 당장 이 판을 박차고 나가 내 칼을 쥐어야 할지, 비굴하게 버텨야 할지 절벽 끝에서 피가 마르지 않았소?",
            "병정": f"어서 오시오. 온 세상을 비출 태양의 열정을 품고도, 꽉 막힌 일터에서 연기만 피우며 재능을 착취당해온 {disp_call}의 울분이 훤히 비치오. 내 공을 가로채는 자들의 면전에 사표를 집어던지고 내 판을 깔고 싶은 충동에 밤잠을 설치지 않았소?",
            "무기": f"어서 오시오. 천하 만물을 품어 안을 거대한 대지의 그릇을 지녔으되, 일터의 온갖 궂은일과 잡무는 다 떠안고 정작 제 대접은 못 받아 가슴이 타들어 간 {disp_call}의 억울함이 역력하오. 언제까지 남의 뒤치다꺼리만 할 것인가 피눈물이 나지 않았소?",
            "경신": f"어서 오시오. 난세를 평정할 보검을 쥐고 태어났으나, 진흙탕 같은 직장에서 칼날이 녹슬고 융통성 없는 빌런들에게 둘러싸여 분노로 치를 떨어온 {disp_call}의 한숨이 들리오. 단칼에 이 판을 베어버리고 탈출하고 싶지 않았소?",
            "임계": f"어서 오시오. 만 갈래 강물을 다스릴 거대한 지략을 품고도, 좁은 어항 같은 조직에 갇혀 부품처럼 소모되어온 {disp_call}의 비명이 들려오오. '내 능력이 고작 이 정도 취급을 받을 그릇인가' 가슴을 쥐어뜯지 않았소?"
        },
        "love": {
            "갑을": f"어서 오시오. 푸른 들꽃처럼 순수한 정을 다 바쳤으나, 가스라이팅과 차가운 배신으로 영혼이 갈기갈기 찢겨나간 {disp_call}의 비명이 들려오오. 겉으로는 담담한 척 웃고 있으나 가슴속에는 피멍이 든 채 홀로 눈물을 삼키고 있지 않았소?",
            "병정": f"어서 오시오. 온 심장을 다 태워 뜨겁게 사랑했으나, 결국 돌아온 것은 얼음장 같은 무관심과 뒤통수뿐이었던 {disp_call}의 타버린 가슴이 비치오. '왜 나만 항상 모든 것을 다 주고 상처받는 바보가 되는가' 원망에 밤을 지새우지 않았소?",
            "무기": f"어서 오시오. 태산처럼 묵묵히 상대방의 허물과 짐을 다 받아주었으나, 내 헌신을 당연한 권리로 착각하고 짓밟은 악연 때문에 속병이 난 {disp_call}의 고독이 역력하오. 믿었던 도끼에 발등을 찍힌 고통에 치를 떨지 않았소?",
            "경신": f"어서 오시오. 티끌 하나 없는 결백과 진심을 바쳤으나, 상대방의 거짓과 기만에 난도질당해 차가운 철벽을 치고 스스로를 가두어버린 {disp_call}의 처절한 상처가 비치오. 또다시 배신당할 바엔 혼자가 낫다며 입술을 깨물지 않았소?",
            "임계": f"어서 오시오. 깊은 바다처럼 영혼의 교감을 갈망했으나, 껍데기뿐인 집착과 외로움의 덫에 걸려 질질 끌려다닌 {disp_call}의 깊은 탄식이 들려오오. 끊어야 하는 줄 알면서도 미련 때문에 심장을 갉아먹히고 있지 않았소?"
        },
        "wealth": {
            "갑을": f"어서 오시오. 거목처럼 억대 부를 일굴 기운을 품고도, 밑 빠진 독에 물 붓듯 모아둔 돈이 새어나가 미래에 대한 공포에 짓눌린 {disp_call}의 무거운 한숨이 비치오. 남들은 그럴듯하게 보아도 통장 잔고를 볼 때마다 피가 마르지 않았소?",
            "병정": f"어서 오시오. 남 좋은 일은 다 시켜주고 거대한 판을 벌여 돈을 벌어다 주었으나, 정작 내 손에는 쥐어지는 알맹이가 없어 벼랑 끝에 몰린 {disp_call}의 번민이 훤히 비치오. 번 돈은 다 어디로 샜는가 가슴을 쥐어뜯지 않았소?",
            "무기": f"어서 오시오. 묵묵히 뼈 빠지게 일해 종잣돈을 모았으나, 지인의 부탁이나 무리한 부동산/투자 덫에 물려 숨이 턱밑까지 차오른 {disp_call}의 절망이 역력하오. 피 같은 내 돈을 떼이고 잠 못 이루지 않았소?",
            "경신": f"어서 오시오. 한 방에 거대한 자산을 쓸어 담을 승부사 기질을 지녔으되, 조급증과 한순간의 잘못된 선택으로 큰돈을 태워 먹고 피눈물을 삼킨 {disp_call}의 칼날이 비치오. 원금을 회복할 길이 막막해 밤마다 가슴을 치지 않았소?",
            "임계": f"어서 오시오. 천하의 재물을 끌어모을 지혜를 품고도, 사기꾼의 감언이설이나 잘못된 동업으로 금고가 털려버린 {disp_call}의 깊은 고통이 들려오오. 손에 쥐었던 황금이 모래알처럼 빠져나간 공포에 몸서리치지 않았소?"
        },
        "timing": {
            "갑을": f"어서 오시오. 대지를 뚫고 솟구칠 거대한 싹을 품었으나, 끝없는 겨울 추위 속에 갇혀 잎을 틔우지 못해 애가 타는 {disp_call}의 기다림이 비치오. '도대체 내 봄날은 언제 오는가' 하늘을 향해 원망을 삼켜오지 않았소?",
            "병정": f"어서 오시오. 온 세상을 비출 폭발력을 장전하고도, 먹구름에 가려 시기를 만나지 못해 어두운 골방에서 속을 태워온 {disp_call}의 번민이 훤히 비치오. 나보다 못한 자들이 승승장구하는 것을 보며 피눈물을 삼키지 않았소?",
            "무기": f"어서 오시오. 거대한 산맥을 이룰 잠재력을 지녔으되, 터전이 흔들리고 기회가 문턱에서 미끄러져 십수 년의 세월을 인내해온 {disp_call}의 고독이 역력하오. '언제까지 버텨야 하는가' 한숨이 깊지 않았소?",
            "경신": f"어서 오시오. 무적의 보검으로 벼려졌으나 칼을 뽑을 전쟁터가 열리지 않아 칼집 속에서 울부짖어온 {disp_call}의 서릿발이 비치오. 칼날이 녹슬기 전에 천하로 출격하고 싶은 갈증에 피가 끓지 않았소?",
            "임계": f"어서 오시오. 태평양으로 뻗어나갈 거대한 대하의 기운을 품고도, 좁은 수로에 막혀 제자리만 맴돌며 세월을 보낸 {disp_call}의 탄식이 들려오오. 막힌 댐이 언제 터질 것인가 하늘의 신탁을 애타게 기다려오지 않았소?"
        }
    }
    c_group = concern if concern in concern_openings else "career"
    opening_words = concern_openings[c_group].get(elem_pair, concern_openings[c_group]["갑을"])

    if day_gan in ["갑", "을"]:
        opening_scene = "(현허도인이 백옥 찻잔을 내려놓고 침묵 속에 청아한 백단향을 피우며, 푸른 거목의 기운을 머금은 그대의 이마를 서늘하게 응시한다)"
    elif day_gan in ["병", "정"]:
        opening_scene = "(현허도인이 엽전을 정갈하게 정돈하며 불꽃처럼 붉고 그윽한 눈빛으로 그대의 심장을 꿰뚫어 본다)"
    elif day_gan in ["무", "기"]:
        opening_scene = "(현허도인이 묵직한 백옥 옥새를 어루만지며 대지처럼 깊고 흔들림 없는 눈빛으로 그대를 관조한다)"
    elif day_gan in ["경", "신"]:
        opening_scene = "(현허도인이 서늘한 놋그릇을 맑게 울리며 서릿발 같은 칼날의 눈빛으로 그대의 눈빛을 꿰뚫어 본다)"
    else: # 임, 계
        opening_scene = "(현허도인이 맑은 정화수를 백옥 잔에 가만히 따르며 끝없는 심해와 같은 깊은 눈빛으로 그대를 응시한다)"

    # 3. 신체 통증 부위 및 도인의 진단 (고민 및 오행 결합 차별화)
    concern_pains = {
        "career": "극심한 직무 스트레스와 분노로 뒷목과 오른쪽 승모근이 돌처럼 굳고, 관자놀이 편두통이 덮치며 턱관절을 악물어 이가 갈릴 지경이오",
        "love": "가슴 한가운데에 서늘한 얼음 비수가 꽂힌 듯 명치가 꽉 막혀 깊은 한숨을 쉬지 않으면 숨이 막히고, 밤마다 심장이 요동쳐 뜬눈으로 지새우고 있소",
        "wealth": "위장이 경련하듯 뒤틀리고 신경성 위염으로 헛구배가 부르며, 다리에 힘이 풀리고 만성 피로로 아침마다 몸을 일으키지 못하고 있소",
        "timing": "온몸의 기혈이 머리끝으로 치솟아 눈이 충혈되고 안구 건조증이 심하며, 가만히 있어도 손발이 떨리고 조급증에 가슴이 불타오르고 있소"
    }
    body_pain = concern_pains.get(concern, concern_pains["career"])

    if day_gan in ["갑", "을"]:
        body_diagnosis = "뿌리를 내리지 못한 채 공중에 떠 있는 나무처럼 기혈이 머리로 솟구쳐, 정작 제 몸 타들어 가는 줄도 모르고 앞만 보고 달려왔기 때문이오."
        shock_comment = "한 번 꺾인 나뭇가지는 겨울을 지나야 새 잎을 틔우듯, 지난 시련은 그대의 그릇을 키우기 위한 하늘의 전정(剪定)이었소."
        closing_prophecy = "동방 푸른 청룡의 봄바람이 불어오니, 2026년 마침내 비옥한 대지를 뚫고 하늘 높이 거목으로 솟구칠 것이오! 고개를 들고 그대의 영토를 선포하시오!"
    elif day_gan in ["병", "정"]:
        body_diagnosis = "심장의 화기(火氣)가 식지 않고 밤낮으로 타올라, 만인을 품어 안으려다 정작 그대 자신의 영혼이 바짝 타들어 간 것이오."
        shock_comment = "숯이 되어야 비로소 영원히 꺼지지 않는 다이아몬드가 되듯, 그 환란은 그대의 불꽃을 제련하기 위한 신령한 용광로였소."
        closing_prophecy = "남방 붉은 주작의 불꽃이 타오르니, 2026년 병오년 한여름 온 세상이 그대의 이름과 빛 앞에 무릎 꿇을 것이오! 주저 말고 온 세상을 비추시오!"
    elif day_gan in ["무", "기"]:
        body_diagnosis = "만인의 무거운 짐과 하소연을 다 받아내느라 비위와 복부가 굳어, 정작 제 마음 하나 편히 쉬지 못하고 속병을 앓아온 탓이오."
        shock_comment = "모든 것을 품어 안은 대지도 지진을 겪어야 새 땅을 빚어내듯, 묵은 터전을 갈아엎는 불가피한 진통이었소."
        closing_prophecy = "중앙 황금 들판의 추수기가 당도했으니, 2026년 마침내 그대가 흘린 피땀의 억대 곳간이 차곡차곡 채워질 것이오! 흔들림 없이 그 자리를 지키시오!"
    elif day_gan in ["경", "신"]:
        body_diagnosis = "차갑게 벼려진 보검의 서슬이 밖으로 나가지 못하고 제 안을 찔러, 타협하기 싫은 그대의 결벽이 몸을 옥죄어온 것이오."
        shock_comment = "수천 번 달구어지고 망치질을 당해야 천하제일의 명검이 탄생하듯, 그 배신과 고통은 그대를 무적의 승부사로 벼리기 위함이었소."
        closing_prophecy = "서방 백호의 서릿발 기운이 그대의 칼날에 깃들었으니, 2026년 하반기 그대를 방해하던 모든 가짜들을 단칼에 베고 승리를 쟁취할 것이오!"
    else: # 임, 계
        body_diagnosis = "도도히 흘러야 할 거대한 물줄기가 좁은 댐에 가로막혀, 냉기와 부종이 하체로 쏠리며 기혈 순환이 정체된 탓이오."
        shock_comment = "깊은 심해의 어둠을 지나야 비로소 거대한 해일로 솟구치듯, 바닥을 친 자만이 하늘 끝까지 튀어 오를 수 있는 법이오."
        closing_prophecy = "북방 현무의 깊은 바다가 요동치기 시작했으니, 2026년 막혔던 댐이 터지며 그대의 재물과 지혜가 세상을 집어삼킬 것이오! 도도히 전진하시오!"

    # 4. 과거 3개년 (2023 계묘년, 2024 갑진년, 2025 을사년) 고민 결합 환란 적중
    concern_shocks = {
        "career": "지난 2024년(갑진년) 격변의 한복판에서, 내 공로를 가로채려는 상사나 무능한 동료와 부딪혀 일터의 판이 뒤흔들리며 '이러다 모든 것이 끝장나는 것 아닌가' 벼랑 끝에 선 듯 피 말리는 위기를 넘겼지 않소?",
        "wealth": "지난 2023~2024년 무렵, 믿었던 사람의 달콤한 꼬임에 넘어가거나 무리한 투자/대출로 피 같은 종잣돈이 묶여 통장 잔고가 바닥을 드러냈을 때의 그 끔찍한 공포를 겪지 않았소?",
        "love": "지난 2023년(계묘년)~2024년(갑진년) 무렵, 가장 믿고 내 영혼을 다 내주었던 사람의 추악한 이면과 거짓말을 목격하고 '사람이란 대체 무엇인가' 치를 떨며 밤잠을 설치지 않았소?",
        "timing": "손에 거의 다 들어왔다고 여겼던 결정적 기회나 합격/승진의 문턱에서 마지막 1cm를 넘지 못하고 미끄러져, 하늘을 향해 주먹을 쥐고 울분을 삭여온 세월이 있지 않소?"
    }
    recent_shock = concern_shocks.get(concern, concern_shocks["career"])

    # 5. 현재 의뢰자의 비밀스러운 속마음 투시 (고민 영역 집중)
    if concern == "career":
        secret_mind = f"그대가 지금 도인 앞에 무릎 꿇고 앉은 진짜 이유는, 지금 몸담은 일터에서 내 청춘과 비범한 재능이 한낱 부품처럼 소모되는 비참함 때문이오. '지금 당장 이 판을 박차고 나가 내 칼을 쥐어야 하는가, 아니면 당장의 생계를 위해 비굴하게 버텨야 하는가' 두 갈래 절벽 끝에서 피가 마르는 번민을 겪고 있소."
    elif concern == "wealth":
        secret_mind = f"남들 눈에는 부족함 없이 사는 것처럼 그럴듯하게 포장되어 있을지 몰라도, 밤마다 스마트폰 뱅킹 앱을 열어볼 때마다 스쳐 지나간 통장 잔고를 보며 '대체 내가 뼈 빠지게 번 돈은 다 어디로 샜는가' 뼈아픈 현타와 미래에 대한 공포에 짓눌려 있소."
    elif concern == "love":
        secret_mind = f"그대의 영혼은 그 누구보다 따뜻한 온기와 온전한 내 편을 갈망하면서도, 마음 한구석에는 '어차피 사람은 다 떠난다, 내 치부를 보였다가 또다시 상처받을 바엔 차라리 외로운 게 낫다'며 스스로 가시를 돋우고 철벽을 치고 있지 않소."
    else: # timing
        secret_mind = f"내 안에 엄청난 폭발력과 남들보다 비범한 성공을 거둘 잠재력이 분명히 꿈틀거리는데도, 이상하게 결정적인 순간마다 발목이 잡혀 '도대체 내 인생의 황금기는 언제 열리는가' 하늘을 향해 속으로 피눈물을 삼키며 때를 기다려 왔소."

    # 6. 오방기 신탁
    obang_data = OBANGGI.get(obanggi_choice, OBANGGI["황"])

    # 7. 소름 돋는 현허도인(玄虛道人)의 천기 신점 직설 공수 전문 (오행별 완전 독립 내러티브)
    opening_header = f"{synchro_data['synchronicity_speech']}\n\n{opening_scene}\n\n{reunion_prefix}"
    ziwei_block = f"\n\n천상의 황실 비전 자미두수(紫微斗數) 성반을 비추어보니...\n{ziwei_data['oracle_summary']}" if ziwei_data and "oracle_summary" in ziwei_data else ""

    if day_gan in ["갑", "을"]:
        shamanic_speech = f"""{opening_header}"{opening_words}

생명의 기운이 머무는 그대의 육신을 먼저 짚어보자면...
그대는 지금 **{body_pain}**.
{body_diagnosis}

비바람에 가지가 찢기던 지난 환란의 세월을 돌아보시오.
**{recent_shock}**
{shock_comment} 그대가 밤마다 홀로 삼킨 눈물을 동방의 청룡신께서 빠짐없이 굽어보고 계셨소.

남들에게는 차마 털어놓지 못한 채 가슴속에 묻어둔 그대의 비밀스러운 속마음...
**{secret_mind}**

도인의 영안으로 {disp_call}의 무의식 심층을 들여다보니, 그대의 내면에는 **[{shadow_type}]**의 응어리가 웅크리고 있소. {shadow_insight}{ziwei_block}

그대의 등 뒤를 지키는 **{spirit_info[0]}**이 이제는 낡은 껍질을 찢고 거목으로 솟구치라며 강한 영동을 일으키고 있소!
{spirit_info[1]}.

의뢰자가 뽑아 든 신령한 깃발, **{obang_data['color']}**이 가리키는 천상의 신탁을 똑똑히 들으시오:
**\"{obang_data['oracle']}\"**

{closing_prophecy} 망설임을 끝내고 당당히 그대만의 영토를 개척하시오!\""""
    elif day_gan in ["병", "정"]:
        shamanic_speech = f"""{opening_header}"{opening_words}

타오르는 화기가 깃든 그대의 육신과 혈맥을 투시해보니...
그대는 지금 **{body_pain}**.
{body_diagnosis}

가슴속에 화염병을 품고 버텨온 지난 2~3년의 고통...
**{recent_shock}**
{shock_comment} 재가 된 가슴을 부여잡고 버텨온 그대의 투혼을 하늘의 신령께서 증명하고 계시오.

화려한 웃음 뒤에 감추어둔 영혼의 비명과 진짜 속내...
**{secret_mind}**

도인의 영안으로 {disp_call}의 무의식 심층을 들여다보니, 그대의 내면에는 **[{shadow_type}]**의 응어리가 웅크리고 있소. {shadow_insight}{ziwei_block}

그대의 영혼을 이끄는 **{spirit_info[0]}**이 잠자던 화톳불을 거대한 태양으로 폭발시키라며 신호를 보내고 있소.
{spirit_info[1]}.

그대의 직관이 선택한 **{obang_data['color']}**의 깃발에서 떨어진 추상같은 천벌과 축복의 신탁:
**\"{obang_data['oracle']}\"**

{closing_prophecy} 그대의 불꽃으로 어두운 천하를 밝히시오!\""""
    elif day_gan in ["무", "기"]:
        shamanic_speech = f"""{opening_header}"{opening_words}

천하 만물을 떠받치는 그대의 골격과 오장육부를 짚어보리다.
그대는 지금 **{body_pain}**.
{body_diagnosis}

대지가 갈라지듯 묵은 터전이 흔들리던 지난 풍파의 세월...
**{recent_shock}**
{shock_comment} 남모르게 무거운 짐을 혼자 짊어지고 피를 토했던 그대의 충직함을 대지의 신령이 보듬어 주시오.

누구에게도 기대지 못한 채 혼자 삭여온 외로운 고백...
**{secret_mind}**

도인의 영안으로 {disp_call}의 무의식 심층을 들여다보니, 그대의 내면에는 **[{shadow_type}]**의 응어리가 웅크리고 있소. {shadow_insight}{ziwei_block}

그대의 터전을 수호하는 **{spirit_info[0]}**이 이제는 황금 곳간을 단단히 잠그고 주인이 되라며 영적 진동을 울리고 있소.
{spirit_info[1]}.

그대가 무의식중에 집어 든 **{obang_data['color']}**을 통해 하달된 천지의 영험한 칙명:
**\"{obang_data['oracle']}\"**

{closing_prophecy} 태산처럼 묵직하게 그대의 자리를 지키며 부의 결실을 수확하시오!\""""
    elif day_gan in ["경", "신"]:
        shamanic_speech = f"""{opening_header}"{opening_words}

서릿발 같은 쇠기운이 맺힌 그대의 신경과 급소를 겨누어보니...
그대는 지금 **{body_pain}**.
{body_diagnosis}

날선 칼끝에 베이고 찔리며 버텨온 지난 시련의 잔해...
**{recent_shock}**
{shock_comment} 억울하게 삼켜야 했던 분노와 피눈물을 서방의 백호신령이 하나도 놓치지 않고 지켜보았소.

자존심의 껍질 속에 숨겨둔 처절한 고독과 고뇌...
**{secret_mind}**

도인의 영안으로 {disp_call}의 무의식 심층을 들여다보니, 그대의 내면에는 **[{shadow_type}]**의 응어리가 웅크리고 있소. {shadow_insight}{ziwei_block}

그대의 등 뒤에서 칼날을 벼리는 **{spirit_info[0]}**이 가짜들을 단칼에 베어내고 새 질서를 세우라 명하고 있소.
{spirit_info[1]}.

순간의 영감으로 뽑아 올린 **{obang_data['color']}**이 증명하는 서슬 퍼런 천기의 신탁:
**\"{obang_data['oracle']}\"**

{closing_prophecy} 보검을 뽑아 들고 당당히 승리의 깃발을 꽂으시오!\""""
    else: # 임, 계
        shamanic_speech = f"""{opening_header}"{opening_words}

도도히 흘러야 할 생명수의 맥박과 하체 기혈을 관조해보니...
그대는 지금 **{body_pain}**.
{body_diagnosis}

댐이 무너지듯 막막한 어둠에 갇혀 헤매던 지난 환란의 기억...
**{recent_shock}**
{shock_comment} 칠흑 같은 심해의 고독 속에서 지새운 밤들을 북방 현무의 영신이 굽어살피고 계셨소.

잔잔한 수면 아래서 소용돌이치는 진짜 갈증과 속내...
**{secret_mind}**

도인의 영안으로 {disp_call}의 무의식 심층을 들여다보니, 그대의 내면에는 **[{shadow_type}]**의 응어리가 웅크리고 있소. {shadow_insight}{ziwei_block}

그대의 영혼을 이끄는 **{spirit_info[0]}**이 막힌 물길을 트고 천하의 부를 쓸어 담으라며 파도를 일으키고 있소.
{spirit_info[1]}.

그대의 직관이 선택한 **{obang_data['color']}**의 깃발이 가리키는 천상의 신령한 계시:
**\"{obang_data['oracle']}\"**

{closing_prophecy} 도도히 흘러 바다를 집어삼키는 거대한 대하가 되시오!\""""

    return {
        "spirit_name": spirit_info[0],
        "spirit_desc": spirit_info[1],
        "body_pain": body_pain,
        "recent_shock": recent_shock,
        "secret_mind": secret_mind,
        "unconscious_shadow": {
            "type": shadow_type,
            "insight": shadow_insight
        },
        "ziwei_summary": ziwei_data.get("oracle_summary", "") if ziwei_data else "",
        "synchronicity": synchro_data,
        "is_reunion": is_reunion,
        "obanggi": obang_data,
        "shamanic_speech": shamanic_speech,
        "moment_timestamp": now.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    }

if __name__ == '__main__':
    from manseryeok import calculate_saju
    s1 = calculate_saju(1993, 8, 17, 18, 0)
    s2 = calculate_saju(1982, 3, 10, 8, 30)
    v1 = analyze_shamanic_vision(s1, "청", "career", "이몽룡")
    v2 = analyze_shamanic_vision(s2, "적", "wealth", "성춘향")
    print("=== 비전 1 ===")
    print(v1["shamanic_speech"][:150])
    print("=== 비전 2 ===")
    print(v2["shamanic_speech"][:150])
