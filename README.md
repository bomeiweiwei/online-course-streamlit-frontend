# ONLINE-COURSE-STREAMLIT-FRONTEND

## Project Structure

```text
online-course-streamlit-frontend/
│
├─ api/
│  ├─ ai_api.py
│  ├─ course_api.py
│  └─ option_api.py
│
├─ components/
│  ├─ course_card.py
│  └─ filters.py
│
├─ config/
│  └─ settings.py
│
├─ enums/
│  └─ sys_preference.py
│
├─ services/
│  ├─ filter_service.py
│  └─ recommendation_service.py
│
├─ utils/
│  └─ formatters.py
│
├─ .env
├─ .env.example
├─ .gitignore
├─ app.py
├─ README.md
└─ requirements.txt
```

---

## Environment

### `.env.example`

```env
API_BASE_URL=http://127.0.0.1:8000
```

---

## Install

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Mac / Linux

```bash
source .venv/bin/activate
```

---

## Install Packages

```bash
pip install -r requirements.txt
```

---

## Run Streamlit

```bash
streamlit run app.py
```

---

## Main Modules

### api/

Handle backend API requests.

```text
option_api.py
→ options API

course_api.py
→ course filter API

ai_api.py
→ AI recommendation API
```

---

### components/

Handle Streamlit UI components.

```text
filters.py
→ sidebar filters

course_card.py
→ course card UI
```

---

### services/

Handle frontend business logic.

```text
recommendation_service.py
→ recommendation score / ranking

filter_service.py
→ frontend filter processing
```

---

### utils/

Utility functions.

```text
formatters.py
→ price / rating / students format
```

---

## Requirements

```txt
streamlit
requests
python-dotenv
pandas
```