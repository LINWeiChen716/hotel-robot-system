# 機器在線_離線狀態變更通知-robotStatus

更新時間:2025-11-17 21:05:27

## 1、說明

### 功能描述

機器連接上雲平台後，雲平台會給開發者推送機器在線的通知。

當機器斷網、斷電後，雲平台檢測到機器離線，會給開發者推送機器離線的通知。但是並非機器斷網後就立即通知，要取決於機器來不來得及主動和雲平台斷開連接，如果沒來得及斷開連接就需要等雲端檢測到機器的心跳超時，一般需要3-5分鐘。

### 適用範圍

* **支援機型**：ALL

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：robotStatus |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器sn |
| run_status | string | 機器運行狀態：online、offline |
| timestamp | int64 | 時間戳秒 |

## 3、呼叫範例

json

{

"callback_type": "robotStatus",

"data": {

"sn": "SV10111....",

"run_status": "online",

"timestamp": 1699364274

}

}

