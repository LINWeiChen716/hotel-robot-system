# 機器工作狀態通知-notifyRobotStatus

更新時間:2025-12-25 17:44:17

## 1、說明

### 功能描述

機器工作狀態(忙碌/空閒)變化、電量變化、移動狀態變化、在線離線都會透過該回呼介面通知開發者。

### 適用範圍

* **支援機型**：ALL

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyRobotStatus |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| mac | string | 設備名,這裡是指機器mac |
| sn | string | 機器sn |
| timestamp | int64 | 服務端推送時間戳秒 |
| battery | int32 | 電量 |
| is_charging | int32 | 1:正在充電 -1沒有充電 |
| charge_type | int32 | 1線充，2樁充(不傳)，正在充電時該欄位有效 |
| move_state | string | 這個欄位只有P-ONE會上報 運動狀態 IDLE :空閒 MOVING :運動中 STUCK :被障礙物阻擋 APPROACHING ：快抵達目標點 ARRIVE ：抵達目標點 PAUSE ：暫停 AVOID ： 與其他機器人進行調度 |
| charge_stage | string | 這個欄位只有P-ONE上報 電池狀態 IDLE:空閒 CHARGING：充電中 CHARGE_FULL：充滿電 CHARGE_ERROR_CONTACT：充電連接異常 CHARGE_ERROR_ELECTRIC：電流異常 ERROR_BATTERY_PACK_COMM：通訊異常 ERROR_OVER_VOLT：電壓異常 ERROR_OVER_ELECTRIC：電流異常 ERROR_OVER_TEMPERATURE：溫度異常 ERROR_OVER_TIME：超時異常 |
| run_state | string | 運行狀態：OFFLINE：機器離線，一般是由於機器網絡問題或者呼叫開關沒有開啟; DISABLE：當前狀態不可用，機器電量太低無法執行任務或者設置了機器充電中無法被呼叫，注意當機器由IDLE變為該狀態時，所有在雲端排隊的呼叫任務都會提前結束; BUSY：機器正在執行任務，或者部分機器觸摸屏幕後10秒內都會時忙碌狀態，該狀態機器是可以呼叫，但是會進入雲端排隊(僅呼叫任務有排隊邏輯) ;IDLE：機器當前空閒，給機器發任務，機器會立即回應。這裡 各個狀態和原v1/get_by_sn回傳各個狀態的映射關係： OFFLINE：is_online!=1 IDLE:is_online=1 && schedule_status=1 && work_status=-1 BUSY:is_online=1 && schedule_status=1 && work_status!=-1 DISABLE:is_online=1 && schedule_status!=1 |
| remain_time | int32 | P1纔會上報 剩餘使用時間 秒 |
| notify_timestamp | int64 | 機器通知時間戳，毫秒 |

## 3、呼叫範例

json

{

"callback_type": "robotEmergencyRecover",

"data": {

"sn": "SN-PD202405000001",

"mac": "機器人001",

"timestamp": 1640995200,

"notify_timestamp": 1640995200000,

"battery": 85,

"is_charging": -1,

"move_state": "IDLE",

"charge_stage": "IDLE",

"remain_time": 0,

"run_state": "IDLE",

"charge_type": 2

}

}

