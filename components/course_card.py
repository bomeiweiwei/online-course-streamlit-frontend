import streamlit as st

from utils.formatters import format_price, format_rating, format_students

from api.ai_api import get_course_ai_recommendation
from api.course_api import get_course_content

def get_course_key(course):
    return (
        f"{course['school_id']}_"
        f"{course['grade_id']}_"
        f"{course['subject_id']}_"
        f"{course['version_id']}_"
        f"{course['degree_id']}_"
        f"{course['goal_id']}"
    )

@st.dialog("課程資訊")
def show_course_info_dialog(ai_key: str, filters: dict, course: dict):
    # st.markdown("### 課程詳細與推薦")
    st.text_input("課程名稱", value=course["course_name"], disabled=True)
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.text_input("學制", value=course["school_name"], disabled=True)
        st.text_input("科目", value=course["subject_name"], disabled=True)
        st.text_input("程度", value=course["degree_name"], disabled=True)

    with info_col2:
        st.text_input("年級", value=course["grade_name"], disabled=True)
        st.text_input("版本", value=course["version_name"], disabled=True)
        st.text_input("目標", value=course["goal_name"], disabled=True)
    
    # ===== 課程資訊 =====
    content = get_course_content(course["subject_name"],course["version_name"])
    description = content["data"]
    st.markdown(
        f"""
        <div style="
            margin-top: 12px;
            padding: 16px;
            border-radius: 12px;
            background-color: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
        ">
            <div style="font-size: 0.9rem; color: #9ca3af; margin-bottom: 6px;">
                課程介紹
            </div>
            <div style="font-size: 1.05rem; line-height: 1.8;">
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    with st.spinner("AI 正在分析課程適合度..."):
        try:
            result = get_course_ai_recommendation(
                filters=filters,
                course=course
            )

            st.session_state[ai_key] = result

        except Exception as e:
            st.session_state[ai_key] = {
                "success": False,
                "message": f"AI 分析失敗：{e}"
            }
    
    if ai_key in st.session_state:
        result = st.session_state[ai_key]

        ai_text = result.get("answer")

        st.markdown(
            f"""
            <div style="
                margin-top: 12px;
                padding: 14px 16px;
                border-radius: 12px;
                background-color: rgba(16, 185, 129, 0.12);
                border-left: 4px solid #34d399;
                line-height: 1.8;
            ">
                🤖 <b>AI 推薦說明：</b>{ai_text}
            </div>
            """,
            unsafe_allow_html=True
        )


def render_course_card(course: dict, rank: int, filters: dict):
    course_name = course.get("course_name", "未命名課程")
    score = course.get("recommend_score", 0)
    reasons = course.get("recommend_reasons", [])

    badge = "🏆" if rank <= 3 else "📘"

    with st.container(border=True):
        # ===== 標題列 =====
        title_col, score_col = st.columns([5, 1])

        with title_col:
            st.markdown(
                f"""
                <div style="font-size: 1.45rem; font-weight: 700; line-height: 1.4;">
                    {badge} Top {rank}｜{course_name}
                </div>
                <div style="font-size: 0.9rem; color: #9ca3af; margin-top: 4px;">
                    {course.get("school_name", "")}・{course.get("grade_name", "")}・
                    {course.get("subject_name", "")}・{course.get("version_name", "")}・
                    {course.get("degree_name", "")}
                </div>
                """,
                unsafe_allow_html=True
            )

        with score_col:
            st.markdown(
                f"""
                <div style="text-align: right;">
                    <div style="font-size: 0.85rem; color: #9ca3af;">推薦分數</div>
                    <div style="font-size: 2rem; font-weight: 700;">{score:.1f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")

        # ===== 指標列 =====
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("價格", format_price(course.get("price")))

        with col2:
            st.metric("評價", format_rating(course.get("rating")))

        with col3:
            st.metric("報名人數", format_students(course.get("students")))

        st.divider()

        course_key = get_course_key(course)
        ai_key = f"ai_reason_{course.get('course_name')}_{rank}"

        if st.button(
            "課程資訊",
            key=f"question_{course_key}",
            use_container_width=False,
        ):
            show_course_info_dialog(ai_key, filters, course)