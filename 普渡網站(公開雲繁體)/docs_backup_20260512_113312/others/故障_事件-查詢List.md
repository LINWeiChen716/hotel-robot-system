# 故障|事件-查詢List

更新時間:2025-11-28 16:07:07

## 1. 介面說明

### 功能描述

查詢範圍內的故障|事件記錄，最小粒度=單次任務

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/log/error/query_list |
| --- | --- |
| 請求方法（Method） | get |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |
| Language | string | N | 預設中文 （支援語系查看附錄） |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| start_time | integer | Y | 開始時間戳(s) |
| end_time | integer | Y | 結束時間戳(s) |
| shop_id | integer | N | 門市ID過濾 |
| timezone_offset | integer | N | 時區偏移小時, 範圍 -12 ~ 14，表示 (UTC-12 ~ UTC+14）；預設UTC+0 |
| offset | integer | N | 偏移量，從 0 開始 |
| limit | integer | N | 每頁條目數，1 ~ 20 |
| error_levels | string | N | 故障等級篩選(多個用英文逗號分割), 枚舉值: Fatal|Error|Warning|\Event 如: Error,Warning |
| error_types | integer | N | 故障類型篩選(多個用英文逗號分割) 如: LostRGBD,LostCAN |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| message | string | 回傳錯誤碼，成功SUCCESS |
| data | **object** | 請求結果資料 |
| trace_id | string | 此次請求的唯一id |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| total | integer | 總條目數 |
| offset | integer | 偏移量 |
| limit | integer | 每頁條目數 |
| list | **object[]** | 當前頁詳細資料 |

### Res.data.list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| id | string |  |
| pid | string | 機器 SN |
| mac | string | 機器 MAC |
| product_code | string | 機型類型編碼，詳見【枚舉】 |
| upload_time | string | 日誌上雲時間(Y-m-d H:i:s) |
| task_time | string | 日誌生成時間(Y-m-d H:i:s) |
| soft_version | string | 軟件版本 |
| hard_version | string | 固件版本 |
| error_level | string | 故障等級: Fatal|Error|Warning|Event |
| error_type | string | 故障類型 |
| error_detail | string | 故障詳細描述 |
| error_id | string | 故障 ID |

## 5.呼叫範例

### 請求範例

```http

/data-board/v1/log/error/query_list?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=323400005&offset=0&limit=10&error_levels=Fatal,Error,Warning,Event&error_types=LostLocalization,LostRGBD

```
### 回傳範例

```json

{

"message": "ok",

"data": {

"total": 49,

"offset": 0,

"limit": 10,

"list": [

{

"id": "a352212e-b9f1-4295-868e-284583263268",

"sn "OP202307051611",

"mac": "50:80:4A:F8:03:F0",

"product_code": "73",

"upload_time": "2023-08-31 20:52:06",

"task_time": "2023-08-31 20:51:59",

"soft_version": "2.0.3.6-relocate_P04C0000B2308312050CNU",

"hard_version": "",

"error_level": "Error",

"error_type": "LostLocalization",

"error_detail": "NoInit",

"error_id": "vir_1693486319"

},

{

"id": "581ab792-1d03-46af-a2f5-832d985e9af9",

"sn": "OP202307051611",

"mac": "50:80:4A:F8:03:F0",

"product_code": "73",

"upload_time": "2023-08-31 20:44:20",

"task_time": "2023-08-31 20:44:12",

"soft_version": "2.0.3.6-relocate_P04C0000B2308312042CNU",

"hard_version": "",

"error_level": "Error",

"error_type": "LostLocalization",

"error_detail": "NoInit",

"error_id": "vir_1693485852"

}

]



```
---

