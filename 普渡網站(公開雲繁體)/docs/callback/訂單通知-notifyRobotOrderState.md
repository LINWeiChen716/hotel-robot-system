# 訂單通知-notifyRobotOrderState

更新時間:2025-11-17 21:03:27

## 1、說明

### 功能描述

該介面是為了兼容舊開放平台(SDK微服務)的開放介面而提供，新版本機型不再支持該介面。

### 適用範圍

* **支援機型**：Flashbot

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyRobotOrderState |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| order_state | string | 分別會有三種狀態， START為開始送餐， CANCEL為取消任務， COMPLETED為完成任務 |
| employee_id | string | 下單員工 |
| ids | **Array&lt;object&gt;** | 訂單集合 |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 當前時間戳秒 |
| notify_timestamp | long | 機器上報的時間戳，毫秒，開發者可用於做亂序消息過濾 |

### Params.data.ids

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| id | string | 訂單的唯一id |
| spend_time | int32 | 開始到取消狀態或完成狀態花費的時間，單位：毫秒 |

## 3、呼叫範例

json

{

"callback_type": "notifyRobotOrderState",

"data": {

"order_state": "START",//START、CANCEL、COMPLETED

"employee_id": "PD001",

"ids": [{

"id":"order001", //orderId

"spend_time":1000 //ms

}],

"sn":"OP21321dsffsd",

"mac":"AA:AA:AA:AA:AA:AA",

"timestamp": 1764325632, // 當前時間戳，秒，

"notify_timestamp" :1764325632000 //機器上報的時間戳 毫秒

}

}


