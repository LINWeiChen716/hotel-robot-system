# 急停恢復通知-robotEmergencyRecover

更新時間:2025-12-17 10:07:31

## 1、說明

### 功能描述

機器按下急停按鈕之後，再恢復會透過該回呼通知開發者。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、BellaBot Pro、PuduT300

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：robotEmergencyRecover |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器sn |
| mac | string | 機器mac |
| timestamp | int64 | 時間戳秒 |

## 3、呼叫範例

```json

{

"callback_type": "robotEmergencyRecover",

"data": {

"sn":"OP21321dsffsd",

"mac":"AA:AA:AA:AA:AA:AA",

"timestamp": 1764325632 // 當前時間戳，秒，

}

}

```
