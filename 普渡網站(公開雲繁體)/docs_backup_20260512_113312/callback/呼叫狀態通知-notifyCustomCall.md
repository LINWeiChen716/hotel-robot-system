# 呼叫狀態通知-notifyCustomCall

更新時間:2025-12-24 10:10:58

## 1、說明

### 功能描述

開發者呼叫開放介面[【機器人任務】-【呼叫機器人】](/zh/cloud-api/d5vkhidure8ibhw5a58bthp1)後，機器人被呼叫後回應狀態（呼叫中 / 成功 / 排隊 / 失敗）會透過該回呼通知開發者。需要注意state的PAUSE和ARRIVE僅當機器為P-ONE版本纔會上報。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、KettyBot Pro、BellaBot Pro、PuduT300、KettyBot、BellaBot、Pudu Bot2、HolaBot

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyCustomCall |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_id | string | 任務id |
| shop_id | int32 | 門市id |
| map_name | string | 地圖名稱 |
| point | string | 地圖點位 |
| queue | int32 | 排隊號,如果機器忙碌中還呼叫該機器，則會回傳state=QUEUING,並且該欄位回傳排隊號，該欄位只在state=QUEUING時有效 |
| state | string | 當前狀態 "CALLING": 呼叫機器中, "CALL_SUCCESS": 機器回應成功, "QUEUING": 排隊中, "CALL_FAILED": 呼叫失敗, "CALL_COMPLETE": 呼叫完成, "QUEUING_CANCEL": 取消排隊, "TASK_CANCEL": 任務被取消, "ROBOT_CANCEL": 機器端取消, "PAUSE" :機器暫停(僅P1機器會上報) "ARRIVE" 到達點位(僅P1機器會上報) |
| sn | string | 回應的機器SN |
| robot_response_code | int32 | 如果該消息是機器回覆的，這裡就放機器的回覆碼 |
| robot_response_message | string | 如果該消息是機器回覆的，這裡就放機器的回覆內容 |

## 3、呼叫範例

```json

{

"callback_type": "notifyCustomCall",

"data": {

"task_id": "123",

"shop_id": 123,

"map_name":"map1",

"point":"point1",

"point_type":"table",

"queue":1,

"state":"QUEUING",

"sn":"PD1234567890123",

"robot_response_code":0,

"robot_response_message:":""

}

```
