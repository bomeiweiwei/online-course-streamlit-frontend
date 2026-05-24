# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Streamlit frontend for an AI-powered online course recommendation system (線上課程智能推薦顧問). It communicates with a FastAPI backend to display filtered course recommendations and AI analysis.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app (requires FastAPI backend at API_BASE_URL)
streamlit run app.py

# Docker build & run
docker build -t course-web:latest .
docker run --rm -p 8501:8080 -e PORT=8080 -e API_BASE_URL=http://host.docker.internal:8000 course-web
```

**Prerequisite:** The FastAPI backend must be running before launching Streamlit. Copy `.env.example` to `.env` and set `API_BASE_URL` accordingly.

## Architecture

**Data flow:** User fills sidebar filters → `api/recommend_api.py` POSTs to backend → `services/recommendation_service.py` scores/ranks results → `components/course_card.py` renders cards → clicking a card fetches course content and AI analysis on demand.

### Module Roles

| Layer | Path | Responsibility |
|---|---|---|
| Entry point | `app.py` | Page layout, wires components together |
| API clients | `api/` | HTTP calls to FastAPI backend (`recommend_api`, `course_api`, `option_api`, `ai_api`, `voice`) |
| Components | `components/` | `filters.py` (sidebar with cascading dropdowns + voice input), `course_card.py` (card + detail dialog) |
| Services | `services/` | `recommendation_service.py` (scoring algorithm), `filter_service.py` (client-side filtering) |
| Config | `config/settings.py` | Loads `API_BASE_URL` from `.env` |
| Enums | `enums/sys_preference.py` | User preference types |
| Utils | `utils/formatters.py` | Price, rating, student count formatting |

### Key Implementation Details

**Cascading dropdowns:** School → Grade → Subject → Version. Each selection change calls a reset callback (`reset_after_school_change()`, etc.) that clears dependent `st.session_state` keys before refetching options.

**Scoring algorithm** (`recommendation_service.py`):
- Base: `rating × 10`
- Student count bonus: +20 (≥1000), +15 (≥500), +10 (≥100)
- Budget match: +20 (exact), +10 (within 20%)
- Preference match: +5 per matched preference

**Voice input:** Records audio via `streamlit-mic-recorder`, sends to `/api/voice/voice_to_text`, then regex-parses the transcript to auto-fill school name, grade, subject, and recommendation count (clamped 3–10).

**AI analysis:** Fetched lazily when the user opens a course detail dialog. Results cached in session state under key `ai_reason_{course_name}_{rank}`.

**Session state:** Heavily used for filter values, voice audio blobs, dropdown option lists, and AI result caching. All state keys are prefixed by their domain (e.g., `selected_school_id`, `grade_options`).

## Deployment

GCP Cloud Run target. The Dockerfile exposes port 8080 (configurable via `PORT` env var) and runs Streamlit in headless mode. The current active feature branch is `feature/cloud`; `develop` is the integration branch.
