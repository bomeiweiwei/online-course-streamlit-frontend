import streamlit as st

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
        value=3,
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