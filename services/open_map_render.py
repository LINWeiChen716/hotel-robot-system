"""
OPEN_MAP_RENDER 對齊：transform-raw-map-data + coodinate-transformation。
用於地圖底圖與機器人世界座標 → Konva 疊圖（預設不繪製 element/zone 向量）。
"""

from __future__ import annotations

import base64
import json
import math
from typing import Any

import requests

# 內嵌 base64 過大時 iframe 內 JSON 解析會失敗
_MAX_INLINE_DATA_URL_CHARS = 5_000_000


def to_konva_vector(origin_vec: Any, resolution: float) -> list[float] | dict[str, float]:
    if isinstance(origin_vec, list):
        konva_vec = [float(v) / resolution for v in origin_vec]
        if len(origin_vec) == 3:
            konva_vec[2] = math.pi * 0.5 - float(origin_vec[2])
        for i in range(len(konva_vec)):
            if i % 2 == 1:
                konva_vec[i] = -1.0 * konva_vec[i]
        return konva_vec

    if isinstance(origin_vec, dict):
        x = float(origin_vec.get("x", 0))
        y = float(origin_vec.get("y", 0))
        out: dict[str, float] = {"x": x / resolution, "y": -1.0 * y / resolution}
        if "z" in origin_vec:
            out["z"] = math.pi * 0.5 - float(origin_vec["z"])
        return out

    raise TypeError(f"unsupported vector type: {type(origin_vec)}")


def convert_map_image_konva(map_image_meta: dict[str, Any], resolution: float) -> dict[str, Any]:
    origin = map_image_meta["origin"]
    image_px_width = float(map_image_meta["width"])
    image_px_height = float(map_image_meta["height"])

    image_vec = to_konva_vector(origin, resolution)
    if not isinstance(image_vec, list):
        raise ValueError("map image origin must be array")
    image_vec = list(image_vec)
    image_vec[1] = image_vec[1] - image_px_height

    top_left = {"x": 0 - image_vec[0], "y": 0 - image_vec[1]}

    return {
        "x": image_vec[0],
        "y": image_vec[1],
        "width": image_px_width,
        "height": image_px_height,
        "translate": {"x": top_left["x"], "y": top_left["y"]},
    }


def extract_map_image_url(raw: dict[str, Any]) -> str:
    if not isinstance(raw, dict):
        return ""
    candidates: list[Any] = [
        raw.get("url"),
        raw.get("map_url"),
        raw.get("image_url"),
        raw.get("map_image_url"),
        raw.get("png_url"),
        raw.get("map_png_url"),
        raw.get("bitmap_url"),
        raw.get("opt_map_url"),
    ]
    for key in ("map_info", "mapInfo", "map_image", "mapImage"):
        sub = raw.get(key)
        if isinstance(sub, dict):
            candidates.extend([sub.get("url"), sub.get("map_url"), sub.get("image_url")])
    for c in candidates:
        if isinstance(c, str):
            s = c.strip()
            if s.startswith(("http://", "https://")):
                return s
    for c in candidates:
        if isinstance(c, str) and c.strip():
            return c.strip()
    return ""


def _origin_to_list(origin: Any) -> list[float]:
    if isinstance(origin, list) and origin:
        return [
            float(origin[0]),
            float(origin[1]) if len(origin) > 1 else 0.0,
            float(origin[2]) if len(origin) > 2 else 0.0,
        ]
    if isinstance(origin, dict):
        return [
            float(origin.get("x", 0)),
            float(origin.get("y", 0)),
            float(origin.get("z", 0)),
        ]
    return [0.0, 0.0, 0.0]


def normalize_map_detail_for_render(raw_map_data: dict[str, Any]) -> dict[str, Any]:
    out = dict(raw_map_data)
    img_url = extract_map_image_url(out) or out.get("url") or ""
    if img_url:
        out["url"] = img_url
    if out.get("origin") is None:
        out["origin"] = [0.0, 0.0, 0.0]
    else:
        out["origin"] = _origin_to_list(out.get("origin"))
    if out.get("width") in (None, "", 0):
        out["width"] = float(out.get("width") or 885)
    else:
        out["width"] = float(out["width"])
    if out.get("height") in (None, "", 0):
        out["height"] = float(out.get("height") or 1161)
    else:
        out["height"] = float(out["height"])
    if not out.get("element_list") and isinstance(out.get("elements"), list):
        out["element_list"] = out["elements"]
    if not out.get("zone_list") and isinstance(out.get("zones"), list):
        out["zone_list"] = out["zones"]
    return out


