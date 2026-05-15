"""
操作頁
- 直接執行「設定頁按鈕」綁定的動作範本
- 不需要群組
"""

import json
import os
import sys
import time
import traceback
from urllib.parse import quote

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import services.repo as repo
from services.open_map_render import (
    build_map_view_payload,
    extract_map_image_url,
    normalize_map_detail_for_render,
    render_konva_map_html,
    world_xy_to_konva,
)
from services.pudu_client import call_pudu
from services.showroom_service import (
    execute_button,
    extract_map_name_from_robot_payload,
    poll_robot_status,
)

ALLOWED_MAP_NAMES = [
    "0#0#內湖展間v20測試",
    "1#1#內湖展間v20",
    "1#7#內湖展間清潔v4",
]

# 與基準圖（例如 v20）對齊：底圖若相對逆時針轉 90°，可設 +90（Konva 順時針為正）。新地圖依實測增列。
MAP_VIEW_ROTATION_DEG: dict[str, float] = {
    "1#7#內湖展間清潔v4": 90.0,
}


def _snapshot_current_map_name(snap: dict) -> str | None:
    """與畫面上選取的 map_name 比對用；優先 API 寫入的 currentMapName，否則從 position 再解析。"""
    v = snap.get("currentMapName")
    if isinstance(v, str) and v.strip():
        return v.strip()
    return extract_map_name_from_robot_payload(snap.get("position"))


def _robot_on_selected_map(snap: dict, selected_map_name: str) -> bool:
    cur = _snapshot_current_map_name(snap)
    if cur is None:
        return False
    return cur == str(selected_map_name).strip()


def _extract_robot_xy(position: dict | None) -> tuple[float | None, float | None]:
    if not isinstance(position, dict):
        return None, None
    x = position.get("x")
    y = position.get("y")
    if (x is None or y is None) and isinstance(position.get("position"), dict):
        x = position.get("position", {}).get("x")
        y = position.get("position", {}).get("y")
    try:
        return float(x), float(y)
    except (TypeError, ValueError):
        return None, None


def _load_map_detail_with_debug(shop_id: int | str, map_name: str) -> tuple[dict | None, list[dict]]:
    """與 API 測試頁「獲取地圖詳情 V1」相同：/map-service/v1/open/map + 模板 replace + quote。"""
    attempts: list[dict] = []
    method = "GET"
    label = "獲取地圖詳情 V1"
    path = (
        "/map-service/v1/open/map?shop_id=${shop_id}&map_name=${map_name}"
        .replace("${map_name}", quote(str(map_name), safe=""))
        .replace("${shop_id}", quote(str(shop_id), safe=""))
    )
    encoded_shop_id = quote(str(shop_id), safe="")
    encoded_map_name = quote(str(map_name), safe="")
    try:
        res = call_pudu(method, path, query=None, body=None, timeout=20, return_raw=True)
        attempts.append(
            {
                "api": label,
                "path": path,
                "query": None,
                "effective_shop_id": str(shop_id),
                "effective_map_name": str(map_name),
                "encoded_shop_id": encoded_shop_id,
                "encoded_map_name": encoded_map_name,
                "status_code": res.get("status_code"),
                "text_preview": (res.get("text") or "")[:500],
                "x_date": res.get("x_date", ""),
                "authorization": (res.get("authorization", "")[:120] + "...") if res.get("authorization") else "",
            }
        )
        if 200 <= int(res.get("status_code", 0)) < 300:
            data = res.get("json") or {}
            detail = data.get("data") or data
            if isinstance(detail, dict) and detail:
                return detail, attempts
    except Exception as exc:
        attempts.append(
            {
                "api": label,
                "path": path,
                "query": None,
                "effective_shop_id": str(shop_id),
                "effective_map_name": str(map_name),
                "status_code": -1,
                "text_preview": str(exc),
                "x_date": "",
                "authorization": "",
            }
        )
    return None, attempts

st.set_page_config(page_title="操作 | Pudu API", page_icon="🤖", layout="wide")

if not st.session_state.get("authenticated"):
    st.warning("請先登入")
    st.stop()


