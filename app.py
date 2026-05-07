import streamlit as st
import requests

from components.filters import render_sidebar_filters
from components.course_card import render_course_card

from api.course_api import filter_courses
from api.recommend_api import get_course_recommends

from services.recommendation_service import get_ranked_courses
from services.filter_service import apply_frontend_filters

st.set_page_config(
    page_title="線上課程智能推薦顧問",
    page_icon="🎓",
    layout="wide"
)

st.title("📚 線上課程智能推薦顧問")

try:
    filters = render_sidebar_filters()
    if not filters:
        st.stop()

     # ===== 顯示目前條件 =====
    with st.expander("目前選擇條件"):
        st.json(filters)

    # ===== 查詢課程 =====
    courses = get_course_recommends(
        filters
    )

    # with st.expander("查詢課程結果"):
    #     st.json(courses["data"][:1])

    # ===== 結果 =====

    st.subheader(f"推薦課程 Top {len(courses)}")

    if not courses:
        st.warning("目前查無符合條件課程")

    else:
        for index, course in enumerate(courses, start=1):
            render_course_card(course, rank=index, filters=filters)

except requests.exceptions.ConnectionError:
    st.error("無法連線到後端 API，請確認 FastAPI 是否已啟動。")

except requests.exceptions.HTTPError as e:
    st.error(f"API 回傳錯誤：{e}")

except Exception as e:
    st.error(f"發生錯誤：{e}")