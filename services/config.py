"""共用設定讀取，支援 Streamlit secrets 與環境變數。"""

import os

import streamlit as st


def get_setting(name: str, default: str = "") -> str:
    """優先讀取 Streamlit secrets，其次讀取環境變數。"""
    if name in st.secrets:
        value = st.secrets.get(name, default)
        return str(value) if value is not None else default
    return os.getenv(name, default)
