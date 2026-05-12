import requests
import streamlit as st

from config.settings import API_BASE_URL


def get_course_recommends(filters: dict):
    url = f"{API_BASE_URL}/api/recommend"

    payload = {
        "school_id": filters.get("school_id", 0),
        "grade_id": filters.get("grade_id", 0),
        "subject_id": filters.get("subject_id", 0),
        "version_id": filters.get("version_id"),
        "degree_id": filters.get("degree_id"),
        "goal_id": filters.get("goal_id"),
        "budget": filters.get("budget", 0),
        "limit": filters.get("limit", 3),
        "preference_ids": filters.get("preferences", []),
    }
    # print('payload', payload)

    response = requests.post(
        url,
        json=payload,
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
        },
        timeout=10
    )

    response.raise_for_status()

    return response.json()

def download_recommend_csv(filters: dict):
    url = f"{API_BASE_URL}/api/recommend/exportcsv"

    payload = {
        "school_id": filters.get("school_id", 0),
        "grade_id": filters.get("grade_id", 0),
        "subject_id": filters.get("subject_id", 0),
        "version_id": filters.get("version_id"),
        "degree_id": filters.get("degree_id"),
        "goal_id": filters.get("goal_id"),
        "budget": filters.get("budget", 0),
        "limit": filters.get("limit", 3),
        "preference_ids": filters.get("preferences", []),
    }

    response = requests.post(
        url,
        json=payload,
        timeout=10
    )

    if response.status_code != 200:
        st.error("CSV 下載失敗")
        return None

    return response.content