# 機器移動狀態通知-notifyRobotMoveState

更新時間:2025-12-24 10:16:27

## 1、說明

### 功能描述

機器做任務時會透過該回呼通知開發者機器的移動狀態

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、KettyBot Pro、BellaBot Pro、PuduT300

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyRobotMoveState |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| state | string | 機器人的運動狀態通知： IDLE :空閒 MOVING :運動中 STUCK :被障礙物阻擋 APPROACHING ：快抵達目標點 ARRIVE ：抵達目標點 PAUSE ：暫停 AVOID ：與其他機器人進行調度 |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int32 | 當前時間戳秒 |
| notify_timestamp | long | 機器上報的時間戳，毫秒，開發者可用於做亂序消息過濾 |

## 3、呼叫範例

```json

{

"callback_type": "notifyRobotMoveState",

"data": {

"state":"IDLE",

"sn":"OP21321dsffsd",

"mac":"AA:AA:AA:AA:AA:AA",

"timestamp": 1764325632, // 當前時間戳，秒，

"notify_timestamp" :1764325632000 //機器上報的時間戳 毫秒

}

}

```
