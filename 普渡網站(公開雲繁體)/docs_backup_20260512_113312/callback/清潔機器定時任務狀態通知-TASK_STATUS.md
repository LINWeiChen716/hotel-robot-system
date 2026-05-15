# 清潔機器定時任務狀態通知-TASK_STATUS

更新時間:2025-11-17 21:05:48

## 1、說明

### 功能描述

清潔機器在執行定時任務時會透過該回呼執行任務狀態。

### 適用範圍

* **支援機型**：CC1、CC1 Pro、MT1、MT1 Vac、MT1 Max

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：TASK_STATUS |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| task_id | string | 任務id |
| task_name | string | 任務名稱 |
| status | string | BEGIN:開始任務,INTERRUP:任務中斷,END:任務結束,START_FAILED ：啟動失敗 |
| task_time | int | 發生任務變化時間，時間戳秒 |
| remark | string | 備註(eg:中斷原因) |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 當前時間戳秒 |

## 3、呼叫範例

```json

{

"callback_type": "TASK_STATUS",

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
