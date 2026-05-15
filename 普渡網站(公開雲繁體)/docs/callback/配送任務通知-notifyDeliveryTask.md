# 配送任務通知-notifyDeliveryTask

更新時間:2025-11-17 21:01:55

## 1、說明

### 功能描述

開發者呼叫[【機器人任務】-【配送任務】](/zh/cloud-api/rbhjd42vj0rt5h31ib195vfx)後，機器會透過該回呼通知上報任務狀態

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、KettyBot Pro、BellaBot Pro、PuduT300、BellaBot、Flashbot、Pudu Bot2

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyDeliveryTask |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **欄位** | **類型** | **描述** |
| --- | --- | --- |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 服務端推送出來的時間戳秒 |
| delivery_mode | string | 配送模式： GENERAL(普通), DIRECT（直達）, BIRTHDAY（生日）, SEPECIAL（特殊） |
| task_id | string | 任務id |
| notify_timestamp | long | 機器通知的時間戳，毫秒 |
| is_over_time | bool | 是否超時 true,false |
| spent_time | int | 任務花費時間 |
| trays | **Array&lt;object&gt;** | 對應的託盤數組 |

### Params.data.trays

| **欄位** | **類型** | **描述** |
| --- | --- | --- |
| destinations | **Array&lt;object&gt;** | 每個託盤上的目標任務 |

### Params.data.trays.destinations

| **欄位** | **類型** | **描述** |
| --- | --- | --- |
| destination | string | 目標點：該值是使用透過“取得機器人的地圖目標點”得到的目標點的name |
| type | string | 任務類型： REMOTE：遠程發送的任務 MANUAL：機器上手動編輯的任務 |
| id | string | 任務id，如果透過“給機器人發送配送任務”來執行機器人任務時帶有任務id，機器人會將就收到的id透過該欄位通知開發者 |
| status | string | 任務狀態 AWAIT: 等待執行 ON_THE_WAY：配送中 ARRIVED：抵達 CANCEL: 取消 COMPLETE：完成 |
| estimated_time | Long | 預估抵達花費時間，當任務開始狀態為ON_THE_WAY時，會計算當前執行任務的花費時間，單位：ms（該時是執行開始執行任務時根據距離與設定速度計算的，可能因為機器人運行中遇到的障礙物導致該值不準確） |
| spend_time | Long | 配送狀態改變一共花費的時間，從第一個任務的ON_THE_WAY開始計時，到該任務COMPLETE結束該任務計時。單位：ms |
| complete_type | string | 機器人完成任務有多種形式，該欄位會回傳機器人抵達後是怎麼完成任務的： TIMEOUT：抵達後超時完成任務 MANUAL：手動點擊操作完成 REMOTE：遠程控制完成 QRCODE：二維碼掃碼完成 TRAY_EMPTY：託盤檢測空自動完成 |
| timeout | bool | 在任意一點位，trays欄位裡面的items在每次ARRIVED狀態持續超過任務下達的時候的wait_time，此標識為true; start_point欄位裡的items在放置物品的時候是否超過wait_time的值 |
| map_info | **Object** | 點位所屬地圖 |

### Params.data.trays.destinations.map_info

| **欄位** | **類型** | **描述** |
| --- | --- | --- |
| map_name | string | 地圖名稱 |

## 3、呼叫範例

json

{

"callback_type": "notifyDeliveryTask",

"data": {

"delivery_mode": "GENERAL",

"sn":"SV1111.....",

"mac":"mac",

"timestamp": 1699364274,

"notify_timestamp": 1699364274000,

"is_over_time":false,

"spent_time":100,

"task_id":"111111111",

"trays": [

{

"destinations": [

{

"destination": "A1",

"type": "REMOTE/MANUAL",

"id": "任務id，狀態同步時會回執",

"estimated_time": 60000,

"spend_time": 80000,

"status": "AWAIT/ON_THE_WAY/ARRIVED/CANCEL/COMPLETE",

"timeout": false,

"complete_type": "REMOTE",

"map_info":{"map_name":"地圖名稱"}

}

]

},

{

"destinations": [

{

"destination": "A1",

"type": "REMOTE/MANUAL",

"id": "任務id，狀態同步時會回執",

"estimated_time": 60000,

"spend_time": 80000,

"status": "AWAIT/ON_THE_WAY/ARRIVED/CANCEL/COMPLETE",


