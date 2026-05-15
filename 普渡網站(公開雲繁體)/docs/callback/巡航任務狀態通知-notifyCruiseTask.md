# 巡航任務狀態通知-notifyCruiseTask

更新時間:2025-12-04 14:26:05

## 1、說明

### 功能描述

機器呼叫[【機器人任務】-【巡航任務】-【發起巡航任務】](/zh/cloud-api/keclytvc5efrh0pwcygm0ct3)給機器下達指令後，機器巡航中會狀態變化透過這個回呼通知開發者。

### 適用範圍

* **支援機型**：PuduRobot2

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifCruiseTask |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **欄位** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 推送該消息的時間戳秒 |
| notify timestamp | long | 機器發生狀態變化的毫秒時間戳 |
| task_id | string | 任務id |
| task_type | string | REMOTE：遠程下達MANUAL：本地手動下達 |
| task_status | String | ON_THE_WAY(開始啟動巡航時報這個)、CANCEL、FAILED、COMPLETE、PAUSE |
| map_cruise_id | struct | 巡航路徑id |
| map_cruise_name | string | 巡航路徑名稱 |
| current_point | string | 當前點位名稱 |
| map_info | object | 當前地圖對像 |

### Params.data.map_info

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| map_name | string | 地圖名稱 |

## 3、呼叫範例

json

{

"callback_type": "notifyCruiseTask",

"data": {

"current_point": "A1",

"mac": "50:80:4A:F8:02:A8",

"map_cruise_id": "1764649613490",

"map_cruise_name": "chixz巡航1202",

"map_info": {

"map_name": "0#0#T600純激光地圖20250815"

},

"notify_timestamp": 1764770839934,

"sn": "6e0226270410014",

"task_id": "1764770838614695",

"task_status": "ON_THE_WAY",

"task_type": "REMOTE",

"timestamp": 1764770840

}

}

