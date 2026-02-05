import streamlit as st
import random
import google.generativeai as genai

# --- 1. 基準値データの定義（提供いただいた最新データ） ---
REF_DATA = {
    "赤沈(男)": {"min": 2, "max": 10, "unit": "mm/1時間"},
    "赤沈(女)": {"min": 3, "max": 15, "unit": "mm/1時間"},
    "赤血球(男)": {"min": 410, "max": 610, "unit": "万/μL"},
    "赤血球(女)": {"min": 380, "max": 530, "unit": "万/μL"},
    "Hb(男)": {"min": 13, "max": 17, "unit": "g/dL"},
    "Hb(女)": {"min": 11, "max": 16, "unit": "g/dL"},
    "Ht(男)": {"min": 40, "max": 54, "unit": "%"},
    "Ht(女)": {"min": 36, "max": 42, "unit": "%"},
    "MCV": {"min": 83, "max": 93, "unit": "fL"},
    "MCH": {"min": 27, "max": 32, "unit": "pg"},
    "MCHC": {"min": 31, "max": 37, "unit": "g/dL"},
    "Ret": {"min": 0.5, "max": 1.5, "unit": "%"},
    "白血球": {"min": 4000, "max": 10000, "unit": "/μL"},
    "桿状核好中球": {"min": 2, "max": 15, "unit": "%"},
    "分葉核好中球": {"min": 40, "max": 60, "unit": "%"},
    "好酸球": {"min": 1, "max": 5, "unit": "%"},
    "好塩基球": {"min": 0, "max": 2, "unit": "%"},
    "単球": {"min": 2, "max": 10, "unit": "%"},
    "リンパ球": {"min": 20, "max": 50, "unit": "%"},
    "血小板": {"min": 13, "max": 35, "unit": "万/μL"},
    "TP": {"min": 6.5, "max": 8.0, "unit": "g/dL"},
    "Alb": {"min": 4.5, "max": 5.5, "unit": "g/dL"},
    "Alb(分画)": {"min": 61.6, "max": 71.2, "unit": "%"},
    "α1-グロブリン": {"min": 1.9, "max": 3.0, "unit": "%"},
    "α2-グロブリン": {"min": 5.3, "max": 8.9, "unit": "%"},
    "β-グロブリン": {"min": 6.9, "max": 10.9, "unit": "%"},
    "γ-グロブリン": {"min": 10.8, "max": 19.6, "unit": "%"},
    "総ビリルビン": {"min": 0.2, "max": 1.1, "unit": "mg/dL"},
    "直接ビリルビン": {"min": 0, "max": 0.5, "unit": "mg/dL以下"},
    "AST": {"min": 10, "max": 35, "unit": "U/L"},
    "ALT": {"min": 5, "max": 40, "unit": "U/L"},
    "UN": {"min": 9, "max": 20, "unit": "mg/dL"},
    "Cr(男)": {"min": 0.7, "max": 1.2, "unit": "mg/dL"},
    "Cr(女)": {"min": 0.5, "max": 0.9, "unit": "mg/dL"},
    "UA(男)": {"min": 3.0, "max": 7.7, "unit": "mg/dL"},
    "UA(女)": {"min": 2.0, "max": 5.5, "unit": "mg/dL"},
    "随時血糖": {"min": 0, "max": 139, "unit": "mg/dL以下"},
    "FBS": {"min": 50, "max": 110, "unit": "mg/dL"},
    "TC": {"min": 0, "max": 220, "unit": "mg/dL以下"},
    "TG": {"min": 30, "max": 135, "unit": "mg/dL"},
    "HDL-C": {"min": 40, "max": 200, "unit": "mg/dL以上"},
    "LDL-C": {"min": 30, "max": 139, "unit": "mg/dL"},
    "Na": {"min": 136, "max": 148, "unit": "mEq/L"},
    "K": {"min": 3.6, "max": 5.0, "unit": "mEq/L"},
    "Cl": {"min": 96, "max": 108, "unit": "mEq/L"},
    "Ca": {"min": 8.4, "max": 10.0, "unit": "mg/dL"},
    "P": {"min": 2.5, "max": 4.5, "unit": "mg/dL"},
    "Fe(男)": {"min": 59, "max": 161, "unit": "μg/dL"},
    "Fe(女)": {"min": 29, "max": 158, "unit": "μg/dL"},
    "CRP": {"min": 0, "max": 0.3, "unit": "mg/dL以下"},
    "pH": {"min": 7.35, "max": 7.45, "unit": "-"},
    "PaCO2": {"min": 35, "max": 45, "unit": "Torr"},
    "PaO2": {"min": 80, "max": 100, "unit": "Torr"},
    "HCO3-": {"min": 22, "max": 26, "unit": "mEq/L"}
}

# --- 2. 設定（APIキー） ---
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. クイズ生成ロジック ---
def generate_local_quiz():
    item = random.choice(list(REF_DATA.keys()))
    ref = REF_DATA[item]
    
    is_normal = random.choice([True, False])
    
    # 少数桁数の判定（pHなどは小数点2桁、他は1桁）
    precision = 2 if item == "pH" else 1
    
    if is_normal:
        # 基準値内のギリギリを攻める
        val = round(random.uniform(ref['min'], ref['max']), precision)
    else:
        # 基準値外
        if random.choice([True, False]) and ref['min'] > 0:
            # 下限を下回る
            val = round(ref['min'] - random.uniform(0.1, ref['min']*0.2), precision)
        else:
            # 上限を上回る
            val = round(ref['max'] + random.uniform(0.1, ref['max']*0.2), precision)
            
    return {"item": item, "value": val, "unit": ref['unit'], "is_normal": is_normal}

# --- 4. 画面表示 ---
st.set_page_config(page_title="血液検査クイズ", page_icon="🩸")
st.title("🩸 血液検査 基準値クイズ")

if 'quiz' not in st.session_state:
    st.session_state.quiz = None
if 'answered' not in st.session_state:
    st.session_state.answered = False

if st.button("問題を出す") or st.session_state.quiz is None:
    st.session_state.quiz = generate_local_quiz()
    st.session_state.answered = False
    st.session_state.ai_explanation = ""

if st.session_state.quiz:
    q = st.session_state.quiz
    st.info(f"### 項目：{q['item']}\n## 検査値：{q['value']} {q['unit']}")

    if not st.session_state.answered:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⭕ 基準値内", use_container_width=True):
                st.session_state.is_correct = q['is_normal']
                st.session_state.answered = True
        with col2:
            if st.button("❌ 基準値外", use_container_width=True):
                st.session_state.is_correct = not q['is_normal']
                st.session_state.answered = True

if st.session_state.answered:
        if st.session_state.is_correct:
            st.success("✨ 正解です！")
        else:
            st.error("😭 不正解...")
        
        st.write(f"判定：{'基準値内' if q['is_normal'] else '基準値外'}")
        
        # 解説だけAIに頼む（API節約のため、必要な時だけ呼ぶ）
        if st.button("AIの詳しい解説を見る"):
            with st.spinner("AIが考え中..."):
                prompt = f"{q['item']}の数値が{q['value']} {q['unit']}であることについて、医学生向けに短い臨床的意義を教えて。"
                try:
                    response = model.generate_content(prompt)
                    st.session_state.ai_explanation = response.text
                except:
                    st.warning("現在API制限中です。少し待ってから再度お試しください。")
        
        if st.session_state.ai_explanation:
            st.markdown(st.session_state.ai_explanation)

        if st.button("次の問題"):
            st.session_state.quiz = generate_local_quiz()
            st.session_state.answered = False
            st.rerun()