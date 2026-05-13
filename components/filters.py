import streamlit as st
import requests
from streamlit_mic_recorder import mic_recorder
from api.voice import voice_to_text
import re

from api.option_api import (
    get_schools,
    get_grades,
    get_subjects,
    get_versions,
    get_degrees,
    get_goals,
    get_preferences,
)


EMPTY_OPTION = {"id": None, "name": "請選擇"}


# =========================================
# callback
# =========================================
def reset_after_school_change():
    """
    學制改變時：
    清空年級、科目、版本
    """
    st.session_state.pop("grade", None)
    st.session_state.pop("subject", None)
    st.session_state.pop("version", None)


def reset_after_grade_change():
    """
    年級改變時：
    清空科目、版本
    """
    st.session_state.pop("subject", None)
    st.session_state.pop("version", None)


def reset_after_subject_change():
    """
    科目改變時：
    清空版本
    """
    st.session_state.pop("version", None)

st.markdown("""
    <style>
    /* 針對錄音元件容器進行縮減 */
    div[data-st-delegate="st_mic_recorder"] {
        margin-bottom: -10px;
        margin-top: -10px;
    }
    
    /* 美化錄音按鈕樣式 */
    div[data-st-delegate="st_mic_recorder"] button {
        width: 100% !important;
        border-radius: 10px !important;
        border: 1px solid #ff4b4b !important;
        background-color: white !important;
        color: #ff4b4b !important;
        height: 2.5rem !important;
    }

    /* 滑鼠懸停效果 */
    div[data-st-delegate="st_mic_recorder"] button:hover {
        background-color: #ff4b4b !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_voice_button(schools): 
    # 使用 expander 收納語音功能，並預設展開
    with st.sidebar.expander("🎙️ 語音快速填寫", expanded=True):
        st.markdown('''
            <p style="color: gray; font-size: 0.8rem;">
            您可以說：<br>
            • 「我想看高中二年級的國文」<br>
            • 「<b>顯示推薦數量改為 5 個</b>」
            </p>
        ''', unsafe_allow_html=True)
        
        # 只保留確定的參數
        audio = mic_recorder(
            start_prompt="開始錄音",
            stop_prompt="停止辨識",
            key='recorder'
        )

        # 處理邏輯
        if audio:
            audio_bytes = audio['bytes']
            
            if len(audio_bytes) < 2000:
                st.warning("錄音太短，請重試")
            else:
                import hashlib
                audio_id = hashlib.md5(audio_bytes).hexdigest()
                
                if st.session_state.get("last_processed_audio") != audio_id:
                    # 辨識時顯示美觀的 spinner
                    with st.status("正在辨識語音...", expanded=False) as status:
                        try:
                            files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
                            result = voice_to_text(files) 
                            
                            if result and "transcript" in result:
                                text = result["transcript"]
                                st.session_state.last_processed_audio = audio_id
                                
                                # 使用 toast 顯示結果，不會推擠到原本的 UI
                                st.toast(f"辨識結果：{text}", icon="🤖")
                                
                                status.update(label=f"辨識成功：{text}", state="complete")
                                auto_select_logic(text, schools) 
                                st.rerun() 
                                
                        except Exception as e:
                            status.update(label="辨識失敗", state="error")
                            st.error(f"連線失敗: {e}")

def auto_select_logic(text, schools):
    # 1. 匹配學制
    for s in schools:
        if s["name"] in text:
            st.session_state.school = s
            reset_after_school_change()
            
            # 2. 匹配年級 (需即時抓取該學制下的年級)
            grades = get_grades(s["id"])
            for g in grades:
                if g["name"] in text:
                    st.session_state.grade = g
                    reset_after_grade_change()
                    
                    # 3. 匹配科目
                    subjects = get_subjects(g["id"])
                    for sub in subjects:
                        if sub["name"] in text:
                            st.session_state.subject = sub
                            reset_after_subject_change()
                            break
            break
    # 匹配顯示推薦數量
    if any(keyword in text for keyword in ["數量", "推薦", "幾個", "顯示"]):
        numbers = re.findall(r'\d+', text)
        if numbers:
            # 取第一個找到的數字，並轉為整數
            target_limit = int(numbers[0])
            
            # 檢查是否在 slider 的範圍內 (3-10)
            if 3 <= target_limit <= 10:
                st.session_state["limit"] = target_limit
                st.toast(f"🔢 已將推薦數量設為：{target_limit}", icon="📊")
            else:
                st.sidebar.warning(f"數量 {target_limit} 超出範圍 (3-10)")

if "limit" not in st.session_state:
    st.session_state["limit"] = 3

# =========================================
# sidebar filters
# =========================================
def render_sidebar_filters():

    st.sidebar.header("篩選條件")

    # =========================================
    # 學制
    # =========================================
    schools = get_schools()

    if not schools:
        st.sidebar.error("無法取得學制資料")
        return None
    
    render_voice_button(schools)
    st.sidebar.write("---")

    selected_school = st.sidebar.selectbox(
        "學制",
        options=schools,
        format_func=lambda item: item["name"],
        key="school",
        on_change=reset_after_school_change,
    )

    school_id = selected_school["id"]

    # =========================================
    # 年級
    # =========================================
    grades = get_grades(school_id)

    if not grades:
        st.sidebar.error("無法取得年級資料")
        return None

    selected_grade = st.sidebar.selectbox(
        "年級",
        options=grades,
        format_func=lambda item: item["name"],
        key="grade",
        on_change=reset_after_grade_change,
    )

    grade_id = selected_grade["id"]

    # =========================================
    # 科目
    # =========================================
    subjects = get_subjects(grade_id)

    if not subjects:
        st.sidebar.error("無法取得科目資料")
        return None

    selected_subject = st.sidebar.selectbox(
        "科目",
        options=subjects,
        format_func=lambda item: item["name"],
        key="subject",
        on_change=reset_after_subject_change,
    )

    subject_id = selected_subject["id"]

    # =========================================
    # 版本
    # =========================================
    versions = get_versions(subject_id)

    if not versions:
        st.sidebar.error("無法取得版本資料")
        return None

    selected_version = st.sidebar.selectbox(
        "版本",
        options=[EMPTY_OPTION] + versions,
        format_func=lambda item: item["name"],
        key="version",
    )

    # =========================================
    # 程度
    # =========================================
    degrees = get_degrees()

    selected_degree = st.sidebar.selectbox(
        "程度",
        options=[EMPTY_OPTION] + degrees,
        format_func=lambda item: item["name"],
        key="degree",
    )

    # =========================================
    # 目標
    # =========================================
    goals = get_goals()

    selected_goal = st.sidebar.selectbox(
        "目標",
        options=[EMPTY_OPTION] + goals,
        format_func=lambda item: item["name"],
        key="goal",
    )

    # =========================================
    # 預算
    # =========================================
    budget = st.sidebar.slider(
        "預算",
        min_value=0,
        max_value=10000,
        value=3000,
        step=500,
        key="budget",
    )

    # =========================================
    # 顯示推薦數量
    # =========================================
    limit = st.sidebar.slider(
        "顯示推薦數量",
        min_value=3,
        max_value=10,
        # value=3,
        step=1,
        key="limit",
    )

    # =========================================
    # 偏好
    # =========================================
    preferences = get_preferences()

    selected_preferences = st.sidebar.multiselect(
        "偏好",
        options=preferences,
        format_func=lambda item: item["name"],
        key="preferences",
    )

    # =========================================
    # debug
    # =========================================
    # st.write(st.session_state)

    return {
        "school_id": selected_school["id"],
        "school_name": selected_school["name"],
        "grade_id": selected_grade["id"],
        "grade_name": selected_grade["name"],
        "subject_id": selected_subject["id"],
        "subject_name": selected_subject["name"],
        "version_id": selected_version["id"],
        "version_name": selected_version["name"],
        "degree_id": selected_degree["id"],
        "degree_name": selected_degree["name"],
        "goal_id": selected_goal["id"],
        "goal_name": selected_goal["name"],
        "budget": budget,
        "limit": limit,
        "preferences": [item["id"] for item in selected_preferences],
    }