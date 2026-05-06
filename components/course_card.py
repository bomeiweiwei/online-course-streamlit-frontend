import streamlit as st

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

def render_course_card(course: dict):
    with st.container(border=True):

        st.subheader(course["course_name"])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "價格",
                f"NT$ {course['price']:,}"
            )

        with col2:
            st.metric(
                "評價",
                f"{course['rating']} ⭐"
            )

        with col3:
            st.metric(
                "報名人數",
                f"{course['students']:,}"
            )

        # st.write("7777777777777777")
        if course["subject_name"] == "國文" and course["version_name"] == "翰林":
            st.write(hardcode_textbook_data["cht_h"])
        elif course["subject_name"] == "國文" and course["version_name"] == "南一":
            st.write(hardcode_textbook_data["cht_n"])
        elif course["subject_name"] == "國文" and course["version_name"] == "康軒":
            st.write(hardcode_textbook_data["cht_k"])
        elif course["subject_name"] == "英文" and course["version_name"] == "翰林":
            st.write(hardcode_textbook_data["eng_h"])
        elif course["subject_name"] == "英文" and course["version_name"] == "南一":
            st.write(hardcode_textbook_data["eng_n"])
        elif course["subject_name"] == "英文" and course["version_name"] == "康軒":
            st.write(hardcode_textbook_data["eng_k"])
        elif course["subject_name"] == "數學" and course["version_name"] == "翰林":
            st.write(hardcode_textbook_data["math_h"])
        elif course["subject_name"] == "數學" and course["version_name"] == "南一":
            st.write(hardcode_textbook_data["math_n"])
        elif course["subject_name"] == "數學" and course["version_name"] == "康軒":
            st.write(hardcode_textbook_data["math_k"])
        else:
            st.write("無課程資訊")