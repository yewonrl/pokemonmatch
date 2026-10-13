import streamlit as st
import requests

# ---------------------------------------------------------
# 1. 페이지 설정 및 커스텀 CSS (크림/노란색 톤, 큰 글씨)
# ---------------------------------------------------------
st.set_page_config(
    page_title="MBTI x 단짝 포켓몬 찾기",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
<style>
    /* 전체 배경색: 따뜻한 크림/노란색 톤 */
    .stApp {
        background-color: #FFFDE7;
        font-family: 'Pretendard', 'Malgun Gothic', sans-serif;
    }
    
    /* 카드 컨테이너 스타일링 */
    .pokemon-card {
        background-color: #FFFFFF;
        border: 3px solid #FFE082;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.08);
        text-align: center;
        margin-top: 10px;
    }

    /* 포켓몬 이름 타이틀 */
    .pokemon-name {
        font-size: 32px !important;
        font-weight: 800;
        color: #F57F17;
        margin-bottom: 5px;
    }

    /* 포켓몬 영어 이름 */
    .pokemon-english {
        font-size: 18px;
        color: #8D6E63;
        margin-bottom: 15px;
    }

    /* 이유 설명 박스 */
    .reason-box {
        background-color: #FFF8E1;
        border-left: 5px solid #FFB300;
        padding: 15px 20px;
        border-radius: 8px;
        text-align: left;
        font-size: 18px;
        line-height: 1.6;
        color: #424242;
        margin-top: 15px;
    }

    /* 큰 라벨 및 설명 글씨 */
    .stSelectbox label {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #5D4037 !important;
    }

    /* 메인 타이틀 커스텀 */
    .main-title {
        font-size: 40px;
        font-weight: 900;
        color: #E65100;
        text-align: center;
        margin-bottom: 10px;
    }

    .sub-title {
        font-size: 20px;
        color: #6D4C41;
        text-align: center;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allowed_html=True)


# ---------------------------------------------------------
# 2. MBTI별 단짝 포켓몬 데이터 및 매칭 이유
# ---------------------------------------------------------
MBTI_POKEMON_MAP = {
    "ISTJ": {
        "id": 9,  # 거북왕
        "reason": "사고가 신중하고 원칙을 중요시하는 ISTJ에게 단단한 껍질과 강한 책임감을 가진 거북왕은 최적의 파트너입니다. 서로를 끝까지 신뢰하며 안정적인 팀워크를 발휘합니다."
    },
    "ISFJ": {
        "id": 113,  # 럭키
        "reason": "온화하고 헌신적인 ISFJ처럼, 럭키는 타인을 다정하게 돌보고 치료해 주는 성향을 가지고 있습니다. 서로의 따뜻한 마음에 깊게 공감할 수 있는 완벽한 조합입니다."
    },
    "INFJ": {
        "id": 196,  # 에스퍼
        "reason": "통찰력이 뛰어나고 직관적인 INFJ와 상대의 마음을 읽어내는 에스피오는 깊은 정신적 교감을 나누기에 가장 어울리는 단짝입니다."
    },
    "INTJ": {
        "id": 150,  # 뮤츠
        "reason": "독립적이고 전략적인 사고를 즐기는 INTJ에게 지성적이고 압도적인 분석력을 가진 뮤츠는 최고의 지적 동반자입니다."
    },
    "ISTP": {
        "id": 252,  # 나무지기
        "reason": "냉철한 상황 판단력과 조용하지만 강한 실행력을 가진 ISTP는 침착하고 뛰어난 순발력을 지닌 나무지기와 찰떡궁합을 자랑합니다."
    },
    "ISFP": {
        "id": 133,  # 이브이
        "reason": "자유롭고 예술적인 감성을 지닌 ISFP는 무한한 가능성을 지니고 온화한 성품을 가진 이브이와 자유롭게 세상을 탐험하기에 좋습니다."
    },
    "INFP": {
        "id": 35,  # 삐삐
        "reason": "이상주의적이고 상상력이 풍부한 INFP에게 달빛 아래에서 신비롭게 춤추는 삐삐는 마음을 나눌 수 있는 따뜻하고 낭만적인 친구입니다."
    },
    "INTP": {
        "id": 65,  # 후딘
        "reason": "지적 호기심이 넘치고 논리적인 INTP에게 IQ 5000을 자랑하는 후딘은 수수께끼와 이론을 함께 탐구할 수 있는 완벽한 라이벌이자 친구입니다."
    },
    "ESTP": {
        "id": 6,  # 리자몽
        "reason": "모험을 두려워하지 않고 스릴을 즐기는 ESTP의 정열적인 에너지는 화끈하고 도전을 좋아하는 리자몽과 최고의 시너지를 냅니다."
    },
    "ESFP": {
        "id": 25,  # 피카츄
        "reason": "사교적이고 분위기 메이커인 ESFP처럼, 누구에게나 사랑받고 통통 튀는 에너지를 가진 피카츄는 일상을 즐겁게 만들어 줍니다."
    },
    "ENFP": {
        "id": 151,  # 뮤
        "reason": "호기심 많고 자유로운 영혼의 ENFP에게 호기심과 장난기가 넘치는 신비의 포켓몬 뮤는 매일 새로운 즐거움을 가져다줍니다."
    },
    "ENTP": {
        "id": 94,  # 팬텀
        "reason": "창의적이고 장난기와 유머 감각이 넘치는 ENTP는 장난치는 것을 좋아하며 독창적인 팬텀과 케미가 매우 뛰어납니다."
    },
    "ESTJ": {
        "id": 248,  # 마기라스
        "reason": "체계적이고 강력한 리더십을 발휘하는 ESTJ에게 언제나 압도적인 존재감과 든든함으로 중심을 잡아주는 마기라스는 최고의 조력자입니다."
    },
    "ESFJ": {
        "id": 175,  # 토게피
        "reason": "주변 사람들을 챙기고 행운과 행복을 전달하기 좋아하는 ESFJ는 다정하고 주변에 행복을 가져다주는 토게피와 잘 어울립니다."
    },
    "ENFJ": {
        "id": 149,  # 망나뇽
        "reason": "카리스마와 따뜻한 마음을 동시에 가진 ENFJ처럼, 망나뇽은 넓은 바다를 누비며 위험에 처한 존재를 돕는 따뜻한 리더입니다."
    },
    "ENTJ": {
        "id": 448,  # 루카리오
        "reason": "목표지향적이고 강한 추진력을 가진 ENTJ에게 불굴의 의지와 강한 신념으로 파트너와 함께 성장하는 루카리오는 진정한 단짝입니다."
    }
}


# ---------------------------------------------------------
# 3. PokeAPI 호출 함수 (캐싱 적용으로 속도 최적화)
# ---------------------------------------------------------
@st.cache_data
def get_pokemon_info(pokemon_id):
    try:
        # 포켓몬 기본 정보 API
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}", timeout=5)
        data = res.json()
        
        # 포켓몬 종 정보 API (한글 이름 및 특징 추출용)
        species_res = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}", timeout=5)
        species_data = species_res.json()

        # 1) 한글 이름 찾기
        korean_name = data['name']
        for name_info in species_data.get('names', []):
            if name_info['language']['name'] == 'ko':
                korean_name = name_info['name']
                break

        # 2) 한글 타입 매핑 및 추출
        type_kor_map = {
            'normal': '노말', 'fire': '불꽃', 'water': '물', 'grass': '풀',
            'electric': '전기', 'ice': '얼음', 'fighting': '격투', 'poison': '독',
            'ground': '땅', 'flying': '비행', 'psychic': '에스퍼', 'bug': '벌레',
            'rock': '바위', 'ghost': '고스트', 'dragon': '드래곤', 'steel': '강철',
            'fairy': '페어리', 'dark': '악'
        }
        types = [type_kor_map.get(t['type']['name'], t['type']['name']) for t in data['types']]
        types_str = " / ".join(types)

        # 3) 도감 설명(특징) 한글 텍스트 추출
        flavor_text = "특징 정보가 없습니다."
        for entry in species_data.get('flavor_text_entries', []):
            if entry['language']['name'] == 'ko':
                flavor_text = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
                break

        # 4) 이미지 URL (공식 아트워크)
        image_url = data['sprites']['other']['official-artwork']['front_default']
        if not image_url:
            image_url = data['sprites']['front_default']

        english_name = data['name'].capitalize()

        return {
            "korean_name": korean_name,
            "english_name": english_name,
            "types": types_str,
            "flavor_text": flavor_text,
            "image_url": image_url
        }
    except Exception:
        return None


