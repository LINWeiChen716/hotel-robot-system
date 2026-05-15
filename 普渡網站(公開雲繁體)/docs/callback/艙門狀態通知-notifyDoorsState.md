# 艙門狀態通知-notifyDoorsState

更新時間:2025-11-17 21:02:04

## 1、說明

### 功能描述

機器艙門開關狀態變化時會透過該回呼通知開發者機器的艙門開關狀態

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyDoorsState |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| target_name | string | 目標點、當前所在抵達點 |
| door_states | **Array&lt;object&gt;** | 艙門狀態數組 |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 服務推送通知的時間戳，秒 |
| notify_timestamp | long | 機器上報的時間戳，業務端可用於做亂序消息處理，毫秒 |

### Params.data.door_states

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| state | string | 艙門狀態OPENING, 正在打開 OPENED, 打開成功 OPEN_FAILED, 打開失敗OPEN_TIMEOUT, 打開超時 CLOSING, 正在關閉 CLOSED, 關閉成功 CLOSE_FAILED, 關閉失敗 CLOSE_TIMEOUT; 關閉超時 |
| door_number | string | 艙門H_01 ， 1號艙門H_02 ， 2號艙門H_03， 3號艙門H_04 ， 4號艙門 |

## 3、呼叫範例

json

{

"callback_type": "notifyDoorsState",

"data": {

"target_name": "1",

"door_states": [{

"door_number": "H_01",

"state": "CLOSED"

}, {

"door_number": "H_03",

"state": "CLOSED"

}, {

"door_number": "H_02",

"state": "CLOSED"

}, {

"door_number": "H_04",

"state": "CLOSED"

}],

"sn":"OP21321dsffsd",

"mac":"AA:AA:AA:AA:AA:AA",

"notify_timestamp":1764325632001,//機器上報的時間戳，業務端可用於做亂序消息處理，毫秒

"timestamp": 1764325632 // 服務推送通知的時間戳，秒

}

}


