"""
自動把 Pudu_Cloud_API_繁體使用說明書_整合版.md 切割成
MkDocs 目錄結構，並生成 mkdocs.yml。
執行一次即可；之後直接用 mkdocs serve 啟動。
"""
import re
import os
import shutil

SRC = "Pudu_Cloud_API_繁體使用說明書_整合版.md"
DOCS_DIR = "docs"
MKDOCS_YML = "mkdocs.yml"

# ─── 章節分類對照 ────────────────────────────────────────────
# key = 要比對的關鍵字（包含在標題內即分入該類）
# value = (中文分類名, 子目錄)
CATEGORIES = [
    ("概述",            ("開發指南",     "guide")),
    ("快速開始",        ("開發指南",     "guide")),
    ("用戶請求普渡開放平臺接口步驟", ("開發指南", "guide")),
    ("鑑權接入",        ("開發指南",     "guide")),
    ("普渡開放平臺的對外固定域名",   ("開發指南", "guide")),
    ("普渡開放平臺鑑權",("開發指南",     "guide")),
    ("簽名生成",        ("開發指南",     "guide")),
    ("呼叫機器調用示例",("開發指南",     "guide")),
    ("呼叫抵達通知回調示例", ("開發指南","guide")),
    ("獲取機器當前使用地圖調用示例",  ("開發指南","guide")),
    ("機器類型",        ("附錄",         "appendix")),
    ("數據中心指標定義",("附錄",         "appendix")),
    ("錯誤碼",          ("附錄",         "appendix")),
    ("Locale枚舉",      ("附錄",         "appendix")),
    # 回調通知
    ("robotErrorWarning",        ("回調通知", "callback")),
    ("robotErrorNotice",         ("回調通知", "callback")),
    ("robotBinding",             ("回調通知", "callback")),
    ("robotUnBinding",           ("回調通知", "callback")),
    ("robotActivate",            ("回調通知", "callback")),
    ("robotStatus",              ("回調通知", "callback")),
    ("robotEmergencyRecover",    ("回調通知", "callback")),
    ("notifyRobotStatus",        ("回調通知", "callback")),
    ("mapElementChange",         ("回調通知", "callback")),
    ("notifyRobotPose",          ("回調通知", "callback")),
    ("notifyRobotMoveState",     ("回調通知", "callback")),
    ("notifySwitchMap",          ("回調通知", "callback")),
    ("notifyCustomCall",         ("回調通知", "callback")),
    ("notifyRobotOrderState",    ("回調通知", "callback")),
    ("robotDeliveryStatus",      ("回調通知", "callback")),
    ("notifyTransportTask",      ("回調通知", "callback")),
    ("notifyDeliveryTask",       ("回調通知", "callback")),
    ("notifyErrandStatus",       ("回調通知", "callback")),
    ("notifyLiftingTask",        ("回調通知", "callback")),
    ("TASK_STATUS",              ("回調通知", "callback")),
    ("notifyCleanStatus",        ("回調通知", "callback")),
    ("notifyCruiseTask",         ("回調通知", "callback")),
    ("notifyRobotPower",         ("回調通知", "callback")),
    ("notifyDoorsState",         ("回調通知", "callback")),
    ("notifyElevatorUtilizeState",("回調通知","callback")),
    ("notifyQrCodeContent",      ("回調通知", "callback")),
    ("notifyLiftingStatus",      ("回調通知", "callback")),
    ("notifyRechargeStatus",     ("回調通知", "callback")),
    # 通用接口
    ("獲取門店列表",    ("通用接口",     "common")),
    ("門店機器列表",    ("通用接口",     "common")),
    ("門店下地圖列表",  ("通用接口",     "common")),
    ("機器可用地圖列表",("通用接口",     "common")),
    ("機器當前使用地圖",("通用接口",     "common")),
    ("獲取地圖詳情",    ("通用接口",     "common")),
    ("繪製解析後的地圖",("通用接口",     "common")),
    ("獲取機器實時地圖位置",("通用接口", "common")),
    ("獲取機器當前使用地圖的點位",("通用接口","common")),
    ("獲取點位分組",    ("通用接口",     "common")),
    # 機器狀態
    ("獲取清潔機器狀態詳情",("機器狀態", "status")),
    ("獲取指定機器人狀態",  ("機器狀態", "status")),
    ("獲取組中機器人狀態",  ("機器狀態", "status")),
    ("獲取當前機器執行任務狀態",("機器狀態","status")),
    ("獲取綁定的機器人組",  ("機器狀態", "status")),
    ("獲取機器人組中的機器人",("機器狀態","status")),
    # 機器人任務
    ("發起呼叫任務",    ("機器人任務",   "tasks")),
    ("取消呼叫任務",    ("機器人任務",   "tasks")),
    ("完成呼叫任務",    ("機器人任務",   "tasks")),
    ("發送自定義展示內容",("機器人任務", "tasks")),
    ("獲取呼叫列表",    ("機器人任務",   "tasks")),
    ("配送任務",        ("機器人任務",   "tasks")),
    ("配送指令",        ("機器人任務",   "tasks")),
    ("運送任務",        ("機器人任務",   "tasks")),
    ("運送指令",        ("機器人任務",   "tasks")),
    ("跑腿任務控制指令",("機器人任務",   "tasks")),
    ("跑腿任務",        ("機器人任務",   "tasks")),
    ("頂升任務控制指令",("機器人任務",   "tasks")),
    ("頂升任務",        ("機器人任務",   "tasks")),
    ("清潔任務列表",    ("機器人任務",   "tasks")),
    ("清潔指令",        ("機器人任務",   "tasks")),
    ("定時任務",        ("機器人任務",   "tasks")),
    ("給機器發送託盤推送任務",("機器人任務","tasks")),
    # 統計數據
    ("獲取廣告列表",    ("統計數據",     "analytics")),
]
# 其他未匹配的全部放「其他」
DEFAULT_CAT = ("其他", "others")


