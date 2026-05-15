# 機器異常故障回呼(10分鐘延遲)-robotErrorWarning

更新時間:2025-11-17 21:05:18

## 1、說明

### 功能描述

機器上報異常到日誌服務，日誌服務定時統計推送通知開發者，該異常通知由10分鐘延遲。

### 適用範圍

* **支援機型**：ALL

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：robotErrorWarning |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器唯一標識sn |
| timestamp | int64 | 通知時間，時間戳秒 |
| error_type | string | 故障(事件)類型【枚舉詳見FAQ】： LostBattery 電池資料丟失 LostCamera 相機資料丟失 LostCAN CAN資料丟失 LostIMU imu資料丟失 LostLidar 雷達資料丟失 LostLocalization 定位丟失 LostRGBD RGBD資料丟失 WheelErrorLeft 左電機故障 WheelErrorRight 右電機故障 |
| error_level | string | 故障(事件)等級： Fatal、Error、Warning、Event |
| error_detail | string | 故障(事件)明細 |
| error_id | string | 故障(事件)編號（注：部分過渡期apk版本無此欄位） |

## 3、呼叫範例

```json

{

"callback_type": "robotErrorWarning",

"data": {

"sn": "SV10111....",

"timestamp": 1699364274,

"error_type": "LostLocalization",

"error_level": "Error",

"error_detail": "",

"error_id": "test00001"

}

}

```
