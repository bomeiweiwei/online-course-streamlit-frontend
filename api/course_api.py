import requests

from config.settings import API_BASE_URL


def filter_courses(
    school_id: int,
    grade_id: int,
    subject_id: int
):
    url = f"{API_BASE_URL}/api/courses/filter"

    params = {
        "school_id": school_id,
        "grade_id": grade_id,
        "subject_id": subject_id,
    }

    response = requests.get(
        url,
        params=params,
        headers={"accept": "application/json"},
        timeout=10
    )

    response.raise_for_status()

    return response.json()