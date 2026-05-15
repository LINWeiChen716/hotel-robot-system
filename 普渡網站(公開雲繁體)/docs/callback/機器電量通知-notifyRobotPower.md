# 機器電量通知-notifyRobotPower

更新時間:2025-12-24 10:08:07

## 1、說明

### 功能描述

機器電量和電池狀態通知。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、KettyBot Pro、BellaBot Pro、PuduT300

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyRobotPower |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| charge_stage | string | 電池狀態： IDLE:空閒 CHARGING：充電中 CHARGE_FULL：充滿電 CHARGE_ERROR_CONTACT：充電連接異常 CHARGE_ERROR_ELECTRIC：電流異常 ERROR_BATTERY_PACK_COMM：通訊異常 ERROR_OVER_VOLT：電壓異常 ERROR_OVER_ELECTRIC：電流異常 ERROR_OVER_TEMPERATURE：溫度異常 ERROR_OVER_TIME：超時異常 |
| power | int32 | 電量百分⽐數，0～100 |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 服務推送通知的時間戳，秒 |
| notify_timestamp | long | 機器上報的時間戳，業務端可用於做亂序消息處理，毫秒 |

## 3、呼叫範例

json

{

"callback_type": "notifyRobotPower",

"data": {

"charge_stage": "IDLE",

"mac": "98:A1:4A:38:C4:6D",

"notify_timestamp": 1761705083466,

"power": 99,

"sn": "TS1732946965085",

"timestamp": 1761705082

}

}

