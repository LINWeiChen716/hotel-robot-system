# -*- coding: utf-8 -*-
"""
普渡開放 API 完整定義（102 個端點）
從 Next.js 專案 lib/pudu/doc-endpoints.ts 轉換
"""

from urllib.parse import parse_qsl

COMMON_APIS = {
    "【數據查詢】": [
        {
            "id": "shop_list",
            "name": "獲取門店列表",
            "path": "/data-open-platform-service/v1/api/shop",
            "method": "GET",
            "description": "獲取門店列表",
            "required_params": {},
            "optional_params": {"limit": "查詢限制的數量（默認爲10）", "offset": "偏移量（默認爲0）"},
            "response_description": "門店列表，包含 shop_id, shop_name, company_id, company_name",
            "examples": {"query": "limit=100&offset=0"}
        },
        {
            "id": "robot_list",
            "name": "獲取機器列表",
            "path": "/data-open-platform-service/v1/api/robot",
            "method": "GET",
            "description": "獲取機器列表，返回機器mac、sn、產品類型等信息。若需指定 shop_id，請到設定頁的商店設定查看 Pudu Shop ID。",
            "required_params": {},
            "optional_params": {"limit": "查詢限制的數量", "offset": "偏移量", "shop_id": "門店ID（請到設定頁商店設定查看 Pudu Shop ID）"},
            "response_description": "機器列表，包含 sn, product_line, mac 等",
            "examples": {"query": "limit=100&offset=0"}
        },
        {
            "id": "map_list",
            "name": "獲取地圖列表",
            "path": "/data-open-platform-service/v1/api/maps",
            "method": "GET",
            "description": "獲取門店可用地圖列表。shop_id 請到設定頁的商店設定查看 Pudu Shop ID。",
            "required_params": {},
            "optional_params": {"shop_id": "門店ID（請到設定頁商店設定查看 Pudu Shop ID）"},
            "response_description": "地圖列表",
            "examples": {"query": "shop_id=408250001"}
        },
    ],

    "【機器狀態】": [
        {
            "id": "status_by_sn_v1",
            "name": "獲取機器狀態 V1（按SN）",
            "path": "/open-platform-service/v1/status/get_by_sn",
            "method": "GET",
            "description": "根據機器SN號獲取機器實時狀態",
            "required_params": {"sn": "機器序列號"},
            "optional_params": {},
            "response_description": "機器狀態信息：電量、在線狀態、位置等",
            "examples": {"query": "sn=PD123456"}
        },
        {
            "id": "status_by_group_id_v1",
            "name": "獲取組狀態 V1（按Group ID）",
            "path": "/open-platform-service/v1/status/get_by_group_id",
            "method": "GET",
            "description": "根據機器組ID獲取組內所有機器的狀態(回傳設備名稱用為mac值)。",
            "required_params": {"group_id": "機器組ID"},
            "optional_params": {},
            "response_description": "組內所有機器的狀態列表（V1格式）",
            "examples": {"query": "group_id=1"}
        },
        {
            "id": "status_by_sn_v2",
            "name": "獲取機器狀態 V2（按SN）",
            "path": "/open-platform-service/v2/status/get_by_sn",
            "method": "GET",
            "description": "根據機器SN號獲取機器實時狀態（V2版本）",
            "required_params": {"sn": "機器序列號"},
            "optional_params": {},
            "response_description": "機器狀態信息（V2格式）",
            "examples": {"query": "sn=PD123456"}
        },
        {
            "id": "status_by_group_id_v2",
            "name": "獲取組狀態 V2（按Group ID）",
            "path": "/open-platform-service/v2/status/get_by_group_id",
            "method": "GET",
            "description": "根據機器組ID獲取組內所有機器的狀態（V2版本）。",
            "required_params": {"group_id": "機器組ID"},
            "optional_params": {},
            "response_description": "組內所有機器的狀態列表（V2格式）",
            "examples": {"query": "group_id=1"}
        },
        {
            "id": "robot_task_state",
            "name": "獲取機器任務狀態",
            "path": "/open-platform-service/v1/robot/task/state/get",
            "method": "GET",
            "description": "獲取機器當前執行任務的狀態",
            "required_params": {"sn": "機器序列號"},
            "optional_params": {},
            "response_description": "任務狀態信息",
            "examples": {"query": "sn=PD123456"}
        },
        {
            "id": "cleanbot_detail",
            "name": "獲取清潔機器狀態詳情",
            "path": "/cleanbot-service/v1/api/open/robot/detail",
            "method": "GET",
            "description": "獲取清潔機器的詳細狀態信息",
            "required_params": {"sn": "機器序列號"},
            "optional_params": {},
            "response_description": "清潔機器詳細狀態",
            "examples": {"query": "sn=CB123456"}
        },
    ],

    "【地圖與位置】": [
        {
            "id": "map_current",
            "name": "機器當前使用地圖",
            "path": "/map-service/v1/open/current",
            "method": "GET",
            "description": "獲取機器當前使用的地圖",
            "required_params": {"sn": "機器序列號"},
            "optional_params": {},
            "response_description": "當前地圖信息",
            "examples": {"query": "sn=PD123456"}
        },
        {
            "id": "map_list_by_robot",
            "name": "獲取機器可用地圖列表",
            "path": "/map-service/v1/open/list",
            "method": "GET",
            "description": "獲取機器可用的地圖列表",
            "required_params": {"sn": "機器序列號"},
            "optional_params": {},
            "response_description": "可用地圖列表",
            "examples": {"query": "sn=PD123456"}
        },
        {
            "id": "map_detail_v1",
            "name": "獲取地圖詳情 V1",
            "path": "/map-service/v1/open/map",
            "method": "GET",
            "description": "獲取地圖詳細信息和元素點位（路徑為 map-service/v1/open/map）",
            "required_params": {"shop_id": "門店ID", "map_name": "地圖名稱"},
            "optional_params": {},
            "response_description": "地圖詳細信息，包含元素點位、線路等",
            "examples": {"query": "shop_id=1&map_name=map1"}
        },
        {
            "id": "robot_position",
            "name": "獲取機器實時位置",
            "path": "/open-platform-service/v1/robot/get_position",
            "method": "GET",
            "description": "獲取機器在地圖上的實時位置坐標",
            "required_params": {"sn": "機器序列號"},
            "optional_params": {},
            "response_description": "機器位置坐標 (x, y)",
            "examples": {"query": "sn=PD123456"}
        },
        {
            "id": "map_points",
            "name": "獲取地圖點位列表",
            "path": "/map-service/v1/open/point",
            "method": "GET",
            "description": "獲取地圖上的所有點位信息",
            "required_params": {"sn": "機器序列號"},
            "optional_params": {"limit": "查詢數量上限", "offset": "偏移量"},
            "response_description": "點位列表，包含坐標、名稱等",
            "examples": {"query": "sn=PD123456"}
        },
        {
            "id": "map_group",
            "name": "獲取點位分組",
            "path": "/map-service/v1/open/group",
            "method": "POST",
            "description": "獲取地圖上的點位分組信息",
            "supported_robots": ["All"],
            "required_params": {"sn": "機器序列號", "map_name": "地圖名稱"},
            "optional_params": {},
            "response_description": "點位分組列表",
            "examples": {"body": {"sn": "PD123456", "map_name": "map1"}}
        },
        {
            "id": "switch_map",
            "name": "切換機器地圖",
            "path": "/open-platform-service/v1/switch_map",
            "method": "POST",
            "description": "切換機器使用的地圖（PuduT300）。map_info 為地圖信息對象。map_name 請從設定頁地圖分頁取得。切換前請讓機器人在地圖對位點再切換，避免切圖後機器人點位偏移。",
            "required_params": {
                "sn": "機器序列號",
                "map_info.map_name": "地圖名稱"
            },
            "optional_params": {},
            "response_description": "切換結果（切換完成通過 notifySwitchMap 回調）",
            "examples": {"body": {"sn": "PD123456", "map_info": {"map_name": "1#1#地圖"}}},
            "callback_example": {
                "callback_type": "notifySwitchMap",
                "data": {
                    "sn": "PD123456",
                    "task_id": "switch_map_task_001",
                    "map_name": "1#1#地圖",
                    "state": "SUCCESS",
                    "message": "switch map finished"
                }
            }
        },
        {
            "id": "switch_map_in_elevator",
            "name": "電梯內切換地圖",
            "path": "/open-platform-service/v1/robot/map/switch_in_elevator",
            "method": "POST",
            "description": "在電梯內切換機器使用的地圖",
            "required_params": {"sn": "機器序列號", "map_name": "地圖名稱"},
            "optional_params": {},
            "response_description": "切換結果",
            "examples": {"body": {"sn": "PD123456", "map_name": "map2"}}
        },
    ],

    "【呼叫與配送】": [
        {
            "id": "custom_call",
            "name": "發起呼叫任務",
            "path": "/open-platform-service/v1/custom_call",
            "method": "POST",
            "description": "向機器發起呼叫任務，可指定或隨機呼叫空閒機器到指定點位。sn 與 shop_id 必須擇一傳入。請先選 call_mode 呼叫模式，頁面會自動提示該模式需要填的欄位。",
            "required_params": {
                "map_name": "地圖名稱",
                "point": "目標點位名稱",
                "point_type": "點位類型（如 table）"
            },
            "optional_params": {
                "sn": "指定機器序列號（與 shop_id 擇一）",
                "shop_id": "門店ID（不指定 sn 時隨機呼叫空閒機器）",
                "call_mode": "呼叫模式（空=到達結束, CALL=到達結束, IMG=圖片, QR_CODE=二維碼, VIDEO=影片, CALL_CONFIRM=確認模式）",
                "do_not_queue": "true=無法執行時直接失敗不排隊"
            },
            "type_field_name": "call_mode",
            "type_label": "呼叫模式 (call_mode)",
            "type_options": {
                "": "普通呼叫（到達即結束）",
                "CALL": "CALL 模式（到達即結束）",
                "IMG": "圖片模式",
                "QR_CODE": "支付二維碼模式",
                "VIDEO": "影片模式",
                "CALL_CONFIRM": "呼叫抵達確認模式"
            },
            "type_param_rules": {
                "by_type": {
                    "IMG": {
                        "required_params": {
                            "mode_data.urls": "圖片URL列表（Array<string>）"
                        },
                        "optional_params": {
                            "mode_data.switch_time": "圖片切換間隔秒數",
                            "mode_data.cancel_btn_time": "取消按鈕顯示時間(秒)",
                            "mode_data.show_timeout": "內容顯示超時時間(秒)"
                        }
                    },
                    "QR_CODE": {
                        "required_params": {
                            "mode_data.qrcode": "二維碼內容"
                        },
                        "optional_params": {
                            "mode_data.text": "二維碼模式下的文本",
                            "mode_data.cancel_btn_time": "取消按鈕顯示時間(秒)",
                            "mode_data.show_timeout": "內容顯示超時時間(秒)"
                        }
                    },
                    "VIDEO": {
                        "required_params": {
                            "mode_data.urls": "影片URL列表（Array<string>）"
                        },
                        "optional_params": {
                            "mode_data.play_count": "影片播放輪詢次數",
                            "mode_data.cancel_btn_time": "取消按鈕顯示時間(秒)",
                            "mode_data.show_timeout": "內容顯示超時時間(秒)"
                        }
                    },
                    "CALL_CONFIRM": {
                        "optional_params": {
                            "mode_data.cancel_btn_time": "取消按鈕顯示時間(秒)",
                            "mode_data.show_timeout": "內容顯示超時時間(秒)"
                        }
                    }
                }
            },
            "response_description": "task_id（用於後續取消/完成任務）",
            "examples": {"body": {"sn": "PD123456", "map_name": "1#1#地圖", "point": "A1", "point_type": "table", "call_mode": ""}}
        },
        {
            "id": "custom_call_cancel",
            "name": "取消呼叫任務",
            "path": "/open-platform-service/v1/custom_call/cancel",
            "method": "POST",
            "description": "取消指定的自定義呼叫任務。task_id 與 sn 至少擇一傳入。",
            "required_params": {},
            "optional_params": {
                "task_id": "呼叫任務ID（發起呼叫時返回）",
                "sn": "機器序列號（不傳 task_id 時取消該機器所有未完成任務）",
                "is_auto_back": "取消後是否自動返航（true/false）"
            },
            "response_description": "取消結果",
            "examples": {"body": {"task_id": "task123", "is_auto_back": False}}
        },
        {
            "id": "custom_call_complete",
            "name": "完成呼叫任務",
            "path": "/open-platform-service/v1/custom_call/complete",
            "method": "POST",
            "description": "當呼叫任務非自動完成模式時，調用此接口提前完成任務，並可選擇執行下一個任務。",
            "required_params": {"task_id": "呼叫任務ID"},
            "optional_params": {
                "next_call_task.map_name": "接續任務的地圖名稱",
                "next_call_task.point": "接續任務的目標點位",
                "next_call_task.point_type": "接續任務的點位類型",
                "next_call_task.call_mode": "接續任務的呼叫模式",
                "next_call_task.mode_data": "接續任務附加內容（含 urls/qrcode/text/cancel_btn_time/show_timeout 等，依 call_mode 決定）"
            },
            "response_description": "完成結果",
            "examples": {"body": {"task_id": "task123"}}
        },
        {
            "id": "custom_content",
            "name": "發送自定義展示內容",
            "path": "/open-platform-service/v1/custom_content",
            "method": "POST",
            "description": "向機器發送自定義展示內容（需攜帶 payload 與 payload.mode_data）。",
            "required_params": {
                "sn": "機器序列號",
                "payload": "自定義內容參數",
                "payload.task_id": "自定義呼叫任務ID",
                "payload.call_mode": "展示模式（IMG/QR_CODE/VIDEO/CALL_CONFIRM/CALL）"
            },
            "optional_params": {
                "payload.mode_data": "模式內容資料",
                "payload.mode_data.urls": "圖片/影片網址陣列",
                "payload.mode_data.qrcode": "二維碼內容",
                "payload.mode_data.text": "二維碼文字",
                "payload.mode_data.play_count": "影片播放輪次",
                "payload.mode_data.switch_time": "圖片切換秒數",
                "payload.mode_data.cancel_btn_time": "取消按鈕顯示秒數",
                "payload.mode_data.show_timeout": "內容顯示超時秒數"
            },
            "response_description": "發送結果",
            "examples": {"body": {"sn": "PD123456", "payload": {"task_id": "task123", "call_mode": "IMG", "mode_data": {"urls": ["https://example.com/a.jpg"], "switch_time": 5}}}}
        },
        {
            "id": "call_list",
            "name": "獲取呼叫列表",
            "path": "/open-platform-service/v1/call/list",
            "method": "GET",
            "description": "獲取呼叫任務列表",
            "required_params": {"sn": "機器序列號"},
            "optional_params": {"limit": "數量限制"},
            "response_description": "呼叫任務列表",
            "examples": {"query": "sn=PD123456&limit=10"}
        },
        {
            "id": "delivery_task",
            "name": "發起配送任務",
            "path": "/open-platform-service/v1/delivery_task",
            "method": "POST",
            "description": "向機器發起配送任務，支持多託盤與多目的地。payload.trays 是託盤列表；每個 trays[i].destinations 可放多個送達目標。",
            "required_params": {
                "sn": "機器序列號",
                "payload.type": "任務類型（NEW=新任務, MODIFY=修改任務）",
                "payload.delivery_sort": "配送排序（AUTO=距離最近, FIXED=按順序）",
                "payload.execute_task": "是否立即執行（true/false）",
                "payload.trays": "託盤列表（Array<object>）",
                "payload.trays[].destinations": "每層託盤目的地列表（Array<object>）",
                "payload.trays[].destinations[].destination": "配送目標點位名稱（舊字段 points）",
                "payload.trays[].destinations[].id": "訂單ID（可選回傳對應）"
            },
            "optional_params": {
                "payload.trays[].destinations[].phone_num": "收件人電話",
                "payload.trays[].destinations[].phone_code": "電話區號",
                "payload.trays[].destinations[].map_info": "跨地圖時的地圖信息（object，如 map_name/map_code）"
            },
            "response_description": "任務ID",
            "examples": {"body": {"sn": "PD123456", "payload": {"type": "NEW", "delivery_sort": "AUTO", "execute_task": True, "trays": [{"destinations": [{"destination": "A1", "id": "order001"}]}]}}}
        },
        {
            "id": "delivery_action",
            "name": "配送指令",
            "path": "/open-platform-service/v1/delivery_action",
            "method": "POST",
            "description": "向機器發送配送任務操作指令（開始/完成/取消）。",
            "required_params": {
                "sn": "機器序列號",
                "payload.action": "操作指令：START（開始配送，需在配送任務界面）、COMPLETE（完成任務，需在到達界面）、CANCEL_ALL_DELIVERY（取消所有配送任務）"
            },
            "optional_params": {},
            "action_options": {
                "START": "開始配送任務（在配送任務界面時生效）",
                "COMPLETE": "完成配送任務（抵達後顯示抵達界面時生效）",
                "CANCEL_ALL_DELIVERY": "取消所有配送任務"
            },
            "action_field_name": "payload.action",
            "response_description": "指令執行結果",
            "examples": {"body": {"sn": "PD123456", "payload": {"action": "START"}}}
        },
        {
            "id": "cancel_task",
            "name": "取消任務（舊版）",
            "path": "/open-platform-service/v1/cancel_task",
            "method": "POST",
            "description": "取消正在執行的任務（舊版接口，僅支援 Flashbot）。payload.tasks 為任務陣列，每項含 name（目標點）和 type（類型）。",
            "required_params": {
                "sn": "機器序列號",
                "payload.tasks": "任務列表（Array<{name: 目標點, type: 類型}>）"
            },
            "optional_params": {},
            "response_description": "取消結果",
            "examples": {"body": {"sn": "PD123456", "payload": {"tasks": [{"name": "table1", "type": "delivery"}]}}}
        },
    ],

    "【運送與託盤】": [
        {
            "id": "transport_task",
            "name": "發起運送任務",
            "path": "/open-platform-service/v1/transport_task",
            "method": "POST",
            "description": "向機器發起運送任務（PuduBot2），可帶出發點、優先級、超時、擴展字段與多託盤目標；狀態可透過配送任務回調追蹤。",
            "required_params": {
                "sn": "機器序列號",
                "payload.task_id": "任務ID（自訂唯一字串）",
                "payload.type": "任務類型（NEW=新任務, MODIFY=修改任務）",
                "payload.delivery_sort": "配送排序（AUTO=距離最近, FIXED=按順序）",
                "payload.execute_task": "是否立即執行（true/false）",
                "payload.start_point": "起始點信息（destination/content_type/content_data）",
                "payload.trays": "託盤列表（Array<object>）",
                "payload.trays[].destinations": "運送目標列表（Array<object>）"
            },
            "optional_params": {
                "payload.priority": "優先級(0-10，越小越優先)",
                "payload.start_point.destination": "起始點名稱",
                "payload.start_point.content_type": "起始點內容類型（IMG/QR_CODE/VIDEO/TEXT）",
                "payload.start_point.content_data": "起始點展示內容（配合 content_type）",
                "payload.task_remark": "任務說明",
                "payload.extend1": "擴展字段1",
                "payload.extend2": "擴展字段2",
                "payload.extend3": "擴展字段3",
                "payload.trays[].destinations[].id": "運送目標ID",
                "payload.trays[].destinations[].name": "物品名稱",
                "payload.trays[].destinations[].points": "目標點位",
                "payload.trays[].destinations[].amount": "數量",
                "payload.trays[].destinations[].content_type": "內容類型（IMG/QR_CODE/VIDEO/TEXT）",
                "payload.trays[].destinations[].content_data": "內容數據",
                "payload.trays[].destinations[].tray_index": "託盤編號（從1開始）"
            },
            "response_description": "任務ID",
            "examples": {"body": {"sn": "PD123456", "payload": {"task_id": "t001", "type": "NEW", "delivery_sort": "AUTO", "execute_task": True, "trays": [{"destinations": [{"id": "d001", "name": "物品A", "points": "A1", "amount": 1}]}]}}}
        },
        {
            "id": "transport_action",
            "name": "運送指令",
            "path": "/open-platform-service/v1/transport_action",
            "method": "POST",
            "description": "向機器發送運送任務操作指令（開始/完成/取消）。",
            "required_params": {
                "sn": "機器序列號",
                "payload.action": "操作指令：START（開始運送，需在任務界面）、COMPLETE（完成任務，需在到達界面）、CANCEL_ALL_DELIVERY（取消所有運送任務）"
            },
            "optional_params": {},
            "action_options": {
                "START": "開始運送任務（在任務界面時生效）",
                "COMPLETE": "完成運送任務（抵達後顯示抵達界面時生效）",
                "CANCEL_ALL_DELIVERY": "取消所有運送任務"
            },
            "action_field_name": "payload.action",
            "response_description": "指令執行結果",
            "examples": {"body": {"sn": "PD123456", "payload": {"action": "START"}}}
        },
        {
            "id": "tray_order",
            "name": "託盤推送任務（舊版）",
            "path": "/open-platform-service/v1/tray_order",
            "method": "POST",
            "description": "向機器託盤推送訂單（舊版接口，僅支援 Flashbot）。payload.orders 為訂單陣列。",
            "required_params": {
                "sn": "機器序列號",
                "payload.orders": "訂單列表（Array<{id,name,table_name,table_no,amount}>）"
            },
            "optional_params": {
                "payload.tray_index": "指定第幾層託盤（0=不指定）"
            },
            "response_description": "任務ID",
            "examples": {"body": {"sn": "PD123456", "payload": {"orders": [{"id": "o001", "name": "炒飯", "table_name": "A1", "table_no": "1", "amount": 1}]}}}
        },
        {
            "id": "task_errand",
            "name": "發起跑腿任務",
            "path": "/open-platform-service/v1/task_errand",
            "method": "POST",
            "description": "向機器發起跑腿任務（FlashBot 系列）。payload.tasks 為子任務陣列，每個子任務含 point_list（2個點位：放貨點+取貨點）。",
            "required_params": {
                "sn": "機器序列號",
                "payload.tasks": "子任務列表（Array<object>，含 task_name/task_desc/point_list）",
                "payload.tasks[].task_name": "子任務名稱（回調會回傳）",
                "payload.tasks[].task_desc": "子任務描述",
                "payload.tasks[].point_list": "點位集合（目前固定2個：放貨點+取貨點）",
                "payload.tasks[].point_list[].map_name": "地圖名稱",
                "payload.tasks[].point_list[].point": "點位ID或點位名稱",
                "payload.tasks[].point_list[].point_type": "點位類型（如 table）"
            },
            "optional_params": {
                "payload.auth": "任務下發授權信息（刷卡卡號或密碼）",
                "payload.back_mode": "返回模式：UNSPECIFIED（沿用機器端設定）、RETURN（無人取物時返航）、BACK_START（多個無人取物逐個返回放物點）",
                "payload.tasks[].hatch_id": "艙門ID"
            },
            "response_description": "session_id（總任務ID）",
            "examples": {"body": {"sn": "PD123456", "payload": {"tasks": [{"task_name": "任務1", "task_desc": "描述", "point_list": [{"map_name": "map1", "point": "A1", "point_type": "table"}, {"map_name": "map1", "point": "B1", "point_type": "table"}]}]}}}
        },
        {
            "id": "errand_action",
            "name": "跑腿任務指令",
            "path": "/open-platform-service/v1/errand_action",
            "method": "POST",
            "description": "向機器發送跑腿任務操作指令（取消/重試）。",
            "required_params": {
                "sn": "機器序列號",
                "payload.action": "操作類型（CANCEL=取消, RETRY=重新配送）",
                "payload.session_id": "總任務ID（下發跑腿任務時機器返回的）"
            },
            "optional_params": {
                "payload.auth": "授權信息（如刷卡卡號、密碼）",
                "payload.hatch_id": "艙門ID"
            },
            "action_options": {
                "CANCEL": "取消配送任務",
                "RETRY": "重新配送"
            },
            "action_field_name": "payload.action",
            "response_description": "指令執行結果",
            "examples": {"body": {"sn": "PD123456", "payload": {"action": "CANCEL", "session_id": "sess123"}}}
        },
        {
            "id": "lifting_task",
            "name": "發起頂升任務",
            "path": "/open-platform-service/v1/lifting_task",
            "method": "POST",
            "description": "向機器發起頂升任務（PuduT300）。payload.tasks 為子任務陣列，每個子任務含 point_list（含取貨點 LIFT_POINT 和放貨點 DROP_POINT）。",
            "required_params": {
                "sn": "機器序列號",
                "payload.type": "配送方式（DISTINCE=最近排序, DEFAULT=按順序）",
                "payload.tasks": "頂升子任務列表（Array<object>）",
                "payload.tasks[].point_list": "點位集合（含取貨點/放貨點，可含逗留點）",
                "payload.tasks[].point_list[].point_name": "點位名稱",
                "payload.tasks[].point_list[].point_type": "點位類型（POINT/SECONDARY_GROUP）",
                "payload.tasks[].point_list[].point_attr": "點位屬性（LIFT_POINT/DROP_POINT/STAY_POINT）",
                "payload.tasks[].point_list[].map_info": "地圖信息（map_name 必填，map_code 選填）"
            },
            "optional_params": {
                "payload.tasks[].point_list[].fail_action.action": "失敗動作（STAY/RETRY/SKIP/GO_BACK_LIFT_POINT/SPEC_POINT）",
                "payload.tasks[].point_list[].fail_action.data": "當 action=SPEC_POINT 時，指定前往目標點資料（含 map_info/point_name/point_type/point_attr）"
            },
            "response_description": "任務ID",
            "examples": {"body": {"sn": "PD123456", "payload": {"type": "DEFAULT", "tasks": [{"point_list": [{"point_name": "廚房", "point_type": "POINT", "point_attr": "LIFT_POINT", "map_info": {"map_name": "map1"}}, {"point_name": "A1", "point_type": "POINT", "point_attr": "DROP_POINT", "map_info": {"map_name": "map1"}}]}]}}}
        },
        {
            "id": "lifting_action",
            "name": "頂升任務指令",
            "path": "/open-platform-service/v1/lifting_action",
            "method": "POST",
            "description": "向機器發送頂升任務操作指令。",
            "required_params": {
                "sn": "機器序列號",
                "task_id": "任務ID（下發任務時機器返回）",
                "action": "操作類型（PAUSE/RESUME/FINISH_ONE/CANCEL_ALL_LIFTIONG）"
            },
            "optional_params": {},
            "action_options": {
                "PAUSE": "暫停任務",
                "RESUME": "恢復任務",
                "FINISH_ONE": "使機器在途徑點結束逗留",
                "CANCEL_ALL_LIFTIONG": "取消所有頂升任務"
            },
            "action_field_name": "action",
            "response_description": "指令執行結果",
            "examples": {"body": {"sn": "PD123456", "task_id": "task123", "action": "PAUSE"}}
        },
    ],

    "【巡航】": [
        {
            "id": "cruise_task",
            "name": "發起巡航任務",
            "path": "/open-platform-service/v1/cruise_task",
            "method": "POST",
            "description": "發起巡航任務（依你指定格式）。",
            "required_params": {"sn": "機器序列號", "task_id": "巡航任務ID", "action": "巡航動作"},
            "optional_params": {},
            "response_description": "任務ID",
            "examples": {"body": {"sn": "PD123456", "task_id": "cruise001", "action": "start"}}
        },
        {
            "id": "cruise_action",
            "name": "巡航控制指令",
            "path": "/open-platform-service/v1/cruise_action",
            "method": "POST",
            "description": "發送巡航任務控制指令（暫停/恢復/取消）。",
            "required_params": {"sn": "機器序列號", "task_id": "任務ID", "action": "動作（pause/resume/cancel 等）"},
            "optional_params": {},
            "response_description": "指令執行結果",
            "examples": {"body": {"sn": "PD123456", "task_id": "task123", "action": "stop"}}
        },
        {
            "id": "get_cruise_line",
            "name": "獲取巡航路徑",
            "path": "/open-platform-service/v1/get_cruise_line",
            "method": "GET",
            "description": "獲取機器可用的巡航路徑列表",
            "required_params": {"sn": "機器序列號"},
            "optional_params": {},
            "response_description": "巡航路徑列表",
            "examples": {"query": "sn=PD123456"}
        },
    ],

    "【清潔】": [
        {
            "id": "cleanbot_task_list",
            "name": "清潔任務列表",
            "path": "/cleanbot-service/v1/api/open/task/list",
            "method": "GET",
            "description": "獲取清潔機器可用任務列表與配置詳情。sn 與 shop_id 二選一即可。",
            "required_params": {},
            "optional_params": {
                "sn": "機器 SN（與 shop_id 二選一）",
                "shop_id": "門店 ID（與 sn 二選一）",
                "mode": "任務類型陣列（Array<int>，1=手動任務, 2=自動任務, 3=巡檢/混合任務；不傳預設2）",
                "product": "產品類型陣列（Array<string>，可傳 cleanbot/mt1/mt1Pro/mt1Max；不傳預設cleanbot）",
                "collaborative": "協同任務（1=先掃後洗，不傳則不生效）"
            },
            "response_description": "清潔任務列表",
            "examples": {"query": "sn=CB123456&mode=2&product=cleanbot"}
        },
        {
            "id": "cleanbot_task_exec",
            "name": "清潔任務指令",
            "path": "/cleanbot-service/v1/api/open/task/exec",
            "method": "POST",
            "description": "下發清潔機器任務/動作指令。請先選 type（任務類型），頁面會自動提示該類型需要填的欄位。",
            "required_params": {
                "sn": "機器序列號",
                "type": "任務類型（1充電, 2加排水, 3清掃, 4補給, 5一鍵返航, 6回返航點, 9切地圖, 10定時任務開關）",
                "clean.status": "任務狀態（1開始, 3暫停, 4取消）"
            },
            "optional_params": {},
            "type_label": "清潔任務 type",
            "type_hint": "提示：不同 type 只有對應欄位才生效。type=3 需先用「清潔任務列表」查到 clean.task_id 與 version；type=10 需先查 cron_id。",
            "type_options": {
                "1": "充電任務",
                "2": "加排水任務",
                "3": "清掃任務",
                "4": "補給任務（充電+換水）",
                "5": "一鍵返航",
                "6": "回返航點",
                "9": "切換地圖",
                "10": "控制定時任務開關"
            },
            "type_param_rules": {
                "by_type": {
                    "1": {
                        "example_body": {
                            "sn": "CB123456",
                            "type": 1,
                            "clean": {
                                "status": 1,
                                "point_id": "charge-point-01"
                            }
                        },
                        "optional_params": {
                            "clean.point_id": "指定充電點位（可省略，省略時機器自選）"
                        }
                    },
                    "2": {
                        "example_body": {
                            "sn": "CB123456",
                            "type": 2,
                            "clean": {
                                "status": 1,
                                "point_id": "water-point-01"
                            }
                        },
                        "optional_params": {
                            "clean.point_id": "指定加排水點位（可省略，省略時機器自選）"
                        }
                    },
                    "3": {
                        "example_body": {
                            "sn": "CB123456",
                            "type": 3,
                            "clean": {
                                "status": 1,
                                "name": "日常清掃",
                                "task_id": "task123",
                                "version": 1.0,
                                "cleanagent_scale": 50
                            }
                        },
                        "required_params": {
                            "clean.name": "清掃任務名稱",
                            "clean.task_id": "清掃任務ID（可先用「清潔任務列表」查詢）",
                            "clean.version": "任務版本"
                        },
                        "optional_params": {
                            "clean.cleanagent_scale": "清潔劑比例（例如 50 代表 1:50）"
                        }
                    },
                    "4": {
                        "example_body": {
                            "sn": "CB123456",
                            "type": 4,
                            "clean": {
                                "status": 1,
                                "point_id": "supply-point-01"
                            }
                        },
                        "optional_params": {
                            "clean.point_id": "指定補給點位（可省略，省略時機器自選）"
                        }
                    },
                    "5": {
                        "example_body": {
                            "sn": "CB123456",
                            "type": 5,
                            "clean": {
                                "status": 1
                            }
                        }
                    },
                    "6": {
                        "example_body": {
                            "sn": "CB123456",
                            "type": 6,
                            "clean": {
                                "status": 1,
                                "point_id": "dock-point-01"
                            }
                        },
                        "optional_params": {
                            "clean.point_id": "指定返航點位（可省略，省略時機器自選）"
                        }
                    },
                    "9": {
                        "example_body": {
                            "sn": "CB123456",
                            "type": 9,
                            "clean": {
                                "status": 1,
                                "map_name": "1#7#內湖展間清潔v4"
                            }
                        },
                        "required_params": {
                            "clean.map_name": "要切換的地圖名稱"
                        }
                    },
                    "10": {
                        "example_body": {
                            "sn": "CB123456",
                            "type": 10,
                            "clean": {
                                "status": 1,
                                "cron_id": "cron-123"
                            }
                        },
                        "required_params": {
                            "clean.cron_id": "定時任務ID（可先用「清潔定時任務列表」查詢）"
                        }
                    }
                }
            },
            "response_description": "執行結果",
            "examples": {
                "body": {
                    "sn": "CB123456",
                    "type": 3,
                    "clean": {
                        "status": 1,
                        "name": "日常清掃",
                        "task_id": "task123",
                        "version": 1.0
                    }
                }
            }
        },
        {
            "id": "cleanbot_cron_list",
            "name": "清潔定時任務列表",
            "path": "/cleanbot-service/v1/api/open/cron/list",
            "method": "GET",
            "description": "獲取清潔機器的定時任務列表",
            "required_params": {"sn": "機器序列號"},
            "optional_params": {},
            "response_description": "定時任務列表",
            "examples": {"query": "sn=CB123456"}
        },
    ],

    "【廣告管理】": [
        {
            "id": "gg_list",
            "name": "獲取廣告列表",
            "path": "/biz-service/openPlatform/api/v1/gg/list",
            "method": "POST",
            "description": "依門店與設備查詢廣告列表。",
            "required_params": {"shop_id": "門店ID", "sn": "機器 SN"},
            "optional_params": {"kind": "廣告類型（1普通場景 2高級場景 3小屏廣告）", "limit": "單頁條數", "offset": "偏移量（offset=page*limit）"},
            "response_description": "廣告列表",
            "examples": {"body": {"shop_id": "408250001", "sn": "8FF055923050007", "kind": "1", "limit": "10", "offset": "0"}}
        },
        {
            "id": "gg_get",
            "name": "獲取廣告詳情",
            "path": "/biz-service/openPlatform/api/v1/gg/get",
            "method": "GET",
            "description": "獲取單個廣告的詳細信息",
            "required_params": {"id": "廣告ID", "shop_id": "門店ID"},
            "optional_params": {},
            "response_description": "廣告詳情",
            "examples": {"query": "id=123&shop_id=408250001"}
        },
        {
            "id": "gg_create",
            "name": "新增廣告",
            "path": "/biz-service/openPlatform/api/v1/gg/create",
            "method": "POST",
            "description": "創建新廣告（請填完整請求參數）。",
            "required_params": {"name": "廣告名稱", "shop_id": "門店ID", "sn": "設備SN", "start_time": "開始時間戳（秒）", "end_time": "結束時間戳（秒）", "ad_list[].url": "資源URL"},
            "optional_params": {"ad_list": "媒資列表", "ad_list[].type": "0圖片 1影片", "ad_list[].md5": "文件MD5", "kind": "類型（1普通 2高級 3輕量）", "map_name": "地圖名稱", "map_point32s": "地圖點位集合", "media_type": "媒體類型（1圖片 2影片）", "scenes": "生效場景", "second": "輪播間隔秒", "show_type": "顯示類型（1單屏 3三屏）", "times": "播放輪次"},
            "response_description": "新廣告ID",
            "examples": {"body": {"name": "ad1", "shop_id": 408250001, "sn": "8FF055923050007", "start_time": "2026/03/01", "end_time": "2026/03/31", "ad_list": [{"url": "https://example.com/ad.jpg", "type": 0}]}}
        },
        {
            "id": "gg_update",
            "name": "更新廣告",
            "path": "/biz-service/openPlatform/api/v1/gg/update",
            "method": "POST",
            "description": "更新現有廣告（與新增相同參數結構，另含 id）。",
            "required_params": {"id": "廣告ID", "name": "廣告名稱", "shop_id": "門店ID", "sn": "設備SN", "start_time": "開始時間戳（秒）", "end_time": "結束時間戳（秒）", "ad_list[].url": "資源URL"},
            "optional_params": {"ad_list": "媒資列表", "ad_list[].type": "0圖片 1影片", "ad_list[].md5": "文件MD5", "kind": "類型（1普通 2高級 3輕量）", "map_name": "地圖名稱", "map_point32s": "地圖點位集合", "media_type": "媒體類型（1圖片 2影片）", "scenes": "生效場景", "second": "輪播間隔秒", "show_type": "顯示類型（1單屏 3三屏）", "times": "播放輪次"},
            "response_description": "更新結果",
            "examples": {"body": {"id": 123, "name": "ad_updated", "shop_id": 408250001, "sn": "8FF055923050007", "start_time": "2026/03/01", "end_time": "2026/03/31"}}
        },
        {
            "id": "gg_delete",
            "name": "刪除廣告",
            "path": "/biz-service/openPlatform/api/v1/gg/delete",
            "method": "POST",
            "description": "刪除廣告",
            "required_params": {"id": "廣告ID", "shop_id": "門店ID"},
            "optional_params": {},
            "response_description": "刪除結果",
            "examples": {"body": {"id": 123, "shop_id": 408250001}}
        },
        {
            "id": "gg_scenes_list",
            "name": "獲取廣告場景",
            "path": "/biz-service/openPlatform/api/v1/gg/scenesMenu/list",
            "method": "POST",
            "description": "獲取廣告展示場景列表（按菜單模式組織）。",
            "required_params": {"kind": "廣告種類（1普通場景 2高級場景 3小屏廣告）"},
            "optional_params": {"lang": "語系（預設中文）", "product_name": "產品名稱"},
            "response_description": "場景列表",
            "examples": {"body": {"kind": 1, "lang": "zh-CN", "product_name": "BellaBotPro"}}
        },
    ],

    "【機器人控制】": [
        {
            "id": "control_doors",
            "name": "艙門控制",
            "path": "/open-platform-service/v1/control_doors",
            "method": "POST",
            "description": "控制機器艙門開關（FlashBot 系列）。payload.control_states 為艙門控制列表，每項含 door_number 艙門編號和 operation（true=開啟, false=關閉）。",
            "required_params": {
                "sn": "機器序列號",
                "payload.control_states": "艙門控制列表（Array）",
                "payload.control_states[].door_number": "艙門編號（字串，例如 1/2/3/4）",
                "payload.control_states[].operation": "艙門操作（true=開啟, false=關閉）"
            },
            "optional_params": {},
            "response_description": "控制結果",
            "examples": {"body": {"sn": "PD123456", "payload": {"control_states": [{"door_number": "1", "operation": True}]}}}
        },
        {
            "id": "door_state",
            "name": "獲取門禁狀態",
            "path": "/open-platform-service/v1/door_state",
            "method": "GET",
            "description": "獲取機器門禁的當前狀態",
            "required_params": {"sn": "機器序列號"},
            "optional_params": {},
            "response_description": "門禁狀態（open/close）",
            "examples": {"query": "sn=PD123456"}
        },
        {
            "id": "robot_screen_set",
            "name": "設置機器屏幕（舊版）",
            "path": "/open-platform-service/v1/robot/screen/set",
            "method": "POST",
            "description": "設置機器屏幕顯示內容（舊版接口，僅支援 Flashbot）。",
            "required_params": {
                "sn": "機器序列號",
                "payload.info.content": "顯示內容（3-50字元）",
                "payload.info.show": "是否顯示（true 顯示, false 隱藏）"
            },
            "optional_params": {},
            "response_description": "設置結果",
            "examples": {"body": {"sn": "PD123456", "payload": {"info": {"content": "歡迎光臨！", "show": True}}}}
        },
        {
            "id": "position_command",
            "name": "通知機器上報位置",
            "path": "/open-platform-service/v1/position_command",
            "method": "POST",
            "description": "命令機器開始上報位置，可指定上報頻率與次數。機器會通過回調將位置推送到 notifyRobotPose 接口（需先在平臺填寫回調地址）。",
            "required_params": {
                "sn": "機器序列號",
                "payload.interval": "最小間隔時間(秒)，最小值為1秒",
                "payload.times": "連續推送次數，最大 1000 次"
            },
            "optional_params": {},
            "response_description": "命令執行結果（位置會通過回調將推送）",
            "examples": {"body": {"sn": "PD123456", "payload": {"interval": 2, "times": 10}}},
            "callback_example": {
                "callback_type": "notifyRobotPose",
                "data": {
                    "sn": "PD123456",
                    "x": 12.34,
                    "y": 56.78,
                    "yaw": 90.0,
                    "map_name": "1#1#地圖",
                    "timestamp": 1710000000
                }
            }
        },
    ],

    "【機器人組與列表】": [
        {
            "id": "robot_group_list",
            "name": "獲取機器人組列表",
            "path": "/open-platform-service/v1/robot/group/list",
            "method": "GET",
            "description": "獲取所有機器人組",
            "required_params": {"shop_id": "門店ID"},
            "optional_params": {"limit": "數量限制", "offset": "偏移量"},
            "response_description": "機器人組列表",
            "examples": {"query": "shop_id=408250001&limit=10"}
        },
        {
            "id": "robot_list_by_device_and_group",
            "name": "按組或設備類型列表機器",
            "path": "/open-platform-service/v1/robot/list_by_device_and_group",
            "method": "GET",
            "description": "按機器人組或設備類型查詢機器列表",
            "required_params": {},
            "optional_params": {"group_id": "組ID", "device_type": "設備類型"},
            "response_description": "機器列表",
            "examples": {"query": "group_id=1"}
        },
    ],

    "【聲音控制】": [
        {
            "id": "voice_list",
            "name": "獲取語音列表",
            "path": "/open-platform-service/v1/voice/list",
            "method": "GET",
            "description": "獲取指定機器人可用的語音列表（Kettybot）。【故障排除】若返回 CLOUD_OPEN_TIMEOUT 錯誤：先用『獲取機器狀態 V1』查詢該 SN 的 is_online 字段。若 is_online = -1 表示機器離線無法連接雲端；is_online = 1 表示機器在線，可重試；is_online = 0 表示機器已關閉。請確保機器已上線、連接到網絡並能正常通信。",
            "required_params": {"sn": "機器序列號"},
            "optional_params": {},
            "response_description": "語音列表",
            "examples": {"query": "sn=8PP044808050001"}
        },
        {
            "id": "voice_play",
            "name": "播放音頻",
            "path": "/open-platform-service/v1/voice/play",
            "method": "POST",
            "description": "控制機器播放指定音頻（Kettybot）。音頻名稱請先用「獲取音頻列表」查詢。",
            "required_params": {
                "sn": "機器序列號",
                "name": "音頻名稱（需對應音頻列表中的名稱）",
                "is_loop": "是否循環播放（true=循環, false=單次）"
            },
            "optional_params": {},
            "response_description": "播放結果",
            "examples": {"body": {"sn": "PD123456", "name": "welcome", "is_loop": False}}
        },
        {
            "id": "voice_action",
            "name": "播放控制指令",
            "path": "/open-platform-service/v1/voice/action",
            "method": "POST",
            "description": "對機器目前播放的音頻進行控制操作（Kettybot）。",
            "required_params": {
                "sn": "機器序列號",
                "action": "操作類型（PAUSE/RESUME/CANCEL）"
            },
            "optional_params": {},
            "action_options": {
                "PAUSE": "暫停播放",
                "RESUME": "恢復播放",
                "CANCEL": "取消播放"
            },
            "action_field_name": "action",
            "response_description": "指令執行結果",
            "examples": {"body": {"sn": "PD123456", "action": "PAUSE"}}
        },
        {
            "id": "volume_set",
            "name": "設置機器音量",
            "path": "/open-platform-service/v1/volume/set",
            "method": "POST",
            "description": "設置機器音量大小",
            "required_params": {"sn": "機器序列號", "volume": "音量（0-100）"},
            "optional_params": {},
            "response_description": "設置結果",
            "examples": {"body": {"sn": "PD123456", "volume": 50}}
        },
    ],

    "【充電】": [
        {
            "id": "recharge_v1",
            "name": "機器人一鍵回充 V1",
            "path": "/open-platform-service/v1/recharge",
            "method": "GET",
            "description": "讓機器執行自動回充命令",
            "required_params": {"sn": "機器序列號"},
            "optional_params": {},
            "response_description": "命令執行結果",
            "examples": {"query": "sn=PD123456"}
        },
        {
            "id": "recharge_v2",
            "name": "機器人一鍵回充 V2",
            "path": "/open-platform-service/v2/recharge",
            "method": "GET",
            "description": "讓機器執行自動回充命令（V2版本）。PuduBot2 回充請走 V1，V2 不適用。",
            "required_params": {"sn": "機器序列號"},
            "optional_params": {},
            "response_description": "命令執行結果",
            "examples": {"query": "sn=PD123456"}
        },
    ],

    "【其他功能】": [
        {
            "id": "robot_door_task_list",
            "name": "機器人門禁任務列表",
            "path": "/biz-open-service/v1/robotDoor/task_list",
            "method": "POST",
            "description": "獲取機器人門禁相關的任務列表",
            "required_params": {"sn": "機器序列號"},
            "optional_params": {},
            "response_description": "任務列表",
            "examples": {"body": {"sn": "PD123456"}}
        },
        {
            "id": "analysis_shop",
            "name": "門店數據分析",
            "path": "/data-board/v1/analysis/shop",
            "method": "GET",
            "description": "獲取門店級別的數據分析統計",
            "required_params": {"shop_id": "門店ID", "start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {},
            "response_description": "門店數據統計",
            "examples": {"query": "shop_id=1&start_date=2024-01-01&end_date=2024-01-31"}
        },
        {
            "id": "analysis_shop_paging",
            "name": "門店數據分析（分頁）",
            "path": "/data-board/v1/analysis/shop/paging",
            "method": "GET",
            "description": "跨門店的數據分析統計，支援分頁，不需指定 shop_id",
            "required_params": {"start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {"limit": "每頁筆數", "offset": "偏移量"},
            "response_description": "門店數據統計（分頁）",
            "examples": {"query": "start_date=2024-01-01&end_date=2024-01-31&limit=20&offset=0"}
        },
        {
            "id": "analysis_run",
            "name": "巡航數據分析",
            "path": "/data-board/v1/analysis/run",
            "method": "GET",
            "description": "獲取巡航相關的數據分析",
            "required_params": {"shop_id": "門店ID", "start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {},
            "response_description": "巡航數據統計",
            "examples": {"query": "shop_id=1&start_date=2024-01-01&end_date=2024-01-31"}
        },
        {
            "id": "analysis_run_paging",
            "name": "巡航數據分析（分頁）",
            "path": "/data-board/v1/analysis/run/paging",
            "method": "GET",
            "description": "跨門店的巡航數據分析，支援分頁，不需指定 shop_id",
            "required_params": {"start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {"limit": "每頁筆數", "offset": "偏移量"},
            "response_description": "巡航數據統計（分頁）",
            "examples": {"query": "start_date=2024-01-01&end_date=2024-01-31&limit=20&offset=0"}
        },
        {
            "id": "analysis_clean_detail",
            "name": "清潔詳細數據分析",
            "path": "/data-board/v1/analysis/clean/detail",
            "method": "GET",
            "description": "獲取清潔任務的詳細數據分析",
            "required_params": {"start_time": "開始時間戳(s)" , "end_time": "結束時間戳(s)"},
            "optional_params": {
                "shop_id": "門店ID過濾",
                "timezone_offset": "時區偏移小時，範圍 -12 ~ 14",
                "time_unit": "時間單位：day | hour",
                "group_by": "分組維度（例如 day/hour/product_code）",
                "clean_mode": "清潔模式過濾（0全部，1洗地，2掃地）",
                "sub_mode": "子模式過濾（-1全部，0自定義、1地毯吸塵、3靜音塵推）"
            },
            "response_description": "清潔任務詳細數據",
            "examples": {"query": "start_time=1704067200&end_time=1706745599&shop_id=1&timezone_offset=8&time_unit=day&clean_mode=0&sub_mode=-1"}
        },
        {
            "id": "analysis_clean_mode",
            "name": "清潔模式分析",
            "path": "/data-board/v1/analysis/clean/mode",
            "method": "GET",
            "description": "獲取清潔機器的模式分析數據",
            "required_params": {"start_time": "開始時間戳(s)", "end_time": "結束時間戳(s)"},
            "optional_params": {
                "shop_id": "門店ID過濾",
                "timezone_offset": "時區偏移小時，範圍 -12 ~ 14",
                "time_unit": "時間單位：day | hour",
                "group_by": "分組維度（例如 day/hour/product_code）",
                "clean_mode": "清潔模式過濾（0全部，1洗地，2掃地）",
                "sub_mode": "子模式過濾（-1全部，0自定義、1地毯吸塵、3靜音塵推）"
            },
            "response_description": "清潔模式分析數據",
            "examples": {"query": "start_time=1704067200&end_time=1706745599&shop_id=1&timezone_offset=8&time_unit=day&clean_mode=0&sub_mode=-1"}
        },
        {
            "id": "analysis_clean_paging",
            "name": "清潔數據分析（分頁）",
            "path": "/data-board/v1/analysis/clean/paging",
            "method": "GET",
            "description": "跨門店的清潔數據分析，支援分頁，不需指定 shop_id",
            "required_params": {"start_time": "開始時間戳(s)", "end_time": "結束時間戳(s)"},
            "optional_params": {
                "shop_id": "門店ID過濾",
                "timezone_offset": "時區偏移小時，範圍 -12 ~ 14",
                "time_unit": "時間單位：day | hour",
                "group_by": "分組維度（例如 day/hour/product_code）",
                "offset": "偏移量，從0開始",
                "limit": "每頁條目數，1 ~ 20",
                "clean_mode": "清潔模式過濾（0全部，1洗地，2掃地）",
                "sub_mode": "子模式過濾（-1全部，0自定義、1地毯吸塵、3靜音塵推）"
            },
            "response_description": "清潔數據統計（分頁）",
            "examples": {"query": "start_time=1704067200&end_time=1706745599&shop_id=1&timezone_offset=8&time_unit=day&group_by=day&offset=0&limit=20&clean_mode=0&sub_mode=-1"}
        },
        {
            "id": "brief_shop",
            "name": "門店摘要數據",
            "path": "/data-board/v1/brief/shop",
            "method": "GET",
            "description": "獲取門店摘要數據（快速視圖）",
            "required_params": {"shop_id": "門店ID"},
            "optional_params": {},
            "response_description": "門店摘要數據",
            "examples": {"query": "shop_id=1"}
        },
        {
            "id": "brief_run",
            "name": "巡航摘要數據",
            "path": "/data-board/v1/brief/run",
            "method": "GET",
            "description": "獲取巡航摘要數據",
            "required_params": {"shop_id": "門店ID"},
            "optional_params": {},
            "response_description": "巡航摘要數據",
            "examples": {"query": "shop_id=1"}
        },
        {
            "id": "brief_robot",
            "name": "機器人摘要數據",
            "path": "/data-board/v1/brief/robot",
            "method": "GET",
            "description": "獲取機器人摘要數據",
            "required_params": {"sn": "機器序列號"},
            "optional_params": {},
            "response_description": "機器人摘要數據",
            "examples": {"query": "sn=PD123456"}
        },
        {
            "id": "task_call",
            "name": "呼叫任務詳情",
            "path": "/data-board/v1/task/call",
            "method": "GET",
            "description": "獲取呼叫任務的詳細信息",
            "required_params": {"task_id": "任務ID"},
            "optional_params": {},
            "response_description": "任務詳情",
            "examples": {"query": "task_id=task123"}
        },
        {
            "id": "task_delivery",
            "name": "配送任務詳情",
            "path": "/data-board/v1/task/delivery",
            "method": "GET",
            "description": "獲取配送任務的詳細信息",
            "required_params": {"task_id": "任務ID"},
            "optional_params": {},
            "response_description": "任務詳情",
            "examples": {"query": "task_id=task123"}
        },
        {
            "id": "task_greeter",
            "name": "迎賓任務詳情",
            "path": "/data-board/v1/task/greeter",
            "method": "GET",
            "description": "獲取迎賓任務的詳細信息",
            "required_params": {"task_id": "任務ID"},
            "optional_params": {},
            "response_description": "任務詳情",
            "examples": {"query": "task_id=task123"}
        },
        {
            "id": "task_lifting",
            "name": "頂升任務詳情",
            "path": "/data-board/v1/task/lifting",
            "method": "GET",
            "description": "獲取頂升任務的詳細信息",
            "required_params": {"task_id": "任務ID"},
            "optional_params": {},
            "response_description": "任務詳情",
            "examples": {"query": "task_id=task123"}
        },
        {
            "id": "task_recovery",
            "name": "回盤任務詳情",
            "path": "/data-board/v1/task/recovery",
            "method": "GET",
            "description": "獲取回盤任務的詳細信息",
            "required_params": {"task_id": "任務ID"},
            "optional_params": {},
            "response_description": "任務詳情",
            "examples": {"query": "task_id=task123"}
        },
        {
            "id": "analysis_task_call",
            "name": "呼叫任務統計",
            "path": "/data-board/v1/analysis/task/call",
            "method": "GET",
            "description": "獲取呼叫任務的統計數據",
            "required_params": {"shop_id": "門店ID", "start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {},
            "response_description": "呼叫任務統計",
            "examples": {"query": "shop_id=1&start_date=2024-01-01&end_date=2024-01-31"}
        },
        {
            "id": "analysis_task_call_paging",
            "name": "呼叫任務統計（分頁）",
            "path": "/data-board/v1/analysis/task/call/paging",
            "method": "GET",
            "description": "跨門店的呼叫任務統計，支援分頁，不需指定 shop_id",
            "required_params": {"start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {"limit": "每頁筆數", "offset": "偏移量"},
            "response_description": "呼叫任務統計（分頁）",
            "examples": {"query": "start_date=2024-01-01&end_date=2024-01-31&limit=20&offset=0"}
        },
        {
            "id": "analysis_task_delivery",
            "name": "配送任務統計",
            "path": "/data-board/v1/analysis/task/delivery",
            "method": "GET",
            "description": "獲取配送任務的統計數據",
            "required_params": {"shop_id": "門店ID", "start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {},
            "response_description": "配送任務統計",
            "examples": {"query": "shop_id=1&start_date=2024-01-01&end_date=2024-01-31"}
        },
        {
            "id": "analysis_task_delivery_paging",
            "name": "配送任務統計（分頁）",
            "path": "/data-board/v1/analysis/task/delivery/paging",
            "method": "GET",
            "description": "跨門店的配送任務統計，支援分頁，不需指定 shop_id",
            "required_params": {"start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {"limit": "每頁筆數", "offset": "偏移量"},
            "response_description": "配送任務統計（分頁）",
            "examples": {"query": "start_date=2024-01-01&end_date=2024-01-31&limit=20&offset=0"}
        },
        {
            "id": "analysis_task_cruise",
            "name": "巡航任務統計",
            "path": "/data-board/v1/analysis/task/cruise",
            "method": "GET",
            "description": "獲取巡航任務的統計數據",
            "required_params": {"shop_id": "門店ID", "start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {},
            "response_description": "巡航任務統計",
            "examples": {"query": "shop_id=1&start_date=2024-01-01&end_date=2024-01-31"}
        },
        {
            "id": "analysis_task_cruise_paging",
            "name": "巡航任務統計（分頁）",
            "path": "/data-board/v1/analysis/task/cruise/paging",
            "method": "GET",
            "description": "跨門店的巡航任務統計，支援分頁，不需指定 shop_id",
            "required_params": {"start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {"limit": "每頁筆數", "offset": "偏移量"},
            "response_description": "巡航任務統計（分頁）",
            "examples": {"query": "start_date=2024-01-01&end_date=2024-01-31&limit=20&offset=0"}
        },
        {
            "id": "analysis_task_greeter",
            "name": "迎賓任務統計",
            "path": "/data-board/v1/analysis/task/greeter",
            "method": "GET",
            "description": "獲取迎賓任務的統計數據",
            "required_params": {"shop_id": "門店ID", "start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {},
            "response_description": "迎賓任務統計",
            "examples": {"query": "shop_id=1&start_date=2024-01-01&end_date=2024-01-31"}
        },
        {
            "id": "analysis_task_greeter_paging",
            "name": "迎賓任務統計（分頁）",
            "path": "/data-board/v1/analysis/task/greeter/paging",
            "method": "GET",
            "description": "跨門店的迎賓任務統計，支援分頁，不需指定 shop_id",
            "required_params": {"start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {"limit": "每頁筆數", "offset": "偏移量"},
            "response_description": "迎賓任務統計（分頁）",
            "examples": {"query": "start_date=2024-01-01&end_date=2024-01-31&limit=20&offset=0"}
        },
        {
            "id": "analysis_task_lifting",
            "name": "頂升任務統計",
            "path": "/data-board/v1/analysis/task/lifting",
            "method": "GET",
            "description": "獲取頂升任務的統計數據",
            "required_params": {"shop_id": "門店ID", "start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {},
            "response_description": "頂升任務統計",
            "examples": {"query": "shop_id=1&start_date=2024-01-01&end_date=2024-01-31"}
        },
        {
            "id": "analysis_task_lifting_paging",
            "name": "頂升任務統計（分頁）",
            "path": "/data-board/v1/analysis/task/lifting/paging",
            "method": "GET",
            "description": "跨門店的頂升任務統計，支援分頁，不需指定 shop_id",
            "required_params": {"start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {"limit": "每頁筆數", "offset": "偏移量"},
            "response_description": "頂升任務統計（分頁）",
            "examples": {"query": "start_date=2024-01-01&end_date=2024-01-31&limit=20&offset=0"}
        },
        {
            "id": "analysis_task_recovery",
            "name": "回盤任務統計",
            "path": "/data-board/v1/analysis/task/recovery",
            "method": "GET",
            "description": "獲取回盤任務的統計數據",
            "required_params": {"shop_id": "門店ID", "start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {},
            "response_description": "回盤任務統計",
            "examples": {"query": "shop_id=1&start_date=2024-01-01&end_date=2024-01-31"}
        },
        {
            "id": "analysis_task_recovery_paging",
            "name": "回盤任務統計（分頁）",
            "path": "/data-board/v1/analysis/task/recovery/paging",
            "method": "GET",
            "description": "跨門店的回盤任務統計，支援分頁，不需指定 shop_id",
            "required_params": {"start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {"limit": "每頁筆數", "offset": "偏移量"},
            "response_description": "回盤任務統計（分頁）",
            "examples": {"query": "start_date=2024-01-01&end_date=2024-01-31&limit=20&offset=0"}
        },
        {
            "id": "analysis_task_solicit",
            "name": "攬客任務統計",
            "path": "/data-board/v1/analysis/task/solicit",
            "method": "GET",
            "description": "獲取攬客任務的統計數據",
            "required_params": {"shop_id": "門店ID", "start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {},
            "response_description": "攬客任務統計",
            "examples": {"query": "shop_id=1&start_date=2024-01-01&end_date=2024-01-31"}
        },
        {
            "id": "analysis_task_solicit_paging",
            "name": "攬客任務統計（分頁）",
            "path": "/data-board/v1/analysis/task/solicit/paging",
            "method": "GET",
            "description": "跨門店的攬客任務統計，支援分頁，不需指定 shop_id",
            "required_params": {"start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {"limit": "每頁筆數", "offset": "偏移量"},
            "response_description": "攬客任務統計（分頁）",
            "examples": {"query": "start_date=2024-01-01&end_date=2024-01-31&limit=20&offset=0"}
        },
        {
            "id": "analysis_task_interactive",
            "name": "互動任務統計",
            "path": "/data-board/v1/analysis/task/interactive",
            "method": "GET",
            "description": "獲取互動任務的統計數據",
            "required_params": {"shop_id": "門店ID", "start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {},
            "response_description": "互動任務統計",
            "examples": {"query": "shop_id=1&start_date=2024-01-01&end_date=2024-01-31"}
        },
        {
            "id": "analysis_task_interactive_paging",
            "name": "互動任務統計（分頁）",
            "path": "/data-board/v1/analysis/task/interactive/paging",
            "method": "GET",
            "description": "跨門店的互動任務統計，支援分頁，不需指定 shop_id",
            "required_params": {"start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {"limit": "每頁筆數", "offset": "偏移量"},
            "response_description": "互動任務統計（分頁）",
            "examples": {"query": "start_date=2024-01-01&end_date=2024-01-31&limit=20&offset=0"}
        },
        {
            "id": "analysis_task_ad",
            "name": "廣告任務統計",
            "path": "/data-board/v1/analysis/task/ad",
            "method": "GET",
            "description": "獲取廣告任務的統計數據",
            "required_params": {"shop_id": "門店ID", "start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {},
            "response_description": "廣告任務統計",
            "examples": {"query": "shop_id=1&start_date=2024-01-01&end_date=2024-01-31"}
        },
        {
            "id": "analysis_task_ad_paging",
            "name": "廣告任務統計（分頁）",
            "path": "/data-board/v1/analysis/task/ad/paging",
            "method": "GET",
            "description": "跨門店的廣告任務統計，支援分頁，不需指定 shop_id",
            "required_params": {"start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {"limit": "每頁筆數", "offset": "偏移量"},
            "response_description": "廣告任務統計（分頁）",
            "examples": {"query": "start_date=2024-01-01&end_date=2024-01-31&limit=20&offset=0"}
        },
        {
            "id": "analysis_task_grid",
            "name": "宮格任務統計",
            "path": "/data-board/v1/analysis/task/grid",
            "method": "GET",
            "description": "獲取宮格任務的統計數據",
            "required_params": {"shop_id": "門店ID", "start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {},
            "response_description": "宮格任務統計",
            "examples": {"query": "shop_id=1&start_date=2024-01-01&end_date=2024-01-31"}
        },
        {
            "id": "analysis_task_grid_paging",
            "name": "宮格任務統計（分頁）",
            "path": "/data-board/v1/analysis/task/grid/paging",
            "method": "GET",
            "description": "跨門店的宮格任務統計，支援分頁，不需指定 shop_id",
            "required_params": {"start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {"limit": "每頁筆數", "offset": "偏移量"},
            "response_description": "宮格任務統計（分頁）",
            "examples": {"query": "start_date=2024-01-01&end_date=2024-01-31&limit=20&offset=0"}
        },
        {
            "id": "log_boot",
            "name": "開機日誌",
            "path": "/data-board/v1/log/boot/query_list",
            "method": "GET",
            "description": "查詢機器開機日誌",
            "required_params": {"sn": "機器序列號", "start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {"limit": "數量限制", "offset": "偏移量"},
            "response_description": "開機日誌列表",
            "examples": {"query": "sn=PD123456&start_date=2024-01-01&end_date=2024-01-31"}
        },
        {
            "id": "log_charge",
            "name": "充電日誌",
            "path": "/data-board/v1/log/charge/query_list",
            "method": "GET",
            "description": "查詢機器充電日誌",
            "required_params": {"sn": "機器序列號", "start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {"limit": "數量限制", "offset": "偏移量"},
            "response_description": "充電日誌列表",
            "examples": {"query": "sn=PD123456&start_date=2024-01-01&end_date=2024-01-31"}
        },
        {
            "id": "log_clean_task",
            "name": "清潔任務日誌",
            "path": "/data-board/v1/log/clean_task/query_list",
            "method": "GET",
            "description": "查詢清潔任務的詳細日誌",
            "required_params": {"sn": "機器序列號", "start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {"limit": "數量限制", "offset": "偏移量"},
            "response_description": "清潔任務日誌列表",
            "examples": {"query": "sn=CB123456&start_date=2024-01-01&end_date=2024-01-31"}
        },
        {
            "id": "log_clean_task_detail",
            "name": "清潔任務詳細查詢",
            "path": "/data-board/v1/log/clean_task/query",
            "method": "GET",
            "description": "查詢單個清潔任務的詳細信息",
            "required_params": {"task_id": "任務ID"},
            "optional_params": {},
            "response_description": "任務詳細信息",
            "examples": {"query": "task_id=task123"}
        },
        {
            "id": "log_error",
            "name": "故障/事件日誌",
            "path": "/data-board/v1/log/error/query_list",
            "method": "GET",
            "description": "查詢機器故障和事件日誌",
            "required_params": {"sn": "機器序列號", "start_date": "開始日期", "end_date": "結束日期"},
            "optional_params": {"limit": "數量限制", "offset": "偏移量"},
            "response_description": "故障/事件日誌列表",
            "examples": {"query": "sn=PD123456&start_date=2024-01-01&end_date=2024-01-31"}
        },
    ],
}


def _extract_apis_by_ids(source_category: str, api_ids: list[str]) -> list[dict]:
    source_list = COMMON_APIS.get(source_category, [])
    if not isinstance(source_list, list):
        return []

    id_set = set(api_ids)
    extracted: list[dict] = []
    remaining: list[dict] = []

    for api in source_list:
        if isinstance(api, dict) and str(api.get("id") or "") in id_set:
            extracted.append(api)
        else:
            remaining.append(api)

    COMMON_APIS[source_category] = remaining

    # 依照指定順序輸出，避免 UI 顯示順序跑掉。
    by_id = {str(api.get("id") or ""): api for api in extracted if isinstance(api, dict)}
    return [by_id[api_id] for api_id in api_ids if api_id in by_id]


_OTHER_FUNCTIONS_CATEGORY = "【其他功能】"
_CATEGORY_SPLIT_RULES: list[tuple[str, list[str]]] = [
    (
        "【總數/折線/柱狀圖數據】",
        [
            "analysis_shop",
            "analysis_run",
            "analysis_clean_mode",
            "analysis_task_ad",
            "analysis_task_call",
            "analysis_task_cruise",
            "analysis_task_delivery",
            "analysis_task_greeter",
            "analysis_task_grid",
            "analysis_task_interactive",
            "analysis_task_recovery",
            "analysis_task_solicit",
            "analysis_task_lifting",
        ],
    ),
    (
        "【列表分頁查詢】",
        [
            "analysis_shop_paging",
            "analysis_run_paging",
            "analysis_clean_paging",
            "analysis_task_ad_paging",
            "analysis_task_call_paging",
            "analysis_task_cruise_paging",
            "analysis_task_delivery_paging",
            "analysis_task_greeter_paging",
            "analysis_task_grid_paging",
            "analysis_task_interactive_paging",
            "analysis_task_recovery_paging",
            "analysis_task_solicit_paging",
            "analysis_task_lifting_paging",
        ],
    ),
    (
        "【摘要數據】",
        [
            "brief_shop",
            "brief_run",
            "brief_robot",
        ],
    ),
    (
        "【任務明細數據】",
        [
            "task_call",
            "task_delivery",
            "task_greeter",
            "task_lifting",
            "task_recovery",
            "analysis_clean_detail",
            "log_clean_task",
            "log_clean_task_detail",
        ],
    ),
    (
        "【日誌數據】",
        [
            "log_boot",
            "log_charge",
            "log_error",
        ],
    ),
    (
        "【機器人控制】",
        [
            "robot_door_task_list",
        ],
    ),
]

for category_name, api_ids in _CATEGORY_SPLIT_RULES:
    moved_apis = _extract_apis_by_ids(_OTHER_FUNCTIONS_CATEGORY, api_ids)
    if moved_apis:
        existing = COMMON_APIS.get(category_name)
        if isinstance(existing, list):
            existing.extend(moved_apis)
        else:
            COMMON_APIS[category_name] = moved_apis

# 使用者已改為分組模式，不再保留「其他功能」分類。
COMMON_APIS.pop(_OTHER_FUNCTIONS_CATEGORY, None)

# 全部 API 補齊可使用機器欄位（優先用官方文檔 Path 對照）
KNOWN_SUPPORTED_ROBOTS_BY_PATH = {
    "/biz-open-service/v1/robotDoor/task_list": ["FlashBot 2025", "FlashBot Pro", "FlashBot Max", "FlashBot Ultra"],
    "/biz-service/openPlatform/api/v1/gg/create": ["KettyBot", "KettyBot Pro", "BellaBot", "BellaBot Pro"],
    "/biz-service/openPlatform/api/v1/gg/delete": ["KettyBot", "KettyBot Pro", "BellaBot", "BellaBot Pro"],
    "/biz-service/openPlatform/api/v1/gg/get": ["KettyBot", "KettyBot Pro", "BellaBot", "BellaBot Pro"],
    "/biz-service/openPlatform/api/v1/gg/list": ["KettyBot", "KettyBot Pro", "BellaBot", "BellaBot Pro"],
    "/biz-service/openPlatform/api/v1/gg/scenesMenu/list": ["KettyBot", "KettyBot Pro", "BellaBot", "BellaBot Pro"],
    "/biz-service/openPlatform/api/v1/gg/update": ["KettyBot", "KettyBot Pro", "BellaBot", "BellaBot Pro"],
    "/cleanbot-service/v1/api/open/cron/list": ["CC1", "CC1 Pro", "MT1", "MT1 Vac", "MT1 Max"],
    "/cleanbot-service/v1/api/open/robot/detail": ["CC1", "CC1 Pro", "MT1", "MT1 Vac", "MT1 Max"],
    "/cleanbot-service/v1/api/open/task/exec": ["CC1", "CC1 Pro", "MT1", "MT1 Vac", "MT1 Max"],
    "/cleanbot-service/v1/api/open/task/list": ["CC1", "CC1 Pro", "MT1", "MT1 Vac", "MT1 Max"],
    "/data-board/v1/analysis/clean/detail": ["CC1", "CC1 Pro", "MT1", "MT1 Vac", "MT1 Max"],
    "/data-board/v1/analysis/clean/mode": ["CC1", "CC1 Pro", "MT1", "MT1 Vac", "MT1 Max"],
    "/data-board/v1/analysis/clean/paging": ["CC1", "CC1 Pro", "MT1", "MT1 Vac", "MT1 Max"],
    "/data-board/v1/analysis/run": ["ALL"],
    "/data-board/v1/analysis/run/paging": ["ALL"],
    "/data-board/v1/analysis/shop": ["ALL"],
    "/data-board/v1/analysis/shop/paging": ["ALL"],
    "/data-board/v1/analysis/task/ad": ["ALL"],
    "/data-board/v1/analysis/task/ad/paging": ["ALL"],
    "/data-board/v1/analysis/task/call": ["ALL"],
    "/data-board/v1/analysis/task/call/paging": ["ALL"],
    "/data-board/v1/analysis/task/cruise": ["ALL"],
    "/data-board/v1/analysis/task/cruise/paging": ["ALL"],
    "/data-board/v1/analysis/task/delivery": ["ALL"],
    "/data-board/v1/analysis/task/delivery/paging": ["ALL"],
    "/data-board/v1/analysis/task/greeter": ["ALL"],
    "/data-board/v1/analysis/task/greeter/paging": ["ALL"],
    "/data-board/v1/analysis/task/grid": ["ALL"],
    "/data-board/v1/analysis/task/grid/paging": ["ALL"],
    "/data-board/v1/analysis/task/interactive": ["ALL"],
    "/data-board/v1/analysis/task/interactive/paging": ["ALL"],
    "/data-board/v1/analysis/task/lifting": ["ALL"],
    "/data-board/v1/analysis/task/lifting/paging": ["ALL"],
    "/data-board/v1/analysis/task/recovery": ["ALL"],
    "/data-board/v1/analysis/task/recovery/paging": ["ALL"],
    "/data-board/v1/analysis/task/solicit": ["ALL"],
    "/data-board/v1/analysis/task/solicit/paging": ["ALL"],
    "/data-board/v1/brief/robot": ["ALL"],
    "/data-board/v1/brief/run": ["ALL"],
    "/data-board/v1/brief/shop": ["ALL"],
    "/data-board/v1/log/boot/query_list": ["ALL"],
    "/data-board/v1/log/charge/query_list": ["ALL"],
    "/data-board/v1/log/clean_task/query": ["CC1", "CC1 Pro", "MT1", "MT1 Vac", "MT1 Max"],
    "/data-board/v1/log/clean_task/query_list": ["CC1", "CC1 Pro", "MT1", "MT1 Vac", "MT1 Max"],
    "/data-board/v1/log/error/query_list": ["ALL"],
    "/data-board/v1/task/call": ["ALL"],
    "/data-board/v1/task/delivery": ["ALL"],
    "/data-board/v1/task/greeter": ["ALL"],
    "/data-board/v1/task/lifting": ["ALL"],
    "/data-board/v1/task/recovery": ["ALL"],
    "/data-open-platform-service/v1/api/maps": ["ALL"],
    "/data-open-platform-service/v1/api/robot": ["ALL"],
    "/data-open-platform-service/v1/api/shop": ["ALL"],
    "/map-service/v1/open/current": ["ALL"],
    "/map-service/v1/open/group": ["PuduT300"],
    "/map-service/v1/open/list": ["ALL"],
    "/map-service/v1/open/map": ["ALL"],
    "/map-service/v1/open/point": ["ALL"],
    "/open-platform-service/v1/call/list": ["FlashBot 2025", "FlashBot Pro", "FlashBot Max", "FlashBot Ultra", "KettyBot Pro", "BellaBot Pro", "PuduT300", "FlashBot", "KettyBot", "BellaBot", "Pudu Bot2", "HolaBot"],
    "/open-platform-service/v1/cancel_task": ["Flashbot"],
    "/open-platform-service/v1/control_doors": ["Flashbot", "FlashBot 2025", "FlashBot Pro", "FlashBot Max", "FlashBot Ultra"],
    "/open-platform-service/v1/cruise_action": ["PuduBot2"],
    "/open-platform-service/v1/cruise_task": ["PuduBot2"],
    "/open-platform-service/v1/custom_call": ["FlashBot 2025", "FlashBot Pro", "FlashBot Max", "FlashBot Ultra", "KettyBot Pro", "BellaBot Pro", "PuduT300", "FlashBot", "KettyBot", "BellaBot", "Pudu Bot2", "HolaBot"],
    "/open-platform-service/v1/custom_call/cancel": ["FlashBot 2025", "FlashBot Pro", "FlashBot Max", "FlashBot Ultra", "KettyBot Pro", "BellaBot Pro", "PuduT300", "FlashBot", "KettyBot", "BellaBot", "Pudu Bot2", "HolaBot"],
    "/open-platform-service/v1/custom_call/complete": ["FlashBot 2025", "FlashBot Pro", "FlashBot Max", "FlashBot Ultra", "KettyBot Pro", "BellaBot Pro", "PuduT300"],
    "/open-platform-service/v1/custom_content": ["FlashBot 2025", "FlashBot Pro", "FlashBot Max", "FlashBot Ultra", "BellaBot Pro", "PuduT300", "PuduBot2"],
    "/open-platform-service/v1/delivery_action": ["FlashBot 2025", "FlashBot Pro", "FlashBot Max", "FlashBot Ultra", "KettyBot Pro", "BellaBot Pro", "PuduT300", "BellaBot", "Pudu Bot2"],
    "/open-platform-service/v1/delivery_task": ["FlashBot 2025", "FlashBot Pro", "FlashBot Max", "FlashBot Ultra", "KettyBot Pro", "BellaBot Pro", "PuduT300", "BellaBot", "Pudu Bot2"],
    "/open-platform-service/v1/door_state": ["Flashbot", "FlashBot 2025", "FlashBot Pro", "FlashBot Max", "FlashBot Ultra"],
    "/open-platform-service/v1/errand_action": ["FlashBot 2025", "FlashBot Pro", "FlashBot Max", "FlashBot Ultra"],
    "/open-platform-service/v1/get_cruise_line": ["PuduBot2"],
    "/open-platform-service/v1/lifting_action": ["PuduT300"],
    "/open-platform-service/v1/lifting_task": ["PuduT300"],
    "/open-platform-service/v1/position_command": ["FlashBot 2025", "FlashBot Pro", "FlashBot Max", "FlashBot Ultra", "KettyBot Pro", "BellaBot Pro", "PuduT300"],
    "/open-platform-service/v1/recharge": ["PuduBot2"],
    "/open-platform-service/v1/robot/get_position": ["ALL"],
    "/open-platform-service/v1/robot/group/list": ["ALL"],
    "/open-platform-service/v1/robot/list_by_device_and_group": ["ALL"],
    "/open-platform-service/v1/robot/map/switch_in_elevator": ["FlashBot 2025", "FlashBot Pro", "FlashBot Max", "FlashBot Ultra", "PuduT300"],
    "/open-platform-service/v1/robot/screen/set": ["Flashbot"],
    "/open-platform-service/v1/robot/task/state/get": ["FlashBot"],
    "/open-platform-service/v1/status/get_by_group_id": ["ALL"],
    "/open-platform-service/v1/status/get_by_sn": ["ALL"],
    "/open-platform-service/v1/switch_map": ["PuduT300"],
    "/open-platform-service/v1/task_errand": ["FlashBot 2025", "FlashBot Pro", "FlashBot Max", "FlashBot Ultra"],
    "/open-platform-service/v1/transport_action": ["PuduBot2"],
    "/open-platform-service/v1/transport_task": ["PuduBot2"],
    "/open-platform-service/v1/tray_order": ["Flashbot"],
    "/open-platform-service/v1/voice/action": ["Kettybot"],
    "/open-platform-service/v1/voice/list": ["Kettybot"],
    "/open-platform-service/v1/voice/play": ["Kettybot"],
    "/open-platform-service/v1/volume/set": ["Kettybot"],
    "/open-platform-service/v2/recharge": ["FlashBot 2025", "FlashBot Pro", "FlashBot Max", "FlashBot Ultra", "PuduT300"],
    "/open-platform-service/v2/status/get_by_group_id": ["ALL"],
    "/open-platform-service/v2/status/get_by_sn": ["ALL"],
}

# 文檔未覆蓋但已確認的機型規則
KNOWN_SUPPORTED_ROBOTS_BY_ID = {
    "recharge_v1": ["PuduBot2"],
}

for category_list in COMMON_APIS.values():
    if not isinstance(category_list, list):
        continue
    for api in category_list:
        path = api.get("path")
        api_id = api.get("id")
        if path in KNOWN_SUPPORTED_ROBOTS_BY_PATH:
            api["supported_robots"] = KNOWN_SUPPORTED_ROBOTS_BY_PATH[path]
        elif api_id in KNOWN_SUPPORTED_ROBOTS_BY_ID:
            api["supported_robots"] = KNOWN_SUPPORTED_ROBOTS_BY_ID[api_id]
        else:
            api.setdefault("supported_robots", ["待補充"])


def _iter_apis():
    for category_list in COMMON_APIS.values():
        if isinstance(category_list, list):
            for api in category_list:
                if isinstance(api, dict):
                    yield api


EXAMPLE_START_TIME = "2026/03/01"
EXAMPLE_END_TIME = "2026/03/31"


def _normalize_time_query_example(example_query):
    if not isinstance(example_query, str):
        return example_query

    pairs = parse_qsl(example_query.lstrip("?"), keep_blank_values=True)
    if not pairs:
        return example_query

    changed = False
    normalized = []
    for key, value in pairs:
        lower_key = str(key).lower()
        if lower_key == "start_time":
            value = EXAMPLE_START_TIME
            changed = True
        elif lower_key == "end_time":
            value = EXAMPLE_END_TIME
            changed = True
        normalized.append((key, value))

    if not changed:
        return example_query
    return "&".join(f"{key}={value}" for key, value in normalized)


def _normalize_time_example_value(value):
    if isinstance(value, dict):
        changed = False
        normalized = {}
        for key, item in value.items():
            lower_key = str(key).lower()
            if lower_key == "start_time":
                normalized[key] = EXAMPLE_START_TIME
                changed = True
            elif lower_key == "end_time":
                normalized[key] = EXAMPLE_END_TIME
                changed = True
            else:
                updated_item = _normalize_time_example_value(item)
                normalized[key] = updated_item
                if updated_item != item:
                    changed = True
        return normalized if changed else value

    if isinstance(value, list):
        normalized = [_normalize_time_example_value(item) for item in value]
        return normalized if normalized != value else value

    return value


def _align_defs_with_docs() -> None:
    id_map = {str(api.get("id") or ""): api for api in _iter_apis()}

    def _set_api(api_id: str, *, name=None, description=None, required=None, optional=None, response=None, example_query=None):
        api = id_map.get(api_id)
        if not api:
            return
        if name is not None:
            api["name"] = name
        if description is not None:
            api["description"] = description
        if required is not None:
            api["required_params"] = required
        if optional is not None:
            api["optional_params"] = optional
        if response is not None:
            api["response_description"] = response
        if example_query is not None:
            examples = dict(api.get("examples") or {})
            examples["query"] = example_query
            api["examples"] = examples

    # 1) 機器人門禁任務列表 -> 獲取艙門拍照（pid）
    door_api = id_map.get("robot_door_task_list")
    if door_api:
        door_api["name"] = "獲取艙門拍照"
        door_api["description"] = "獲取艙門拍照任務列表與照片資料（FlashBot 系列）。"
        door_api["required_params"] = {
            "pid": "機器 SN（文件欄位名為 pid）",
        }
        door_api["optional_params"] = {
            "offset": "偏移量，預設 0",
            "limit": "每頁筆數，預設 10",
        }
        door_api["response_description"] = "照片任務列表（含 count/shop_id/pid/items）"
        door_api["examples"] = {
            "body": {
                "pid": "xxxCDEFGBOT01032",
                "limit": 10,
                "offset": 0,
            }
        }

    # 2) 迎賓任務詳情改名
    greeter_detail_api = id_map.get("task_greeter")
    if greeter_detail_api:
        greeter_detail_api["name"] = "廣告-總數|折線|柱狀圖數據"
        greeter_detail_api["description"] = "依文件需求改名；如需廣告圖表請使用 /data-board/v1/analysis/task/ad。"

    # 3) 先將所有 start_date/end_date 同步為 start_time/end_time
    for api in _iter_apis():
        req = dict(api.get("required_params") or {})
        opt = dict(api.get("optional_params") or {})
        changed = False

        for src, dst, default_desc in (
            ("start_date", "start_time", "開始時間戳(s)"),
            ("end_date", "end_time", "結束時間戳(s)"),
        ):
            if src in req:
                req[dst] = req.pop(src) or default_desc
                changed = True
            if src in opt:
                opt[dst] = opt.pop(src) or default_desc
                changed = True

        examples = dict(api.get("examples") or {})
        q = examples.get("query")
        if isinstance(q, str) and ("start_date" in q or "end_date" in q):
            q = q.replace("start_date", "start_time").replace("end_date", "end_time")
            examples["query"] = q
            changed = True

        if changed:
            api["required_params"] = req
            api["optional_params"] = opt
            api["examples"] = examples

    # 4) data-board 類查詢，補齊 timezone/time_unit 與 shop_id 過濾說明
    for api in _iter_apis():
        path = str(api.get("path") or "")
        if not path.startswith("/data-board/v1/"):
            continue

        req = dict(api.get("required_params") or {})
        opt = dict(api.get("optional_params") or {})
        has_time = ("start_time" in req or "start_time" in opt) and ("end_time" in req or "end_time" in opt)

        # 文件定義中多數 data-board 的 shop_id 為可選過濾。
        if "shop_id" in req:
            desc = req.pop("shop_id") or "門店ID過濾"
            opt["shop_id"] = "門店ID過濾（不填表示全部門店）"
        elif "shop_id" in opt:
            opt["shop_id"] = "門店ID過濾（不填表示全部門店）"

        if has_time:
            req.setdefault("start_time", "開始時間戳(s)")
            req.setdefault("end_time", "結束時間戳(s)")
            opt.setdefault("timezone_offset", "時區偏移小時，範圍 -12 ~ 14，預設 0")

            if "/analysis/" in path and not path.endswith("/paging"):
                opt.setdefault("time_unit", "時間單位：day|hour（時間跨度 >24h 預設 day，<=24h 可用 hour）")

        api["required_params"] = req
        api["optional_params"] = opt

    # 5) 精準覆寫：門店數據分析說明與範例（避免「門店ID過濾」語意不清）
    analysis_shop = id_map.get("analysis_shop")
    if analysis_shop:
        analysis_shop["description"] = (
            "門店分析-折線|柱狀圖數據。可查詢期間內門店機器數據並用於繪圖；"
            "shop_id 為可選過濾，不填代表統計全部門店。"
        )
        analysis_shop["required_params"] = {
            "start_time": "開始時間戳(s)",
            "end_time": "結束時間戳(s)",
        }
        analysis_shop["optional_params"] = {
            "shop_id": "門店ID過濾（不填表示全部門店）",
            "timezone_offset": "時區偏移小時，範圍 -12 ~ 14，預設 0",
            "time_unit": "時間單位：day|hour",
        }
        analysis_shop["response_description"] = "summary/qoq/chart/qoq_chart（總數與折線/柱狀圖資料）"
        analysis_shop["examples"] = {
            "query": "timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day"
        }

    analysis_shop_paging = id_map.get("analysis_shop_paging")
    if analysis_shop_paging:
        analysis_shop_paging["description"] = "門店分析分頁資料。shop_id 為可選過濾，不填代表統計全部門店。"
        analysis_shop_paging["required_params"] = {
            "start_time": "開始時間戳(s)",
            "end_time": "結束時間戳(s)",
        }
        analysis_shop_paging["optional_params"] = {
            "shop_id": "門店ID過濾（不填表示全部門店）",
            "timezone_offset": "時區偏移小時，範圍 -12 ~ 14，預設 0",
            "limit": "每頁筆數",
            "offset": "偏移量",
        }
        analysis_shop_paging["examples"] = {
            "query": "timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&limit=20&offset=0"
        }

    # 6) 廣告圖表名稱對齊文件
    analysis_task_ad = id_map.get("analysis_task_ad")
    if analysis_task_ad:
        analysis_task_ad["name"] = "廣告-總數|折線|柱狀圖數據"
        analysis_task_ad["description"] = "廣告數據（總數、折線、柱狀圖）"
        analysis_task_ad["required_params"] = {
            "start_time": "開始時間戳(s)",
            "end_time": "結束時間戳(s)",
        }
        analysis_task_ad["optional_params"] = {
            "shop_id": "門店ID過濾（不填表示全部門店）",
            "timezone_offset": "時區偏移小時，範圍 -12 ~ 14，預設 0",
            "time_unit": "時間單位：day|hour",
        }
        analysis_task_ad["examples"] = {
            "query": "timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day"
        }

    # 7) 依最新使用者需求覆寫 data-board 名稱/參數/說明
    _set_api(
        "analysis_run",
        name="機器運行分析-折線/柱狀圖數據",
        description="查詢範圍內的機器運行數據，用於折線與柱狀圖。",
        required={
            "start_time": "開始時間戳(s)",
            "end_time": "結束時間戳(s)",
        },
        optional={
            "shop_id": "門店ID過濾（不填表示全部門店）",
            "timezone_offset": "時區偏移小時，範圍 -12 ~ 14，預設 0",
            "time_unit": "時間單位：hour|day（最小粒度為 hour）",
        },
        response="機器運行折線/柱狀圖數據",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=hour",
    )

    _set_api(
        "analysis_run_paging",
        name="機器運行分析-列表分頁查詢",
        description="查詢範圍內的機器運行明細列表（分頁）。",
        required={
            "start_time": "開始時間戳(s)",
            "end_time": "結束時間戳(s)",
        },
        optional={
            "shop_id": "門店ID過濾（不填表示全部門店）",
            "timezone_offset": "時區偏移小時，範圍 -12 ~ 14，預設 0",
            "time_unit": "時間單位：hour|day",
            "limit": "每頁筆數",
            "offset": "偏移量",
        },
        response="機器運行分頁列表",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day&limit=20&offset=0",
    )

    _set_api(
        "analysis_clean_detail",
        name="清潔-24小時運行分佈",
        description="查詢清潔任務在 24 小時內的運行分佈。",
        required={
            "start_time": "開始時間戳(s)",
            "end_time": "結束時間戳(s)",
        },
        optional={
            "shop_id": "門店ID過濾（不填表示全部門店）",
            "timezone_offset": "時區偏移小時，範圍 -12 ~ 14，預設 0",
            "clean_mode": "清潔模式",
            "sub_mode": "子模式",
        },
        response="清潔 24 小時運行分佈資料",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&clean_mode=auto&sub_mode=normal",
    )

    _set_api(
        "analysis_clean_mode",
        name="清潔-折線/柱狀圖數據",
        description="查詢清潔模式的折線/柱狀圖分析數據。",
        required={
            "start_time": "開始時間戳(s)",
            "end_time": "結束時間戳(s)",
        },
        optional={
            "shop_id": "門店ID過濾（不填表示全部門店）",
            "timezone_offset": "時區偏移小時，範圍 -12 ~ 14，預設 0",
            "clean_mode": "清潔模式",
            "sub_mode": "子模式",
        },
        response="清潔模式折線/柱狀圖資料",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&clean_mode=auto&sub_mode=normal",
    )

    _set_api(
        "brief_shop",
        name="門店摘要數據",
        description="查詢週期內的門店總數：活躍、新增、累計門店數 + TOP10 門店運行時長。",
        required={
            "start_time": "開始時間戳(s)",
            "end_time": "結束時間戳(s)",
            "timezone_offset": "時區偏移小時，範圍 -12 ~ 14",
        },
        optional={
            "shop_id": "門店ID過濾（不填表示全部門店）",
        },
        response="週期內門店總覽與 TOP10 運行時長",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000",
    )

    _set_api(
        "brief_run",
        name="機器運行概覽",
        description="查詢週期內的運行總數：里程、時長、任務數、清潔面積。",
        required={
            "start_time": "開始時間戳(s)",
            "end_time": "結束時間戳(s)",
            "timezone_offset": "時區偏移小時，範圍 -12 ~ 14",
        },
        optional={
            "shop_id": "門店ID過濾（不填表示全部門店）",
        },
        response="週期內機器運行概覽",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000",
    )

    _set_api(
        "brief_robot",
        name="機器人摘要數據",
        description="查詢週期內的機器總數：開機、綁定、激活機器數。",
        required={
            "start_time": "開始時間戳(s)",
            "end_time": "結束時間戳(s)",
            "timezone_offset": "時區偏移小時，範圍 -12 ~ 14",
            "shop_id": "門店ID",
        },
        optional={},
        response="週期內機器數量摘要",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000",
    )

    _set_api(
        "analysis_shop",
        description="查詢範圍內的機器運行數據。最小時間粒度為 hour。",
        optional={
            "shop_id": "門店ID過濾（不填表示全部門店）",
            "timezone_offset": "時區偏移小時，範圍 -12 ~ 14，預設 0",
            "time_unit": "時間單位：hour|day（最小粒度為 hour）",
        },
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=hour",
    )

    task_detail_required = {
        "start_time": "開始時間戳(s)",
        "end_time": "結束時間戳(s)",
    }
    task_detail_optional = {
        "shop_id": "門店ID過濾（不填表示全部門店）",
        "timezone_offset": "時區偏移小時，範圍 -12 ~ 14，預設 0",
        "offset": "偏移量",
        "limit": "每頁筆數",
    }

    _set_api(
        "task_call",
        name="呼叫-目的地執行明細",
        description="查詢呼叫任務在指定期間的目的地執行明細。",
        required=task_detail_required,
        optional=task_detail_optional,
        response="呼叫目的地執行明細列表",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&offset=0&limit=20",
    )

    _set_api(
        "task_delivery",
        name="配送-目的地執行明細",
        description="查詢配送任務在指定期間的目的地執行明細。",
        required=task_detail_required,
        optional=task_detail_optional,
        response="配送目的地執行明細列表",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&offset=0&limit=20",
    )

    _set_api(
        "task_greeter",
        name="領位-目的地執行明細",
        description="查詢領位任務在指定期間的目的地執行明細。",
        required=task_detail_required,
        optional=task_detail_optional,
        response="領位目的地執行明細列表",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&offset=0&limit=20",
    )

    # 9) 頂升任務詳情和回盤任務詳情改參數
    _set_api(
        "task_lifting",
        name="頂升-目的地執行明細",
        description="查詢頂升任務在指定期間的目的地執行明細。",
        required=task_detail_required,
        optional=task_detail_optional,
        response="頂升目的地執行明細列表",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&offset=0&limit=20",
    )

    _set_api(
        "task_recovery",
        name="回盤-目的地執行明細",
        description="查詢回盤任務在指定期間的目的地執行明細。",
        required=task_detail_required,
        optional=task_detail_optional,
        response="回盤目的地執行明細列表",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&offset=0&limit=20",
    )

    # 10) 任務統計 API 改名與補齊參數
    analysis_stat_required = {
        "start_time": "開始時間戳(s)",
        "end_time": "結束時間戳(s)",
    }
    analysis_stat_optional = {
        "shop_id": "門店ID過濾（不填表示全部門店）",
        "timezone_offset": "時區偏移小時，範圍 -12 ~ 14，預設 0",
        "time_unit": "時間單位：day|hour",
    }
    analysis_stat_paging_optional = dict(analysis_stat_optional)
    analysis_stat_paging_optional.update({
        "limit": "每頁筆數",
        "offset": "偏移量",
    })

    _set_api(
        "analysis_task_call",
        name="呼叫-總數/折線/柱狀圖數據",
        description="查詢呼叫任務的統計數據。",
        required=analysis_stat_required,
        optional=analysis_stat_optional,
        response="呼叫任務統計數據",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day",
    )

    _set_api(
        "analysis_task_call_paging",
        name="呼叫任務統計（分頁）",
        description="",
        required=analysis_stat_required,
        optional=analysis_stat_paging_optional,
        response="呼叫任務統計（分頁）",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day&limit=20&offset=0",
    )

    _set_api(
        "analysis_task_delivery",
        name="配送-總數/折線/柱狀圖數據",
        description="查詢配送任務的統計數據。",
        required=analysis_stat_required,
        optional=analysis_stat_optional,
        response="配送任務統計數據",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day",
    )

    _set_api(
        "analysis_task_delivery_paging",
        name="配送任務統計（分頁）",
        description="",
        required=analysis_stat_required,
        optional=analysis_stat_paging_optional,
        response="配送任務統計（分頁）",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day&limit=20&offset=0",
    )

    _set_api(
        "analysis_task_cruise",
        name="巡航-總數/折線/柱狀圖數據",
        description="查詢巡航任務的統計數據。",
        required=analysis_stat_required,
        optional=analysis_stat_optional,
        response="巡航任務統計數據",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day",
    )

    _set_api(
        "analysis_task_cruise_paging",
        name="巡航任務統計（分頁）",
        description="",
        required=analysis_stat_required,
        optional=analysis_stat_paging_optional,
        response="巡航任務統計（分頁）",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day&limit=20&offset=0",
    )

    _set_api(
        "analysis_task_greeter",
        name="迎賓-總數/折線/柱狀圖數據",
        description="查詢迎賓任務的統計數據。",
        required=analysis_stat_required,
        optional=analysis_stat_optional,
        response="迎賓任務統計數據",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day",
    )

    _set_api(
        "analysis_task_greeter_paging",
        name="迎賓任務統計（分頁）",
        description="",
        required=analysis_stat_required,
        optional=analysis_stat_paging_optional,
        response="迎賓任務統計（分頁）",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day&limit=20&offset=0",
    )

    _set_api(
        "analysis_task_lifting",
        name="頂升-總數/折線/柱狀圖數據",
        description="查詢頂升任務的統計數據。",
        required=analysis_stat_required,
        optional=analysis_stat_optional,
        response="頂升任務統計數據",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day",
    )

    _set_api(
        "analysis_task_lifting_paging",
        name="頂升任務統計（分頁）",
        description="",
        required=analysis_stat_required,
        optional=analysis_stat_paging_optional,
        response="頂升任務統計（分頁）",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day&limit=20&offset=0",
    )

    _set_api(
        "analysis_task_recovery",
        name="回盤-總數/折線/柱狀圖數據",
        description="查詢回盤任務的統計數據。",
        required=analysis_stat_required,
        optional=analysis_stat_optional,
        response="回盤任務統計數據",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day",
    )

    _set_api(
        "analysis_task_recovery_paging",
        name="回盤任務統計（分頁）",
        description="",
        required=analysis_stat_required,
        optional=analysis_stat_paging_optional,
        response="回盤任務統計（分頁）",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day&limit=20&offset=0",
    )

    _set_api(
        "analysis_task_solicit",
        name="攬客-總數/折線/柱狀圖數據",
        description="查詢攬客任務的統計數據。",
        required=analysis_stat_required,
        optional=analysis_stat_optional,
        response="攬客任務統計數據",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day",
    )

    _set_api(
        "analysis_task_solicit_paging",
        name="攬客任務統計（分頁）",
        description="",
        required=analysis_stat_required,
        optional=analysis_stat_paging_optional,
        response="攬客任務統計（分頁）",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day&limit=20&offset=0",
    )

    _set_api(
        "analysis_task_interactive",
        name="互動-總數/折線/柱狀圖數據",
        description="查詢互動任務的統計數據。",
        required=analysis_stat_required,
        optional=analysis_stat_optional,
        response="互動任務統計數據",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day",
    )

    _set_api(
        "analysis_task_interactive_paging",
        name="互動任務統計（分頁）",
        description="",
        required=analysis_stat_required,
        optional=analysis_stat_paging_optional,
        response="互動任務統計（分頁）",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day&limit=20&offset=0",
    )

    _set_api(
        "analysis_task_ad",
        name="廣告-總數/折線/柱狀圖數據",
        description="查詢廣告任務的統計數據。",
        required=analysis_stat_required,
        optional=analysis_stat_optional,
        response="廣告任務統計數據",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day",
    )

    _set_api(
        "analysis_task_ad_paging",
        name="廣告任務統計（分頁）",
        description="",
        required=analysis_stat_required,
        optional=analysis_stat_paging_optional,
        response="廣告任務統計（分頁）",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day&limit=20&offset=0",
    )

    _set_api(
        "analysis_task_grid",
        name="宮格-總數/折線/柱狀圖數據",
        description="查詢宮格任務的統計數據。",
        required=analysis_stat_required,
        optional=analysis_stat_optional,
        response="宮格任務統計數據",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day",
    )

    _set_api(
        "analysis_task_grid_paging",
        name="宮格任務統計（分頁）",
        description="",
        required=analysis_stat_required,
        optional=analysis_stat_paging_optional,
        response="宮格任務統計（分頁）",
        example_query="timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&time_unit=day&limit=20&offset=0",
    )

    # 11) 日誌相關 API 改動
    _set_api(
        "log_boot",
        name="開機自檢-查詢list",
        description="查詢範圍內的開機自檢記錄，最小粒度=單次任務",
        required={
            "shop_id": "門店ID",
            "start_time": "開始時間戳(s)",
            "end_time": "結束時間戳(s)",
        },
        optional={
            "timezone_offset": "時區偏移小時，範圍 -12 ~ 14，預設 0",
            "check_step": "檢查步驟",
            "is_success": "是否成功",
            "limit": "數量限制",
            "offset": "偏移量",
        },
        response="開機自檢記錄列表",
        example_query="shop_id=331300000&timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&limit=20&offset=0",
    )

    _set_api(
        "log_charge",
        name="充電紀錄-查詢list",
        description="查詢範圍內的開機自檢記錄，最小粒度=單次任務",
        required={
            "shop_id": "門店ID",
            "start_time": "開始時間戳(s)",
            "end_time": "結束時間戳(s)",
        },
        optional={
            "timezone_offset": "時區偏移小時，範圍 -12 ~ 14，預設 0",
            "limit": "數量限制",
            "offset": "偏移量",
        },
        response="充電紀錄列表",
        example_query="shop_id=331300000&timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&limit=20&offset=0",
    )

    _set_api(
        "log_clean_task",
        name="清潔報告-查詢list",
        description="查詢清潔任務的詳細日誌",
        required={
            "shop_id": "門店ID",
            "start_time": "開始時間戳(s)",
            "end_time": "結束時間戳(s)",
        },
        optional={
            "timezone_offset": "時區偏移小時，範圍 -12 ~ 14，預設 0",
            "limit": "數量限制",
            "offset": "偏移量",
        },
        response="清潔任務日誌列表",
        example_query="shop_id=331300000&timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&limit=20&offset=0",
    )

    _set_api(
        "log_clean_task_detail",
        name="清潔任務詳細查詢",
        description="查詢單個清潔任務的詳細信息。report_id 可從『獲取清潔機器狀態詳情』的 Res.data.cleanbot.clean.report_id 取得。",
        required={
            "start_time": "開始時間戳(s)",
            "end_time": "結束時間戳(s)",
            "shop_id": "門店ID",
            "timezone_offset": "時區偏移小時",
            "sn": "機器序列號",
            "report_id": "報告ID",
        },
        optional={
            "limit": "數量限制",
            "offset": "偏移量",
        },
        response="任務詳細信息",
        example_query="start_time=2026/03/01&end_time=2026/03/31&shop_id=331300000&timezone_offset=8&sn=CC1234567&report_id=report123&limit=20&offset=0",
    )

    _set_api(
        "log_error",
        name="故障/事件-查詢list",
        description="查詢範圍內的開機自檢記錄，最小粒度=單次任務",
        required={
            "shop_id": "門店ID",
            "start_time": "開始時間戳(s)",
            "end_time": "結束時間戳(s)",
        },
        optional={
            "timezone_offset": "時區偏移小時，範圍 -12 ~ 14，預設 0",
            "error_levels": "錯誤等級",
            "error_types": "錯誤類型",
            "limit": "數量限制",
            "offset": "偏移量",
        },
        response="故障/事件日誌列表",
        example_query="shop_id=331300000&timezone_offset=8&start_time=2026/03/01&end_time=2026/03/31&limit=20&offset=0",
    )

    # 12) 更新語音列表說明
    _set_api(
        "voice_list",
        description="獲取指定機器人可用的語音列表",
    )

    _set_api(
        "robot_group_list",
        required={
            "shop_id": "門店ID",
        },
        optional={
            "limit": "數量限制",
            "offset": "偏移量",
        },
        example_query="shop_id=408250001&limit=10&offset=0",
    )

    _set_api(
        "control_doors",
        required={
            "sn": "機器序列號",
            "payload.control_states": "艙門控制列表（Array）",
            "payload.control_states[].door_number": "艙門編號（字串，例如 1/2/3/4）",
            "payload.control_states[].operation": "艙門操作（true=開啟, false=關閉）",
        },
        optional={},
    )

    switch_map_api = id_map.get("switch_map")
    if switch_map_api:
        switch_map_api["description"] = "切換機器使用的地圖（PuduT300）。map_info 為地圖信息對象（需先在平臺填寫回調地址，透過 notifySwitchMap 接收結果）。"

    position_cmd_api = id_map.get("position_command")
    if position_cmd_api:
        position_cmd_api["description"] = "命令機器開始上報位置，可指定上報頻率與次數（需先在平臺填寫回調地址，透過 notifyRobotPose 接收位置回報）。"
        position_cmd_api["callback_example"] = {
            "callback_type": "notifyRobotPose",
            "data": {
                "sn": "PD123456",
                "x": 12.34,
                "y": 56.78,
                "yaw": 90.0,
                "map_name": "1#1#地圖",
                "timestamp": 1710000000,
            },
        }

    # 8) 所有 time examples 一律改為斜線日期字串，讓 API 測試頁預設值一致
    for api in _iter_apis():
        examples = dict(api.get("examples") or {})
        changed = False

        normalized_query = _normalize_time_query_example(examples.get("query"))
        if normalized_query != examples.get("query"):
            examples["query"] = normalized_query
            changed = True

        normalized_body = _normalize_time_example_value(examples.get("body"))
        if normalized_body != examples.get("body"):
            examples["body"] = normalized_body
            changed = True

        if changed:
            api["examples"] = examples


_align_defs_with_docs()

# 計算總 API 數
def count_apis():
    total = 0
    for category_list in COMMON_APIS.values():
        if isinstance(category_list, list):
            total += len(category_list)
    return total

API_COUNT = count_apis()

# 按分類組織 API 的標籤
API_CATEGORIES = {
    "【數據查詢】": "data_query",
    "【機器狀態】": "robot_status",
    "【地圖與位置】": "map_position",
    "【呼叫與配送】": "task_call_delivery",
    "【運送與託盤】": "transport_errand",
    "【巡航】": "cruise",
    "【清潔】": "cleaning",
    "【廣告管理】": "advertisement",
    "【機器人控制】": "robot_control",
    "【機器人組與列表】": "robot_group",
    "【聲音控制】": "voice_control",
    "【充電】": "recharge",
    "【其他功能】": "other",
}
