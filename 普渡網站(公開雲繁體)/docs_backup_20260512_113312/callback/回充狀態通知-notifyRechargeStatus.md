# 回充狀態通知-notifyRechargeStatus

更新時間:2025-11-17 21:03:02

## 1、說明

### 功能描述

在呼叫開放介面給機器下達回充指令後[【控制指令】-【機器人一鍵回充】-【機器人一鍵回充V2】](/zh/cloud-api/h517ik6b4gu8r8lz2teh7xex)，機器會將前端充電樁進行回充的過程狀態透過該回呼通知。

### 適用範圍

* **支援機型**：PuduT300、FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyRechargeStatus |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **欄位** | **類型** | **描述** |
| --- | --- | --- |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| task_id | string | 任務id |
| status | string | ON_THE_WAY 機器執行任務中、CANCEL 取消任務、FAILED(機器回傳拒絕任務時，雲端自己更新)、COMPLETED 完成任務、PAUSE 任務暫停中 |
| map_name | string | 當前所在地圖 |
| point | string | 當前所處點位 |
| point_type | string | 點位類型 |
| timestamp | int | 服務推送通知的時間戳，秒 |
| notify_timestamp | long | 機器上報的時間戳，業務端可用於做亂序消息處理，毫秒 |

## 3、呼叫範例

```json

{

"callback_type": "notifyRechargeStatus",

"data": {

"mac": "98:A1:4A:38:C4:DA",

"map_name": "0#0#Flashbot純激光",

"notify_timestamp": 1760440430417,

"point": "財務室門口充電樁",

"point_type": "ChargePile",

"sn": "OPG7jpSvFoA8cEdP",

"state": "COMPLETE",

"task_id": "07058bab9ef84625bcfc55d442c5766b",

"timestamp": 1760440431

}

}

```