def _bytes_to_jpeg_data_url(img_bytes: bytes, *, max_side: int, quality: int = 82) -> str | None:
    try:
        from io import BytesIO

        from PIL import Image
    except ImportError:
        return None
    try:
        im = Image.open(BytesIO(img_bytes))
        im = im.convert("RGBA") if im.mode in ("P", "PA") else im
        if im.mode == "RGBA":
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[3])
            im = bg
        elif im.mode != "RGB":
            im = im.convert("RGB")
        w, h = im.size
        if w > 0 and h > 0 and max(w, h) > max_side:
            ratio = max_side / float(max(w, h))
            im = im.resize((max(1, int(w * ratio)), max(1, int(h * ratio))), Image.Resampling.LANCZOS)
        buf = BytesIO()
        im.save(buf, format="JPEG", quality=quality, optimize=True)
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        return f"data:image/jpeg;base64,{b64}"
    except Exception:
        return None


def fetch_image_as_data_url(url: str, *, timeout: int = 45) -> str | None:
    if not url or url.startswith("data:"):
        return url if url.startswith("data:") else None
    try:
        r = requests.get(
            url,
            timeout=timeout,
            headers={"User-Agent": "Mozilla/5.0 (compatible; PuduMapRender/1.0)"},
        )
        r.raise_for_status()
        raw = r.content
        ct = (r.headers.get("Content-Type") or "image/png").split(";")[0].strip()
        if not ct.startswith("image/"):
            ct = "image/png"
        b64 = base64.b64encode(raw).decode("ascii")
        data_url = f"data:{ct};base64,{b64}"
        if len(data_url) <= _MAX_INLINE_DATA_URL_CHARS:
            return data_url
        # 過大：縮圖後改 JPEG，必要時逐步縮小長邊
        for max_side in (4096, 3072, 2048, 1536, 1024, 768):
            jpeg_url = _bytes_to_jpeg_data_url(raw, max_side=max_side)
            if jpeg_url and len(jpeg_url) <= _MAX_INLINE_DATA_URL_CHARS:
                return jpeg_url
        return None
    except Exception:
        return None


def transform_raw_map_data(raw_map_data: dict[str, Any]) -> dict[str, Any]:
    element_list = raw_map_data.get("element_list") or []
    zone_list = raw_map_data.get("zone_list") or []
    map_name = raw_map_data.get("map_name") or ""
    map_image_url = extract_map_image_url(raw_map_data) or raw_map_data.get("url") or ""
    resolution = float(raw_map_data.get("resolution") or 0.05)
    if resolution <= 0:
        resolution = 0.05

    origin = raw_map_data.get("origin")
    map_image_width = raw_map_data.get("width")
    map_image_height = raw_map_data.get("height")

    for element in element_list:
        if not isinstance(element, dict):
            continue
        vl = element.get("vector_list")
        if vl is not None:
            element["vector_list"] = to_konva_vector(vl, resolution)
        cpl = element.get("clean_path_list") or []
        element["clean_path_list"] = [to_konva_vector(p, resolution) for p in cpl if isinstance(p, dict)]

    for zone in zone_list:
        if not isinstance(zone, dict):
            continue
        for node in zone.get("zone_node_list") or []:
            if isinstance(node, dict) and "vector_list" in node:
                node["vector_list"] = to_konva_vector(node["vector_list"], resolution)

    map_image_meta = convert_map_image_konva(
        {"origin": origin, "width": map_image_width, "height": map_image_height},
        resolution,
    )
    return {
        "mapName": map_name,
        "mapImage": {"url": map_image_url, **map_image_meta},
        "elementList": element_list,
        "zoneList": zone_list,
        "resolution": resolution,
    }


