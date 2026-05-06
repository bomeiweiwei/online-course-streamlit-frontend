import requests

from config.settings import API_BASE_URL


def get_course_ai_recommendation(filters: dict, course: dict):
    url = f"{API_BASE_URL}/api/ai/course/recommendation"

    payload = {
        "prompt_type": "recommend_explanation",
        "question": "",
        "data": {
            "filters": filters,
            "course": course,
        }
    }

    response = requests.post(
        url,
        json=payload,
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
        },
        timeout=60
    )

    response.raise_for_status()

    return response.json()