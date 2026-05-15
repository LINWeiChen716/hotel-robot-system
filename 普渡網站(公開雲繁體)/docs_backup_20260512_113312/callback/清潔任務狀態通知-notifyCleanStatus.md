# 清潔任務狀態通知-notifyCleanStatus

更新時間:2025-11-17 21:01:36

## 1、說明

### 功能描述

機器做清潔任務時會透過該回呼通知開發者機器的任務狀態

### 適用範圍

* **支援機型**：CC1、CC1 Pro、MT1、MT1 Vac、MT1 Max

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyCleanStatus |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| 欄位名稱 | 類型 | 描述 |
| --- | --- | --- |
| task_id | string | 任務id |
| task_name | string | 任務名稱 |
| status | string | START_FAILED： 任務啟動失敗、BEGIN：任務開始END：任務結束INTERRUP：任務中斷 CANCEL：任務被取消 LONG_TERM_USED_CLEANING ：機器長時間執行掃地任務 LONG_TERM_USED_WASHING ：機器長時間執行洗滌任務 GO_MAINTENANCE： 機器正前往維護點ARRIVE_MAINTENANCE： 機器已到達維護點 WEATHER_WARNING_LOW_TEM：溫度過低 WEATHER_WARNING_HIGH_TEM：溫度過高 WEATHER_WARNING_SNOW：雪天 WEATHER_WARNING_RAIN：雨天 |
| task_time | int32 | 發生任務變化時間，時間戳秒 |
| remark | string | 備註(eg:中斷原因) |
| task_method | string | 任務除非方式：AUTOMATIC說明是機器上點擊任務執行觸發 |

## 3、呼叫範例

```json

{

"callback_type": "notifyCleanStatus",

"data":{

"task_id":"單測任務id",

"task_name":"單測任務名稱",

"status":"BEGIN",

"task_time":1703749732,

"remark":"",

"sn":"xxxxx",

"mac":"08:E9:xxxx",

"timestamp":1703749732

}

}

```
