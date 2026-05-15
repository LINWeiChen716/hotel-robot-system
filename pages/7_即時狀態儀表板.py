from __future__ import annotations

import datetime as dt
import json
import math
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

from services.dashboard_common import (
    build_group_robot_options,
    call_api,
    ensure_authenticated,
    extract_payload,
    load_store_context,
    to_unix,
)
from services.open_map_render import (
    build_map_view_payload,
    extract_map_image_url,
    fetch_image_as_data_url,
    normalize_map_detail_for_render,
    render_konva_map_html,
    transform_raw_map_data,
    world_xy_to_konva,
)
from services.showroom_service import extract_map_name_from_robot_payload


PALETTES = {
    "商務深藍": {
        "bg": "#0F172A",
        "panel": "#1E293B",
        "panel_soft": "rgba(30, 41, 59, 0.70)",
        "text": "#E2E8F0",
        "muted": "#94A3B8",
        "accent": "#38BDF8",
        "danger": "#FB7185",
        "warning": "#FBBF24",
        "ok": "#34D399",
        "idle": "#60A5FA",
        "line": "rgba(148, 163, 184, 0.25)",
    },
    "現代極簡白": {
        "bg": "#F8FAFC",
        "panel": "#FFFFFF",
        "panel_soft": "rgba(255, 255, 255, 0.72)",
        "text": "#334155",
        "muted": "#64748B",
        "accent": "#6366F1",
        "danger": "#E11D48",
        "warning": "#F59E0B",
        "ok": "#16A34A",
        "idle": "#3B82F6",
        "line": "rgba(15, 23, 42, 0.10)",
    },
}


def _inject_theme_css(palette_name: str) -> None:
    c = PALETTES.get(palette_name, PALETTES["商務深藍"])
    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;800&family=Space+Grotesk:wght@500;700&display=swap');
