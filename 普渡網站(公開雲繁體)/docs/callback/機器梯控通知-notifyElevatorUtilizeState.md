# 機器梯控通知-notifyElevatorUtilizeState

更新時間:2025-12-24 10:14:14

## 1、說明

### 功能描述

機器乘坐電梯時，會回呼通知乘梯狀態。

### 適用範圍

* **支援機型**：PuduT300、FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyElevatorUtilizeState |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| elevator_utilize_state | string | 梯控狀態CALLING_ELEVATOR ：正在呼叫電梯 WAITING_ELEVATOR ：呼梯完成等待進梯 ENTERING_ELEVATOR ：進梯中 FINISH_ENTER_ELEVATOR：完成進梯 LEAVING_ELEVATOR：出梯中 FINISH_LEFT_ELEVATOR：出梯完成 OVERTIME_CALL_ELEVATOR ：呼叫電梯超時 OVERTIME_ENTER_ELEVATOR：進入電梯失敗 OVERTIME_ENTERED_ACK ：電梯回覆超時 OVERTIME_LEAVE_ELV：出梯超時 |
| elevator_event_param | **object** | 梯控參數 |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 服務推送通知的時間戳，秒 |
| notify_timestamp | long | 機器上報的時間戳，業務端可用於做亂序消息處理，毫秒 |

### Params.data.elevator_event_param

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| curr_floor | string | 當前樓層 |
| dst_floor | string | 目標樓層 |
| ele_id | string | 電梯ID |

## 3、呼叫範例

json

{

"callback_type": "notifyElevatorUtilizeState",

"data": {

"elevator_event_param": {

"curr_floor": "1",

"dst_floor": "1",

"ele_id": "865012064565160"

},

"elevator_utilize_state": "CALLING_ELEVATOR",

"env": "cxg-test-internal",

"mac": "00:D6:CB:4B:17:9D",

"notify_timestamp": 1761663939155,

"sn": "TS1732254968923",

"timestamp": 1761663938

}

}

