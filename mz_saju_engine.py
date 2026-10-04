# -*- coding: utf-8 -*-
"""
2030 세대 특화 바이럴 사주 인텔리전스 엔진 (MZ Saju Intelligence Engine)
- 60갑자 일주별 2030 고유 캐릭터 페르소나 60종 전수 매핑
- 심리 애착 유형(회피형/불안형/자유형/안정형) 사주 알고리즘 매핑
- 직장 번아웃 지수(0~100%) 및 퇴사/이직 골든타임 월별 캘린더
- 재테크 돈복 성향 (코인/스윙 vs 안정배당 vs 지식콘텐츠)
- 인스타 스토리 / 카카오톡 바이럴 공유 카드 텍스트 생성
"""

# 60갑자 2030 고유 캐릭터 페르소나 (60종 전수 구축)
MZ_PERSONA_60 = {
    # 1~10 갑자순
    "갑자": {
        "title": "밤을 지새우는 은둔형 천재 디렉터",
        "mbti": "INTJ",
        "tags": ["#철벽바운더리", "#야행성아이디어", "#말보다결과"],
        "punchline": "겉으론 덤덤하게 웃어주지만, 속으로는 0.1초 만에 상대방 손절 견적 다 뽑아둠.",
        "career_fit": "1인 기획자, 데이터 전략가, 독창적 크리에이터",
        "bad_habit": "혼자 다 끌어안고 끙끙 앓다가 번아웃 폭발."
    },
    "을축": {
        "title": "빙판을 뚫고 피어나는 끈기의 생존러",
        "mbti": "ISTJ",
        "tags": ["#존버의달인", "#통장잔고안식", "#실속주의"],
        "punchline": "남들이 힘들다고 때려칠 때 끝까지 살아남아서 마지막에 건물 올릴 사람.",
        "career_fit": "금융/회계, 정밀 엔지니어링, 전문 자격직",
        "bad_habit": "남의 눈치 보느라 정작 자기가 하고 싶은 말은 목구멍으로 삼킴."
    },
    "병인": {
        "title": "멈추지 않는 도파민 기관차 리더",
        "mbti": "ENFP",
        "tags": ["#열정폭발", "#충동적실행력", "#흥미식으면끝"],
        "punchline": "아이디어 100개 던지고 첫날엔 밤새서 불태우지만, 3일 지나면 다음 관심사로 워프.",
        "career_fit": "스타트업 창업, 마케팅 디렉터, 엔터테인먼트",
        "bad_habit": "벌려놓은 일 수습 못 해서 주변 사람들이 대신 뜀."
    },
    "정묘": {
        "title": "새벽 감성에 젖은 팩폭 힐러",
        "mbti": "INFJ",
        "tags": ["#영혼스캐너", "#감성완벽주의", "#겉따속냉"],
        "punchline": "상담은 세상 따뜻하게 해놓고, 집에 돌아오면 핸드폰 비행기 모드 켜고 침대에 쓰러짐.",
        "career_fit": "심리/상담, 브랜드 스토리텔러, UX/UI 디자인",
        "bad_habit": "상대방의 사소한 눈빛 하나에 온갖 의미 부여하며 밤새 잠 못 잠."
    },
    "무진": {
        "title": "판을 뒤엎는 야망의 불도저 수장",
        "mbti": "ENTJ",
        "tags": ["#카리스마폭격", "#큰그림장인", "#무능한상사극혐"],
        "punchline": "내 밑으로 들어오면 뼈를 갈아서라도 성공시켜 주지만, 어설픈 징징거림은 가차 없이 차단.",
        "career_fit": "프로젝트 총괄 PM, 신사업 기획, 경영 전략",
        "bad_habit": "모든 것을 통제하려다 몸과 간이 먼저 망가짐."
    },
    "기사": {
        "title": "디테일에 집착하는 완벽주의 조율자",
        "mbti": "ISFJ",
        "tags": ["#메모광", "#치밀한설계", "#실수용납불가"],
        "punchline": "화려하게 나서는 것보다 뒤에서 모든 시스템이 오차 없이 돌아가게 세팅하는 흑막.",
        "career_fit": "시스템 아키텍트, 운영 총괄, 재무 분석가",
        "bad_habit": "계획대로 안 풀리면 세상이 무너진 것처럼 극심한 스트레스."
    },
    "경오": {
        "title": "칼 품은 백마 위의 겉바속촉 워커홀릭",
        "mbti": "ESTJ",
        "tags": ["#팩폭주의보", "#자존심이목숨", "#의외로순정파"],
        "punchline": "말은 세상 차갑고 살벌하게 쏘아붙이지만, 뒤에서 몰래 내 편 챙겨주는 츤데레 끝판왕.",
        "career_fit": "전문직 수장, 법조/감사, 브랜드 디렉터",
        "bad_habit": "남한테 아쉬운 소리 죽어도 못 해서 혼자 독박 쓰고 과로사 직전까지 감."
    },
    "신미": {
        "title": "사막에서 보석을 깎는 고독한 장인",
        "mbti": "ISFP",
        "tags": ["#취향원탑", "#예민보스", "#내공간침범금지"],
        "punchline": "남들이 유행 쫓아갈 때 혼자 마이너한 취향 파고들어서 독보적인 영역 구축함.",
        "career_fit": "아트 디렉터, 럭셔리 제품 기획, 프리랜서 전문가",
        "bad_habit": "자존심 긁히면 마음의 문을 철문으로 닫고 영구 잠수."
    },
    "임신": {
        "title": "수를 백 번 앞서보는 지략가",
        "mbti": "INTP",
        "tags": ["#통찰력만렙", "#포커페이스", "#기회포착귀신"],
        "punchline": "평소엔 멍 때리는 척 가만히 있다가 타이밍 오면 아무도 예상 못한 한 방으로 판을 독식.",
        "career_fit": "퀀트 투자, 전략 컨설팅, AI 리서처",
        "bad_habit": "생각이 너무 많아서 결정적 순간에 타이밍 재다가 버스 떠남."
    },
    "계유": {
        "title": "맑은 이슬 속에 독을 품은 완벽주의자",
        "mbti": "ISTP",
        "tags": ["#칼같은선긋기", "#결벽적깔끔함", "#효율지상주의"],
        "punchline": "조용하고 얌전해 보이지만, 본인 영역 건드리면 한마디로 숨통 끊어놓는 팩트 폭격기.",
        "career_fit": "보안/품질 감사, 정밀 코딩, 연구원",
        "bad_habit": "사람 관계를 0과 1로 계산해서 정나미 떨어진다는 소리 종종 들음."
    },

    # 11~20 갑자순
    "갑술": {"title": "충직한 의리의 들불 개척가", "mbti": "ENFJ", "tags": ["#의리파", "#직진본능", "#내사람무한쉴드"], "punchline": "내 편 건드리면 물불 안 가리고 달려들지만, 배신당하면 회복에 3년 걸림.", "career_fit": "팀 리딩, 대외 협력, 이벤트 디렉터", "bad_habit": "남 좋은 일만 시켜주고 정작 자기 실속은 못 챙김."},
    "을해": {"title": "푸른 바다 위를 떠다니는 낭만 선장", "mbti": "INFP", "tags": ["#감성치트키", "#자유로운영혼", "#예술적촉"], "punchline": "회의 시간에 영혼은 이미 유럽 카페 테라스에 가 있음. 감정 기복이 파도 수준.", "career_fit": "에세이 작가, 영상 크리에이터, 공간 기획", "bad_habit": "현실적 서류 작업이나 세금 계산 앞에서 무기력증에 빠짐."},
    "병자": {"title": "얼어붙은 호수를 녹이는 태양의 쇼맨", "mbti": "ESFP", "tags": ["#인싸력폭발", "#주목공포증제로", "#화려한조명"], "punchline": "어딜 가나 모임의 중심에 서야 직성이 풀림. 관심 끊기면 우울증 도짐.", "career_fit": "방송/미디어, 쇼호스트, 인플루언서", "bad_habit": "충동구매와 화려한 겉치레로 통장 잔고가 항상 파도침."},
    "정축": {"title": "소리 없이 부를 쌓는 지하 암반수", "mbti": "ISTJ", "tags": ["#통장비밀주의", "#묵직한내공", "#겉소속용"], "punchline": "평소엔 돈 없는 척 제일 허름하게 입고 다니는데 알고 보면 부동산 숨겨둠.", "career_fit": "부동산 투자, 자산 관리, 인프라 개발", "bad_habit": "돈 쓰는 데 너무 인색해서 주변 사람들 답답해 죽음."},
    "무인": {"title": "포효하는 호랑이 등 위의 승부사", "mbti": "ENTJ", "tags": ["#야망원탑", "#호랑이기상", "#2인자는없다"], "punchline": "누구 밑에서 시키는 일 절대 못 함. 내 사업을 하든가 팀을 쥐고 흔들어야 함.", "career_fit": "벤처 CEO, 사모펀드 운용, M&A", "bad_habit": "급발진 성격 때문에 다 잡은 물고기를 그물 찢어서 놓침."},
    "기묘": {"title": "풀밭을 달리는 예민한 산토끼", "mbti": "ISFP", "tags": ["#안테나풀가동", "#불안감높음", "#민첩한도망"], "punchline": "위기 감지 능력이 세계 1위. 쎄한 느낌 들면 남들보다 3초 먼저 탈출구 찾음.", "career_fit": "트렌드 캐처, 패션 MD, 리스크 관리", "bad_habit": "아직 일어나지도 않은 미래의 걱정 때문에 매일 밤샘."},
    "경진": {"title": "비늘 속에 칼을 감춘 괴강의 백룡", "mbti": "ESTP", "tags": ["#승부욕괴물", "#기싸움무패", "#압도적기세"], "punchline": "지각해도 당당하고 혼나도 콧방귀 뀜. 기싸움에서 져본 역사가 없는 괴물 멘탈.", "career_fit": "투자 유치, 영업 총괄, 대형 협상가", "bad_habit": "자기가 항상 옳다는 독선 때문에 사람 여럿 떠나보냄."},
    "신사": {"title": "화려한 백화점 1층의 빛나는 다이아", "mbti": "ESFJ", "tags": ["#귀티좔좔", "#센스천재", "#평판관리원탑"], "punchline": "남들에게 보이는 내 이미지와 평판이 곧 생명. 단점이나 빈틈 절대 안 보임.", "career_fit": "VIP 마케팅, 큐레이터, 브랜드 컨설턴트", "bad_habit": "완벽한 가면 쓰느라 혼자 있을 때 우울감 폭발."},
    "임오": {"title": "물과 불을 동시에 품은 반전 매력러", "mbti": "ENFP", "tags": ["#극과극텐션", "#스위치온오프", "#마성의매력"], "punchline": "어제는 세상 우울한 철학자였다가 오늘은 클럽에서 춤추고 있는 종잡을 수 없는 영혼.", "career_fit": "광고 카피라이터, 공연 기획, 유튜브 크리에이터", "bad_habit": "감정에 따라 일의 퀄리티가 천국과 지옥을 오감."},
    "계미": {"title": "가뭄 든 메마른 땅을 적시는 단비", "mbti": "INFJ", "tags": ["#외유내강", "#사막의오아시스", "#은근한집념"], "punchline": "온순하고 착해 보이지만, 자기가 목표한 것은 10년이 걸려도 기어이 이뤄냄.", "career_fit": "사회공헌, 교육, 연구직, 심리상담", "bad_habit": "자기 희생이 너무 심해서 에너지 다 빨리고 기절함."},

    # 21~30 갑자순
    "갑신": {"title": "바위산을 가르는 천둥 번개의 검객", "mbti": "ENTP", "tags": ["#기동력갑", "#틀깨기달인", "#말싸움최강"], "punchline": "기존의 틀이나 꼰대 문화 보면 발작 버튼 눌려서 바로 시스템 붕괴시키러 감.", "career_fit": "혁신 컨설팅, 테크 스타트업, 법정 변호", "bad_habit": "말이 너무 직설적이라 의도치 않게 적을 많이 만듦."},
    "을유": {"title": "절벽 위에 핀 날카로운 난초", "mbti": "INTJ", "tags": ["#극단적결벽", "#예리한촉", "#타협불가"], "punchline": "어설픈 퀄리티는 내 눈앞에 들이밀지도 마라. 1픽셀 틀린 것도 찾아내는 매의 눈.", "career_fit": "정밀 검수, 코드 리뷰어, 오디오/비주얼 마스터링", "bad_habit": "자기 자신을 너무 채찍질해서 스스로 피폐해짐."},
    "병술": {"title": "황혼의 노을을 품은 고독한 사색가", "mbti": "INTP", "tags": ["#철학자모드", "#통찰과허무", "#현실초월"], "punchline": "세상 돌아가는 꼴 다 부질없다고 하면서도, 막상 게임이나 취미엔 광적으로 몰입.", "career_fit": "게임 기획, 세계관 설계, 인문학 연구", "bad_habit": "우울의 늪에 한 번 빠지면 몇 주 동안 연락 두절."},
    "정해": {"title": "밤바다를 비추는 천상의 은하수 등대", "mbti": "INFJ", "tags": ["#천을귀인보유", "#영적아우라", "#우아한품격"], "punchline": "별 노력 안 하는 것 같은데 이상하게 주변에 귀인들이 알아서 길을 터줌.", "career_fit": "문화예술 디렉터, 해외 주재원, 럭셔리 브랜딩", "bad_habit": "남의 부탁을 거절 못 해서 혼자 덤터기 씀."},
    "무자": {"title": "어둠 속의 황금 광산을 찾아낸 채굴러", "mbti": "ISTJ", "tags": ["#현금창출능력", "#지하비밀기지", "#철저한보안"], "punchline": "사람들은 쟤가 뭐 해서 돈 버는지 아무도 모름. 계좌엔 조용히 현금이 쌓이는 중.", "career_fit": "비상장 투자, 암호화폐 퀀트, 무역 유통", "bad_habit": "비밀이 너무 많아서 연애할 때 상대방이 의심병 걸림."},
    "기축": {"title": "눈 덮인 논밭을 지키는 뚝심의 농부", "mbti": "ISFJ", "tags": ["#소처럼묵묵히", "#신뢰도200%", "#약속목숨"], "punchline": "화려한 말발은 없지만 이 사람이 맡은 프로젝트는 단 한 번도 펑크 난 적 없음.", "career_fit": "공공기관, 대기업 운영 관리, 백엔드 개발", "bad_habit": "변화를 극도로 두려워해서 새로운 기회를 놓치기 일쑤."},
    "경인": {"title": "정글을 휘어잡는 백호의 사냥꾼", "mbti": "ESTP", "tags": ["#돌격앞으로", "#리스크테이커", "#한방승부"], "punchline": "안전한 길은 지루해서 못 참음. 하이리스크 하이리턴 판에 인생을 던지는 승부사.", "career_fit": "스윙 트레이더, 벤처 캐피탈리스트, 영업 킹", "bad_habit": "한 번 삐끗하면 전 재산 털릴 위험이 상존함."},
    "신묘": {"title": "가위를 든 정밀한 세공사", "mbti": "ISTP", "tags": ["#손기술장인", "#빠른눈치", "#실리우선"], "punchline": "예술적 감각과 상업적 계산이 기가 막히게 결합됨. 돈 안 되는 예술은 안 함.", "career_fit": "영상 편집, 그래픽 디자인, 전자상거래 셀러", "bad_habit": "가까운 사람에게도 계산적인 태도가 튀어나와 서운하게 만듦."},
    "임진": {"title": "여의주를 입에 문 흑룡의 지배자", "mbti": "ENTJ", "tags": ["#판을뒤흔듦", "#압도적스케일", "#승부사기질"], "punchline": "조무래기들과의 싸움엔 관심 없음. 시장 전체를 먹어치울 큰 판만 기획함.", "career_fit": "플랫폼 창업, 글로벌 펀드, 종합 엔터테인먼트", "bad_habit": "승리에 눈이 멀어 곁에 있는 소중한 사람을 외롭게 만듦."},
    "계사": {"title": "햇살 아래 반짝이는 영롱한 샘물", "mbti": "ENFJ", "tags": ["#재물귀인", "#처세술의신", "#미소속계산"], "punchline": "웃는 얼굴로 모두와 친하게 지내지만, 누구와 손잡아야 이득인지 이미 엑셀표로 정리 끝.", "career_fit": "대외협력 IR, 프라이빗 뱅커, 인재 헤드헌터", "bad_habit": "가식적이라는 오해를 사기 쉬우니 진심을 보여야 함."},

    # 31~40 갑자순
    "갑오": {"title": "불꽃을 품은 질주의 야생마", "mbti": "ENFP", "tags": ["#스피드광", "#솔직담백", "#뒤끝제로"], "punchline": "생각나면 3초 안에 액션 시작. 말도 거침없이 시원하게 쏘아붙이고 뒤끝은 없음.", "career_fit": "라이브 커머스, 스포츠/액티비티, PR 매니저", "bad_habit": "인내심이 바닥이라 장기 프로젝트 맡으면 온몸이 비비 꼬임."},
    "을미": {"title": "모래사막을 건너는 지혜로운 백양", "mbti": "INFJ", "tags": ["#백절불굴", "#차분한독기", "#조용한승리"], "punchline": "세상 순둥이처럼 보이지만 밟히면 두 배로 갚아주는 무서운 집념의 소유자.", "career_fit": "학술 연구, 지식재산권, 바이오/헬스케어", "bad_habit": "속으로 한을 품으면 평생 안 잊고 복수의 칼을 갊."},
    "병신": {"title": "재주 많은 붉은 원숭이의 천재성", "mbti": "ENTP", "tags": ["#아이디어화수분", "#재주꾼", "#말빨만렙"], "punchline": "어려운 문제도 남들과 전혀 다른 각도에서 1분 만에 묘수를 찾아내는 천재.", "career_fit": "크리에이티브 디렉터, 예능 PD, 발명가", "bad_habit": "하나를 진득하게 끝까지 못 파고 딴짓하러 감."},
    "정유": {"title": "어둠 속에서 빛나는 금빛 촛불", "mbti": "ISFJ", "tags": ["#천을귀인", "#정밀함의극치", "#고급진센스"], "punchline": "남들이 못 보는 작은 흠집 하나까지 잡아내는 완벽한 심미안과 배려심.", "career_fit": "주얼리 디자인, 정밀 의료, 고급 호텔리어", "bad_habit": "남의 시선과 평가에 지나치게 신경 쓰느라 피곤함."},
    "무술": {"title": "태산처럼 우뚝 솟은 괴강의 거인", "mbti": "ESTJ", "tags": ["#불도저추진", "#신용과의리", "#타협없는원칙"], "punchline": "한번 약속한 것은 손해를 보더라도 지킴. 원칙을 어기면 누구든 얄짤없음.", "career_fit": "건설/부동산, 공공 안전, 대형 총괄", "bad_habit": "고집이 황소고집이라 주변의 좋은 충고를 다 튕겨냄."},
    "기해": {"title": "바다를 품은 비옥한 평야의 기획가", "mbti": "INFP", "tags": ["#다정다감", "#재물복탑재", "#풍요로운감성"], "punchline": "사람들에게 밥 잘 사주고 따뜻하게 대해주는데, 이상하게 본인 통장은 더 불어남.", "career_fit": "F&B 브랜드, 식문화 기획, 커뮤니티 매니저", "bad_habit": "우유부단해서 맺고 끊는 것을 잘 못함."},
    "경자": {"title": "얼음물 속에 담긴 날카로운 비수", "mbti": "INTP", "tags": ["#촌철살인", "#차가운이성", "#냉철한비판"], "punchline": "감정에 휘둘리는 꼴을 제일 혐오함. 팩트와 논리로 상대를 순식간에 제압.", "career_fit": "데이터 사이언스, 감사원, 디버깅 전문가", "bad_habit": "차가운 말 한마디로 연인이나 친구에게 평생 상처 줌."},
    "신축": {"title": "빙판 속에서 빛을 발하는 차가운 백금", "mbti": "ISTJ", "tags": ["#인내심괴물", "#절대안흔들림", "#비밀금고"], "punchline": "남들이 뭐라고 떠들든 내 갈 길만 묵묵히 걸어서 결국 제일 높은 곳에 도달.", "career_fit": "전략 연구원, 자산 운용, 특허 변리사", "bad_habit": "마음속 응어리를 절대 안 풀고 속으로 삭임."},
    "임인": {"title": "새벽 호수를 가로지르는 푸른 호랑이", "mbti": "ENFJ", "tags": ["#식신문창", "#풍류와지혜", "#천재적표현력"], "punchline": "공부도 잘하고 노는 것도 1등. 가만히 있어도 사람들이 따르는 마성의 인덕.", "career_fit": "베스트셀러 작가, 대학교수, 문화 멘토", "bad_habit": "자기 재능만 믿고 게으름 피우다가 마감 직전에 벼락치기."},
    "계묘": {"title": "아침 이슬을 머금은 숲속의 꽃사슴", "mbti": "ESFP", "tags": ["#귀여움만렙", "#천을귀인", "#사랑받는체질"], "punchline": "남들에게 미움받을 수 없는 러블리한 에너지. 부탁하면 거절하기 힘든 마력.", "career_fit": "키즈/펫 산업, 캐릭터 디자이너, 뷰티 크리에이터", "bad_habit": "현실 감각이 부족해서 뜬구름 잡는 소리 자주 함."},

    # 41~50 갑자순
    "갑진": {"title": "용의 등을 타고 승천하는 거목", "mbti": "ENTJ", "tags": ["#백호대살보유", "#돌파력100단", "#리더의표본"], "punchline": "역경이 오면 오히려 눈빛이 살아남. 남들이 포기한 프로젝트를 살려내는 구원투수.", "career_fit": "위기관리 전문가, 기업 회생, 신규 사업 총괄", "bad_habit": "부하 직원들을 자기 기준에 맞추려다 숨 막히게 만듦."},
    "을사": {"title": "화려하게 피어난 매혹의 붉은 꽃", "mbti": "ENFP", "tags": ["#끼폭발", "#말솜씨치트키", "#화려한스포트라이트"], "punchline": "가만히 있어도 도화의 기운이 뚝뚝 떨어짐. 사람 홀리는 말솜씨와 표현력.", "career_fit": "엔터테이너, 패션 스타일리스트, 마케터", "bad_habit": "변덕이 심하고 질투심이 많아서 감정 낭비 심함."},
    "병오": {"title": "하늘 한가운데 타오르는 한낮의 태양", "mbti": "ENTP", "tags": ["#양인살보유", "#폭발적에너지", "#절대타협없음"], "punchline": "그대의 존재감 자체가 핵폭탄. 숨기려 해도 숨길 수 없는 압도적인 오오라.", "career_fit": "스포츠 스타, 탑티어 인플루언서, 승부형 CEO", "bad_habit": "성질 한 번 내면 주변이 초토화되어 후폭풍 수습 불가."},
    "정미": {"title": "달빛 아래서 도자기를 굽는 열정의 장인", "mbti": "ISFJ", "tags": ["#은근한집념", "#내면의불꽃", "#의외의고집"], "punchline": "평소엔 조용하고 착하지만, 자기가 꽂힌 일에는 며칠 밤을 새우며 집착하는 광기.", "career_fit": "전문 장인, R&D 연구, 전문 테라피스트", "bad_habit": "속에 화를 쌓아두다가 한 번에 폭발해서 판을 깸."},
    "무신": {"title": "드넓은 대지를 누비는 역마의 탐험가", "mbti": "ESTP", "tags": ["#역마살장착", "#전국구인맥", "#글로벌무대"], "punchline": "한 사무실에 갇혀 있으면 병남. 비행기 타고 전 세계를 돌아다녀야 돈이 붙음.", "career_fit": "해외 영업, 무역, 물류 혁신, 여행 비즈니스", "bad_habit": "한곳에 정착을 못 해서 연애가 장기적으로 이어지기 힘듦."},
    "기유": {"title": "풍요로운 가을 들판의 알곡 감별사", "mbti": "ISTJ", "tags": ["#문창귀인", "#실속의화신", "#정확한데이터"], "punchline": "감으로 일하지 않고 오직 데이터와 숫자로만 승부. 수익 안 나는 구조는 칼같이 정리.", "career_fit": "데이터 애널리스트, 벤치마킹 분석, 세무사", "bad_habit": "낭만이나 감성을 무시해서 로봇 같다는 소리 들음."},
    "경술": {"title": "철벽 요새를 지키는 괴강의 맹장", "mbti": "ESTJ", "tags": ["#괴강살보유", "#강철멘탈", "#군림하는리더"], "punchline": "어떤 위기 상황이 닥쳐도 눈 하나 깜짝 안 함. 조직의 든든한 방패이자 칼날.", "career_fit": "보안 수석, 법률 자문, 리스크 테이킹", "bad_habit": "남의 약점을 보면 무의식중에 지적해서 원망을 삼."},
    "신해": {"title": "맑은 샘물에 씻은 영롱한 에메랄드", "mbti": "INFP", "tags": ["#금수상청", "#예술적천재", "#촌철살인팩폭"], "punchline": "두뇌 회전이 슈퍼컴퓨터급. 똑똑하고 아름다우나 오만함이 있어 아무나 안 쳐다봄.", "career_fit": "프리미엄 브랜딩, UX 디자인 디렉터, 영화/시나리오", "bad_habit": "자기 기준에 못 미치는 사람을 은근히 무시함."},
    "임자": {"title": "심해의 깊은 어둠을 지배하는 제왕", "mbti": "INTJ", "tags": ["#양인살보유", "#거대한스케일", "#속을알수없음"], "punchline": "겉은 한없이 고요하지만 속으로는 대양을 집어삼킬 파도를 준비하는 절대적 강자.", "career_fit": "빅데이터 인프라, 해운/글로벌 펀드, 전략가", "bad_habit": "자기 속마음을 죽어도 털어놓지 않아 벽이 느껴짐."},
    "계축": {"title": "한겨울 눈보라를 버티는 검은 소", "mbti": "ISTP", "tags": ["#백호대살", "#독기품은끈기", "#결정타의신"], "punchline": "모진 고난도 묵묵히 삼켜냄. 나중에 성공해서 나를 무시했던 사람들 앞에 당당히 등장.", "career_fit": "핵심 기술 엔지니어, 전문 의료, 자산 증식", "bad_habit": "자신을 너무 억누르다 우울증이나 신체화 증상으로 고생."},

    # 51~60 갑자순
    "갑인": {"title": "원시림의 거대한 호랑이 나무", "mbti": "ENTJ", "tags": ["#간여지동", "#자존심최강", "#독립선언"], "punchline": "남의 간섭은 0.1초도 못 참음. 내가 내 인생의 법이고 규칙이어야 숨을 쉼.", "career_fit": "전문직 1인 대표, 프리랜서 거물, 독자 연구", "bad_habit": "타협을 모르는 성격 때문에 부러지기 쉬움."},
    "을묘": {"title": "싱그러운 생명력의 넝쿨 담쟁이", "mbti": "ENFP", "tags": ["#간여지동", "#친화력끝판왕", "#끈질긴생존력"], "punchline": "어떤 척박한 환경에 던져놔도 사람들과 인맥을 트고 벽을 기어올라 기어이 햇살을 봄.", "career_fit": "네트워킹 디렉터, 에이전시 대표, 미디어 기획", "bad_habit": "여기저기 사람 챙기느라 정작 자기 시간과 통장이 텅 빔."},
    "병진": {"title": "아침 호수 위를 떠오르는 희망의 태양", "mbti": "ENFJ", "tags": ["#관대함", "#만인의형님/언니", "#스케일큰배려"], "punchline": "주변에 늘 사람이 바글거림. 퍼주고 베푸는 것을 좋아해서 따르는 동생들이 많음.", "career_fit": "커뮤니티 수장, 교육 사업, 대형 협회장", "bad_habit": "밑 빠진 독에 물 붓듯 남 퍼주다가 자기 통장 털림."},
    "정사": {"title": "용광로처럼 타오르는 예술혼의 화신", "mbti": "ESFP", "tags": ["#간여지동", "#불타는열정", "#순수한광기"], "punchline": "적당히 하는 것은 없다. 사랑이든 일이든 내 모든 영혼을 불살라야 끝이 남.", "career_fit": "무대 예술, 파인다이닝 셰프, 패션 디자이너", "bad_habit": "감정이 격해지면 앞뒤 안 가리고 폭주함."},
    "무오": {"title": "화산재를 뿜어내는 붉은 화산의 군주", "mbti": "ENTP", "tags": ["#양인살보유", "#압도적카리스마", "#판세를뒤집음"], "punchline": "작은 일엔 덤벙거리지만, 판이 커지고 위기가 닥치면 영웅적 기질을 발휘함.", "career_fit": "위기 돌파형 수장, 대형 부동산 개발, 투자 총괄", "bad_habit": "디테일한 실무 관리를 극도로 귀찮아함."},
    "기미": {"title": "태양 볕에 단단히 구워진 대지의 옹기", "mbti": "ISTJ", "tags": ["#간여지동", "#철벽신용", "#뚝심의승리자"], "punchline": "한 번 맺은 인연과 신뢰는 평생 감. 속마음은 쉽게 안 열지만 열리면 간 쓸개 다 줌.", "career_fit": "신용 평가, 보안 및 감사, 프랜차이즈 본부", "bad_habit": "변화에 너무 둔감해서 시대 트렌드를 놓치기 쉬움."},
    "경신": {"title": "바위산을 가르는 서슬 퍼런 보검", "mbti": "ESTJ", "tags": ["#간여지동", "#타협없는정의", "#카리스마종결"], "punchline": "부정한 꼴이나 꼼수를 죽어도 못 봄. 거짓말하는 사람은 그 자리에서 응징.", "career_fit": "감사원, 컴플라이언스 총괄, 법조계, 보안", "bad_habit": "너무 차갑고 엄격해서 주변 사람들이 무서워서 피함."},
    "신유": {"title": "순도 99.9%의 차가운 순백 다이아몬드", "mbti": "INTJ", "tags": ["#간여지동", "#결벽증적완벽", "#독보적미모/센스"], "punchline": "티끌 하나 묻는 것도 용납 못 함. 나의 품격과 자존심을 건드리면 평생 안 봄.", "career_fit": "명품/하이엔드 산업, 정밀 분석, 럭셔리 큐레이터", "bad_habit": "타인에 대한 기준치가 너무 높아 연애하기 극도로 힘듦."},
    "임술": {"title": "사막의 오아시스를 숨긴 신비의 호수", "mbti": "INTP", "tags": ["#백호대살", "#지혜와비밀", "#재물창고보유"], "punchline": "남들에게는 절대 속을 안 보여주지만, 머릿속엔 이미 10년 치 부의 설계도가 완성됨.", "career_fit": "자산 신탁, 비밀 프로젝트 PM, 암호학", "bad_habit": "외로움을 즐기면서도 고독감 때문에 괴로워함."},
    "계해": {"title": "끝없는 대해의 심해를 누비는 고래", "mbti": "INFP", "tags": ["#간여지동", "#심오한영감", "#무한한잠재력"], "punchline": "세상의 모든 슬픔과 지혜를 다 품은 듯한 깊은 눈빛. 예술과 영감의 바다 그 자체.", "career_fit": "순수 예술, 명상/영성 멘토, 철학, 음악", "bad_habit": "현실 세계의 금전 감각이 희미해져 사기당하기 쉬움."}
}