:root {{
  --bg: {c['bg']};
  --panel: {c['panel']};
  --panel-soft: {c['panel_soft']};
  --txt: {c['text']};
  --muted: {c['muted']};
  --accent: {c['accent']};
  --danger: {c['danger']};
  --warn: {c['warning']};
  --ok: {c['ok']};
  --idle: {c['idle']};
  --line: {c['line']};
}}
.stApp {{
  font-family: 'Noto Sans TC', sans-serif;
  color: var(--txt);
  background:
    radial-gradient(circle at 10% 8%, rgba(56,189,248,0.22), transparent 28%),
    radial-gradient(circle at 85% 0%, rgba(99,102,241,0.18), transparent 30%),
    linear-gradient(165deg, var(--bg), color-mix(in oklab, var(--bg), #020617 18%));
}}
h1, h2, h3 {{
  font-family: 'Space Grotesk', 'Noto Sans TC', sans-serif;
  letter-spacing: 0.2px;
}}
[data-testid="stForm"], .bento-card, [data-testid="stMetric"] {{
  border: 1px solid var(--line);
  border-radius: 22px;
  background: linear-gradient(145deg, var(--panel-soft), color-mix(in oklab, var(--panel), transparent 10%));
  backdrop-filter: blur(10px);
}}
.bento-card {{
  padding: 14px;
  min-height: 124px;
  box-shadow: 0 12px 28px rgba(2, 6, 23, 0.20);
}}
.chip {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 4px 10px;
  margin-right: 8px;
  background: color-mix(in oklab, var(--panel), transparent 18%);
  color: var(--txt);
  font-size: 12px;
}}
.dot {{
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}}
.pulse {{
  animation: pulse 1.8s ease-in-out infinite;
}}
@keyframes pulse {{
  0% {{ opacity: 0.50; transform: scale(0.96); }}
  50% {{ opacity: 1; transform: scale(1.08); }}
  100% {{ opacity: 0.50; transform: scale(0.96); }}
}}
.legend {{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 8px;
  margin-bottom: 8px;
}}
.event-l1 {{ border-left: 4px solid var(--accent); }}
.event-l2 {{ border-left: 4px solid var(--warn); }}
.event-l3 {{ border-left: 4px solid var(--danger); }}
</style>
        """,
        unsafe_allow_html=True,
    )


def _to_dict(payload: Any) -> dict:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, list) and payload and isinstance(payload[0], dict):
        return payload[0]
    return {}


def _to_list(payload: Any) -> list[dict]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if isinstance(payload, dict):
        for key in ("list", "items", "records", "data", "rows"):
            val = payload.get(key)
            if isinstance(val, list):
                return [x for x in val if isinstance(x, dict)]
    return []


def _safe_float(value: Any) -> float | None:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _safe_int(value: Any) -> int | None:
    try:
        if value is None or value == "":
            return None
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _pick(obj: dict, *keys: str) -> Any:
    for k in keys:
        if k in obj and obj.get(k) not in (None, ""):
            return obj.get(k)
    return None


def _extract_map_names(payload: Any) -> list[str]:
    rows = _to_list(payload)
    out: list[str] = []
    for row in rows:
        name = str(_pick(row, "map_name", "name", "mapName") or "").strip()
        if name and name not in out:
            out.append(name)
    if not out and isinstance(payload, dict):
        raw_names = payload.get("map_names")
        if isinstance(raw_names, list):
            for name in raw_names:
                txt = str(name or "").strip()
                if txt and txt not in out:
                    out.append(txt)
    return out


def _extract_coordinate(data: Any) -> tuple[float | None, float | None, float | None]:
    node = _to_dict(data)
    pos = _to_dict(_pick(node, "position", "pose", "robot_pose"))
    yaw = _safe_float(_pick(node, "yaw", "theta", "heading", "direction", "angle"))

    x = _safe_float(_pick(node, "x", "pos_x", "robot_x"))
    y = _safe_float(_pick(node, "y", "pos_y", "robot_y"))
    if x is None:
        x = _safe_float(_pick(pos, "x", "pos_x", "robot_x"))
    if y is None:
        y = _safe_float(_pick(pos, "y", "pos_y", "robot_y"))
    if yaw is None:
        yaw = _safe_float(_pick(pos, "yaw", "theta", "heading", "direction", "angle"))
    return x, y, yaw


def _status_color_key(status_text: str) -> str:
    s = status_text.lower()
    if any(k in s for k in ["異常", "故障", "error", "stuck", "卡住"]):
        return "danger"
    if any(k in s for k in ["充電", "recharge", "charging", "回充"]):
        return "warning"
    if any(k in s for k in ["閒置", "待命", "idle", "standby"]):
        return "idle"
    return "ok"


def _classify_robot_state(status_v2: dict, status_v1: dict, task: dict, has_error: bool) -> tuple[str, str]:
    if has_error:
        return "異常 / 卡住", "danger"

    text_pool = " ".join(
        [
            str(_pick(task, "status", "task_status", "state") or ""),
            str(_pick(status_v2, "work_status", "schedule_status", "state") or ""),
            str(_pick(status_v1, "work_status", "schedule_status", "state") or ""),
        ]
    ).lower()

    if any(k in text_pool for k in ["charge", "recharge", "回充", "充電"]):
        return "自動回充中", "warning"
    if any(k in text_pool for k in ["idle", "standby", "待命", "閒置", "空閒"]):
        return "待命", "idle"
    if text_pool.strip():
        return "任務中", "ok"
    return "待命", "idle"


def _extract_eta_distance(task_payload: dict) -> tuple[str, str]:
    eta = _pick(task_payload, "eta", "eta_min", "arrive_in", "remain_time", "left_time")
    dist = _pick(task_payload, "distance", "remain_distance", "left_distance", "target_distance")

    eta_text = "-"
    if isinstance(eta, (int, float)):
        eta_val = float(eta)
        eta_text = f"{eta_val:.0f} 分鐘" if eta_val > 0 else "已到達"
    elif eta not in (None, ""):
        eta_text = str(eta)

    dist_text = "-"
    if isinstance(dist, (int, float)):
        d_val = float(dist)
        if d_val >= 1000:
            dist_text = f"{d_val/1000:.2f} km"
        else:
            dist_text = f"{d_val:.1f} m"
    elif dist not in (None, ""):
        dist_text = str(dist)
    return eta_text, dist_text


def _infer_destination(task_payload: dict) -> tuple[float | None, float | None, str]:
    task = _to_dict(task_payload)
    dest = _to_dict(_pick(task, "target", "destination", "goal", "point"))
    x = _safe_float(_pick(task, "target_x", "goal_x", "dest_x"))
    y = _safe_float(_pick(task, "target_y", "goal_y", "dest_y"))
    if x is None:
        x = _safe_float(_pick(dest, "x", "target_x", "goal_x"))
    if y is None:
        y = _safe_float(_pick(dest, "y", "target_y", "goal_y"))
    name = str(_pick(task, "target_name", "point_name", "destination_name", "goal_name") or "")
    if not name:
        name = str(_pick(dest, "name", "point_name") or "")
    return x, y, name


def _extract_route_points(task_payload: dict) -> list[tuple[float, float]]:
    task = _to_dict(task_payload)
    candidates = [
        _pick(task, "route", "path", "waypoints", "points", "trajectory", "plan_points", "move_path"),
        _pick(task, "target_path", "route_points", "path_points"),
    ]

    for candidate in candidates:
        if not candidate:
            continue
        points: list[tuple[float, float]] = []
        if isinstance(candidate, list):
            for item in candidate:
                if isinstance(item, dict):
                    x = _safe_float(_pick(item, "x", "pos_x", "robot_x", "lng"))
                    y = _safe_float(_pick(item, "y", "pos_y", "robot_y", "lat"))
                    if x is not None and y is not None:
                        points.append((x, y))
                elif isinstance(item, (list, tuple)) and len(item) >= 2:
                    x = _safe_float(item[0])
                    y = _safe_float(item[1])
                    if x is not None and y is not None:
                        points.append((x, y))
        elif isinstance(candidate, dict):
            maybe_list = _pick(candidate, "list", "points", "route", "path", "waypoints")
            if isinstance(maybe_list, list):
                for item in maybe_list:
                    if isinstance(item, dict):
                        x = _safe_float(_pick(item, "x", "pos_x", "robot_x", "lng"))
                        y = _safe_float(_pick(item, "y", "pos_y", "robot_y", "lat"))
                        if x is not None and y is not None:
                            points.append((x, y))
        if points:
            return points
    return []


_RT_STATUS_COLORS = {
    "ok": "#34D399",
    "idle": "#60A5FA",
    "warning": "#FBBF24",
    "danger": "#FB7185",
}


def _render_rt_map_html(
    raw_map_data: dict,
    rows: list[dict],
    selected_sn: str,
    route_points: list[tuple[float, float]] | None = None,
    *,
    width: int = 900,
    height: int = 530,
) -> str:
    norm = normalize_map_detail_for_render(dict(raw_map_data)) if raw_map_data else {}
    resolution = float(norm.get("resolution") or 0.05)

    img_url = extract_map_image_url(norm) if norm else ""
    if img_url and not img_url.startswith("data:"):
        inlined = fetch_image_as_data_url(img_url)
        if inlined:
            norm["url"] = inlined

    robots_js: list[dict] = []
    for r in rows:
        wx, wy = r.get("x"), r.get("y")
        color = _RT_STATUS_COLORS.get(str(r.get("status_color") or "idle"), _RT_STATUS_COLORS["idle"])
        if not isinstance(wx, (int, float)) or not isinstance(wy, (int, float)):
            robots_js.append({
                "sn": str(r.get("sn") or ""),
                "name": str(r.get("display_name") or r.get("sn") or ""),
                "color": color, "noPos": True,
                "selected": str(r.get("sn") or "") == selected_sn,
            })
            continue
        kx, ky = world_xy_to_konva(float(wx), float(wy), resolution)
        yaw_konva = math.pi * 0.5 - float(r.get("yaw") or 0)
        robots_js.append({
            "x": kx, "y": ky,
            "name": str(r.get("display_name") or r.get("sn") or ""),
            "sn": str(r.get("sn") or ""),
            "color": color,
            "yaw": yaw_konva,
            "selected": str(r.get("sn") or "") == selected_sn,
        })

    route_points_js: list[dict[str, float]] = []
    for point in route_points or []:
        if not isinstance(point, (tuple, list)) or len(point) < 2:
            continue
        px = _safe_float(point[0])
        py = _safe_float(point[1])
        if px is None or py is None:
            continue
        kx, ky = world_xy_to_konva(float(px), float(py), resolution)
        route_points_js.append({"x": kx, "y": ky})

    norm["element_list"] = []
    norm["zone_list"] = []
    transformed = transform_raw_map_data(norm)
    
    # 正確提取地圖圖檔 URL
    img_base_url = transformed.get("url", "") or extract_map_image_url(norm) or ""
    if img_base_url and not img_base_url.startswith("data:"):
        img_base_url = fetch_image_as_data_url(img_base_url) or img_base_url
    
    map_image_data = {
        "x": float(transformed.get("x", 0)),
        "y": float(transformed.get("y", 0)),
        "translate": {"x": float(transformed.get("translate_x", 0)), "y": float(transformed.get("translate_y", 0))},
        "url": img_base_url
    }
    
    payload = {
        "map": {
            "mapImage": map_image_data,
            "elements": [],
            "zones": []
        },
        "robots": robots_js,
        "routePoints": route_points_js
    }
    data_json = json.dumps(payload, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"/>
<script src="https://unpkg.com/konva@9.3.6/konva.min.js"></script>
<style>
  html,body{{margin:0;padding:0;height:100%;background:#0f172a;overflow:hidden;
    font-family:"Microsoft JhengHei","PingFang TC","Noto Sans TC",sans-serif;}}
  #container{{width:100%;height:100%;}}
  .err{{color:#fb7185;padding:6px;font-size:12px;background:rgba(251,113,133,0.12);}}
</style></head><body>
<div id="container"></div>
<script type="application/json" id="payload">{data_json}</script>
<script>
(function(){{
  const p = JSON.parse(document.getElementById('payload').textContent);
  const mapData = p.map || {{}};
  const robots = p.robots || [];
  const routePoints = p.routePoints || [];
  
  // 使用直接的寬高，不依賴 container 尺寸
  const W = {width};
  const H = {height};
  
  if (!mapData.mapImage) {{
    document.body.innerHTML='<p class="err">地圖資料遺失</p>';
    return;
  }}
  
  const stage = new Konva.Stage({{container:'container', width:W, height:H}});
  const layer = new Konva.Layer();
  const g = new Konva.Group({{
    x: (mapData.mapImage.translate?.x || 0),
    y: (mapData.mapImage.translate?.y || 0)
  }});
  let imgW = 0, imgH = 0;

  function robotMarker(rb) {{
    if (rb.noPos) return null;
    const rg = new Konva.Group({{x:rb.x, y:rb.y}});
    const color = rb.color || '#60A5FA';
    if (rb.selected) {{
      rg.add(new Konva.Circle({{radius:18, fill:'transparent', stroke:'#ffffff', strokeWidth:2, dash:[5,4], opacity:0.85}}));
    }}
    rg.add(new Konva.Circle({{radius:11, fill:color, stroke:'#ffffff', strokeWidth:2.5}}));
    const yaw = typeof rb.yaw === 'number' ? rb.yaw : 0;
    const arrowLen = 17;
    rg.add(new Konva.Line({{
      points:[0,0, arrowLen*Math.cos(yaw), arrowLen*Math.sin(yaw)],
      stroke:'#ffffff', strokeWidth:2.5, lineCap:'round', opacity:0.92
    }}));
    if (rb.name) {{
      const tt = new Konva.Text({{
        y:-28, text:String(rb.name), fontSize:12,
        fill:'#ffffff', fontFamily:'Microsoft JhengHei,PingFang TC,sans-serif',
        padding:3, shadowColor:'rgba(0,0,0,0.9)', shadowBlur:6,
      }});
      tt.offsetX(tt.width()/2);
      rg.add(tt);
    }}
    return rg;
  }}

  function drawTrajectory(routePoints) {{
    if (!routePoints || routePoints.length < 2) return;
    const pts = [];
    for (let i = 0; i < routePoints.length; i++) {{
      const pt = routePoints[i];
      if (pt && typeof pt.x === 'number' && typeof pt.y === 'number') {{
        pts.push(pt.x, pt.y);
      }}
    }}
    if (pts.length < 4) return;

    const path = new Konva.Line({{
      points: pts,
      stroke: '#38BDF8',
      strokeWidth: 3.25,
      dash: [9, 7],
      lineCap: 'round',
      lineJoin: 'round',
      tension: 0.25,
      opacity: 0.92,
      shadowColor: 'rgba(56,189,248,0.35)',
      shadowBlur: 6,
      shadowOffsetX: 0,
      shadowOffsetY: 0,
    }});
    g.add(path);

    if (pts.length >= 4) {{
      const arrow = new Konva.Arrow({{
        points: pts,
        stroke: '#38BDF8',
        fill: '#38BDF8',
        strokeWidth: 3.25,
        pointerLength: 11,
        pointerWidth: 11,
        pointerAtEnding: true,
        pointerAtBeginning: false,
        lineCap: 'round',
        lineJoin: 'round',
        tension: 0.25,
        opacity: 0.82,
        shadowColor: 'rgba(56,189,248,0.20)',
        shadowBlur: 4,
      }});
      g.add(arrow);

      const startNode = routePoints[0];
      const endNode = routePoints[routePoints.length - 1];
      if (startNode && typeof startNode.x === 'number' && typeof startNode.y === 'number') {{
        g.add(new Konva.Circle({{
          x: startNode.x,
          y: startNode.y,
          radius: 5,
          fill: '#ffffff',
          stroke: '#38BDF8',
          strokeWidth: 2,
          opacity: 0.95,
        }}));
      }}
      if (endNode && typeof endNode.x === 'number' && typeof endNode.y === 'number') {{
        g.add(new Konva.Circle({{
          x: endNode.x,
          y: endNode.y,
          radius: 8,
          fill: '#38BDF8',
          stroke: '#ffffff',
          strokeWidth: 2,
          opacity: 0.98,
        }}));
      }}

      for (let i = 0; i < routePoints.length; i++) {{
        const pt = routePoints[i];
        if (!pt || typeof pt.x !== 'number' || typeof pt.y !== 'number') continue;
        const fade = 0.92 - (i * 0.12);
        g.add(new Konva.Circle({{
          x: pt.x,
          y: pt.y,
          radius: i === 0 ? 4 : 3,
          fill: i === routePoints.length - 1 ? '#38BDF8' : '#dff4ff',
          stroke: '#38BDF8',
          strokeWidth: 1,
          opacity: Math.max(0.25, fade),
        }}));
      }}
    }}
  }}
  }}

  function drawRobots() {{
    for (let i=0;i<robots.length;i++) {{
      const m = robotMarker(robots[i]);
      if (m) g.add(m);
    }}
    const sel = robots.find(r=>r.selected && !r.noPos);
    if (sel) {{
      const routePoints = Array.isArray(p.routePoints) ? p.routePoints : [];
      if (routePoints.length >= 2) {{
        drawTrajectory(routePoints);
      }}
    }}
  }}

  function finalizeMap() {{
    drawRobots();
    const fitGroup = new Konva.Group();
    fitGroup.add(g);
    layer.add(fitGroup);
    stage.add(layer);
        stage.draggable(true);
        layer.draw();
    const r = fitGroup.getClientRect();
    if (r.width > 0 && r.height > 0) {{
      const s = Math.min(W/r.width, H/r.height) * 0.94;
      fitGroup.scale({{x:s,y:s}});
      layer.draw();
      const r2 = fitGroup.getClientRect();
      fitGroup.x(fitGroup.x() + W/2-(r2.x+r2.width/2));
      fitGroup.y(fitGroup.y() + H/2-(r2.y+r2.height/2));
      layer.draw();
    }}

        const minScale = 0.35;
        const maxScale = 3.5;
        stage.on('wheel', function(e) {{
            e.evt.preventDefault();
            const oldScale = stage.scaleX() || 1;
            const pointer = stage.getPointerPosition();
            if (!pointer) return;
            const mousePointTo = {{
                x: (pointer.x - stage.x()) / oldScale,
                y: (pointer.y - stage.y()) / oldScale,
            }};
            const direction = e.evt.deltaY > 0 ? -1 : 1;
            const scaleBy = 1.08;
            let newScale = direction > 0 ? oldScale * scaleBy : oldScale / scaleBy;
            newScale = Math.max(minScale, Math.min(maxScale, newScale));
            stage.scale({{ x: newScale, y: newScale }});
            stage.position({{
                x: pointer.x - mousePointTo.x * newScale,
                y: pointer.y - mousePointTo.y * newScale,
            }});
            stage.batchDraw();
        }});
  }}

  const srcUrl = mapData.mapImage.url || '';
  if (srcUrl) {{
    const imgObj = new Image();
    imgObj.onload = function() {{
      imgW = imgObj.naturalWidth || 0;
      imgH = imgObj.naturalHeight || 0;
      g.add(new Konva.Image({{image:imgObj, x:mapData.mapImage.x, y:mapData.mapImage.y}}));
      finalizeMap();
    }};
    imgObj.onerror = function() {{
      document.body.insertAdjacentHTML('afterbegin','<p class="err">底圖載入失敗，僅顯示機器人位置。</p>');
      finalizeMap();
    }};
    imgObj.src = srcUrl;
  }} else {{
    document.body.insertAdjacentHTML('afterbegin','<p class="err">無地圖圖檔，僅顯示機器人位置。</p>');
    finalizeMap();
  }}
}})();
</script></body></html>"""


def _build_event_items(robots_snapshot: list[dict], prev: dict[str, dict]) -> list[dict]:
    items: list[dict] = []
    now_text = dt.datetime.now().strftime("%H:%M:%S")

    for r in robots_snapshot:
        sn = str(r.get("sn") or "")
        if not sn:
            continue
        curr = {
            "status": str(r.get("status_text") or ""),
            "battery": r.get("battery"),
            "is_online": r.get("is_online"),
            "error_count": int(r.get("error_count") or 0),
        }
        before = prev.get(sn, {})

        if not before:
            items.append(
                {
                    "level": 1,
                    "time": now_text,
                    "title": f"機器人 {sn} 已連線，狀態：{curr['status'] or '待命'}",
                    "sn": sn,
                }
            )
            continue

        if curr["status"] != before.get("status"):
            items.append(
                {
                    "level": 1,
                    "time": now_text,
                    "title": f"機器人 {sn} 狀態變更：{before.get('status', '-')} → {curr['status']}",
                    "sn": sn,
                }
            )

        b = _safe_float(curr.get("battery"))
        if isinstance(b, float):
            if b < 10:
                items.append(
                    {
                        "level": 3,
                        "time": now_text,
                        "title": f"機器人 {sn} 電量低於 10%，建議立即接管。",
                        "sn": sn,
                    }
                )
            elif b < 20:
                items.append(
                    {
                        "level": 2,
                        "time": now_text,
                        "title": f"機器人 {sn} 電量低於 20%，已進入預警。",
                        "sn": sn,
                    }
                )

        if int(curr.get("error_count") or 0) > int(before.get("error_count") or 0):
            items.append(
                {
                    "level": 3,
                    "time": now_text,
                    "title": f"機器人 {sn} 新增故障/異常事件，請立即檢查。",
                    "sn": sn,
                }
            )

        if str(curr.get("is_online")) == "0" and str(before.get("is_online")) != "0":
            items.append(
                {
                    "level": 2,
                    "time": now_text,
                    "title": f"機器人 {sn} 連線中斷，請檢查 Wi-Fi 或設備電源。",
                    "sn": sn,
                }
            )

    return items


def _sn_state_snapshot(robots_snapshot: list[dict]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for r in robots_snapshot:
        sn = str(r.get("sn") or "")
        if not sn:
            continue
        out[sn] = {
            "status": str(r.get("status_text") or ""),
            "battery": r.get("battery"),
            "is_online": r.get("is_online"),
            "error_count": int(r.get("error_count") or 0),
        }
    return out


ensure_authenticated("即時狀態儀表板 | Pudu API", "🛰️")

store, robots, groups, robot_map = load_store_context()

st.title("🛰️ 即時狀態儀表板")
st.caption("Digital Twin Map + Robot Asset List + Live Event Log")

with st.sidebar:
    st.subheader("顯示設定")
    palette_name = st.radio("配色方案", options=list(PALETTES.keys()), index=0)
    _inject_theme_css(palette_name)

    default_end = dt.date.today()
    default_start = default_end - dt.timedelta(days=1)
    date_range = st.date_input("事件查詢區間", value=(default_start, default_end))
    log_limit = st.number_input("每台日誌筆數", min_value=5, max_value=100, value=20, step=5)
    refresh_now = st.button("立即刷新", type="primary", use_container_width=True)

timezone_offset = 8  # 固定台灣時區

_RT_KEYWORDS = ["flashbot", "flash", "閃電", "運送", "配送", "delivery", "pudubot", "清潔", "clean", "cc1", "mt1"]
_rt_options = build_group_robot_options(groups, robot_map, _RT_KEYWORDS)
_rt_sns = set(_rt_options.values())
enabled_robots = [
    r for r in robots
    if r.get("is_enabled")
    and str(r.get("sn") or "").strip()
    and (not _rt_sns or str(r.get("sn") or "").strip() in _rt_sns)
    and str(r.get("nickname") or "").strip() in ["閃閃", "讓讓", "聰聰"]
]
if not enabled_robots:
    st.warning("目前沒有啟用中的機器人，請先到設定頁新增並啟用機器人。")
    st.stop()

if refresh_now:
    st.rerun()

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range

shop_id = _safe_int(store.get("pudu_shop_id"))
map_payload = {}
map_names: list[str] = []
if shop_id and shop_id > 0:
    map_list_res = call_api("map_list", {"shop_id": shop_id})
    map_payload = extract_payload(map_list_res)
    map_names = _extract_map_names(map_payload)

# 限制地圖清單
map_names = [n for n in map_names if n in ["1#1#內湖展間v20", "1#7#內湖展間清潔v4"]]
if not map_names:
    map_names = ["1#1#內湖展間v20", "1#7#內湖展間清潔v4"]

default_floor = st.session_state.get("rt_floor")
if default_floor not in map_names:
    default_floor = map_names[0]

floor = st.sidebar.radio("樓層切換", options=map_names, index=map_names.index(default_floor))
st.session_state["rt_floor"] = floor

time_query = {
    "start_date": start_date.isoformat(),
    "end_date": end_date.isoformat(),
    "limit": int(log_limit),
    "offset": 0,
    "start_time": to_unix(start_date, end_of_day=False, timezone_offset=int(timezone_offset)),
    "end_time": to_unix(end_date, end_of_day=True, timezone_offset=int(timezone_offset)),
    "timezone_offset": int(timezone_offset),
}

rows: list[dict] = []
progress_bar = st.progress(0)
for idx, robot in enumerate(enabled_robots):
    progress_bar.progress((idx + 1) / len(enabled_robots))
    sn = str(robot.get("sn") or "").strip()
    if not sn:
        continue

    status_v2 = _to_dict(extract_payload(call_api("status_by_sn_v2", {"sn": sn})))
    position = _to_dict(extract_payload(call_api("robot_position", {"sn": sn})))
    task = _to_dict(extract_payload(call_api("robot_task_state", {"sn": sn})))

    battery = _safe_float(_pick(status_v2, "battery", "battery_percent"))
    eta_text, dist_text = _extract_eta_distance(task)
    has_error = False
    status_text, status_color = _classify_robot_state(status_v2, {}, task, has_error)
    rssi = _safe_int(_pick(status_v2, "rssi", "wifi_rssi", "signal", "signal_dbm"))

    x, y, yaw = _extract_coordinate(position)
    current_map_name = (
        extract_map_name_from_robot_payload(position)
        or extract_map_name_from_robot_payload(status_v2)
        or extract_map_name_from_robot_payload(task)
    )

    rows.append(
        {
            "sn": sn,
            "display_name": str(robot.get("nickname") or sn),
            "battery": battery,
            "status_text": status_text,
            "status_color": status_color,
            "task_raw": str(_pick(task, "status", "task_status", "state") or "-")[:60],
            "eta": eta_text,
            "distance": dist_text,
            "rssi": rssi,
            "is_online": _pick(status_v2, "is_online", "online", "isOnline", "connect_status"),
            "x": x,
            "y": y,
            "yaw": yaw if isinstance(yaw, (int, float)) else 0,
            "current_map_name": current_map_name,
            "task_payload": task,
            "position_payload": position,
            "error_count": 0,
            "charge_count": 0,
        }
    )

if not rows:
    st.info("目前查無可展示的機器人狀態。")
    st.stop()

selected_robot_label = st.sidebar.selectbox(
    "地圖聚焦機器人",
    options=[f"{r['display_name']} ({r['sn']})" for r in rows if str(r.get("current_map_name") or "").strip() == floor] or [f"{r['display_name']} ({r['sn']})" for r in rows],
    index=0,
)
selected_sn = selected_robot_label.rsplit("(", 1)[-1].replace(")", "").strip()
selected_robot = next((r for r in rows if r.get("sn") == selected_sn), rows[0])
selected_task_payload = _to_dict(selected_robot.get("task_payload"))
selected_route_points = _extract_route_points(selected_task_payload)
selected_dest_x, selected_dest_y, _selected_dest_name = _infer_destination(selected_task_payload)
if not selected_route_points and selected_robot.get("status_color") == "ok" and str(selected_robot.get("current_map_name") or "").strip() == floor:
    if (
        isinstance(selected_robot.get("x"), (int, float))
        and isinstance(selected_robot.get("y"), (int, float))
        and isinstance(selected_dest_x, (int, float))
        and isinstance(selected_dest_y, (int, float))
    ):
        selected_route_points = [
            (float(selected_robot["x"]), float(selected_robot["y"])),
            (float(selected_dest_x), float(selected_dest_y)),
        ]

map_detail_payload = {}
if shop_id and shop_id > 0:
    map_detail_res = call_api("map_detail_v1", {"shop_id": int(shop_id), "map_name": floor})
    map_detail_payload = extract_payload(map_detail_res)

st.markdown(
    """
<div class='legend'>
  <span class='chip'><span class='dot pulse' style='background: var(--ok)'></span>任務中</span>
  <span class='chip'><span class='dot' style='background: var(--idle)'></span>待命</span>
  <span class='chip'><span class='dot pulse' style='background: var(--warn)'></span>自動回充中</span>
  <span class='chip'><span class='dot pulse' style='background: var(--danger)'></span>異常 / 卡住</span>
</div>
    """,
    unsafe_allow_html=True,
)

g1, g2 = st.columns([2.05, 1.15])
with g1:
    st.markdown("### 1) 全域實體地圖 (Digital Twin Map)")
    _map_raw = _to_dict(map_detail_payload) if map_detail_payload else {}
    _map_norm = normalize_map_detail_for_render(dict(_map_raw)) if _map_raw else {}
    _map_resolution = float(_map_norm.get("resolution") or 0.05)
    focus_rows = [r for r in rows if str(r.get("current_map_name") or "").strip() == floor and isinstance(r.get("x"), (int, float)) and isinstance(r.get("y"), (int, float))]
    if not focus_rows:
        focus_rows = [r for r in rows if isinstance(r.get("x"), (int, float)) and isinstance(r.get("y"), (int, float))]

    robots_konva = []
    for r in focus_rows:
        if not isinstance(r.get("x"), (int, float)) or not isinstance(r.get("y"), (int, float)):
            continue
        robot_x, robot_y = world_xy_to_konva(float(r["x"]), float(r["y"]), _map_resolution)
        robots_konva.append(
            {
                "x": robot_x,
                "y": robot_y,
                "name": str(r.get("display_name") or r.get("sn") or ""),
                "sn": str(r.get("sn") or ""),
                "selected": str(r.get("sn") or "") == selected_sn,
                "color": _RT_STATUS_COLORS.get(str(r.get("status_color") or "idle"), _RT_STATUS_COLORS["idle"]),
            }
        )
    route_points_konva: list[dict[str, float]] = []
    if selected_robot.get("status_color") == "ok" and str(selected_robot.get("current_map_name") or "").strip() == floor:
        for pt in selected_route_points:
            if not isinstance(pt, (tuple, list)) or len(pt) < 2:
                continue
            px = _safe_float(pt[0])
            py = _safe_float(pt[1])
            if px is None or py is None:
                continue
            kx, ky = world_xy_to_konva(float(px), float(py), _map_resolution)
            route_points_konva.append({"x": kx, "y": ky})

    map_payload = build_map_view_payload(_map_raw, robots_konva, inline_map_image=True, robots_only_overlay=True)
    if route_points_konva:
        map_payload["routePoints"] = route_points_konva
    map_html = render_konva_map_html(map_payload, width=900, height=530)
    components.html(map_html, height=550, scrolling=False)
    st.caption(f"已選擇機器人：{selected_robot.get('display_name')} | 地圖可用滑鼠滾輪縮放、拖曳平移")

with g2:
    st.markdown("### 2) 機器人狀態列表 (Robot Asset List)")

    table_rows = []
    for r in rows:
        b = _safe_float(r.get("battery"))
        if isinstance(b, float):
            if b < 10:
                battery_text = f"🔴 {b:.0f}%"
            elif b < 20:
                battery_text = f"🟡 {b:.0f}%"
            else:
                battery_text = f"🟢 {b:.0f}%"
        else:
            battery_text = "-"

        eta_text = str(r.get("eta") or "-")
        if eta_text not in {"-", "已到達"} and "分鐘" in eta_text:
            try:
                eta_num = float(eta_text.replace("分鐘", "").strip())
                if eta_num > 15:
                    eta_text = f"🔴 {eta_text}"
            except ValueError:
                pass

        rssi = r.get("rssi")
        rssi_text = f"{rssi} dBm" if isinstance(rssi, int) else "-"
        if isinstance(rssi, int) and rssi < -75:
            rssi_text = f"⚠️ {rssi_text}"

        table_rows.append(
            {
                "機器人名稱": f"{r['display_name']} ({r['sn']})",
                "當前電量": battery_text,
                "任務狀態": r.get("status_text"),
                "預計到達": eta_text,
                "剩餘距離": r.get("distance"),
                "連線品質": rssi_text,
            }
        )

    st.dataframe(table_rows, use_container_width=True, hide_index=True)

st.markdown("### 3) 即時事件與警報日誌 (Live Event Log & Alerts)")

prev_key = "_rt_dashboard_prev"
log_key = "_rt_dashboard_logs"
prev_snapshot = st.session_state.get(prev_key) or {}

new_items = _build_event_items(rows, prev_snapshot)
all_items = (new_items + (st.session_state.get(log_key) or []))[:80]
st.session_state[log_key] = all_items
st.session_state[prev_key] = _sn_state_snapshot(rows)

if not all_items:
    st.info("尚未產生事件，請點擊右側「立即刷新」後查看。")
else:
    for item in all_items[:30]:
        level = int(item.get("level") or 1)
        css = "event-l1" if level == 1 else "event-l2" if level == 2 else "event-l3"
        badge = "INFO" if level == 1 else "WARN" if level == 2 else "CRITICAL"
        with st.container(border=True):
            st.markdown(f"<div class='{css}' style='padding-left:10px;'><strong>[{badge}] {item.get('time')}</strong> {item.get('title')}</div>", unsafe_allow_html=True)

            if level == 3:
                c1, c2, c3 = st.columns([1, 1, 2])
                with c1:
                    if hasattr(st, "page_link"):
                        st.page_link("pages/3_API測試.py", label="查看鏡頭", icon="📹")
                    else:
                        st.button("查看鏡頭", disabled=True, key=f"camera_{item.get('time')}_{item.get('sn')}")
                with c2:
                    if hasattr(st, "page_link"):
                        st.page_link("pages/3_API測試.py", label="遠端遙控", icon="🕹️")
                    else:
                        st.button("遠端遙控", disabled=True, key=f"remote_{item.get('time')}_{item.get('sn')}")
                with c3:
                    st.caption("目前 API 定義中未找到 camera/teleop 專用端點，捷徑已導向 API 測試頁做應急操作。")

with st.expander("偵錯資料（地圖與狀態原始回應）"):
    st.write("目前樓層", floor)
    st.json({
        "map_list": map_payload,
        "map_detail": map_detail_payload,
        "rows": rows,
        "events": all_items,
    })
