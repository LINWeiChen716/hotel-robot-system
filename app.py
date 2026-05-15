"""
Pudu Python 控制檯 — 登入頁
多頁面結構：
  app.py        ← 登入
  pages/1_設定.py ← 設定
  pages/2_操作.py ← 操作
  pages/3_API.py ← API 測試
"""

import streamlit as st

from services.config import get_setting

st.set_page_config(page_title="Pudu 控制檯", page_icon="🤖", layout="wide")

# ── 登入狀態管理 ──────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False


def _check_pin(pin: str) -> bool:
    expected = get_setting("SHOWROOM_ACCESS_PIN", "")
    if not expected:          # 未設定 PIN 則直接放行
        return True
    return pin == expected


if not st.session_state["authenticated"]:
    st.title("展間系統登入")
    st.caption("請輸入 SHOWROOM_ACCESS_PIN 進入設定與操作頁。")
    with st.form("login_form"):
        pin = st.text_input("PIN", type="password", placeholder="輸入 PIN")
        submitted = st.form_submit_button("登入")
    if submitted:
        if _check_pin(pin):
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("PIN 不正確")
    st.stop()

# ── 已登入：顯示首頁 ──────────────────────────────────────────
st.title("Pudu 控制檯")
st.markdown("""
請從 **左側側欄** 切換功能頁：

| 頁面 | 說明 |
|------|------|
| 設定 | 門店、機器人、羣組、動作範本、按鈕、地圖分頁管理 |
| 操作 | 即時機器人狀態、地圖視覺化、按鈕控制 |
| API  | 自訂 API 請求測試 |
| 即時狀態儀表板 | Digital Twin 地圖、機器人狀態清單、事件警報日誌 |
""")

if st.button("登出"):
    st.session_state["authenticated"] = False
    st.rerun()

