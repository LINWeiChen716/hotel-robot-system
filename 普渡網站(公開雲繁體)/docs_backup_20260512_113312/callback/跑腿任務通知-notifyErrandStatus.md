# 頝隞餃??-notifyErrandStatus

?湔??:2025-11-17 21:02:27

## 1?牧??

### ??膩

璈?券脰?頝隞餃?????閰脣??潮璈?瑁?隞餃?銝剔????

### ?拍蝭?

* **?舀璈?**嚗lashBot 2025?lashBot Pro?lashBot Max?lashBot Ultra

## 2???澆???

POST <https://yourdomain.com/youruri>

??https://yourdomain.com/youruri>??梢??潸?靘?嗅??潮???Ｗ?嚗?閬?唾?APPKey???‵?啜??澆??銝甈ㄐ嚗??賣?圈??

### 隢??批捆嚗arams嚗?

| **???* | **憿?** | **隤芣?** |
| --- | --- | --- |
| callback_type | string | ?瘨憿?嚗ㄐ嚗otifyErrandStatus |
| data | **object** | ????????寞?callback_type銝?嚗府蝯?銝? |

### Params.data

| 甈? | 憿? | ?膩 |
| --- | --- | --- |
| sn | string | 璈SN |
| mac | string | 璈MAC?啣? |
| timestamp | int | ?嗅????喟? |
| session_id | string | 蝮賭遙?d |
| auth | string | ??蝣潘?銝?隞餃???摰?|
| task_type | string | 隞餃?憿?嚗?REMOTE嚗?蝔???MANUAL嚗?唳?????|
| task_time | int | 隞餃?銝????嚗? |
| notify_timestamp | long | 璈銝???嚗神蝘????冽??摨??舫?瞈?|
| tasks | **Array&lt;object&gt;** | 頝隞餃? |

### Params.data.tasks

| 甈? | 憿? | ?膩 |
| --- | --- | --- |
| task_id | string | 隞餃?id |
| task_name | string | 摮遙??蝔?璈銝??????|
| task_status | string | 摮遙???? AWAIT:蝑? ONGOING:?脰?銝?CANCEL:?? COMPLETE:摰? FAIL:憭望? OUT_OF_STOCK:蝻箄疏 TAKE_ADVANCE:??? RETURN_SUCCESS:?????RETURN_FAIL:??仃??|
| point_list | **Array&lt;object&gt;** | 暺??? |

### Params.data.tasks.point_list

| 甈? | 憿? | ?膩 |
| --- | --- | --- |
| map_name | string | ?啣??迂 |
| map_code | string | ?啣?code |
| point | string | 暺?id/?迂 |
| point_type | string | 暺?憿?嚗able.... |
| point_status | string | 暺???? AWAIT :蝑?銝?ON_THE_WAY :??銝?ARRIVED :?圈? CANCEL:?? COMPLETE :摰? |
| verification_code | string | 暺?撽?蝣潘?銝?隞餃??隞交?摰?|

## 3??怎?靘?

```json

{

"callback_type": "notifyErrandStatus",

"data": {

"auth": "",

"mac": "14:80:CC:89:27:6E",

"notify_timestamp": 1760622854691,

"session_id": "1760622848496",

"sn": "8FG015401050021",

"task_time": 1760622848496,

"task_type": "MANUAL",

"tasks": [

{

"point_list": [

{

"map_code": "0#0#1015-test",

"map_name": "0#0#1015-test",

"point": "A2",

"point_status": "AWAIT",

"point_type": "Table",

"verification_code": ""

},

{

"map_code": "0#0#1015-test",

"map_name": "0#0#1015-test",

"point": "B2",

"point_status": "AWAIT",

"point_type": "Table",

"verification_code": ""

}

],

"task_desc": "",

"task_id": "1760622848441",

"task_name": "A2-B2",

"task_status": "AWAIT"

}

],

```

