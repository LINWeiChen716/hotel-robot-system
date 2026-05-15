# 機器人點位配送通知-robotDeliveryStatus

更新時間:2025-11-17 21:04:44

## 1、說明

### 功能描述

歡樂送2定製功能，機器在執行任務時，會上報任務中每個點位的狀態。

### 適用範圍

* **支援機型**：Pudubot2

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：robotDeliveryStatus |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_id | string | 任務id |
| task_name | string | 任務名稱 |
| status | string | BEGIN:開始任務 INTERRUP:任務中斷 END:任務結束 |
| task_time | long | 發生任務變化時間，時間戳秒 |
| remark | string | 備註(eg:中斷原因) |
| map_name | string | 當前地圖名稱 |
| points | **Array&lt;object&gt;** | 地圖點位集合 |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 當前時間戳秒 |
| notify_timestamp | long | 機器上報的時間戳，毫秒，開發者可用於做亂序消息過濾 |

### Params.data.points

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| point_name | string | 點位名稱 |
| point_status | string | 點位狀態 AWAIT :等待中 ON_THE_WAY :當前前往中 ARRIVED :已配送到達 CANCEL :配送取消 COMPLETED ：已配送完成 |
| point_type | string | 點位類型 |

## 3、呼叫範例

json

{

"callback_type": "robotDeliveryStatus",

"data": {

"task_id": "taskId1",//START、CANCEL、COMPLETED

"task_name": "taskName",

"status": "BEGIN",//BEGIN:開始任務 INTERRUP:任務中斷 END:任務結束

"task_time": 1699364274,

"remark": "中斷原因",

"map_name": "map001",

"points": [{

"point_name": "pointName",

"point_status": "AWAIT",//點位狀態 AWAIT :等待中 ON_THE_WAY :當前前往中 ARRIVED :已配送到達 CANCEL :配送取消 COMPLETED ：已配送完成

"point_type": "pointType"

}],

"sn":"OP21321dsffsd",

"mac":"AA:AA:AA:AA:AA:AA",

"timestamp": 1764325632, // 當前時間戳，秒

"notify_timestamp" :1764325632000 //機器上報的時間戳 毫秒

}

}


