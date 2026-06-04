# CLAUDE.md

此檔案提供 Claude Code (claude.ai/code) 在此專案中的操作指引。

## 專案概述

這是一個以 Streamlit 建構的前端應用，用於 AI 驅動的線上課程智能推薦顧問系統。透過呼叫 FastAPI 後端，顯示篩選後的課程推薦結果與 AI 分析。

## 開發指令

```bash
# 安裝相依套件
pip install -r requirements.txt

# 啟動應用程式（需先啟動 FastAPI 後端，並設定 API_BASE_URL）
streamlit run app.py

# Docker 建置與執行
docker build -t course-web:latest .
docker run --rm -p 8501:8080 -e PORT=8080 -e API_BASE_URL=http://host.docker.internal:8000 course-web
```

**前置條件：** 啟動 Streamlit 前，必須先執行 FastAPI 後端。請將 `.env.example` 複製為 `.env`，並設定 `API_BASE_URL`。

## 架構說明

**資料流：** 使用者填寫側邊欄篩選條件 → `api/recommend_api.py` 以 POST 呼叫後端 → `services/recommendation_service.py` 計分排序 → `components/course_card.py` 渲染課程卡片 → 點擊卡片後，依需求取得課程內容與 AI 分析。

### 模組職責

| 層級 | 路徑 | 職責 |
|---|---|---|
| 入口點 | `app.py` | 頁面佈局，串接各元件 |
| API 客戶端 | `api/` | 呼叫 FastAPI 後端的 HTTP 請求（`recommend_api`、`course_api`、`option_api`、`ai_api`、`voice`）|
| 元件 | `components/` | `filters.py`（含級聯下拉選單與語音輸入的側邊欄）、`course_card.py`（卡片與詳細資訊彈窗）|
| 服務 | `services/` | `recommendation_service.py`（計分演算法）、`filter_service.py`（客戶端篩選邏輯）|
| 設定 | `config/settings.py` | 從 `.env` 載入 `API_BASE_URL` |
| 列舉 | `enums/sys_preference.py` | 使用者偏好類型定義 |
| 工具 | `utils/formatters.py` | 價格、評分、學生人數格式化 |

### 關鍵實作細節

**級聯下拉選單：** 學校 → 年級 → 科目 → 版本。每次選項變更時，會呼叫對應的重置 callback（`reset_after_school_change()` 等），清除下游 `st.session_state` 的鍵值後重新取得選項。

**計分演算法**（`recommendation_service.py`）：
- 基礎分：`評分 × 10`
- 學生人數加分：+20（≥1000）、+15（≥500）、+10（≥100）
- 預算符合：+20（完全符合）、+10（在 20% 範圍內）
- 偏好符合：每項符合 +5

**語音輸入：** 透過 `streamlit-mic-recorder` 錄製音訊，送至 `/api/voice/voice_to_text`，再以正規表達式解析逐字稿，自動填入學校名稱、年級、科目與推薦數量（限制在 3–10 之間）。

**AI 分析：** 使用者開啟課程詳細彈窗時才進行延遲載入，結果以 `ai_reason_{course_name}_{rank}` 為鍵值快取於 session state。

**Session State：** 大量用於儲存篩選條件、語音音訊 blob、下拉選單選項清單及 AI 結果快取。所有鍵值皆以所屬領域為前綴命名（例如 `selected_school_id`、`grade_options`）。

## 部署

目標平台為 GCP Cloud Run。Dockerfile 預設公開 8080 埠（可透過 `PORT` 環境變數調整），並以 headless 模式執行 Streamlit。目前的功能開發分支為 `feature/cloud`，整合分支為 `develop`。
