# 充電記錄-查詢List

更新時間:2025-11-28 16:01:13

## 1. 介面說明

### 功能描述

查詢範圍內的充電記錄，最小粒度=單次任務

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/log/charge/query_list |
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
| sn | string | 機器 SN |
| mac | string | 機器 MAC |
| product_code | string | 機型類型編碼，詳見【枚舉】 |
| upload_time | string | 日誌上雲時間(Y-m-d H:i:s) |
| task_time | string | 日誌生成時間(Y-m-d H:i:s) |
| soft_version | string | 軟件版本 |
| hard_version | string | 固件版本 |
| charge_power_percent | double | 充電電量,百分比 |
| charge_duration | double | 充電時長(s) |
| min_power_percent | double | 開始充電電量,百分比 |
| max_power_percent | double | 結束充電電量,百分比 |

## 5.呼叫範例

### 請求範例


```http
GET /data-board/v1/log/charge/query_list?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=201200012&offset=0&limit=10 HTTP/1.1
```
### 回傳範例


```json
{

"message": "ok",

"data": {

"total": 2,

"offset": 0,

"limit": 10,

"list": [

{

"id": "03e74dda-049f-423b-9cfc-f75154c02e30",

"sn": "P08E9F6CF62D4",

"mac": "08:E9:F6:CF:62:D4",

"product_code": "61",

"upload_time": "2023-08-31 18:04:11",

"task_time": "2023-08-31 18:03:57",

"soft_version": "",

"hard_version": "",

"charge_power_percent": 0,

"charge_duration": 0,

"min_power_percent": 28,

"max_power_percent": 28

},

{

"id": "56556f4b-75a9-4819-83c4-8fd9343dc4dd",

"sn": "P08E9F6CF62D4",

"mac": "08:E9:F6:CF:62:D4",

"product_code": "61",

"upload_time": "2023-08-30 18:33:38",

"task_time": "2023-08-30 18:33:22",

"soft_version": "",

"hard_version": "",

"charge_power_percent": 0,

"charge_duration": 0,

"min_power_percent": 20,

"max_power_percent": 20

}

]


```


