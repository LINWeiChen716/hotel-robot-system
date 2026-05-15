# 機器綁定門市通知-robotBinding

更新時間:2025-11-17 21:04:34

## 1、說明

### 功能描述

在雲平台操作機器綁定門市後，機器的生命週期狀態會由【unbind(未綁定)】更新為【unactivated(待激活)】的狀態，同時透過該回呼消息通知開發者。

### 適用範圍

* **支援機型**：ALL

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：robotBinding |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器sn |
| name | string | 機器暱稱 |
| shop_id | int32 | 門市id |
| timestamp | int64 | 通知時間，時間戳秒 |

## 3、呼叫範例

```json

{

"callback_type": "robotBinding",

"data": {

"sn": "SV10111....",

"shop_id": 1001,

"timestamp": 1699364274

}

}

```
