# 頂升任務通知-notifyLiftingTask

更新時間:2025-11-17 21:02:44

## 1、說明

### 功能描述

機器在執行頂升任務時，機器會透過該回呼通知任務狀態。

### 適用範圍

* **支援機型**：PuduT300

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyLiftingTask |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 服務推送通知的時間戳，秒 |
| notify_timestamp | long | 機器上報的時間戳，業務端可用於做亂序消息處理，毫秒 |
| task_id | string | 總任務id |
| task_status | string | 總任務狀態，ON_THE_WAY 機器執行任務中、CANCEL 取消任務、FAILED(機器回傳拒絕任務時，雲端自己更新)、COMPLETED 完成任務、PAUSE 任務暫停中、STARTING 正在給機器發送任務中 |
| tasks | **Array&lt;object&gt;** | 子任務集合 |

### Params.data.tasks

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| status | string | 子任務狀態AWAIT:等待執行ON_THE_WAY:執行中COMPLETE:已完成CANCEL:被取消 |
| points | **Array&lt;object&gt;** | 所有點位集合 |

### Params.data.tasks.points

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| map_info | **object** | 點位所屬地圖 |
| point_name | sting | 點位名稱 |
| point_type | string | 點位類型，點位和貨架組POINT、SECONDARY_GROUP |
| point_attr | string | 點位屬性：取貨點、途徑點、放貨點DROP_POINT 放貨點 LIFT_POINT 取貨點 STAY_POINT 逗留點 |
| point_status | string | 點位執行階段 - START：開始執行 - ACTIVE:更換點位 - MOVING：前往中 - APPROACHING：抵達中 - ARRIVED：抵達 - COMPLETE：完成 - LIFTING_IN_PROGRESS：頂起貨物中 - DROP_OFF_IN_PROGRESS：放貨中（1）對於頂升點：+ 開始前往：START+ 更換點位：ACTIVE+ 機器人前往頂升點中：MOVING+ 進入到後退抵達流程：APPROACHING+ 抵達點位：ARRIVED+ 頂升過程中：LIFTING_IN_PROGRESS+ 頂升完成：COMPLETE（2）對於途徑點+ 開始前往：START+ 機器人前往途徑點中：MOVING+ 進入到後退抵達流程：APPROACHING+ 抵達點位：ARRIVED+ 完成：COMPLETE（3）對於放貨點+ 開始前往：START+ 更換點位：ACTIVE+ 機器人前往放貨點中：MOVING+ 進入到後退抵達流程：APPROACHING+ 抵達點位：ARRIVED+ 放貨過程中：DROP_OFF_IN_PROGRESS+ 放貨完成：COMPLETE |

### Params.data.tasks.points.map_info

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| map_name | string | 地圖名稱 |

## 3、呼叫範例

json

{

"callback_type": "notifyLiftingTask",

"data": {

"is_overtime": false,

"mac": "90:03:71:42:9A:9A",

"notify_timestamp": 1760630481083,

"progress": 0,

"ratio": "0/1",

"sn": "8260047101A0007",

"spend_time": 0,

"task_id": "eee38b4016b74b8bbadc5e0c9ce3ea08",

"task_status": "PAUSE",

"task_type": "MANUAL",

"tasks": [

{

"desc_code": "",

"points": [

{

"point_attr": "LIFT_POINT",

"point_name": "原地頂升",

"point_status": "COMPLETE",

"point_type": "LIFT_IN_PLACE"

},

{

"map_info": {

"map_code": "3#3#333",

"map_name": "3#3#333"

},

"point_attr": "DROP_POINT",

"point_name": "3-點位4",

"point_status": "PAUSE",

"point_type": "POINT"

}

],

"status": "PAUSE",

"timestamp": 1760630481076