@st.cache_data(ttl=30)
def load_bootstrap():
    store = repo.get_or_create_default_store()
    sid = store["id"]
    return {
        "store": store,
        "robots": repo.list_robots(sid),
        "buttons": repo.list_buttons(sid),
        "map_tabs": repo.list_map_tabs(sid),
    }


try:
    bs = load_bootstrap()
except Exception as exc:
    st.error(f"讀取資料失敗: {exc}")
    st.stop()

store = bs["store"]
store_id = store["id"]
robots = bs["robots"]
buttons = bs["buttons"]
map_tabs = [t for t in bs["map_tabs"] if t.get("is_enabled")]

enabled_robots = [r for r in robots if r.get("is_enabled")]

tab_display_map = {
    str(t.get("map_name")): (t.get("display_name") or t.get("map_name") or "")
    for t in map_tabs
    if t.get("map_name")
}

# 操作頁地圖僅保留指定清單，避免混入其他地圖名稱。
all_map_names = [m for m in ALLOWED_MAP_NAMES]
# 若設定頁沒有對應 display_name，則顯示 map_name 本身。
for map_name in all_map_names:
    tab_display_map.setdefault(map_name, map_name)

st.title("🤖 操作")

col_refresh, _ = st.columns([1, 8])
with col_refresh:
    if st.button("重新整理"):
        st.cache_data.clear()
        st.session_state.pop("_status_cache", None)
        st.rerun()

left_col, right_col = st.columns([1, 2])

with left_col:
    st.subheader("按鈕執行")

    enabled_buttons = [b for b in buttons if b.get("is_enabled")]
    if not enabled_buttons:
        st.info("請先到設定頁建立按鈕並綁定動作範本")
    elif not enabled_robots:
        st.info("目前沒有啟用中的機器人")
    else:
        for r in enabled_robots:
            _k = f"chk_exec_{r['sn']}"
            if _k not in st.session_state:
                st.session_state[_k] = True

        _n_sel = sum(
            1 for r in enabled_robots if st.session_state.get(f"chk_exec_{r['sn']}", True)
        )
        _nr = len(enabled_robots)
        if _n_sel == _nr and _nr > 0:
            _tgt_label = "全部機器人"
        elif _n_sel <= 0:
            _tgt_label = "未選取"
        else:
            _tgt_label = f"已選 {_n_sel} 台"

        with st.popover(f"目標機器人：{_tgt_label} ▼"):
            _b1, _b2 = st.columns(2)
            with _b1:
                if st.button("全選", key="btn_robot_target_all", use_container_width=True):
                    for r in enabled_robots:
                        st.session_state[f"chk_exec_{r['sn']}"] = True
                    st.rerun()
            with _b2:
                if st.button("全不選", key="btn_robot_target_none", use_container_width=True):
                    for r in enabled_robots:
                        st.session_state[f"chk_exec_{r['sn']}"] = False
                    st.rerun()
            st.divider()
            for r in enabled_robots:
                _nick = (r.get("nickname") or "").strip()
                _lab = f"{_nick}（{r['sn']}）" if _nick else r["sn"]
                st.checkbox(_lab, key=f"chk_exec_{r['sn']}")

        target_robots = [
            r
            for r in enabled_robots
            if st.session_state.get(f"chk_exec_{r['sn']}", True)
        ]
        st.caption(
            f"本次按鈕傳入 **{len(target_robots)}** 台（共 {len(enabled_robots)} 台啟用）。"
            "若按鈕內範本皆能從 Body 辨識 **sn**，只會打與勾選相符的 API；"
            "勾到按鈕裡沒有對應範本的機器人會自動略過。"
        )

        for btn in enabled_buttons:
            btn_key = f"btn_{btn['id']}"
            if st.button(btn["name"], key=btn_key, use_container_width=True):
                if not target_robots:
                    st.warning("目前篩選條件下沒有可執行的機器人")
                else:
                    with st.spinner(f"執行 {btn['name']} 中..."):
                        result = execute_button(btn, target_robots, store)
                        st.session_state[f"_exec_result_{btn['id']}"] = result
                        overall = "ok" if result["ok"] else "error"
                        try:
                            repo.insert_event(
                                store_id=store_id,
                                event_type="button_execute",
                                source="button_execute",
                                status=overall,
                                payload={
                                    "buttonName": btn["name"],
                                    "robots": [r["robotSn"] for r in result["robots"]],
                                },
                                group_id=btn.get("group_id"),
                                button_id=btn["id"],
                            )
                        except Exception:
                            pass

            exec_result = st.session_state.get(f"_exec_result_{btn['id']}")
            if exec_result:
                icon = "✅" if exec_result["ok"] else "❌"
                with st.expander(f"{icon} {btn['name']} 執行結果", expanded=True):
                    for r_res in exec_result["robots"]:
                        r_icon = "✅" if r_res["ok"] else "❌"
                        st.markdown(f"**{r_icon} {r_res['robotSn']}**")
                        for act in r_res["actions"]:
                            a_icon = "✅" if act["ok"] else "❌"
                            st.markdown(
                                f"**{a_icon}** `{act['method']}` · HTTP {act['status']} · "
                                f"{act['elapsedMs']}ms · {act.get('actionName') or ''}"
                            )
                            req_url = (act.get("requestUrl") or "").strip()
                            if req_url:
                                st.markdown(f"**API URL** `{req_url}`")
                            else:
                                st.markdown(f"**路徑** `{act['path']}`")
                            rq = act.get("requestQuery")
                            rb = act.get("requestBody")
                            if isinstance(rq, dict) and rq:
                                st.caption("Query 參數")
                                st.json(rq)
                            if isinstance(rb, dict) and rb:
                                st.caption("Request Body")
                                st.json(rb)
                            st.caption("回應內容")
                            rj = act.get("responseJson")
                            if rj is not None:
                                st.json(rj)
                            else:
                                st.code(act.get("responseBody") or "", language="text")