# 2030 심리 애착 유형 사주 매핑
def analyze_attachment_style(saju_data):
    pillars = saju_data.get("pillars", {})
    shinsal = saju_data.get("shinsal", {})
    strength = saju_data.get("strength", {})
    total_score = strength.get("total_score", 50)
    
    # 십성 카운트
    sipseong_list = []
    for p in pillars.values():
        if "gan_sipseong" in p: sipseong_list.append(p["gan_sipseong"])
        if "ji_sipseong" in p: sipseong_list.append(p["ji_sipseong"])

    pyeon_in_count = sipseong_list.count("편인")
    gwan_count = sipseong_list.count("편관") + sipseong_list.count("정관")
    sik_sang_count = sipseong_list.count("식신") + sipseong_list.count("상관")
    jae_count = sipseong_list.count("편재") + sipseong_list.count("정재")
    bi_geop_count = sipseong_list.count("비견") + sipseong_list.count("겁재")

    if pyeon_in_count >= 2 or (bi_geop_count >= 3 and total_score >= 65):
        style = "단절 회피형 (Dismissive-Avoidant)"
        badge = "🛡️ 철벽 동굴 잠수러"
        desc = "상대방이 내 개인 영역이나 감정의 바운더리를 침범하면 급격한 피로감을 느끼며 동굴로 숨어버림. 갈등이 생기면 대화로 풀기보다 잠수나 차단을 먼저 고민하는 성향."
        flirting_advice = "상대방을 닥달하거나 '왜 연락 안 해?'라고 쏘아붙이지 말고, 혼자만의 시간을 철저히 보장해줄 때 서서히 마음을 엶."
        warning = "독립심이 지나쳐 상대방을 '너 없이도 나 혼자 잘 살아' 모드로 밀어내다 소중한 인연을 놓치기 십상."
    elif gwan_count >= 2 or (total_score <= 35 and pyeon_in_count >= 1):
        style = "초조 불안형 (Anxious-Preoccupied)"
        badge = "⚡ 1분 간격 답장 확인러"
        desc = "상대방의 사소한 말투 변화, 카톡 답장 속도 10분 지연에도 '내가 뭐 잘못했나?' 밤새 불안에 떪. 끊임없이 애정을 확인받고 싶어 하는 인정 욕구 과다."
        flirting_advice = "예측 가능한 연락과 명확한 확신 표현이 최고의 보약. '지금 회의 중이야, 3시에 연락할게' 한마디면 마음이 녹아내림."
        warning = "불안해서 쥐어짜듯 집착하다가 상대방의 숨통을 조여 도망가게 만드는 악순환 경계."
    elif sik_sang_count >= 3 or (sik_sang_count >= 2 and jae_count >= 2):
        style = "자유 탐색형 (Free-Spirited / Fearful)"
        badge = "🕊️ 구속 즉시 탈출러"
        desc = "연애 초반엔 불나방처럼 타오르지만, 상대방이 구속하거나 결혼/정착을 압박하는 순간 숨이 턱 막힘. 도파민과 새로움이 끊임없이 필요한 영혼."
        flirting_advice = "친구처럼 유쾌하게 같이 놀아주되, 일상의 루틴을 침범하지 않는 쿨한 텐션 유지가 정답."
        warning = "감정이 식으면 미련 없이 차갑게 돌아서 '어장관리러'라는 오해를 받기 쉬움."
    else:
        style = "단단한 안정형 (Secure Attachment)"
        badge = "⚓ 흔들림 없는 안식처"
        desc = "서로의 다름을 존중하고 감정을 솔직하게 표현할 줄 아는 성숙한 연애관. 상대를 소유하려 하지 않고 든든한 지원군이 되어줌."
        flirting_advice = "솔직하고 꾸밈없는 진정성 있는 태도로 다가갈 때 가장 큰 호감을 느낌."
        warning = "선을 넘거나 예의 없는 행동을 보면 단호하게 정리하므로 최소한의 예의는 필수."

    return {
        "style": style,
        "badge": badge,
        "desc": desc,
        "flirting_advice": flirting_advice,
        "warning": warning
    }

