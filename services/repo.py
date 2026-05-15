"""
Showroom 資料庫 CRUD（對應 Next.js 版的 lib/showroom/repo.ts）
所有資料都在 Supabase robot schema 下的 showroom_ 開頭資料表。
"""

from __future__ import annotations

from services.supabase_client import robot_table

DEFAULT_STORE_CODE = "default"
DEFAULT_BUTTON_GROUP_NAME = "_default_button_group"


def _rows(res) -> list[dict]:
    """兼容不同客戶端：execute() 可能回 None。"""
    if res is None:
        return []
    data = getattr(res, "data", None)
    return data or []


# ─────────────────────────── Store ───────────────────────────

def get_or_create_default_store() -> dict:
    res = (
        robot_table("showroom_stores")
        .select("*")
        .eq("code", DEFAULT_STORE_CODE)
        .maybe_single()
        .execute()
    )
    if res.data:
        return res.data

    ins = (
        robot_table("showroom_stores")
        .insert({
            "code": DEFAULT_STORE_CODE,
            "name": "預設展間",
            "pudu_shop_id": 0,
            "timezone": "Asia/Taipei",
            "exec_robot_concurrency": 5,
            "exec_api_concurrency": 4,
            "status_poll_sec": 10,
            "position_poll_sec": 10,
        })
        .select("*")
        .single()
        .execute()
    )
    return ins.data


def update_store(store_id: str, patch: dict) -> dict:
    col_map = {
        "name": "name",
        "pudu_shop_id": "pudu_shop_id",
        "timezone": "timezone",
        "exec_robot_concurrency": "exec_robot_concurrency",
        "exec_api_concurrency": "exec_api_concurrency",
        "status_poll_sec": "status_poll_sec",
        "position_poll_sec": "position_poll_sec",
    }
    payload = {col_map[k]: v for k, v in patch.items() if k in col_map}
    res = (
        robot_table("showroom_stores")
        .update(payload)
        .eq("id", store_id)
        .select("*")
        .single()
        .execute()
    )
    return res.data


# ─────────────────────────── Robots ───────────────────────────

def list_robots(store_id: str) -> list[dict]:
    res = (
        robot_table("showroom_robots")
        .select("*")
        .eq("store_id", store_id)
        .order("created_at", desc=False)
        .execute()
    )
    return res.data or []


def create_robot(store_id: str, sn: str, nickname: str | None = None, is_enabled: bool = True) -> dict:
    table = robot_table("showroom_robots")
    payload = {"store_id": store_id, "sn": sn, "nickname": nickname, "is_enabled": is_enabled}
    try:
        res = table.insert(payload).select("*").single().execute()
        if res is not None and getattr(res, "data", None):
            return res.data
    except AttributeError:
        pass
    table.insert(payload).execute()
    fallback = (
        robot_table("showroom_robots")
        .select("*")
        .eq("store_id", store_id)
        .eq("sn", sn)
        .limit(1)
        .execute()
    )
    rows = _rows(fallback)
    return rows[0] if rows else {}


def update_robot(robot_id: str, patch: dict) -> dict:
    allowed = {"nickname", "is_enabled", "last_seen_at", "last_run_state", "last_position"}
    payload = {k: v for k, v in patch.items() if k in allowed}
    table = robot_table("showroom_robots")
    try:
        res = table.update(payload).eq("id", robot_id).select("*").single().execute()
        if res is not None and getattr(res, "data", None):
            return res.data
    except AttributeError:
        pass
    table.update(payload).eq("id", robot_id).execute()
    fallback = robot_table("showroom_robots").select("*").eq("id", robot_id).limit(1).execute()
    rows = _rows(fallback)
    return rows[0] if rows else {}


def delete_robot(robot_id: str) -> None:
    robot_table("showroom_robots").delete().eq("id", robot_id).execute()