with right_col:
    st.subheader("機器人狀態")

    auto_refresh_pos = st.toggle(
        "每 10 秒自動更新機器人位置",
        value=bool(st.session_state.get("_map_auto_refresh_pos", False)),
        key="_map_auto_refresh_pos",
    )
    if auto_refresh_pos:
        # 用 Python 端 sleep + rerun，保留 session_state（含登入狀態），不觸發瀏覽器重新整理。
        # 底圖存於 session_state，不會被重新載入。
        import time as _time
        _time.sleep(10)
        st.rerun()

    if enabled_robots and st.button("更新機器人狀態"):
        with st.spinner("讀取中..."):
            snapshots = poll_robot_status(enabled_robots, store, int(store.get("exec_api_concurrency") or 4))
            st.session_state["_status_cache"] = snapshots
            for snap in snapshots:
                try:
                    repo.update_robot_snapshot(
                        store_id,
                        snap["sn"],
                        {
                            "last_run_state": snap.get("runState"),
                            "last_position": snap.get("position"),
                            "last_seen_at": snap.get("updatedAt"),
                        },
                    )
                except Exception:
                    pass

    snapshots: list[dict] = st.session_state.get("_status_cache") or [
        {
            "robotId": r["id"],
            "sn": r["sn"],
            "nickname": r.get("nickname"),
            "runState": r.get("last_run_state"),
            "online": False,
            "position": r.get("last_position"),
            "currentMapName": extract_map_name_from_robot_payload(r.get("last_position")),
            "updatedAt": r.get("updated_at", ""),
        }
        for r in enabled_robots
    ]

    if snapshots:
        status_cols = st.columns(min(4, len(snapshots)))
        for i, snap in enumerate(snapshots):
            with status_cols[i % len(status_cols)]:
                online_icon = "🟢" if snap.get("online") else "🔴"
                label = snap.get("nickname") or snap.get("sn", "?")
                run_state = snap.get("runState") or "未知"
                st.metric(f"{online_icon} {label}", run_state)
    else:
        st.info("目前沒有可顯示的機器人")

    st.markdown("---")
    st.subheader("地圖資訊")
    _map_sel, _map_load = st.columns([3, 1])
    with _map_sel:
        selected_map_name = st.selectbox(
            "地圖",
            all_map_names,
            format_func=lambda x: tab_display_map.get(x, x),
            index=0,
            placeholder="目前無可用地圖",
            key="operate_page_map_select",
        )
    try:
        _shop = int(float(store.get("pudu_shop_id") or 0))
    except (TypeError, ValueError):
        _shop = 0
    map_cache_key = f"_map_{selected_map_name}"
    map_debug_key = f"_map_debug_{selected_map_name}"
    map_base_payload_key = f"_map_base_payload_{selected_map_name}"
    with _map_load:
        load_map_clicked = st.button("載入地圖資料", key="load_map_data_btn", use_container_width=True)

    if selected_map_name:
        if auto_refresh_pos and enabled_robots:
            now_ts = time.time()
            last_poll_ts = float(st.session_state.get("_map_last_robot_poll_ts", 0.0))
            if now_ts - last_poll_ts >= 10.0:
                live_snaps = poll_robot_status(enabled_robots, store, int(store.get("exec_api_concurrency") or 4))
                st.session_state["_status_cache"] = live_snaps
                snapshots = live_snaps
                st.session_state["_map_last_robot_poll_ts"] = now_ts
                for snap in live_snaps:
                    try:
                        repo.update_robot_snapshot(
                            store_id,
                            snap["sn"],
                            {
                                "last_run_state": snap.get("runState"),
                                "last_position": snap.get("position"),
                                "last_seen_at": snap.get("updatedAt"),
                            },
                        )
                    except Exception:
                        pass

        # 僅在使用者按「載入地圖資料」時同步一次即時位置，避免與自動輪詢／整頁重跑互相干擾。
        if load_map_clicked and enabled_robots:
            with st.spinner("同步機器人即時位置中..."):
                live_snaps = poll_robot_status(enabled_robots, store, int(store.get("exec_api_concurrency") or 4))
                st.session_state["_status_cache"] = live_snaps
                snapshots = live_snaps
                st.session_state["_map_last_robot_poll_ts"] = time.time()
                for snap in live_snaps:
                    try:
                        repo.update_robot_snapshot(
                            store_id,
                            snap["sn"],
                            {
                                "last_run_state": snap.get("runState"),
                                "last_position": snap.get("position"),
                                "last_seen_at": snap.get("updatedAt"),
                            },
                        )
                    except Exception:
                        pass

        if load_map_clicked or map_cache_key not in st.session_state:
            with st.spinner("讀取地圖中..."):
                detail, attempts = _load_map_detail_with_debug(_shop, selected_map_name)
                st.session_state[map_cache_key] = detail
                st.session_state[map_debug_key] = attempts
            st.session_state.pop(map_base_payload_key, None)

        map_detail = st.session_state.get(map_cache_key)
        map_debug_attempts = st.session_state.get(map_debug_key, [])
        if map_detail:
            resolution = float(map_detail.get("resolution") or 0.05) or 0.05
            try:
                _norm = normalize_map_detail_for_render(dict(map_detail))
                if not extract_map_image_url(_norm):
                    st.info("回應中未偵測到圖檔網址時，僅顯示機器人標記；請展開 JSON 確認 url / map_url 等欄位。")
            except Exception:
                pass

            robots_konva: list[dict] = []
            for snap in snapshots:
                if not _robot_on_selected_map(snap, selected_map_name):
                    continue
                rx, ry = _extract_robot_xy(snap.get("position"))
                if rx is None or ry is None:
                    continue
                try:
                    kx, ky = world_xy_to_konva(float(rx), float(ry), resolution)
                except Exception:
                    continue
                robots_konva.append(
                    {
                        "x": kx,
                        "y": ky,
                        "name": str(snap.get("nickname") or snap.get("sn") or ""),
                    }
                )

            if snapshots and not robots_konva:
                with_xy = [
                    s
                    for s in snapshots
                    if _extract_robot_xy(s.get("position"))[0] is not None
                ]
                if with_xy:
                    if all(_snapshot_current_map_name(s) is None for s in with_xy):
                        st.caption(
                            "無法在圖上標示：get_position／狀態回傳中未含可辨識的 **map_name**，"
                            "無法對應到目前選取的地圖。請按「更新機器人狀態」或確認開放平台回傳欄位。"
                        )
                    else:
                        st.caption(
                            f"目前選取「{selected_map_name}」：僅顯示回報所在地圖與此名稱一致的機器人；"
                            "其餘機器人已隱藏。"
                        )

            st.markdown("##### 地圖預覽（自動縮放至視窗、不可拖曳）")
            try:
                _rot = float(MAP_VIEW_ROTATION_DEG.get(selected_map_name, 0.0))
                # 底圖 payload 只在地圖切換/重新載入時更新；平時僅替換機器人點位。
                base_payload = st.session_state.get(map_base_payload_key)
                if not isinstance(base_payload, dict):
                    base_payload = build_map_view_payload(
                        map_detail,
                        [],
                        inline_map_image=True,
                        view_rotation_deg=_rot,
                    )
                    st.session_state[map_base_payload_key] = base_payload

                payload = dict(base_payload)
                payload["robots"] = robots_konva
                html = render_konva_map_html(payload, width=880, height=460)
                components.html(html, width=900, height=460, scrolling=False)
            except Exception as exc:
                st.error(f"Konva 疊圖失敗：{exc}")
                st.code(traceback.format_exc(), language="text")

            with st.expander("機器人座標（世界座標 → Konva，僅此地圖）"):
                rows = []
                for snap in snapshots:
                    if not _robot_on_selected_map(snap, selected_map_name):
                        continue
                    rx, ry = _extract_robot_xy(snap.get("position"))
                    if rx is None:
                        continue
                    try:
                        kx, ky = world_xy_to_konva(float(rx), float(ry), resolution)
                    except Exception:
                        kx, ky = None, None
                    rows.append(
                        {
                            "sn": snap.get("sn"),
                            "current_map": _snapshot_current_map_name(snap) or "",
                            "world_x": rx,
                            "world_y": ry,
                            "konva_x": kx,
                            "konva_y": ky,
                        }
                    )
                if rows:
                    st.dataframe(rows, use_container_width=True)
                else:
                    st.caption(
                        "尚無符合此地圖的機器位置，或尚未更新狀態；請按「更新機器人狀態」。"
                    )

            with st.expander("地圖原始回應 JSON（data）"):
                st.json(map_detail)
            with st.expander("地圖 API 除錯紀錄"):
                st.dataframe(map_debug_attempts, use_container_width=True)
        elif map_detail is not None:
            st.warning("地圖資料為空（可能是 shop_id/map_name 不匹配，或地圖詳情接口返回錯誤）")
            if map_debug_attempts:
                with st.expander("地圖 API 除錯紀錄"):
                    st.dataframe(map_debug_attempts, use_container_width=True)
        else:
            st.error("尚未成功取得地圖資料（API 回傳失敗或解析為空）。請按「載入地圖資料」重試，並查看除錯紀錄。")
            if map_debug_attempts:
                with st.expander("地圖 API 除錯紀錄"):
                    st.dataframe(map_debug_attempts, use_container_width=True)

st.markdown("---")
st.subheader("事件紀錄")
if st.button("讀取事件紀錄"):
    try:
        st.session_state["_events"] = repo.list_events(store_id, limit=50)
    except Exception as exc:
        st.error(str(exc))

events = st.session_state.get("_events", [])
if events:
    rows = []
    for e in events:
        rows.append(
            {
                "時間": (e.get("created_at", "")[:19] or "").replace("T", " "),
                "狀態": "✅" if e.get("status") == "ok" else ("⚠️" if e.get("status") == "partial" else "❌"),
                "類型": e.get("event_type", ""),
                "來源": e.get("source", ""),
                "機器人": e.get("robot_sn") or "",
                "Payload": json.dumps(e.get("payload") or {}, ensure_ascii=False)[:120],
            }
        )
    st.dataframe(rows, use_container_width=True)
else:
    st.caption("尚無紀錄")