# 직장 번아웃 지수 및 퇴사/이직 골든타임
def analyze_career_and_burnout(saju_data):
    strength = saju_data.get("strength", {})
    total_score = strength.get("total_score", 50)
    shinsal = saju_data.get("shinsal", {})
    yongsin = saju_data.get("yongsin", {})
    pillars = saju_data.get("pillars", {})

    # 번아웃 지수 산출 (0~100%)
    # 관살 과다, 극신약, 극신강에 따라 에너지 고갈도 측정
    base_burnout = 45
    if total_score <= 25: base_burnout += 30 # 극신약
    elif total_score >= 80: base_burnout += 25 # 극신강 (워커홀릭)
    
    if shinsal.get("guimun"): base_burnout += 10
    if shinsal.get("baekho") or shinsal.get("yangin"): base_burnout += 10
    if shinsal.get("yeokma"): base_burnout -= 5

    burnout_score = min(98, max(20, base_burnout))

    if burnout_score >= 75:
        burnout_status = "위험 (레드 경보 🚨)"
        burnout_msg = "이미 몸과 정신의 배터리가 3% 미만! 무능한 상사와 영혼 없는 회의에 시달려 '월요일 출근길에 차라리 차가 살짝 박아줬으면' 생각하는 한계 상태."
    elif burnout_score >= 50:
        burnout_status = "주의 (옐로우 경보 ⚠️)"
        burnout_msg = "퇴근 후 아무것도 하기 싫어 유튜브 쇼츠만 멍하니 보다가 새벽 2시에 잠드는 만성 피로 모드. 이직 포트폴리오를 벼려야 할 타이밍."
    else:
        burnout_status = "안정 (그린 라이트 🌿)"
        burnout_msg = "에너지 컨트롤이 양호하며, 일과 삶의 바운더리를 건강하게 지켜내고 있는 상태."

    # 이직/퇴사 골든타임 도출 (용신 오행 및 계절 연계)
    main_yong = yongsin.get("main", "화")
    yong_months_map = {
        "목": ["양력 2~4월 (봄의 도약기)", "양력 11월 (물길이 열리는 수생목 타이밍)"],
        "화": ["양력 5~7월 (초여름 불꽃 승부수)", "양력 2월 (봄바람이 불을 지피는 시기)"],
        "토": ["양력 4월/7월/10월 (환절기 안정적 착륙)", "양력 6월 (화생토 결실기)"],
        "금": ["양력 8~10월 (가을의 단칼 결단기)", "양력 4월/12월 (내실 다지기)"],
        "수": ["양력 11~1월 (겨울 심해의 은밀한 이적)", "양력 8월 (금생수 물길 트기)"]
    }
    golden_months = yong_months_map.get(main_yong, ["양력 3~5월", "양력 9~11월"])

    return {
        "burnout_score": burnout_score,
        "burnout_status": burnout_status,
        "burnout_msg": burnout_msg,
        "turnover_months": golden_months,
        "hate_boss_type": "말 바꾸기 달인이자 성과는 자기가 먹고 실수는 팀원 탓하는 상사",
        "golden_career_advice": f"그대의 용신 기운({main_yong})이 들어오는 {golden_months[0]} 전후로 이력서에 손을 대시오. 홧김에 사표 먼저 던지지 말고 환승 이직이 천기누설의 정답이오!"
    }

