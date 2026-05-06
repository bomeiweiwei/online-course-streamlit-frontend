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


def render_sidebar_filters():
    EMPTY_OPTION = {"id": None, "name": "請選擇"}

    # 左側 sidebar =====
    st.sidebar.header("篩選條件")
    # =========================================
    schools = get_schools()

    if not schools:
        st.sidebar.error("無法取得學制資料")
        return None

    selected_school = st.sidebar.selectbox(
        "學制", options=schools, format_func=lambda item: item["name"], key="school"
    )

    school_id = selected_school["id"]
    # =========================================
    # =========================================
    grades = get_grades(school_id)

    if not grades:
        st.sidebar.error("無法取得年級資料")
        return None

    selected_grade = st.sidebar.selectbox(
        "年級",
        options=grades,
        format_func=lambda item: item["name"],
        key=f"grade_{selected_school['id']}",
    )

    grade_id = selected_grade["id"]
    # =========================================
    subjects = get_subjects(grade_id)

    if not subjects:
        st.sidebar.error("無法取得科目資料")
        return None

    selected_subject = st.sidebar.selectbox(
        "科目",
        options=subjects,
        format_func=lambda item: item["name"],
        key=f"subject_{selected_school['id']}_{selected_grade['id']}",
    )

    subject_id = selected_subject["id"]
    # =========================================
    versions = get_versions(subject_id)

    if not versions:
        st.sidebar.error("無法取得版本資料")
        return None

    selected_version = st.sidebar.selectbox(
        "版本",
        options=[EMPTY_OPTION] + versions,
        format_func=lambda item: item["name"],
        key=f"version_{selected_school['id']}_{selected_grade['id']}_{selected_subject['id']}",
    )

    version_id = selected_version["id"]
    # =========================================
    degrees = get_degrees()
    selected_degree = st.sidebar.selectbox(
        "程度",
        options=[EMPTY_OPTION] + degrees,
        format_func=lambda item: item["name"],
        key="degree",
    )
    # =========================================
    goals = get_goals()
    selected_goal = st.sidebar.selectbox(
        "目標",
        [EMPTY_OPTION] + goals,
        format_func=lambda item: item["name"],
        key="goal",
    )
    # =========================================
    budget = st.sidebar.slider(
        "預算", min_value=0, max_value=10000, value=3000, step=500, key="budget"
    )
    # =========================================
    limit = st.sidebar.slider(
        "顯示推薦數量", min_value=3, max_value=10, value=3, step=1
    )
    # =========================================
    preferences = get_preferences()
    selected_preferences = st.sidebar.multiselect(
        "偏好",
        options=preferences,
        format_func=lambda item: item["name"],
        key="preferences",
    )
    # =========================================

    return {
        "school_id": selected_school["id"],
        "school_name": selected_school["name"],
        "grade_id": selected_grade["id"],
        "grade_name": selected_grade["name"],
        "subject_id": selected_subject["id"],
        "subject_name": selected_subject["name"],
        "varsion_id": selected_version["id"],
        "varsion_name": selected_version["name"],
        "degree_id": selected_degree["id"],
        "degree_name": selected_degree["name"],
        "goal_id": selected_goal["id"],
        "goal_name": selected_goal["name"],
        "budget": budget,
        "limit": limit,
        "preferences": [selected_pref["id"] for selected_pref in selected_preferences],
    }