def slug(title: str) -> str:
    """把中文標題轉成安全的英文+數字檔名."""
    # 先保留英文、數字、連字號，中文字轉拼音用索引碼
    s = re.sub(r'[（）()【】\[\]《》<>「」『』、。，：:；;！!？?—~@#$%^&*+=/\\|`\'""\s]+', "_", title)
    s = s.strip("_")
    return s[:60] if s else "section"


def get_category(title: str):
    for kw, cat in CATEGORIES:
        if kw in title:
            return cat
    return DEFAULT_CAT


def split_markdown(src_path: str):
    with open(src_path, encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines(keepends=True)
    sections = []
    current_title = "首頁"
    current_lines = []

    for line in lines:
        m = re.match(r"^# (.+)", line)
        if m:
            if current_lines:
                sections.append((current_title, "".join(current_lines)))
            current_title = m.group(1).strip()
            current_lines = [line]
        else:
            current_lines.append(line)
    if current_lines:
        sections.append((current_title, "".join(current_lines)))

    return sections


def build_docs(sections):
    # 重建 docs 資料夾
    if os.path.exists(DOCS_DIR):
        shutil.rmtree(DOCS_DIR)
    os.makedirs(DOCS_DIR)

    # 類別 → [(title, rel_path, content)]
    cat_map: dict[str, list] = {}
    # 保留輸出到的目錄
    subdir_created = set()

    for title, body in sections:
        cat_name, subdir = get_category(title)
        full_dir = os.path.join(DOCS_DIR, subdir)
        if full_dir not in subdir_created:
            os.makedirs(full_dir, exist_ok=True)
            subdir_created.add(full_dir)

        fname = slug(title) + ".md"
        rel_path = f"{subdir}/{fname}"
        full_path = os.path.join(DOCS_DIR, rel_path)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(body)

        cat_map.setdefault(cat_name, []).append((title, rel_path))

    return cat_map


def build_nav(cat_map: dict):
    # 控制分類順序
    order = ["開發指南", "回調通知", "通用接口", "機器狀態", "機器人任務", "統計數據", "附錄", "其他"]
    nav = []
    for cat in order:
        if cat not in cat_map:
            continue
        items = cat_map[cat]
        nav.append({cat: [{title: path} for title, path in items]})
    return nav


def write_mkdocs_yml(nav):
    import yaml as _yaml

    config = {
        "site_name": "Pudu Cloud API 說明書",
        "site_description": "普渡雲開放平臺 API 技術文件",
        "docs_dir": "docs",
        "theme": {
            "name": "material",
            "language": "zh",
            "palette": [
                {
                    "scheme": "default",
                    "primary": "blue",
                    "accent": "blue",
                    "toggle": {"icon": "material/brightness-7", "name": "切換至深色模式"},
                },
                {
                    "scheme": "slate",
                    "primary": "blue",
                    "accent": "blue",
                    "toggle": {"icon": "material/brightness-4", "name": "切換至淺色模式"},
                },
            ],
            "features": [
                "navigation.tabs",
                "navigation.sections",
                "navigation.top",
                "search.highlight",
                "search.share",
                "content.code.copy",
            ],
        },
        "markdown_extensions": [
            {"pymdownx.highlight": {"anchor_linenums": True}},
            "pymdownx.superfences",
            {"pymdownx.tabbed": {"alternate_style": True}},
            "tables",
            {"toc": {"permalink": True}},
        ],
        "nav": nav,
    }

    with open(MKDOCS_YML, "w", encoding="utf-8") as f:
        _yaml.dump(config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"✅ 已生成 {MKDOCS_YML}")


if __name__ == "__main__":
    print("📖 讀取來源文件…")
    sections = split_markdown(SRC)
    print(f"   共 {len(sections)} 個章節")

    print("📁 切割成個別 .md 文件…")
    cat_map = build_docs(sections)
    for cat, items in cat_map.items():
        print(f"   [{cat}] {len(items)} 個頁面")

    print("⚙️  生成 mkdocs.yml…")
    nav = build_nav(cat_map)
    write_mkdocs_yml(nav)

    print()
    print("🚀 完成！執行以下指令啟動預覽：")
    print("   .venv\\Scripts\\mkdocs.exe serve")
