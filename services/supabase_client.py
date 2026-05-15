"""Supabase 連線（robot schema）"""

import os
from functools import lru_cache

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()


@lru_cache(maxsize=1)
def get_db() -> Client:
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    if not url or not key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in environment variables")
    return create_client(url, key)


def robot_table(table_name: str):
    """回傳 robot schema 下的資料表查詢物件"""
    return get_db().schema("robot").from_(table_name)
