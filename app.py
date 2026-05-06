import streamlit as st
import requests

from components.filters import render_sidebar_filters


st.set_page_config(
    page_title="線上課程智能推薦顧問",
    page_icon="🎓",
    layout="wide"
)

st.title("📚 線上課程智能推薦顧問")

try:
    filters = render_sidebar_filters()

    if filters:
        st.subheader("目前選擇條件")
        st.json(filters)

except requests.exceptions.ConnectionError:
    st.error("無法連線到後端 API，請確認 FastAPI 是否已啟動。")

except requests.exceptions.HTTPError as e:
    st.error(f"API 回傳錯誤：{e}")

except Exception as e:
    st.error(f"發生錯誤：{e}")