def world_xy_to_konva(x: float, y: float, resolution: float) -> tuple[float, float]:
    vec = to_konva_vector([float(x), float(y)], resolution)
    if isinstance(vec, list) and len(vec) >= 2:
        return float(vec[0]), float(vec[1])
    raise ValueError("expected 2d konva vector")


def build_map_view_payload(
    raw_map_data: dict[str, Any],
    robots_konva: list[dict[str, Any]],
    *,
    inline_map_image: bool = True,
    robots_only_overlay: bool = True,
    view_rotation_deg: float = 0.0,
) -> dict[str, Any]:
    data = normalize_map_detail_for_render(dict(raw_map_data))
    if robots_only_overlay:
        data["element_list"] = []
        data["zone_list"] = []
    if inline_map_image:
        u = extract_map_image_url(data)
        if u and not str(u).startswith("data:"):
            inlined = fetch_image_as_data_url(u)
            if inlined:
                data["url"] = inlined
    transformed = transform_raw_map_data(data)
    return {
        "map": transformed,
        "robots": robots_konva,
        "viewRotationDeg": float(view_rotation_deg),
    }


def render_konva_map_html(payload: dict[str, Any], *, width: int = 880, height: int = 460) -> str:
    data_json = json.dumps(payload, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"/>
<script src="https://unpkg.com/konva@9.3.6/konva.min.js"></script>
<style>
  html, body {{ margin:0; padding:0; height:100%; background:#ffffff; overflow:hidden;
    font-family:"Microsoft JhengHei","PingFang TC","Noto Sans TC",sans-serif; }}
  #container {{ width:100%; height:100%; box-sizing:border-box; }}
  .err {{ color:#b91c1c; padding:8px; font-size:12px; background:#fee2e2; }}
</style></head>
<body>
<div id="container"></div>
<script type="application/json" id="map-payload">{data_json}</script>
<script>
(function() {{
  const payload = JSON.parse(document.getElementById('map-payload').textContent);
  const mapData = payload.map;
  const robots = payload.robots || [];
    const routePoints = payload.routePoints || [];
  const viewRot = typeof payload.viewRotationDeg === 'number' ? payload.viewRotationDeg : 0;
  const el = document.getElementById('container');
  const W = Math.max(320, el.clientWidth || {width});
  const H = Math.max(240, el.clientHeight || {height});

  if (!mapData || !mapData.mapImage) {{
    document.body.innerHTML = '<p class="err">地圖資料格式異常</p>';
    return;
  }}

  const stage = new Konva.Stage({{ container: 'container', width: W, height: H }});
  const layer = new Konva.Layer({{ draggable: false, listening: true }});
  const g = new Konva.Group({{
    x: mapData.mapImage.translate.x,
    y: mapData.mapImage.translate.y,
  }});
  let imgNaturalW = 0;
  let imgNaturalH = 0;

  const srcUrl = mapData.mapImage.url || '';

  function robotMarker(x, y, name) {{
    const rg = new Konva.Group({{ x: x, y: y }});
    const innerR = 10;
    rg.add(new Konva.Circle({{
      radius: innerR + 6,
      stroke: '#a855f7',
      strokeWidth: 4,
      fill: 'transparent',
    }}));
    rg.add(new Konva.Circle({{
      radius: innerR,
      fill: '#3b82f6',
      stroke: '#ffffff',
      strokeWidth: 2,
    }}));
    const s = 12;
    rg.add(new Konva.Line({{ points: [-s, 0, s, 0], stroke: '#a855f7', strokeWidth: 2.5 }}));
    rg.add(new Konva.Line({{ points: [0, -s, 0, s], stroke: '#a855f7', strokeWidth: 2.5 }}));
    if (name) {{
      const tt = new Konva.Text({{
        y: -innerR - 32,
        text: String(name),
        fontSize: 11,
        fill: '#ffffff',
        fontFamily: 'Microsoft JhengHei, PingFang TC, sans-serif',
        padding: 4,
        shadowColor: 'rgba(0,0,0,0.85)',
        shadowBlur: 5,
        shadowOffsetY: 1,
      }});
      tt.offsetX(tt.width() / 2);
      rg.add(tt);
    }}
    return rg;
  }}

    function drawRoute() {{
        if (!Array.isArray(routePoints) || routePoints.length < 2) return;
        const pts = [];
        for (let i = 0; i < routePoints.length; i++) {{
            const pt = routePoints[i];
            if (pt && typeof pt.x === 'number' && typeof pt.y === 'number') {{
                pts.push(pt.x, pt.y);
            }}
        }}
        if (pts.length < 4) return;

        g.add(new Konva.Line({{
            points: pts,
            stroke: '#38bdf8',
            strokeWidth: 3,
            dash: [10, 7],
            lineCap: 'round',
            lineJoin: 'round',
            tension: 0.25,
            opacity: 0.88,
            shadowColor: 'rgba(56,189,248,0.25)',
            shadowBlur: 5,
        }}));

        g.add(new Konva.Arrow({{
            points: pts,
            stroke: '#38bdf8',
            fill: '#38bdf8',
            strokeWidth: 3,
            pointerLength: 10,
            pointerWidth: 10,
            pointerAtEnding: true,
            lineCap: 'round',
            lineJoin: 'round',
            tension: 0.25,
            opacity: 0.8,
        }}));

        for (let i = 0; i < routePoints.length; i++) {{
            const pt = routePoints[i];
            if (!pt || typeof pt.x !== 'number' || typeof pt.y !== 'number') continue;
            g.add(new Konva.Circle({{
                x: pt.x,
                y: pt.y,
                radius: i === 0 ? 4 : 3,
                fill: i === 0 ? '#ffffff' : (i === routePoints.length - 1 ? '#38bdf8' : '#dff4ff'),
                stroke: '#38bdf8',
                strokeWidth: 1,
                opacity: i === 0 || i === routePoints.length - 1 ? 0.98 : 0.75,
            }}));
        }}
    }}

  function drawVectors() {{
    for (let r = 0; r < robots.length; r++) {{
      const rb = robots[r];
      g.add(robotMarker(rb.x, rb.y, rb.name || ''));
    }}
  }}

  function finalizeMap() {{
        drawRoute();
    drawVectors();
    const iw = imgNaturalW || Number(mapData.mapImage.width || 885);
    const ih = imgNaturalH || Number(mapData.mapImage.height || 1161);
    const px = mapData.mapImage.x + iw * 0.5;
    const py = mapData.mapImage.y + ih * 0.5;
    if (Math.abs(viewRot) > 0.001) {{
      g.offsetX(px);
      g.offsetY(py);
      g.x(mapData.mapImage.translate.x + px);
      g.y(mapData.mapImage.translate.y + py);
      g.rotation(viewRot);
    }}
    const fitGroup = new Konva.Group();
    fitGroup.add(g);
    layer.add(fitGroup);
    stage.add(layer);
    layer.draw();
    const r = fitGroup.getClientRect();
    if (r.width > 0 && r.height > 0) {{
      const pad = 0.94;
      const s = Math.min(W / r.width, H / r.height) * pad;
      fitGroup.scale({{ x: s, y: s }});
      layer.draw();
      const r2 = fitGroup.getClientRect();
      fitGroup.x(fitGroup.x() + W / 2 - (r2.x + r2.width / 2));
      fitGroup.y(fitGroup.y() + H / 2 - (r2.y + r2.height / 2));
      layer.draw();
    }}
  }}

  if (srcUrl) {{
    const imgObj = new Image();
    imgObj.onload = function() {{
      imgNaturalW = imgObj.naturalWidth || 0;
      imgNaturalH = imgObj.naturalHeight || 0;
      g.add(new Konva.Image({{
        image: imgObj,
        x: mapData.mapImage.x,
        y: mapData.mapImage.y,
      }}));
      finalizeMap();
    }};
    imgObj.onerror = function() {{
      const hint = document.createElement('p');
      hint.className = 'err';
      hint.textContent = '底圖載入失敗，僅顯示機器人位置。';
      document.body.insertBefore(hint, document.body.firstChild);
      finalizeMap();
    }};
    imgObj.src = srcUrl;
  }} else {{
    const hint = document.createElement('p');
    hint.className = 'err';
    hint.textContent = '無圖檔網址，僅顯示機器人位置。';
    document.body.insertBefore(hint, document.body.firstChild);
    finalizeMap();
  }}
}})();
</script>
</body></html>"""
