# 地圖資訊(元素點)上傳_變更_刪除-mapElementChange

更新時間:2025-12-29 17:17:12

## 1、說明

### 功能描述

機器端地圖管理工具，修改地圖後，點擊同步雲端，雲端檢測到地圖發生變化，則會透過該回呼通知開發者。

### 適用範圍

* **支援機型**：ALL

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：mapElementChange |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| timestamp | int32 | 通知時間，時間戳秒 |
| shop_id | int32 | 門市id |
| map_name | string | 地圖名稱 |

## 3、呼叫範例

json

{

"callback_type": "mapElementChange",

"data": {

"map_name": "map123",

"shop_id": 1001,

"timestamp": 1699364274

}

}