# ---------------------------------------------------------
# 4. 메인 화면 구성
# ---------------------------------------------------------
st.markdown("<div class='main-title'>⚡ MBTI x 단짝 포켓몬 ⚡</div>", unsafe_allowed_html=True)
st.markdown("<div class='sub-title'>나의 성격 유형에 딱 맞는 운명의 포켓몬 파트너를 만나보세요!</div>", unsafe_allowed_html=True)

# MBTI 선택 박스
mbti_list = list(MBTI_POKEMON_MAP.keys())
selected_mbti = st.selectbox(
    "👉 당신의 MBTI 성격 유형을 선택해 주세요:",
    ["선택하세요"] + mbti_list,
    index=0
)

# MBTI를 선택했을 때 결과 출력
if selected_mbti != "선택하세요":
    pokemon_id = MBTI_POKEMON_MAP[selected_mbti]["id"]
    reason = MBTI_POKEMON_MAP[selected_mbti]["reason"]

    with st.spinner("운명의 단짝 포켓몬을 불러오는 중입니다..."):
        info = get_pokemon_info(pokemon_id)

    if info:
        # 축하 화면 효과 (폭죽 애니메이션)
        st.balloons()

        # 카드로 포켓몬 정보 출력
        st.markdown(f"""
        <div class="pokemon-card">
            <div class="pokemon-name">🎉 {info['korean_name']} 🎉</div>
            <div class="pokemon-english">({info['english_name']})</div>
        </div>
        """, unsafe_allowed_html=True)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.image(info['image_url'], use_container_width=True)

        with col2:
            st.markdown(f"### 🏷️ 타입: **{info['types']}**")
            st.markdown(f"### 📖 특징")
            st.info(info['flavor_text'])

        st.markdown(f"""
        <div class="reason-box">
            <b>💡 {selected_mbti} 유형과 잘 어울리는 이유:</b><br>
            {reason}
        </div>
        """, unsafe_allowed_html=True)
    else:
        st.error("포켓몬 정보를 불러오는데 실패했습니다. 인터넷 연결 상태를 확인해 주세요.")
