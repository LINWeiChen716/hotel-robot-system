# 開機自檢-查詢List

更新時間:2025-11-28 16:01:27

## 1. 介面說明

### 功能描述

查詢範圍內的開機自檢記錄，最小粒度=單次任務

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/log/boot/query_list |
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
| check_step | string | N | 自檢項目, 如: CheckCAN |
| is_success | integer | N | 全部項目均自檢成功：0 失敗(有異常) 1 成功(無異常) -1 不過濾 |

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
| ip | string | 機器 IP |
| check_result | **object[]** | 自檢明細 |
| is_success | integer | 全部項目均自檢成功：0 失敗(有異常) 1 成功(無異常) |

### Res.data.list.check_result

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| check_step | string | 自檢項目(階段) |
| check_state | string | 自檢狀態： Success 正常 Fail 異常 |
| check_description | string | 自檢描述 |

### 

## 5.呼叫範例

### 請求範例


```http
GET /data-board/v1/log/boot/query_list?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=325100001&offset=0&limit=10 HTTP/1.1
```
### 回傳範例


```json
{

"message": "ok",

"data": {

"total": 14,

"offset": 0,

"limit": 10,

"list": [

{

"id": "5b102f00-30e7-4006-8247-ea0349780239",

"sn": "OPz8uN6AJvRjr2EP",

"mac": "08:E9:F6:8C:20:54",

"product_code": "67",

"upload_time": "2023-08-31 19:08:42",

"task_time": "2023-08-31 19:08:42",

"soft_version": "9.14.1.13",

"hard_version": "40.0.20",

"ip": "113.98.235.154",

"check_result": [

{

"check_step": "CheckCAN",

"check_state": "Success",

"check_description": ""

},

{

"check_step": "CheckESP",

"check_state": "Success",

"check_description": ""

},

{

"check_step": "CheckRGBD",

"check_state": "Success",

"check_description": ""

},

{

"check_step": "CheckLidar",

"check_state": "Success",


```


