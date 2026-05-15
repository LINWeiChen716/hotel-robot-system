# 跑腿任務通知-notifyErrandStatus

更新時間:2025-11-17 21:02:27

## 1、說明

### 功能描述

機器在進行跑腿任務時，會透過該回呼通知機器執行任務中的狀態。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyErrandStatus |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 當前時間戳秒 |
| session_id | string | 總任務id |
| auth | string | 授權碼，下達任務時指定 |
| task_type | string | 任務類型： REMOTE：遠程下達 MANUAL：本地手動下達 |
| task_time | int | 任務下達的時間戳，秒 |
| notify_timestamp | long | 機器上報的時間戳，毫秒，開發者可用於做亂序消息過濾 |
| tasks | **Array&lt;object&gt;** | 跑腿任務 |

### Params.data.tasks

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| task_id | string | 任務id |
| task_name | string | 子任務名稱,機器上報狀態時會用這個 |
| task_status | string | 子任務狀態： AWAIT:等待 ONGOING:進行中 CANCEL:取消 COMPLETE:完成 FAIL:失敗 OUT_OF_STOCK:缺貨 TAKE_ADVANCE:提前取出 RETURN_SUCCESS:退回成功 RETURN_FAIL:退回失敗 |
| point_list | **Array&lt;object&gt;** | 點位集合 |

### Params.data.tasks.point_list

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| map_name | string | 地圖名稱 |
| map_code | string | 地圖code |
| point | string | 點位id/名稱 |
| point_type | string | 點位類型，table.... |
| point_status | string | 點位狀態： AWAIT :等待中 ON_THE_WAY :前往中 ARRIVED :到達 CANCEL:取消 COMPLETE :完成 |
| verification_code | string | 點位驗證碼，下達任務時可以指定 |

## 3、呼叫範例

json

{

"callback_type": "notifyErrandStatus",

"data": {

"auth": "",

"mac": "14:80:CC:89:27:6E",

"notify_timestamp": 1760622854691,

"session_id": "1760622848496",

"sn": "8FG015401050021",

"task_time": 1760622848496,

"task_type": "MANUAL",

"tasks": [

{

"point_list": [

{

"map_code": "0#0#1015-test",

"map_name": "0#0#1015-test",

"point": "A2",

"point_status": "AWAIT",

"point_type": "Table",

"verification_code": ""

},

{

"map_code": "0#0#1015-test",

"map_name": "0#0#1015-test",

"point": "B2",

"point_status": "AWAIT",

"point_type": "Table",

"verification_code": ""

}

],

"task_desc": "",

"task_id": "1760622848441",

"task_name": "A2-B2",

"task_status": "AWAIT"

}

],


