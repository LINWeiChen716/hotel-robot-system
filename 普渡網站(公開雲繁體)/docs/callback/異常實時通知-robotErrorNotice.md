# 異常實時通知-robotErrorNotice

更新時間:2025-11-17 21:05:07

## 1、說明

### 功能描述

機器出現一些特殊異常的時候會透過該回呼通知給開發者。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、KettyBot Pro、BellaBot Pro、PuduT300、CC1、CC1 Pro、MT1、MT1 Vac、MT1 Max

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：robotErrorNotice |
| data | object | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

data結構:

| **參數名稱** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器sn |
| error_type | string | 故障(事件)類型： EmergencyStop 急停 |
| error_level | string | 故障(事件)等級： Fatal、Error |
| error_detail | string | 故障(事件)明細 |
| language | string | detail描述的語言： 'zh-CN': 簡體中文, 'zh-HK': 繁體中文-香港, 'zh-TW': 繁體中文-臺灣, 'en-US': 英語, 'ja-JP': 日語, 'ko-KR': 韓語, 'de-DE': 德語, 'fr-FR': 法語, 'ru-RU': 俄語, 'es-ES': 西班牙語, 'th-TH': 泰語, 'it-IT': 意大利, 'nl-NL': 荷蘭, 'pt-PT': 葡萄牙語, |
| error_id | string | 故障(事件)編號（注：部分過渡期apk版本無此欄位） |
| timestamp | int32 | 推送給消息中心的時間戳，秒 |
| extend_info | **object** | 機器擴展資訊 |

### Params.data.extend_info

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| mac | string | 機器mac |
| sn | string | 機器sn,這裡冗餘一個欄位推送 |
| map_name | string | 地圖名 |
| map_point | string | 當前機器所在點位 |
| battery | int32 | 剩餘電量0-100 |
| floor | string | 機器所在樓層 |
| shop_id | int32 | 機器所在門市id |
| shop_name | string | 機器所在門市名稱 |
| task_id | string | 當前任務id，目前僅T300和閃電匣Pro串接 |
| task_type | string | 當前任務類型\* 回充：Charge \* 返航：BackHome \* 巡航：Cruise \* 呼叫：Call \* 帶客：Guest \* 配送：Delivery \* 跑腿：Legwork \* 貨櫃：Cabinet \* 頂升 Lifting |
| position | **object** | 當前機器所在位置 |

### Params.data.extend_info.position

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| x | double | x座標 |
| y | double | y座標 |
| yaw | double | 角度 |

### error_type枚舉

| **故障類型** | **故障描述** |
| --- | --- |
| MobileStationCleanWaterEmpty | 清水箱已空 |
| MobileStationNotConnected | 基座和工作站未連接 |
| MobileStationNotPaired | 基座和移動水箱未連接 |
| MobileStationSewageFull | 污水箱已滿 |
| MobileStationWaterError | 污水箱已滿、清水箱已空 |
| PlanFailOverTime | 機器人路徑規劃失敗，無法繼續運動 |
| ReplanError | 機器人路徑被阻擋，無法繼續運動 |
| TrashFull | 垃圾已滿 |
| CanNotReach | 機器人無法到達目標點 |
| DockingPileFail | 機器人對樁異常 |
| EmergencyStop | 急停 |
| LostLocalization | 定位丟失 |
| LowBatteryLevel | 電量過低 |
| MobileStationBaseError | 基座或移動水箱出現異常 |
| CleanWaterEmpty | 機器人清水不足 |
| CleanSewageFull | 機器人污水箱滿 |
| CleanAgentEmpty | 工作站清潔劑不足 |
| SecondaryPollutionNotify | 清潔結構異常請檢查 |
| SecondaryPollutionCleaning | 清潔結構異常已返航自清潔 |
| SecondaryPollutionAbort | 清潔結構異常已終止任務 |

## 3、呼叫範例

json

{

"callback_type": "robotErrorNotice",

"data": {

"error_detail": "EmergencyKeyPressed",

"error_id": "",

"error_level": "Event",

"error_type": "EmergencyStop",

"extend_info": {

"battery": 58,

"floor": "",

"mac": "00:D6:CB:D5:28:01",

"map_name": "0#0#T600純激光地圖20250815",

"map_point": "",

"sn": "826004C17060045",

"task_id": "1222222222222",

"task_type": "Delivery",

"position": {

"x": -0.004843229,

"y": 4.99104,

"yaw": 1.3746479

},

},

"language": "",

"sn": "826004C17060045",

"timestamp": 1764325632 // 服務推送通知的時間戳，秒

}

}

