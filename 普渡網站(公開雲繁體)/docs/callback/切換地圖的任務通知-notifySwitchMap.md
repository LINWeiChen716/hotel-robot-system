# 切換地圖的任務通知-notifySwitchMap

更新時間:2025-11-17 21:04:05

## 1、說明

### 功能描述

機器呼叫[【控制指令】-【地圖與位置】-【切換地圖】](/zh/cloud-api/ycsqzal01xjrpwekwlhnfhbj)給機器下達指令後，切換結果會透過這個回呼通知開發者。

### 適用範圍

* **支援機型**：PuduT300

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
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int32 | 當前時間戳秒 |
| notify_timestamp | long | 機器上報的時間毫秒 |
| task_id | string | 任務id |
| task_status | string | CANCEL:取消， COMPLETE:完成， FAIL:失敗 |
| remark | string | 機器上報的備註資訊 |
| task_status | string | CANCEL:取消， COMPLETE:完成， FAIL:失敗 |
| map_info | **object** | 地圖資訊 |

### Params.data.map_info

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| map_name | string | 地圖名稱 |

## 3、呼叫範例

json

{

"callback_type": "notifySwitchMap",

"data": {

"sn": "8260047101A0007",

"mac": "90:03:71:42:9A:9A",

"map_info": {

"map_name": "2#2#222"

},

"notify_timestamp": 1760624622839,

"remark": "success",

"task_id": "1760624617357856",

"task_status": "COMPLETE",

"timestamp": 1760624624

}

}

