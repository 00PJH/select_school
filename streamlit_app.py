import streamlit as st
import random
import time
import re
import os
import base64

# ==========================================
# 페이지 설정
# ==========================================
st.set_page_config(page_title="🦆 실습학교 배정 추첨", page_icon="🦆", layout="centered", initial_sidebar_state="collapsed")

# ==========================================
# 마스코트 이미지 (base64 인라인)
# ==========================================
DUCK_IMG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pixel_duck_mascot.png")

def get_duck_base64():
    """이미지 파일을 base64로 읽어 인라인 삽입"""
    if os.path.exists(DUCK_IMG_PATH):
        with open(DUCK_IMG_PATH, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f'data:image/png;base64,{data}'
    return None

def duck_html(width=120):
    src = get_duck_base64()
    if src:
        return f'<img src="{src}" width="{width}">'
    return "🦆"

# ==========================================
# CSS 디자인 시스템
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;900&display=swap');

.stApp {
    background: linear-gradient(160deg, #0a0a0f 0%, #1a1a2e 40%, #16213e 70%, #0f1525 100%) !important;
    font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
.stMainBlockContainer { max-width: 860px !important; padding-top: 2rem !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }

@keyframes fadeInUp { from { opacity:0; transform:translateY(30px); } to { opacity:1; transform:translateY(0); } }

@keyframes pulse-glow { 0%,100% { box-shadow:0 0 20px rgba(255,210,60,0.15); } 50% { box-shadow:0 0 40px rgba(255,210,60,0.3); } }
@keyframes gradientShift { 0% { background-position:0% 50%; } 50% { background-position:100% 50%; } 100% { background-position:0% 50%; } }
@keyframes cardEnter { from { opacity:0; transform:translateY(24px) scale(0.97); } to { opacity:1; transform:translateY(0) scale(1); } }

.hero-container { text-align:center; padding:1rem 1rem 0.5rem; animation:fadeInUp 0.8s ease-out; }
.hero-duck { margin-bottom:0.5rem; }
.hero-title {
    font-size:2.2rem; font-weight:900;
    background:linear-gradient(135deg,#FFD93D,#FF8C42,#FFD93D,#FFA726);
    background-size:300% 100%; -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    animation:gradientShift 4s ease infinite; margin:0.2rem 0; letter-spacing:-0.5px;
}
.hero-subtitle { color:rgba(255,255,255,0.45); font-size:0.92rem; font-weight:300; letter-spacing:3px; text-transform:uppercase; margin-top:0.2rem; }

.fancy-divider { height:1px; background:linear-gradient(90deg,transparent,rgba(255,210,60,0.3),transparent); margin:1.5rem 0; border:none; }

.stButton > button {
    width:100%;
    background:linear-gradient(135deg,#FFD93D 0%,#FF8C42 50%,#FFD93D 100%) !important;
    background-size:200% auto !important; color:#1a1a2e !important;
    font-family:'Noto Sans KR',sans-serif !important;
    font-size:1.15rem !important; font-weight:800 !important; padding:0.9rem 2rem !important;
    border:none !important; border-radius:16px !important;
    box-shadow:0 8px 30px rgba(255,210,60,0.3) !important;
    transition:all 0.4s cubic-bezier(0.175,0.885,0.32,1.275) !important;
    letter-spacing:1px !important; animation:pulse-glow 2.5s ease-in-out infinite;
}
.stButton > button:hover { background-position:right center !important; transform:translateY(-3px) scale(1.02) !important; box-shadow:0 12px 40px rgba(255,210,60,0.45) !important; }

.school-result-card {
    background:rgba(255,255,255,0.04); backdrop-filter:blur(16px);
    border:1px solid rgba(255,255,255,0.08); border-radius:18px;
    padding:1.4rem 1.6rem; margin:0.6rem 0;
    box-shadow:0 6px 24px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.05);
    animation:cardEnter 0.5s ease-out backwards;
}
.school-result-card:hover { transform:translateY(-3px); }

.student-pill {
    display:inline-block; padding:0.35rem 0.85rem; border-radius:50px;
    font-size:0.85rem; font-weight:500; margin:0.2rem;
    box-shadow:0 2px 10px rgba(0,0,0,0.15); transition:all 0.3s ease;
}
.student-pill:hover { transform:translateY(-2px) scale(1.05); }

.info-box {
    background:rgba(255,210,60,0.06); border:1px solid rgba(255,210,60,0.15);
    border-radius:16px; padding:1.2rem 1.4rem; margin:1rem 0;
    color:rgba(255,255,255,0.8); font-size:0.9rem; line-height:1.7;
}
.info-box strong { color:#FFD93D; }

.stat-box {
    background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06);
    border-radius:14px; padding:1rem; text-align:center;
}
.stat-num {
    font-size:1.6rem; font-weight:900;
    background:linear-gradient(135deg,#FFD93D,#FF8C42);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.stat-lbl { font-size:0.72rem; color:rgba(255,255,255,0.4); margin-top:0.2rem; }

.demand-row {
    display:flex; align-items:center; justify-content:space-between;
    padding:0.55rem 0; border-bottom:1px solid rgba(255,255,255,0.04);
}
.demand-school { color:rgba(255,255,255,0.85); font-weight:500; }
.demand-status-ok { color:#64d2a0; font-weight:600; font-size:0.78rem; padding:0.15rem 0.5rem; border-radius:20px; background:rgba(100,210,160,0.1); }
.demand-status-over { color:#ff7b7b; font-weight:600; font-size:0.78rem; padding:0.15rem 0.5rem; border-radius:20px; background:rgba(255,82,82,0.1); }

.banned-pill {
    display:inline-block;
    background:linear-gradient(135deg,rgba(255,82,82,0.15),rgba(255,82,82,0.08));
    border:1px solid rgba(255,82,82,0.25); color:#ff7b7b;
    padding:0.4rem 0.9rem; border-radius:50px; margin:0.25rem;
    font-size:0.85rem; font-weight:500;
}

.footer-text { text-align:center; padding:2rem 0; color:rgba(255,255,255,0.2); font-size:0.75rem; letter-spacing:1px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# Hero Section
# ==========================================
st.markdown(f"""
<div class="hero-container">
    <div class="hero-duck">{duck_html(130)}</div>
    <div class="hero-title">실습학교 배정 추첨</div>
    <div class="hero-subtitle">Fair School Assignment System</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# ==========================================
# 고정 데이터
# ==========================================
BANNED_LIST = ["강은채", "김도연", "박현주", "채희수", "서지민", "곽정현", "남하린", "이정흔", "전혜영"]

SCHOOL_COLORS = {
    '부설초': ('#8884d8', '136,132,216'), '덕성초': ('#ff8cb4', '255,140,180'),
    '운동초': ('#64d2a0', '100,210,160'), '원평초': ('#78beff', '120,190,255'),
    '봉정초': ('#ffb464', '255,180,100'),
}
SCHOOL_EMOJIS = {'부설초': '🏫', '덕성초': '🌸', '운동초': '⚽', '원평초': '🌿', '봉정초': '🏔️'}

# 부설초 불가 명단
banned_pills = " ".join([f'<span class="banned-pill">{n}</span>' for n in BANNED_LIST])
st.markdown(f"""
<div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:20px; padding:1.4rem 1.6rem; margin:0.8rem 0;">
<div style="font-size:1.1rem; font-weight:700; color:rgba(255,255,255,0.9); margin-bottom:0.8rem;">🚫 부설초 기실습자 ({len(BANNED_LIST)}명)</div>
<div style="color:rgba(255,255,255,0.4); font-size:0.82rem; margin-bottom:0.6rem;">과거 부설초 실습 이력으로 인해 부설초 배정이 불가합니다.</div>
{banned_pills}
</div>
""", unsafe_allow_html=True)

# 알고리즘 설명
with st.expander("🔍 추첨 알고리즘은 어떻게 작동하나요?"):
    st.markdown("""
    **기각 표본추출(Rejection Sampling)** 기법으로 공정한 배정을 보장합니다.

    1. 🎲 **1차 추첨** — 초과 지원 학교에서 무작위 추첨
    2. 🔒 **조건 검증** — 탈락자 중 부설초 불가 인원이 남은 안전 자리보다 많으면 즉시 폐기
    3. 🔄 **자동 재추첨** — 조건 충족까지 반복
    4. ✅ **안전 배정** — 부설초 불가 인원부터 안전 자리에 우선 배치
    5. 🎯 **최종 확정** — 나머지 탈락자를 남은 전체 자리에 무작위 배정
    """)

st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# ==========================================
# 데이터 입력 영역 (네이티브 Streamlit)
# ==========================================
st.subheader("📋 지원자 명단 입력")
st.caption("각 학교에 지원한 인원의 이름을 한 줄에 한 명씩 입력해 주세요.")

col1, col2, col3, col4, col5 = st.columns(5)
with col1: cap_buseol = st.number_input("부설초 정원", value=5, step=1)
with col2: cap_deokseong = st.number_input("덕성초 정원", value=4, step=1)
with col3: cap_undong = st.number_input("운동초 정원", value=8, step=1)
with col4: cap_wonpyeong = st.number_input("원평초 정원", value=4, step=1)
with col5: cap_bongjeong = st.number_input("봉정초 정원", value=6, step=1)

capacities = {
    '부설초': cap_buseol, '덕성초': cap_deokseong,
    '운동초': cap_undong, '원평초': cap_wonpyeong, '봉정초': cap_bongjeong
}

c1, c2 = st.columns(2)
with c1:
    txt_buseol = st.text_area("🏫 부설초 지원자", "이시아")
    txt_deokseong = st.text_area("🌸 덕성초 지원자", "고윤하 남하린 문시온")
    txt_bongjeong = st.text_area("🏔️ 봉정초 지원자", "강은채 이시온 정연우 주예원 희희덕덕")
with c2:
    txt_undong = st.text_area("⚽ 운동초 지원자", "곽정현 문소연 박지혜 이보람 이윤영 이현정 전혜영 채희수 천세은")
    txt_wonpyeong = st.text_area("🌿 원평초 지원자", "김도연 김수현 김지안 박현주 서지민 이정흔 차윤지 황지윤")

def parse_names(text):
    return [n for n in re.split(r'[, \n]+', text.strip()) if n]

raw_inputs = {
    '부설초': parse_names(txt_buseol), '덕성초': parse_names(txt_deokseong),
    '운동초': parse_names(txt_undong), '원평초': parse_names(txt_wonpyeong),
    '봉정초': parse_names(txt_bongjeong)
}

students_data = []
for school, names in raw_inputs.items():
    for name in names:
        students_data.append({'name': name, '1st_choice': school, 'banned': name in BANNED_LIST})

# ── 학교별 지원 현황 (네이티브 Streamlit) ──
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
st.subheader("📊 학교별 지원 현황")

for school in capacities:
    cnt = len(raw_inputs[school])
    cap = capacities[school]
    emoji = SCHOOL_EMOJIS[school]
    hex_color = SCHOOL_COLORS[school][0]

    if cnt < cap:
        status_txt = "미달"
        status_emoji = "🟢"
    elif cnt == cap:
        status_txt = "정원"
        status_emoji = "🔵"
    else:
        status_txt = "초과"
        status_emoji = "🔴"

    cols = st.columns([3, 2, 1])
    with cols[0]:
        st.markdown(f"**{emoji} {school}**")
    with cols[1]:
        st.markdown(f"지원 **{cnt}** / {cap}명")
    with cols[2]:
        st.markdown(f"{status_emoji} {status_txt}")

# ── 통계 ──
total_students = len(students_data)
banned_count = sum(1 for s in students_data if s['banned'])

st.markdown(f"""
<div style="display:flex; gap:0.8rem; margin:1rem 0; flex-wrap:wrap;">
<div class="stat-box" style="flex:1; min-width:100px;"><div class="stat-num">{total_students}</div><div class="stat-lbl">총 인원</div></div>
<div class="stat-box" style="flex:1; min-width:100px;"><div class="stat-num">{len(capacities)}</div><div class="stat-lbl">실습학교</div></div>
<div class="stat-box" style="flex:1; min-width:100px;"><div class="stat-num">{sum(capacities.values())}</div><div class="stat-lbl">총 정원</div></div>
<div class="stat-box" style="flex:1; min-width:100px;"><div class="stat-num">{banned_count}</div><div class="stat-lbl">부설초 불가</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# ==========================================
# 추첨 실행
# ==========================================
col_l, col_c, col_r = st.columns([1, 2, 1])
with col_c:
    run_clicked = st.button("🦆 추첨 시작하기", use_container_width=True)

if run_clicked:
    with st.spinner('시뮬레이션을 통해 최적의 경우의 수를 찾는 중입니다...'):
        time.sleep(1.0)
        attempt = 0
        while True:
            attempt += 1
            allocation = {s: [] for s in capacities}
            failed = []
            for school in capacities:
                current_apps = [s for s in students_data if s['1st_choice'] == school]
                cap = capacities[school]
                if len(current_apps) <= cap:
                    allocation[school].extend(current_apps)
                else:
                    random.shuffle(current_apps)
                    allocation[school].extend(current_apps[:cap])
                    failed.extend(current_apps[cap:])

            remaining = {s: capacities[s] - len(allocation[s]) for s in capacities}
            banned_fails = [s for s in failed if s['banned']]
            normal_fails = [s for s in failed if not s['banned']]
            safe_seats = sum(v for k, v in remaining.items() if k != '부설초')

            if len(banned_fails) > safe_seats:
                continue

            safe_pool = []
            for sch, seats in remaining.items():
                if sch != '부설초':
                    safe_pool.extend([sch] * seats)
            buseol_pool = ['부설초'] * remaining['부설초']

            random.shuffle(safe_pool)
            for s in banned_fails:
                allocation[safe_pool.pop()].append(s)

            total_pool = safe_pool + buseol_pool
            random.shuffle(total_pool)
            for s in normal_fails:
                allocation[total_pool.pop()].append(s)
            break

    # ==========================================
    # 결과 출력
    # ==========================================
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # 시뮬레이션 안내
    if attempt > 1:
        st.markdown(f"""
<div class="info-box">
<strong>🔄 시뮬레이션 완료 — 총 {attempt}회 반복</strong><br>
이전 {attempt-1}번의 추첨에서 '부설초 불가 인원'이 남은 안전한 자리보다 많이 탈락하여 규정상 배정이 불가능한 상황이 발생했습니다.<br><br>
본 시스템은 이러한 오류를 내부적으로 자동 폐기하고, <strong>모든 참여자가 모순 없이 배정될 수 있는 공정한 결과</strong>를 도출했습니다.
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown("""
<div class="info-box">
<strong>✨ 단 1회 만에 완벽한 결과 도출!</strong><br>
첫 번째 추첨에서 모든 조건을 만족하는 결과가 도출되어, 추가 시뮬레이션 없이 즉시 확정되었습니다.
</div>
""", unsafe_allow_html=True)

    # 결과 헤더
    st.markdown(f"""
<div style="text-align:center; margin:1.5rem 0 0.5rem;">
<div style="font-size:1.4rem; font-weight:800; color:rgba(255,255,255,0.9);">
{duck_html(40)} 최종 배정 결과 {duck_html(40)}
</div>
</div>
""", unsafe_allow_html=True)

    # 학교별 결과 카드
    for school, assigned in allocation.items():
        hex_color, rgb = SCHOOL_COLORS[school]
        emoji = SCHOOL_EMOJIS[school]
        cap = capacities[school]

        pills = ""
        for s in assigned:
            label = s['name']
            if s['banned']:
                label += " ⚠️"
            pills += f'<span class="student-pill" style="background:rgba({rgb},0.12); border:1px solid rgba({rgb},0.25); color:{hex_color};">{label}</span>'

        st.markdown(f"""
<div class="school-result-card" style="border-left:3px solid {hex_color};">
<div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.8rem;">
<span style="font-size:1.2rem; font-weight:700; color:rgba(255,255,255,0.95);">{emoji} {school}</span>
<span style="font-size:0.78rem; font-weight:600; padding:0.3rem 0.8rem; border-radius:50px; background:rgba({rgb},0.12); color:{hex_color}; border:1px solid rgba({rgb},0.2);">{len(assigned)} / {cap}명</span>
</div>
<div>{pills}</div>
</div>
""", unsafe_allow_html=True)



    # Footer
    st.markdown(f"""
<div class="fancy-divider"></div>
<div class="footer-text">
{duck_html(36)}<br>
<span style="margin-top:0.5rem; display:inline-block;">Powered by Rejection Sampling Algorithm · Built with Streamlit</span>
</div>
""", unsafe_allow_html=True)