# 2030 재테크 돈복 성향 분석
def analyze_wealth_style(saju_data):
    day_gan = saju_data.get("day_gan", "갑")
    pillars = saju_data.get("pillars", {})
    
    sipseong_list = [p.get("gan_sipseong", "") for p in pillars.values()] + [p.get("ji_sipseong", "") for p in pillars.values()]
    has_pyeonjae = "편재" in sipseong_list
    has_jeongjae = "정재" in sipseong_list
    has_siksang = any("식" in s or "상" in s for s in sipseong_list)

    if has_pyeonjae:
        style = "하이리스크 승부사 (코인/미국주식 스윙형)"
        desc = "따박따박 적금 넣으면 속 터지는 타입. 판의 흐름을 읽고 테마주나 암호화폐, 스타트업 지분 등 한 방이 터지는 곳에 과감히 베팅하여 자산을 퀀텀 점프시킴."
        tip = "손절 기준(-7%)을 칼같이 세우지 않으면 한 번의 욕심으로 3년 치 수익을 반납하니 기계적 분할 매매 필수."
    elif has_siksang:
        style = "재능 콘텐츠 부업형 (N잡러/지식수익화형)"
        desc = "내 손재주, 글쓰기, 전문 지식, 유튜브, 크리에이티브를 통해 부수입 파이프라인을 뚫는 천재. 자본보다 내 몸값이 최고의 배당주."
        tip = "외주나 부업에 너무 기력을 쏟아 본업까지 망가지지 않도록 자동화 툴과 시스템 구축에 집중할 것."
    else:
        style = "스노우볼 자산가 (시드머니 배당/부동산형)"
        desc = "느리지만 절대 망하지 않는 복리의 마법사. 꼬박꼬박 모은 시드로 우량 배당주나 청약, 부동산을 사 모아 10년 뒤에 조용히 건물주 대열에 합류."
        tip = "너무 지나친 안전지향으로 인플레이션에 현금 가치가 녹지 않도록 분할 적립식 인덱스 펀드 비중 확대."

    return {
        "style": style,
        "desc": desc,
        "tip": tip
    }

