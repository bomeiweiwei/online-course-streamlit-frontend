import streamlit as st

from utils.formatters import format_price, format_rating, format_students

hardcode_textbook_data = {
    # --- 國文 (Chinese) ---
    "cht_h": "翰林版國文：融合古典文學與現代美學，強調跨文本的敘事分析。優點為選文精煉，能有效提升學生對修辭意境的感悟力。",
    "cht_n": "南一版國文：深耕在地文化連結，透過生活化議題引導文學思辨。優點為課後延伸豐富，有助於建構完整的邏輯表達體系。",
    "cht_k": "康軒版國文：採螺旋式教學編排，注重字詞基礎與大考趨勢的平衡。優點為排版視覺舒適，能大幅降低學生對長文閱讀的壓力感。",

    # --- 英文 (English) ---
    "eng_h": "翰林版英文：引進國際新聞與當代科普主題，語法進階且嚴謹。優點為聽力練習模擬真實情境，能培養紮實的口說應變能力。",
    "eng_n": "南一版英文：核心導向式編寫，單字重複率高，強化長期記憶記憶。優點為圖解文法清晰易懂，非常適合基礎與進階同步並行。",
    "eng_k": "康軒版英文：主打互動式溝通教學，選材活潑且具備高度趣味性。優點為提供多元化數位教材，讓學生在沉浸式環境中學習外語。",

    # --- 數學 (Math) ---
    "math_h": "翰林版數學：邏輯嚴密且題型變化多樣，強調從幾何直觀推導抽象公式。優點為解析過程極度詳盡，適合追求深度思考的學生。",
    "math_n": "南一版數學：注重生活實踐與數學素養，將複雜代數融入日常情境。優點為計算步驟層次分明，有效降低初學者的學習挫折感。",
    "math_k": "康軒版數學：以視覺化建模輔助教學，將抽象概念具象化處理。優點為重點標註明確，能幫助學生快速抓取章節的核心運算邏輯。"
}

def get_textbook_description(course: dict) -> str:
    subject_name = course.get("subject_name")
    version_name = course.get("version_name")

    key_map = {
        ("國文", "翰林"): "cht_h",
        ("國文", "南一"): "cht_n",
        ("國文", "康軒"): "cht_k",
        ("英文", "翰林"): "eng_h",
        ("英文", "南一"): "eng_n",
        ("英文", "康軒"): "eng_k",
        ("數學", "翰林"): "math_h",
        ("數學", "南一"): "math_n",
        ("數學", "康軒"): "math_k",
    }

    key = key_map.get((subject_name, version_name))

    if not key:
        return "目前尚無課程資訊。"

    return hardcode_textbook_data[key]

def render_course_card(course: dict, rank: int):
    course_name = course.get("course_name", "未命名課程")
    score = course.get("recommend_score", 0)
    reasons = course.get("recommend_reasons", [])

    badge = "🏆" if rank <= 3 else "📘"
    reasons_text = "、".join(reasons) if reasons else "符合目前篩選條件"

    description = course.get("description") or get_textbook_description(course)

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

        # ===== 課程資訊 =====
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
                    課程資訊
                </div>
                <div style="font-size: 1.05rem; line-height: 1.8;">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ===== 推薦原因 =====
        st.markdown(
            f"""
            <div style="
                margin-top: 14px;
                padding: 12px 14px;
                border-radius: 10px;
                background-color: rgba(37, 99, 235, 0.18);
                border-left: 4px solid #60a5fa;
                font-size: 0.95rem;
                line-height: 1.6;
            ">
                💡 <b>推薦原因：</b>{reasons_text}
            </div>
            """,
            unsafe_allow_html=True
        )