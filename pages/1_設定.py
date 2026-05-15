"""
設定頁
- 管理商店 / 機器人 / 群組 / 動作範本 / 按鈕 / 地圖分頁
- 按鈕只需要綁定動作範本，不需要使用者手動管理群組
"""

import json
import os
import sys

import streamlit as st
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import services.repo as repo
from services.showroom_service import list_pudu_maps, list_pudu_robots, list_pudu_shops


# ── 機器人型號管理 ──────────────────────────────────────────
ROBOT_MODELS_FILE = os.path.join(os.path.dirname(__file__), "..", "robot_models.json")
ROBOT_MODELS_LIST = ["", "CC1", "CC1 Pro", "MT1 MAX", "MT1 VAC", "MT1", "SH1", "T300", "T150", "T600", "閃電匣", "閃電匣 Max", "歡樂送 2", "貝拉 Pro", "葫蘆 Pro"]

def load_robot_models():
    """載入機器人型號映射"""
    if os.path.exists(ROBOT_MODELS_FILE):
        try:
            with open(ROBOT_MODELS_FILE, "r", encoding="utf-8") as f:
                return json.load(f) or {}
        except Exception:
            return {}
    return {}

def save_robot_models(models_dict):
    """保存機器人型號映射"""
    try:
        with open(ROBOT_MODELS_FILE, "w", encoding="utf-8") as f:
            json.dump(models_dict, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def get_robot_model(robot_id):
    """獲取機器人型號"""
    models = load_robot_models()
    return models.get(robot_id, "")

def set_robot_model(robot_id, model):
    """設置機器人型號"""
    models = load_robot_models()
    if model:
        models[robot_id] = model
    elif robot_id in models:
        del models[robot_id]
    save_robot_models(models)



CLEAN_PRODUCT_CODES = {
    "CC1",
    "CC1Pro",
    "MT1",
    "MT1Vac",
    "MT1Max",
}


def _is_clean_product(product_code: str) -> bool:
    code = str(product_code or "").strip()
    if not code:
        return False
    if code in CLEAN_PRODUCT_CODES:
        return True
    low = code.lower()
    return low.startswith("cc1") or low.startswith("mt1")


def _upsert_group_with_members(store_id: str, name: str, color: str, sort_order: int, robot_ids: list[str]) -> None:
    groups = repo.list_groups(store_id)
    target = next((g for g in groups if str(g.get("name") or "").strip() == name), None)
    if target:
        repo.update_group(target["id"], {"name": name, "color": color, "sort_order": sort_order})
        repo.set_group_members(target["id"], robot_ids)
        return

    created = repo.create_group(store_id, name=name, color=color, sort_order=sort_order)
    if created and created.get("id"):
        repo.set_group_members(created["id"], robot_ids)

st.set_page_config(page_title="設定 | Pudu API", page_icon="⚙️", layout="wide")

if not st.session_state.get("authenticated"):
    st.warning("請先登入")
    st.stop()


@st.cache_data(ttl=30)
def load_bootstrap():
    store = repo.get_or_create_default_store()
    store_id = store["id"]
    return {
        "store": store,
        "robots": repo.list_robots(store_id),
        "groups": repo.list_groups(store_id),
        "actions": repo.list_action_templates(store_id),
        "buttons": repo.list_buttons(store_id),
        "map_tabs": repo.list_map_tabs(store_id),
    }


def reload_page():
    st.cache_data.clear()
    st.rerun()


try:
    bs = load_bootstrap()
except Exception as exc:
    st.error(f"讀取設定失敗: {exc}")
    st.stop()

store = bs["store"]
store_id = store["id"]

st.title("⚙️ 設定")
tab_store, tab_robots, tab_groups, tab_actions, tab_buttons, tab_maps = st.tabs(
    ["商店", "機器人", "群組", "動作範本", "按鈕", "地圖分頁"]
)

with tab_store:
    st.subheader("商店設定")
    with st.form("store_form"):
        name = st.text_input("商店名稱", value=store.get("name") or "")
        shop_id_input = st.number_input("Pudu Shop ID", value=int(store.get("pudu_shop_id") or 0), min_value=0, step=1)
        timezone = st.text_input("時區", value=store.get("timezone") or "Asia/Taipei")

        c1, c2 = st.columns(2)
        with c1:
            exec_robot = st.number_input("機器人並發", value=int(store.get("exec_robot_concurrency") or 5), min_value=1, max_value=20)
            status_poll = st.number_input("狀態輪詢秒數", value=int(store.get("status_poll_sec") or 10), min_value=3)
        with c2:
            exec_api = st.number_input("API 並發", value=int(store.get("exec_api_concurrency") or 4), min_value=1, max_value=20)
            pos_poll = st.number_input("位置輪詢秒數", value=int(store.get("position_poll_sec") or 10), min_value=3)

        if st.form_submit_button("儲存"):
            try:
                repo.update_store(
                    store_id,
                    {
                        "name": name,
                        "pudu_shop_id": int(shop_id_input),
                        "timezone": timezone,
                        "exec_robot_concurrency": int(exec_robot),
                        "exec_api_concurrency": int(exec_api),
                        "status_poll_sec": int(status_poll),
                        "position_poll_sec": int(pos_poll),
                    },
                )
                st.success("商店設定已更新")
                reload_page()
            except Exception as exc:
                st.error(str(exc))

    with st.expander("從 Pudu 讀取商店清單"):
        if st.button("讀取商店"):
            with st.spinner("讀取中..."):
                try:
                    shops = list_pudu_shops()
                    if shops:
                        st.dataframe(shops, use_container_width=True)
                    else:
                        st.info("查無資料")
                except Exception as exc:
                    st.error(str(exc))

with tab_robots:
    st.subheader("機器人")
    robots = bs["robots"]

    st.caption("群組管理已獨立到「群組」分頁。")

    with st.expander("新增機器人"):
        with st.form("new_robot"):
            new_sn = st.text_input("SN")
            new_nick = st.text_input("暱稱（可留空）")
            new_model = st.selectbox("機器人型號（可留空）", ROBOT_MODELS_LIST, format_func=lambda x: x if x else "未設定")
            new_enabled = st.checkbox("啟用", value=True)
            if st.form_submit_button("新增"):
                if not new_sn.strip():
                    st.error("SN 不可空白")
                else:
                    try:
                        robot = repo.create_robot(store_id, new_sn.strip(), new_nick.strip() or None, new_enabled)
                        # 保存機器人型號
                        if robot and robot.get("id") and new_model:
                            set_robot_model(robot["id"], new_model)
                        st.success("機器人已新增")
                        reload_page()
                    except Exception as exc:
                        st.error(str(exc))

    with st.expander("從 Pudu 匯入機器人"):
        pudu_shop_id = int(store.get("pudu_shop_id") or 0)
        if st.button("讀取 Pudu 機器人"):
            with st.spinner("讀取中..."):
                try:
                    st.session_state["_pudu_robots"] = list_pudu_robots(pudu_shop_id)
                except Exception as exc:
                    st.error(str(exc))

        pudu_robots_list = st.session_state.get("_pudu_robots", [])
        if pudu_robots_list:
            existing_sns = {r["sn"] for r in robots}
            new_ones = [r for r in pudu_robots_list if r.get("sn") not in existing_sns]
            if new_ones:
                options = [r["sn"] for r in new_ones]
                to_add = st.multiselect("選擇要匯入的 SN", options)
                if st.button("匯入所選") and to_add:
                    for sn in to_add:
                        try:
                            repo.create_robot(store_id, sn)
                        except Exception:
                            pass
                    reload_page()
            else:
                st.info("沒有可新增的機器人")

    for robot in robots:
        label = f"{'🟢' if robot.get('is_enabled') else '🔴'} {robot['sn']}"
        if robot.get("nickname"):
            label += f" ({robot['nickname']})"
        # 顯示型號
        robot_model = get_robot_model(robot["id"])
        if robot_model:
            label += f" [{robot_model}]"
        with st.expander(label):
            with st.form(f"edit_robot_{robot['id']}"):
                nick = st.text_input("暱稱", value=robot.get("nickname") or "", key=f"nick_{robot['id']}")
                current_model = get_robot_model(robot["id"])
                model_index = ROBOT_MODELS_LIST.index(current_model) if current_model in ROBOT_MODELS_LIST else 0
                model = st.selectbox("機器人型號", ROBOT_MODELS_LIST, index=model_index, key=f"model_{robot['id']}", format_func=lambda x: x if x else "未設定")
                enabled = st.checkbox("啟用", value=bool(robot.get("is_enabled")), key=f"en_{robot['id']}")
                c1, c2 = st.columns(2)
                with c1:
                    if st.form_submit_button("儲存"):
                        try:
                            repo.update_robot(robot["id"], {"nickname": nick.strip() or None, "is_enabled": enabled})
                            # 保存機器人型號
                            set_robot_model(robot["id"], model)
                            st.success("已更新")
                            reload_page()
                        except Exception as exc:
                            st.error(str(exc))
                with c2:
                    if st.form_submit_button("🗑️ 刪除", type="secondary"):
                        try:
                            repo.delete_robot(robot["id"])
                            # 刪除型號記錄
                            set_robot_model(robot["id"], "")
                            reload_page()
                        except Exception as exc:
                            st.error(str(exc))

with tab_groups:
    st.subheader("群組管理")
    robots = bs["robots"]
    groups_all = bs.get("groups") or []
    groups = [
        g for g in groups_all
        if not str(g.get("name") or "").strip().startswith("_")
    ]

    st.caption("可直接在這裡新增群組、修改群組名稱、調整群組成員。")

    if st.button("重建預設分組（清潔機器人 / 運送機器人）", key="btn_rebuild_default_groups", use_container_width=True):
        if not robots:
            st.warning("目前沒有機器人可分組")
        else:
            try:
                pudu_shop_id = int(store.get("pudu_shop_id") or 0)
                pudu_robots = list_pudu_robots(pudu_shop_id)
                product_by_sn = {
                    str(item.get("sn") or "").strip(): str(item.get("product_code") or "").strip()
                    for item in (pudu_robots or [])
                }

                clean_robot_ids: list[str] = []
                delivery_robot_ids: list[str] = []
                for r in robots:
                    sn = str(r.get("sn") or "").strip()
                    product_code = product_by_sn.get(sn, "")
                    if _is_clean_product(product_code):
                        clean_robot_ids.append(r["id"])
                    else:
                        delivery_robot_ids.append(r["id"])

                _upsert_group_with_members(
                    store_id,
                    name="清潔機器人",
                    color="#1F8A70",
                    sort_order=10,
                    robot_ids=clean_robot_ids,
                )
                _upsert_group_with_members(
                    store_id,
                    name="運送機器人",
                    color="#2F5D8A",
                    sort_order=20,
                    robot_ids=delivery_robot_ids,
                )

                st.success(
                    f"已重建分組：清潔機器人 {len(clean_robot_ids)} 台、運送機器人 {len(delivery_robot_ids)} 台"
                )
                reload_page()
            except Exception as exc:
                st.error(f"重建分組失敗：{exc}")

    with st.form("new_group_form"):
        gname = st.text_input("新群組名稱", placeholder="例如 全場機器")
        if st.form_submit_button("新增群組"):
            if not gname.strip():
                st.error("群組名稱不可空白")
            else:
                try:
                    existing_names = {str(g.get("name") or "").strip() for g in groups_all}
                    if gname.strip() in existing_names:
                        st.error("群組名稱已存在")
                    else:
                        next_order = (max((int(g.get("sort_order") or 0) for g in groups_all), default=0) + 10)
                        repo.create_group(store_id, name=gname.strip(), color="#1F8A70", sort_order=next_order)
                        st.success("群組已新增")
                        reload_page()
                except Exception as exc:
                    st.error(str(exc))

    robot_option_labels = []
    robot_id_by_label: dict[str, str] = {}
    for r in robots:
        sn = str(r.get("sn") or "").strip()
        if not sn:
            continue
        nick = str(r.get("nickname") or "").strip()
        label = f"{nick}（{sn}）" if nick else sn
        robot_option_labels.append(label)
        robot_id_by_label[label] = r["id"]

    if groups:
        st.caption("目前群組")
        st.dataframe(
            [
                {
                    "群組名稱": g.get("name"),
                    "group_id": g.get("id"),
                    "台數": len(g.get("robot_ids") or []),
                }
                for g in groups
            ],
            use_container_width=True,
            hide_index=True,
        )

    if not groups:
        st.info("目前沒有群組，請先新增群組。")
    else:
        for g in groups:
            gid = g.get("id")
            gname_cur = str(g.get("name") or "")
            member_ids = set(g.get("robot_ids") or [])
            selected_labels = [
                label for label in robot_option_labels
                if robot_id_by_label.get(label) in member_ids
            ]

            st.markdown("---")
            st.markdown(f"### {gname_cur}")
            st.caption(f"group_id: {gid}")
            with st.form(f"edit_group_{gid}"):
                new_name = st.text_input("群組名稱", value=gname_cur, key=f"group_name_{gid}")
                new_members = st.multiselect(
                    "群組成員",
                    robot_option_labels,
                    default=selected_labels,
                    key=f"group_members_{gid}",
                )

                c1, c2 = st.columns(2)
                with c1:
                    save_group = st.form_submit_button("儲存群組內容")
                with c2:
                    delete_group = st.form_submit_button("🗑️ 刪除群組", type="secondary")

                if save_group:
                    try:
                        _name = new_name.strip()
                        if not _name:
                            st.error("群組名稱不可空白")
                        else:
                            duplicate = next(
                                (
                                    x for x in groups_all
                                    if str(x.get("id") or "") != str(gid)
                                    and str(x.get("name") or "").strip() == _name
                                ),
                                None,
                            )
                            if duplicate:
                                st.error("群組名稱已存在")
                            else:
                                selected_ids = [robot_id_by_label[label] for label in new_members if label in robot_id_by_label]
                                repo.update_group(gid, {"name": _name})
                                repo.set_group_members(gid, selected_ids)
                                st.success(f"已更新群組：{_name}")
                                reload_page()
                    except Exception as exc:
                        st.error(str(exc))

                if delete_group:
                    try:
                        repo.delete_group(gid)
                        st.success(f"已刪除群組：{gname_cur}")
                        reload_page()
                    except Exception as exc:
                        st.error(str(exc))

with tab_actions:
    st.subheader("動作範本")
    st.caption(
        "若 **Body / Query / Path** 裡有寫死機器 `sn`（純文字、非 `{{robot.sn}}`），"
        "系統會自動辨識為『一範本一台機』，按鈕執行時只打一次，且僅在操作頁有勾選該 SN 時才跑。"
        "若模板全用占位符，則對每台勾選機器人各執行一次。"
    )
    actions = bs["actions"]

    with st.expander("新增動作範本"):
        with st.form("new_action"):
            aname = st.text_input("名稱")
            amethod = st.selectbox("Method", ["GET", "POST", "PUT", "DELETE", "PATCH"])
            apath = st.text_input("Path", placeholder="/open-platform-service/v2/status/get_by_sn")
            aquery = st.text_area("Query Template JSON", value="{}", height=80)
            abody = st.text_area("Body Template JSON", value="{}", height=80)
            atimeout = st.number_input("Timeout (ms)", value=15000, min_value=1000, step=1000)
            if st.form_submit_button("新增"):
                if not aname.strip() or not apath.strip():
                    st.error("名稱與 Path 不能空白")
                else:
                    try:
                        row = {
                            "name": aname.strip(),
                            "method": amethod,
                            "path": apath.strip(),
                            "query_template": json.loads(aquery or "{}"),
                            "body_template": json.loads(abody or "{}"),
                            "timeout_ms": int(atimeout),
                            "is_enabled": True,
                        }
                        repo.create_action_template(store_id, row)
                        st.success("已新增")
                        reload_page()
                    except Exception as exc:
                        st.error(str(exc))

    for action in actions:
        label = f"{'🟢' if action.get('is_enabled') else '🔴'} [{action.get('method', 'GET')}] {action.get('name', '')}"
        with st.expander(label):
            with st.form(f"edit_action_{action['id']}"):
                an = st.text_input("名稱", value=action.get("name") or "", key=f"an_{action['id']}")
                methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
                cur_method = action.get("method", "GET")
                am = st.selectbox("Method", methods, index=methods.index(cur_method) if cur_method in methods else 0, key=f"am_{action['id']}")
                ap = st.text_input("Path", value=action.get("path") or "", key=f"ap_{action['id']}")
                aq = st.text_area(
                    "Query Template JSON",
                    value=json.dumps(action.get("query_template") or {}, ensure_ascii=False, indent=2),
                    height=80,
                    key=f"aq_{action['id']}",
                )
                ab = st.text_area(
                    "Body Template JSON",
                    value=json.dumps(action.get("body_template") or {}, ensure_ascii=False, indent=2),
                    height=80,
                    key=f"ab_{action['id']}",
                )
                at = st.number_input("Timeout (ms)", value=int(action.get("timeout_ms") or 15000), min_value=1000, step=1000, key=f"at_{action['id']}")
                ae = st.checkbox("啟用", value=bool(action.get("is_enabled")), key=f"ae_{action['id']}")

                c1, c2 = st.columns(2)
                with c1:
                    if st.form_submit_button("儲存"):
                        try:
                            _patch = {
                                "name": an.strip(),
                                "method": am,
                                "path": ap.strip(),
                                "query_template": json.loads(aq or "{}"),
                                "body_template": json.loads(ab or "{}"),
                                "timeout_ms": int(at),
                                "is_enabled": ae,
                            }
                            repo.update_action_template(action["id"], _patch)
                            st.success("已更新")
                            reload_page()
                        except Exception as exc:
                            st.error(str(exc))
                with c2:
                    if st.form_submit_button("🗑️ 刪除", type="secondary"):
                        try:
                            repo.delete_action_template(action["id"])
                            reload_page()
                        except Exception as exc:
                            st.error(str(exc))

with tab_buttons:
    st.subheader("按鈕")
    buttons = bs["buttons"]
    actions = bs["actions"]
    action_options = {a["name"]: a["id"] for a in actions}

    with st.expander("新增按鈕"):
        with st.form("new_button"):
            bname = st.text_input("名稱")
            bdesc = st.text_input("描述（可留空）")
            border = st.number_input("排序", value=0, step=1)
            linked_actions_new = st.multiselect("綁定動作範本（可多選）", list(action_options.keys()), key="ba_new")
            if st.form_submit_button("新增"):
                if not bname.strip():
                    st.error("名稱不可空白")
                elif not linked_actions_new:
                    st.error("請至少選擇 1 個動作範本")
                else:
                    try:
                        btn = repo.create_button(store_id, bname.strip(), bdesc.strip() or None, int(border))
                        new_ids = [action_options[n] for n in linked_actions_new if n in action_options]
                        repo.set_button_actions(btn["id"], new_ids)
                        st.success("按鈕已新增")
                        reload_page()
                    except Exception as exc:
                        st.error(str(exc))

    for btn in buttons:
        label = f"{'🟢' if btn.get('is_enabled') else '🔴'} {btn.get('name', '')}"
        with st.expander(label):
            with st.form(f"edit_btn_{btn['id']}"):
                bn = st.text_input("名稱", value=btn.get("name") or "", key=f"bn_{btn['id']}")
                bd = st.text_input("描述", value=btn.get("description") or "", key=f"bd_{btn['id']}")
                bo = st.number_input("排序", value=int(btn.get("sort_order") or 0), key=f"bo_{btn['id']}")
                be = st.checkbox("啟用", value=bool(btn.get("is_enabled")), key=f"be_{btn['id']}")

                current_action_ids = [a.get("action_template_id") for a in btn.get("actions", [])]
                current_action_names = [a["name"] for a in actions if a["id"] in current_action_ids]
                linked_actions = st.multiselect(
                    "綁定動作範本（可多選）",
                    list(action_options.keys()),
                    default=current_action_names,
                    key=f"ba_{btn['id']}",
                )

                c1, c2 = st.columns(2)
                with c1:
                    if st.form_submit_button("儲存"):
                        try:
                            repo.update_button(
                                btn["id"],
                                {
                                    "name": bn.strip(),
                                    "description": bd.strip() or None,
                                    "sort_order": int(bo),
                                    "is_enabled": be,
                                },
                            )
                            new_ids = [action_options[n] for n in linked_actions if n in action_options]
                            repo.set_button_actions(btn["id"], new_ids)
                            st.success("按鈕已更新")
                            reload_page()
                        except Exception as exc:
                            st.error(str(exc))
                with c2:
                    if st.form_submit_button("🗑️ 刪除", type="secondary"):
                        try:
                            repo.delete_button(btn["id"])
                            reload_page()
                        except Exception as exc:
                            st.error(str(exc))

with tab_maps:
    st.subheader("地圖分頁")
    map_tabs = bs["map_tabs"]
    pudu_shop_id = int(store.get("pudu_shop_id") or 0)

    with st.expander("新增地圖分頁"):
        with st.form("new_map_tab"):
            mt_map = st.text_input("map_name")
            mt_display = st.text_input("顯示名稱")
            mt_order = st.number_input("排序", value=0, step=1)
            if st.form_submit_button("新增"):
                if not mt_map.strip():
                    st.error("map_name 不可空白")
                else:
                    try:
                        repo.create_map_tab(store_id, mt_map.strip(), mt_display.strip() or mt_map.strip(), int(mt_order))
                        st.success("已新增")
                        reload_page()
                    except Exception as exc:
                        st.error(str(exc))

    with st.expander("從 Pudu 讀取地圖"):
        if st.button("讀取地圖"):
            if not pudu_shop_id:
                st.error("請先到「商店」分頁設定 Pudu Shop ID，再讀取地圖。")
            else:
                with st.spinner("讀取中..."):
                    try:
                        st.session_state["_pudu_maps"] = list_pudu_maps(pudu_shop_id)
                    except Exception as exc:
                        st.error(str(exc))
        pudu_maps = st.session_state.get("_pudu_maps", [])
        if pudu_maps:
            st.dataframe(pudu_maps, use_container_width=True)

    for tab in map_tabs:
        label = f"{'🟢' if tab.get('is_enabled') else '🔴'} {tab.get('display_name', '')} ({tab.get('map_name', '')})"
        with st.expander(label):
            with st.form(f"edit_mt_{tab['id']}"):
                mt_mn = st.text_input("map_name", value=tab.get("map_name") or "", key=f"mn_{tab['id']}")
                mt_dn = st.text_input("顯示名稱", value=tab.get("display_name") or "", key=f"dn_{tab['id']}")
                mt_o = st.number_input("排序", value=int(tab.get("sort_order") or 0), key=f"mto_{tab['id']}")
                mt_e = st.checkbox("啟用", value=bool(tab.get("is_enabled")), key=f"mte_{tab['id']}")
                c1, c2 = st.columns(2)
                with c1:
                    if st.form_submit_button("儲存"):
                        try:
                            repo.update_map_tab(
                                tab["id"],
                                {
                                    "map_name": mt_mn.strip(),
                                    "display_name": mt_dn.strip() or mt_mn.strip(),
                                    "sort_order": int(mt_o),
                                    "is_enabled": mt_e,
                                },
                            )
                            st.success("已更新")
                            reload_page()
                        except Exception as exc:
                            st.error(str(exc))
                with c2:
                    if st.form_submit_button("🗑️ 刪除", type="secondary"):
                        try:
                            repo.delete_map_tab(tab["id"])
                            reload_page()
                        except Exception as exc:
                            st.error(str(exc))
