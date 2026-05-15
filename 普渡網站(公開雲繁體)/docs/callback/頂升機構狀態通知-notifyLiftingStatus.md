# 頂升機構狀態通知-notifyLiftingStatus

更新時間:2025-11-17 21:02:36

## 1、說明

### 功能描述

機器頂升設備狀態發生變化時會透過該回呼進行通知

### 適用範圍

* **支援機型**：PuduT300

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyLiftingStatus |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| status | string | 頂升機構狀態+ RESET：頂升機構在復位位置+ LIFTING_IN_PROGRESS：頂升機構升起中+ LIFTED：頂升機構在上限位+ DROP_OFF_IN_PROGRESS：頂升機構放貨中 |
| mac | string | 機器mac |
| sn | string | 機器sn |
| timestamp | int | 服務推送通知的時間戳，秒 |
| notify_timestamp | long | (1.5.1版本支持)機器上報的時間戳，業務端可用於做亂序消息處理，毫秒 |

## 3、呼叫範例

json

{

"callback_type": "notifyLiftingStatus",

"data": {

"status": "RESET",

"mac": "90:03:71:42:9A:E0",

"sn": "8BROC20240902",

"notify_timestamp":1764325632001,//(1.5.1版本支持)機器上報的時間戳，業務端可用於做亂序消息處理，毫秒

"timestamp": 1764325632 // 服務推送通知的時間戳，秒

}

}