def update_robot_snapshot(store_id: str, sn: str, patch: dict) -> None:
    allowed = {"last_seen_at", "last_run_state", "last_position"}
    payload = {k: v for k, v in patch.items() if k in allowed}
    if not payload:
        return
    robot_table("showroom_robots").update(payload).eq("store_id", store_id).eq("sn", sn).execute()


# ─────────────────────────── Groups ───────────────────────────

def list_groups(store_id: str) -> list[dict]:
    res = (
        robot_table("showroom_groups")
        .select("*")
        .eq("store_id", store_id)
        .order("sort_order", desc=False)
        .execute()
    )
    groups = res.data or []
    if not groups:
        return []

    group_ids = [g["id"] for g in groups]
    members_res = (
        robot_table("showroom_group_members")
        .select("group_id,robot_id")
        .in_("group_id", group_ids)
        .execute()
    )
    members = members_res.data or []
    membership: dict[str, list[str]] = {}
    for m in members:
        membership.setdefault(m["group_id"], []).append(m["robot_id"])

    for g in groups:
        g["robot_ids"] = membership.get(g["id"], [])
    return groups


def create_group(store_id: str, name: str, color: str = "#1f8a70", sort_order: int = 0) -> dict:
    table = robot_table("showroom_groups")
    payload = {"store_id": store_id, "name": name, "color": color, "sort_order": sort_order}
    try:
        res = table.insert(payload).select("*").single().execute()
        if res is not None and getattr(res, "data", None):
            return res.data
    except AttributeError:
        pass
    table.insert(payload).execute()
    fallback = (
        robot_table("showroom_groups")
        .select("*")
        .eq("store_id", store_id)
        .eq("name", name)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    rows = _rows(fallback)
    return rows[0] if rows else {}


def get_or_create_default_button_group(store_id: str) -> dict:
    res = (
        robot_table("showroom_groups")
        .select("*")
        .eq("store_id", store_id)
        .eq("name", DEFAULT_BUTTON_GROUP_NAME)
        .maybe_single()
        .execute()
    )
    if res is not None and getattr(res, "data", None):
        return res.data
    return create_group(store_id, DEFAULT_BUTTON_GROUP_NAME, color="#1f8a70", sort_order=0)


def update_group(group_id: str, patch: dict) -> dict:
    allowed = {"name", "color", "sort_order"}
    payload = {k: v for k, v in patch.items() if k in allowed}
    table = robot_table("showroom_groups")
    try:
        res = table.update(payload).eq("id", group_id).select("*").single().execute()
        if res is not None and getattr(res, "data", None):
            return res.data
    except AttributeError:
        pass
    table.update(payload).eq("id", group_id).execute()
    fallback = robot_table("showroom_groups").select("*").eq("id", group_id).limit(1).execute()
    rows = _rows(fallback)
    return rows[0] if rows else {}


def delete_group(group_id: str) -> None:
    robot_table("showroom_groups").delete().eq("id", group_id).execute()


def set_group_members(group_id: str, robot_ids: list[str]) -> None:
    robot_table("showroom_group_members").delete().eq("group_id", group_id).execute()
    if robot_ids:
        # 去除重複與空值，避免 (group_id, robot_id) 主鍵衝突。
        unique_robot_ids: list[str] = []
        seen: set[str] = set()
        for rid in robot_ids:
            rid_text = str(rid or "").strip()
            if not rid_text or rid_text in seen:
                continue
            seen.add(rid_text)
            unique_robot_ids.append(rid_text)

        rows = [{"group_id": group_id, "robot_id": rid} for rid in unique_robot_ids]
        robot_table("showroom_group_members").insert(rows).execute()


# ─────────────────────────── Action Templates ───────────────────────────

def list_action_templates(store_id: str) -> list[dict]:
    res = (
        robot_table("showroom_action_templates")
        .select("*")
        .eq("store_id", store_id)
        .order("created_at", desc=False)
        .execute()
    )
    return res.data or []


def create_action_template(store_id: str, data: dict) -> dict:
    data["store_id"] = store_id
    table = robot_table("showroom_action_templates")
    try:
        res = table.insert(data).select("*").single().execute()
        return res.data
    except AttributeError:
        # 相容舊版 postgrest/supabase-py：insert 後不支援再接 .select()
        table.insert(data).execute()
        fallback = (
            robot_table("showroom_action_templates")
            .select("*")
            .eq("store_id", store_id)
            .eq("name", data.get("name"))
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        rows = fallback.data or []
        return rows[0] if rows else {}
    except Exception as exc:
        msg = str(exc)
        if "fixed_robot_sn" in msg and "PGRST204" in msg:
            fallback_data = {k: v for k, v in data.items() if k != "fixed_robot_sn"}
            res = table.insert(fallback_data).select("*").single().execute()
            return res.data
        raise


def update_action_template(template_id: str, patch: dict) -> dict:
    allowed = {
        "name",
        "method",
        "path",
        "doc_key",
        "query_template",
        "body_template",
        "timeout_ms",
        "is_enabled",
        "fixed_robot_sn",
    }
    payload = {k: v for k, v in patch.items() if k in allowed}
    table = robot_table("showroom_action_templates")
    try:
        res = (
            table
            .update(payload)
            .eq("id", template_id)
            .select("*")
            .single()
            .execute()
        )
        return res.data
    except AttributeError:
        # 相容舊版 postgrest/supabase-py：update 後不支援再接 .select()
        table.update(payload).eq("id", template_id).execute()
        fallback = (
            robot_table("showroom_action_templates")
            .select("*")
            .eq("id", template_id)
            .limit(1)
            .execute()
        )
        rows = fallback.data or []
        return rows[0] if rows else {}
    except Exception as exc:
        msg = str(exc)
        if "fixed_robot_sn" in msg and "PGRST204" in msg:
            fallback_payload = {k: v for k, v in payload.items() if k != "fixed_robot_sn"}
            res = (
                table
                .update(fallback_payload)
                .eq("id", template_id)
                .select("*")
                .single()
                .execute()
            )
            return res.data
        raise


def delete_action_template(template_id: str) -> None:
    robot_table("showroom_action_templates").delete().eq("id", template_id).execute()


# ─────────────────────────── Buttons ───────────────────────────

def list_buttons(store_id: str) -> list[dict]:
    buttons_res = (
        robot_table("showroom_buttons")
        .select("*")
        .eq("store_id", store_id)
        .order("sort_order", desc=False)
        .execute()
    )
    buttons = _rows(buttons_res)
    if not buttons:
        return []

    button_ids = [b["id"] for b in buttons]
    actions_res = (
        robot_table("showroom_button_actions")
        .select("*, showroom_action_templates(*)")
        .in_("button_id", button_ids)
        .order("action_order", desc=False)
        .execute()
    )
    actions = _rows(actions_res)
    action_map: dict[str, list[dict]] = {}
    for a in actions:
        action_map.setdefault(a["button_id"], []).append(a)

    for b in buttons:
        b["actions"] = action_map.get(b["id"], [])
    return buttons


def create_button(store_id: str, name: str, description: str | None = None, sort_order: int = 0, group_id: str | None = None) -> dict:
    resolved_group_id = group_id or get_or_create_default_button_group(store_id)["id"]
    table = robot_table("showroom_buttons")
    payload = {
        "store_id": store_id,
        "group_id": resolved_group_id,
        "name": name,
        "description": description,
        "sort_order": sort_order,
        "is_enabled": True,
    }
    try:
        res = table.insert(payload).select("*").single().execute()
        if res is not None and getattr(res, "data", None):
            return res.data
    except AttributeError:
        pass

    table.insert(payload).execute()
    fallback = (
        robot_table("showroom_buttons")
        .select("*")
        .eq("store_id", store_id)
        .eq("name", name)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    rows = (fallback.data or []) if fallback is not None else []
    return rows[0] if rows else {}


def update_button(button_id: str, patch: dict) -> dict:
    allowed = {"name", "description", "is_enabled", "sort_order", "group_id"}
    payload = {k: v for k, v in patch.items() if k in allowed}
    table = robot_table("showroom_buttons")
    try:
        res = (
            table
            .update(payload)
            .eq("id", button_id)
            .select("*")
            .single()
            .execute()
        )
        if res is not None and getattr(res, "data", None):
            return res.data
    except AttributeError:
        pass

    table.update(payload).eq("id", button_id).execute()
    fallback = (
        robot_table("showroom_buttons")
        .select("*")
        .eq("id", button_id)
        .limit(1)
        .execute()
    )
    rows = (fallback.data or []) if fallback is not None else []
    return rows[0] if rows else {}


def delete_button(button_id: str) -> None:
    robot_table("showroom_buttons").delete().eq("id", button_id).execute()


def set_button_actions(button_id: str, template_ids: list[str]) -> None:
    robot_table("showroom_button_actions").delete().eq("button_id", button_id).execute()
    if template_ids:
        rows = [
            {"button_id": button_id, "action_template_id": tid, "action_order": i, "is_enabled": True}
            for i, tid in enumerate(template_ids)
        ]
        robot_table("showroom_button_actions").insert(rows).execute()


# ─────────────────────────── Map Tabs ───────────────────────────

def list_map_tabs(store_id: str) -> list[dict]:
    res = (
        robot_table("showroom_map_tabs")
        .select("*")
        .eq("store_id", store_id)
        .order("sort_order", desc=False)
        .execute()
    )
    return res.data or []


def create_map_tab(store_id: str, map_name: str, display_name: str, sort_order: int = 0) -> dict:
    table = robot_table("showroom_map_tabs")
    payload = {
        "store_id": store_id,
        "map_name": map_name,
        "display_name": display_name,
        "sort_order": sort_order,
        "is_enabled": True,
    }
    try:
        res = table.insert(payload).select("*").single().execute()
        if res is not None and getattr(res, "data", None):
            return res.data
    except AttributeError:
        pass
    table.insert(payload).execute()
    fallback = (
        robot_table("showroom_map_tabs")
        .select("*")
        .eq("store_id", store_id)
        .eq("map_name", map_name)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    rows = _rows(fallback)
    return rows[0] if rows else {}


def update_map_tab(tab_id: str, patch: dict) -> dict:
    allowed = {"map_name", "display_name", "sort_order", "is_enabled"}
    payload = {k: v for k, v in patch.items() if k in allowed}
    table = robot_table("showroom_map_tabs")
    try:
        res = table.update(payload).eq("id", tab_id).select("*").single().execute()
        if res is not None and getattr(res, "data", None):
            return res.data
    except AttributeError:
        pass
    table.update(payload).eq("id", tab_id).execute()
    fallback = robot_table("showroom_map_tabs").select("*").eq("id", tab_id).limit(1).execute()
    rows = _rows(fallback)
    return rows[0] if rows else {}


def delete_map_tab(tab_id: str) -> None:
    robot_table("showroom_map_tabs").delete().eq("id", tab_id).execute()


# ─────────────────────────── Events ───────────────────────────

def list_events(store_id: str, limit: int = 50) -> list[dict]:
    res = (
        robot_table("showroom_events")
        .select("*")
        .eq("store_id", store_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return res.data or []


def insert_event(
    store_id: str,
    event_type: str,
    source: str,
    status: str,
    payload: dict,
    group_id: str | None = None,
    button_id: str | None = None,
    robot_sn: str | None = None,
) -> None:
    robot_table("showroom_events").insert({
        "store_id": store_id,
        "event_type": event_type,
        "source": source,
        "status": status,
        "payload": payload,
        "group_id": group_id,
        "button_id": button_id,
        "robot_sn": robot_sn,
    }).execute()
