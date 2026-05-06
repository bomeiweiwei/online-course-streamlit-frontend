import requests
from config.settings import API_BASE_URL


def get_schools():
    url = f"{API_BASE_URL}/api/options/schools"

    response = requests.get(
        url,
        headers={"accept": "application/json"},
        timeout=10
    )
    response.raise_for_status()

    return response.json()


def get_grades(school_id: int):
    url = f"{API_BASE_URL}/api/options/grades"

    response = requests.get(
        url,
        params={"school_id": school_id},
        headers={"accept": "application/json"},
        timeout=10
    )
    response.raise_for_status()

    return response.json()

def get_subjects(grade_id: int):
    url = f"{API_BASE_URL}/api/options/subjects"

    response = requests.get(
        url,
        params={"grade_id": grade_id},
        headers={"accept": "application/json"},
        timeout=10
    )
    response.raise_for_status()

    return response.json()

def get_versions(subject_id: int):
    url = f"{API_BASE_URL}/api/options/versions"

    response = requests.get(
        url,
        params={"subject_id": subject_id},
        headers={"accept": "application/json"},
        timeout=10
    )
    response.raise_for_status()

    return response.json()

def get_degrees():
    url = f"{API_BASE_URL}/api/options/degrees"

    response = requests.get(
        url,
        headers={"accept": "application/json"},
        timeout=10
    )
    response.raise_for_status()

    return response.json()

def get_goals():
    url = f"{API_BASE_URL}/api/options/goals"

    response = requests.get(
        url,
        headers={"accept": "application/json"},
        timeout=10
    )
    response.raise_for_status()

    return response.json()

def get_preferences():
    url = f"{API_BASE_URL}/api/options/preferences"

    response = requests.get(
        url,
        headers={"accept": "application/json"},
        timeout=10
    )
    response.raise_for_status()

    return response.json()