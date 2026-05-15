# 二維碼消息通知-notifyQrCodeContent

更新時間:2025-11-17 21:02:53

## 1、說明

### 功能描述

該回呼介面是兼容SDK微服務的，新機型已經不再支持。

### 適用範圍

* **支援機型**：

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyQrCodeContent |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器sn |
| mac | string | 機器mac |
| content | string | 二位碼內容 |
| notify_timestamp | string | 機器上報的時間戳，業務端可用於做亂序消息處理，毫秒 |
| timestamp | int32 | 服務推送通知的時間戳，秒 |

## 3、呼叫範例

```json

{

"callback_type":"notifyQrCodeContent",

"data":{

"mac": "00:D6:CB:4B:17:9D",

"sn": "TS1732254968923",

"content":"111111111111111",

"notify_timestamp":1764325632001,//(1.5.1版本支持)機器上報的時間戳，業務端可用於做亂序消息處理，毫秒

"timestamp": 1764325632 // 服務推送通知的時間戳，秒

}

}

```
