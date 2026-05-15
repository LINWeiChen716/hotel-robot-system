# 機器位置上報-notifyRobotPose

更新時間:2025-11-17 21:03:41

## 1、說明

### 功能描述

開發者透過開放介面[【控制指令】-【地圖與位置】-【通知機器上報位置】](/zh/cloud-api/cl4mlqsqsz5xo7lpos124se2)給機器下達上報指令後，機器會按參數的上報頻率和上報次數進行上報實時位置，機器上報後會透過該回呼通知開發者。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、KettyBot Pro、BellaBot Pro、PuduT300

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyRobotPose |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| x | float | x座標 |
| y | float | y座標 |
| yaw | float | 角度 |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int32 | 當前時間戳秒 |
| notify_timestamp | long | 機器上報的時間戳，毫秒，開發者可用於做亂序消息過濾 |

## 3、呼叫範例

```json

{

"callback_type": "notifyRobotPose",

"data": {

"x":1.234,

"y":2.345,

"yaw":32.34,

"sn":"OP21321dsffsd",

"mac":"AA:AA:AA:AA:AA:AA",

"timestamp": 1764325632, // 當前時間戳，秒，

"notify_timestamp" :1764325632000 //機器上報的時間戳 毫秒

}

}

```