# 전체 2030 통합 종합 분석
def get_mz_comprehensive_analysis(saju_data, name="그대"):
    day_pillar = saju_data.get("raw", {}).get("day", "갑자")
    persona = MZ_PERSONA_60.get(day_pillar, MZ_PERSONA_60["갑자"])
    attachment = analyze_attachment_style(saju_data)
    career = analyze_career_and_burnout(saju_data)
    wealth = analyze_wealth_style(saju_data)

    name_str = name.strip() if name and name not in ["자네", "그대"] else "그대"

    # 인스타그램 스토리 / 카카오톡 바이럴 공유 텍스트 생성
    viral_share_text = f"""[2030 천명 스펙 카드 | {name_str}의 사주 페르소나]
🔮 60갑자 본캐: {day_pillar} ({persona['title']})
🏷️ 핵심 태그: {' '.join(persona['tags'])}
🔥 팩폭 한마디: "{persona['punchline']}"
⚡ 심리 애착: {attachment['badge']} ({attachment['style'].split(' ')[0]})
💼 직장 번아웃: {career['burnout_score']}% [{career['burnout_status']}]
🚀 이직 골든타임: {career['turnover_months'][0]}
💰 재테크 스타일: {wealth['style']}

👉 도인의 신점명경에서 내 천명 스펙 확인하기: http://localhost:8088"""

    return {
        "day_pillar": day_pillar,
        "persona": persona,
        "attachment": attachment,
        "career": career,
        "wealth": wealth,
        "viral_share_text": viral_share_text
    }

if __name__ == "__main__":
    from manseryeok import calculate_saju
    s = calculate_saju(1993, 8, 17, 18, 0, "male")
    res = get_mz_comprehensive_analysis(s, "김테스터")
    print("=== 2030 바이럴 페르소나 ===")
    print("일주:", res["day_pillar"])
    print("타이틀:", res["persona"]["title"])
    print("태그:", res["persona"]["tags"])
    print("팩폭:", res["persona"]["punchline"])
    print("애착유형:", res["attachment"]["style"])
    print("번아웃:", res["career"]["burnout_score"], res["career"]["burnout_status"])
    print("이직적기:", res["career"]["turnover_months"])
    print("=== 바이럴 공유 텍스트 ===")
    print(res["viral_share_text"])
