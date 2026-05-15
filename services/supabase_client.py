"""Supabase 連線（robot schema）"""

from functools import lru_cache

from supabase import Client, create_client

from services.config import get_setting


@lru_cache(maxsize=1)
def get_db() -> Client:
    url = get_setting("SUPABASE_URL", "")
    key = get_setting("SUPABASE_SERVICE_ROLE_KEY", "")
    if not url or not key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in Streamlit secrets or environment variables")
    return create_client(url, key)


def robot_table(table_name: str):
    """回傳 robot schema 下的資料表查詢物件"""
    return get_db().schema("robot").from_(table_name)
