import requests
import streamlit as st

from config.settings import API_BASE_URL


def voice_to_text(files: dict):
    url = f"{API_BASE_URL}/api/voice/voice_to_text"
    # 建議增加 timeout (例如 30 秒)，因為語音 API 較耗時
    response = requests.post(url, files=files, timeout=30)
    response.raise_for_status()
    return response.json()