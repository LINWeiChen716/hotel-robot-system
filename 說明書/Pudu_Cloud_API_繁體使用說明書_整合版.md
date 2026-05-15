# Pudu Cloud API 手冊（整理版）


# 概述

更新時間:2025-12-09 21:14:45

普渡雲開放介面（Open API） 是連接開發者與普渡機器人生態的核心技術樞紐，旨在為全球開發者提供標準化、模組化的機器人能力呼叫服務。透過這套開放介面體系，開發者可快速整合普渡機器人的地圖管理、任務調度、設備控制、資料監控等核心能力，無需深入底層技術，即可靈活構建適用於餐飲、醫療、物流、零售、倉儲等多行業的智慧化解決方案。

## 開放平台互動方式

開放介面主要分為兩種互動：開放API和回呼通知。

| **互動方式** | **說明** |
| --- | --- |
| 開放API | 開發者主動發起呼叫給機器推送任務、或者取得一些基礎資料。（開發者主動向普渡開放平台請求） |
| 回呼通知 | 當機器任務狀態發生變化、或者機器自身狀態發生變化時需要主動推送給開發者，讓開發者能收到通知後完成一些後續動作。（普渡開放平台主動推送給開發者） |

## 回呼介面說明

- 1.

  串接方可在代理商平台/商家平台填寫回呼地址，**普渡會回傳一個callback_code**，當有預警通知的時候，會主動回呼串接方的URL，用於告知串接方。

- 2.

  預設情況下我方不會進行預警通知，需提出申請設定後才能收到回呼資訊。

- 3.

  超時時間：5 秒，回應時間超過 5 秒則放棄本地回呼，失敗會重試（最多3次）。

# 快速開始

更新時間:2025-12-09 21:16:55

# 用戶請求普渡開放平台介面步驟

## 第 1 步：申請授權獲得**ApiAppKey 和 ApiAppSecret**

當前僅支持PUDU的代理商和自營商家申請，其他人員如有需求請透過官網的聯繫方式聯繫我們。

代理商：登錄代理商平台→應用中心→開放平台，進行API申請即可

自營商家或代理商終端可登錄商家平台，進行API申請

鑑權詳細方式詳見文檔：[【開放指南】-【鑑權串接】](/zh/cloud-api/diyrjw201ofqnc8ca3jiv6vf)

## 第 2 步：使用**ApiAppKey 和 ApiAppSecret呼叫健康檢查介面**

呼叫健康檢查介面，確保申請的授權資訊準確無誤。

普渡提供了幾種語言的Demo示例，Go、Java、JavaScript、Python和C#，用戶可以按需使用。

詳見文檔：【開放指南】-【鑑權串接】

以Go語言為例，用戶需要修改以下參數，就可以嘗試發起健康檢查請求

## 第 3 步：健康檢查透過後，可以按業務所需呼叫介面

所有的介面呼叫，都需要使用ApiAppKey 和 ApiAppSecret進行簽名，詳情請參考第2步健康檢查的呼叫方式。

示例代碼參考：【開發指南】-【呼叫範例】

## 第 4 步：接收普渡開放平台回呼通知

- 1.

  串接方可在代理商平台填寫回呼地址，**普渡會回傳一個callback_code**，當有預警通知的時候，會主動回呼串接方的URL，用於告知串接方。

- 2.

  預設情況下我方不會進行預警通知，需提出申請設定後才能收到回呼資訊。

- 3.

  超時時間：5 秒，回應時間超過 5 秒則放棄本地回呼，失敗會重試（最多3次）。

回呼地址填寫位置：  

回呼地址填寫完畢後會以下面方式請求開發者地址

**請求URL：**

* <https://yourdomain.com/youruri>

**請求方式：**

* post

**Header：**

| Header Name | **是否必選** | **類型** | **說明** |
| --- | --- | --- | --- |
| Content-Type | 必填 | string | application/json |
| TraceId | 必填 | string | 此次回呼請求的唯一id |
| CallbackCode | 必填 | string | 串接方和我方協商的暗號字符串，用於接 入方在收到回呼請求之後識別是我方的合法請求，而不是第三方的非法請求。此暗 號字符串一般由我方隨機生成後提供給接 入方，長度為 32 字節。如串接方有特殊要 求可以由串接方提供，最長不能超過 64 字 節，只允許大小寫字母和數字。此暗號字 符串不能透漏給第三方。 |

**請求參數示例**

{

"callback_type": "robotErrorWarning",

"data": {

}

}

**請求參數說明**

這裡的callback_type和data結構詳細【回呼通知】目錄下的各個回呼類型

| **參數名** | 類型 | **必填** | 說明 |
| --- | --- | --- | --- |
| callback_type | string | Y | 回呼類型： robotErrorWarning-機器異常故障 robotBinding-機器綁定門市 robotUnBinding-機器解綁門市 robotActivate-機器激活 mapElementChange-地圖資訊(元素點)上傳/變更/刪除 robotStatus-機器在線/離線狀態變更通知 |
| data | object | Y | 回呼資料結構 |

**回傳參數說明**

* HTTP狀態碼回傳200則判定為回呼成功

# 鑑權串接

更新時間:2025-11-07 14:23:20

# 普渡開放平台的對外固定域名

* 海外日韓新加坡生產節點: <https://css-open-platform.pudutech.com/pudu-entry>

* 國內生產節點: <https://open-platform.pudutech.com/pudu-entry>

* 德國生產節點：<https://csg-open-platform.pudutech.com/pudu-entry>

* 美國生產節點：<https://csu-open-platform.pudutech.com/pudu-entry>

# 普渡開放平台鑑權-應用認證方式

應用認證方式（\*\*ApiAppKey 和 ApiAppSecret：這兩個參數需要在平台上申請並透過審批獲得\*\*），客戶端在呼叫 API 時，需要使用簽名密鑰對請求內容進行簽名計算，並將簽名同步傳輸給服務器端進行簽名驗證，您可以參考本文檔在客戶端實現簽名計算過程。

常用語言的應用認證簽名 Demo 請參考: 《多種語言生成應用認證簽名-JavaScript（應用認證）》

## 概述

API 網關提供前端簽名及驗籤功能，該功能可實現：

* 驗證客戶端請求的合法性，確認請求中攜帶授權後的 App Key 生成的簽名。

* 防止請求資料在網絡傳輸過程中被篡改。

客戶端呼叫 API 時，需要使用已授權簽名密鑰對請求內容的關鍵資料進行加密簽名計算，並且將 ApiAppKey 和加密後生成的字符串放在請求的 Header 傳輸給 API 網關，API 網關會讀取請求中的 ApiAppKey 的頭資訊，並且根據 ApiAppKey 的值查詢到對應的 ApiAppSecret 的值，使用 ApiAppSecret 對收到的請求中的關鍵資料進行簽名計算，並且使用自己的生成的簽名和客戶端傳上來的簽名進行比對，來驗證簽名的正確性。只有簽名驗證透過的請求才會發送給後端服務，否則 API 網關會認為該請求為非法請求，直接回傳錯誤應答。

## 多種語言生成應用認證簽名

### Go（應用認證）

#### 操作場景

該任務指導您使用 Go 語言，透過應用認證來對您的 API 進行認證管理。

#### JSON 請求方式示例代碼

##### GET請求：

go

package main

import (

"crypto/hmac"

"crypto/md5"

"crypto/sha1"

"encoding/base64"

"encoding/hex"

"fmt"

"io/ioutil"

"log"

"net/http"

"net/url"

"sort"

"strings"

"time"

)

func main() {

// 應用 ApiAppKey

const ApiAppKey = "Your ApiAppKey"

//應用 ApiAppSecret

const ApiAppSecret = "Your ApiAppSecret"

// ###特殊字符測試 --->>>>> %23%23%23特殊字符測試

// xxxxxx.com 請使用真實的普渡開放平台對外固定域名：比如測試環境 open-platform-test.pudutech.com

var Url = "https://xxxxxx.com/pudu-entry/data-open-platform-service/v1/api/healthCheck?b=${b}&a=${a}&c=${c}"

Url = strings.ReplaceAll(Url, "${b}", encode("2"))

Url = strings.ReplaceAll(Url, "${a}", encode("###特殊字符測試"))

Url = strings.ReplaceAll(Url, "${c}", encode("3"))

const GmtFormat = "Mon, 02 Jan 2006 15:04:05 GMT"

const HTTPMethod = "GET"

const Accept = "application/json"

const ContentType = "application/json"

##### POST請求：

go

package main

import (

"crypto/hmac"

"crypto/md5"

"crypto/sha1"

"encoding/base64"

"encoding/hex"

"fmt"

"io/ioutil"

"log"

"net/http"

"net/url"

"sort"

"strings"

"time"

)

func main() {

// 應用 ApiAppKey

const ApiAppKey = "Your ApiAppKey"

//應用 ApiAppSecret

const ApiAppSecret = "Your ApiAppSecret"

// xxxxxx.com 請使用真實的普渡開放平台對外固定域名：比如測試環境 open-platform-test.pudutech.com

const Url = "https://xxxxxx.com/pudu-entry/data-open-platform-service/v1/api/healthCheck"

const GmtFormat = "Mon, 02 Jan 2006 15:04:05 GMT"

const HTTPMethod = "POST"

const Accept = "application/json"

const ContentType = "application/json"

// 根據 Url 解析 Host 和 Path

u, err := url.Parse(Url)

if err != nil {

log.Fatal(err)

### JavaScript（應用認證）

#### 操作場景

該任務指導您使用 JavaScript 語言，透過應用認證來對您的 API 進行認證管理。

#### JSON 請求方式示例代碼

##### GET請求：

javascript

const https = require("https");

const crypto = require("crypto");

// 應用 ApiAppKey，注意：需要替換成真實參數

const apiAppKey = "Your ApiAppKey";

// 應用 ApiAppSecret，注意：需要替換成真實參數

const apiAppSecret = "Your ApiAppSecret";

// 請求 host

// xxxxxx.com 請使用真實的普渡開放平台對外固定域名：比如測試環境 open-platform-test.pudutech.com

const hostname = "xxxxxx.com";

// 端口號：https 對應 443，http 對應 80

const port = 443;

// 請求 path

const path = "/pudu-entry/data-open-platform-service/v1/api/healthCheck";

// 請求方法

// const method = "POST";

const method = "GET";

const dateTime = new Date().toUTCString();

// 請求參數，注意：需要替換成真實參數

const body = {

b: encodeURIComponent(""),

a: encodeURIComponent('###特殊字符測試'), // ###特殊字符測試 --->>>>> %23%23%23特殊字符測試

c: encodeURIComponent("3"),

d: [encodeURIComponent("d2"), encodeURIComponent("d1"), encodeURIComponent("d3")],

};

// 排序

const sortedBodyStr = sortBody(body);

const bodyJsonStr = JSON.stringify(body);

// MD5需要包裝一層base64

// const contentMD5 = Buffer.from(

// crypto.createHash("md5").update(bodyJsonStr, "utf8").digest("hex")

##### POST請求：

javascript

const https = require("https");

const crypto = require("crypto");

// 應用 ApiAppKey，注意：需要替換成真實參數

const apiAppKey = "Your ApiAppKey";

// 應用 ApiAppSecret，注意：需要替換成真實參數

const apiAppSecret = "Your ApiAppSecret";

// 請求 host

// xxxxxx.com 請使用真實的普渡開放平台對外固定域名：比如測試環境 open-platform-test.pudutech.com

const hostname = "xxxxxx.com";

// 端口號：https 對應 443，http 對應 80

const port = 443;

// 請求 path

const path = "/pudu-entry/data-open-platform-service/v1/api/healthCheck";

// 請求方法

const method = "POST";

// const method = "GET";

const dateTime = new Date().toUTCString();

// 請求參數，注意：需要替換成真實參數

const body = {

b: "2",

a: "###特殊字符測試",

c: "3",

};

// 排序

const sortedBodyStr = sortBody(body);

const bodyJsonStr = JSON.stringify(body);

// MD5需要包裝一層base64

const contentMD5 = Buffer.from(

crypto.createHash("md5").update(bodyJsonStr, "utf8").digest("hex")

).toString("base64");

### **Java（應用認證）**

#### 操作場景

該任務指導您使用 Java 語言，透過應用認證來對您的 API 進行認證管理。

#### 環境依賴

* API 網關提供 JSON 請求方式和 form 請求方式的示例代碼，請您根據自己業務的實際情況合理選擇。

* 應用認證 Java Demo 中需要引入外部依賴，具體引入的依賴如下：

xml

<dependency>

<groupId>org.apache.httpcomponents</groupId>

<artifactId>httpclient</artifactId>

<version>4.5.13</version>

</dependency>

<dependency>

<groupId>commons-codec</groupId>

<artifactId>commons-codec</artifactId>

<version>1.11</version>

</dependency>

#### JSON 請求方式示例代碼

##### GET請求：

java

package com.fourleaf.tencentApiGateway;

import org.apache.commons.codec.digest.DigestUtils;

import org.apache.http.HttpEntity;

import org.apache.http.client.methods.CloseableHttpResponse;

import org.apache.http.client.methods.HttpGet;

import org.apache.http.client.methods.HttpPost;

import org.apache.http.entity.StringEntity;

import org.apache.http.impl.client.CloseableHttpClient;

import org.apache.http.impl.client.HttpClients;

import org.apache.http.util.EntityUtils;

import javax.crypto.Mac;

import javax.crypto.SecretKey;

import javax.crypto.spec.SecretKeySpec;

import java.net.URL;

import java.net.URLDecoder;

import java.net.URLEncoder;

import java.text.SimpleDateFormat;

import java.util.\*;

public class TestTencentApiGatewayGet {

private static final String MAC_NAME = "HmacSHA1";

private static final String ENCODING = "UTF-8";

private static final String HTTP_METHOD_GET = "GET";

private static final String HTTP_METHOD_POST = "POST";

public static void main(String[] args) throws Exception {

// xxxxxx.com 請使用真實的普渡開放平台對外固定域名：比如測試環境 open-platform-test.pudutech.com

String host = "apisix-cxg-test-internal.pudu.work";

String apiAppKey = "APID512h40iamHg5PslKR5dbeq1h5RoeBmk8BVF";

String apiAppSecret = "1uz4lFmsmU3wX1NakwHrJLc1lvvD6K50HtmcQ62f";

String environment = "";

// ###特殊字符測試 --->>>>> %23%23%23特殊字符測試

// xxxxxx.com 請使用真實的普渡開放平台對外固定域名：比如測試環境 open-platform-test.pudutech.com

String url = "https://" + host + "/pudu-entry/data-open-platform-service/v1/api/healthCheck?b=${b}&a=${a}&d=${d2}&d=${d1}&d=${d3}&c=${c}";

##### POST請求：

java

import org.apache.commons.codec.digest.DigestUtils;

import org.apache.http.HttpEntity;

import org.apache.http.client.methods.CloseableHttpResponse;

import org.apache.http.client.methods.HttpGet;

import org.apache.http.client.methods.HttpPost;

import org.apache.http.entity.StringEntity;

import org.apache.http.impl.client.CloseableHttpClient;

import org.apache.http.impl.client.HttpClients;

import org.apache.http.util.EntityUtils;

import javax.crypto.Mac;

import javax.crypto.SecretKey;

import javax.crypto.spec.SecretKeySpec;

import java.net.URL;

import java.net.URLDecoder;

import java.net.URLEncoder;

import java.text.SimpleDateFormat;

import java.util.\*;

public class TestTencentApiGatewayPost {

private static final String MAC_NAME = "HmacSHA1";

private static final String ENCODING = "UTF-8";

private static final String HTTP_METHOD_GET = "GET";

private static final String HTTP_METHOD_POST = "POST";

public static void main(String[] args) throws Exception {

String environment = "";

// ###特殊字符測試 --->>>>> %23%23%23特殊字符測試

// xxxxxx.com 請使用真實的普渡開放平台對外固定域名：比如測試環境 open-platform-test.pudutech.com

String url = "https://xxxxxx.com/pudu-entry/data-open-platform-service/v1/api/healthCheck";

String host = "xxxxxx.com";

String apiAppKey = "Your apiAppKey";

String apiAppSecret = "Your apiAppSecret";

String httpMethod = "POST";

String acceptHeader = "application/json";

### Python（應用認證）

#### 操作場景

該任務指導您使用 Python 語言，透過應用認證來對您的 API 進行認證管理。

#### Python 3 json 請求方式示例代碼

##### GET請求：

python


import base64

import datetime

import hashlib

import hmac

import json

from urllib.parse import urlparse

from urllib.parse import quote

from urllib.parse import unquote

from urllib.parse import parse_qs

import requests

ApiAppKey = 'Your ApiAppKey'

ApiAppSecret = 'Your ApiAppSecret'

Url = "https://xxxxxx.com/pudu-entry/data-open-platform-service/v1/api/healthCheck?b=${b}&a=${a}&c=${c}"

Url = Url.replace("${b}", quote("2"))

Url = Url.replace("${a}", quote("###特殊字符測試"))

Url = Url.replace("${c}", quote("3"))

HTTPMethod = "GET" # method

Accept = "application/json"

ContentType = "application/json"

urlInfo = urlparse(Url)

Host = urlInfo.hostname

Path = urlInfo.path

if Path.startswith(("/release", "/test", "/prepub")):

##### POST請求：

python


import base64

import datetime

import hashlib

import hmac

import json

from urllib.parse import urlparse

from urllib.parse import quote

from urllib.parse import unquote

import requests

ApiAppKey = 'Your ApiAppKey'

ApiAppSecret = 'Your ApiAppSecret'

Url = "https://xxxxxx.com/pudu-entry/data-open-platform-service/v1/api/healthCheck"

HTTPMethod = "POST" # method

Accept = "application/json"

ContentType = "application/json"

urlInfo = urlparse(Url)

Host = urlInfo.hostname

Path = urlInfo.path

if Path.startswith(("/release", "/test", "/prepub")):

Path = "/" + Path[1:].split("/", 1)[1]

Path = Path if Path else "/"

### C#（應用認證）

#### 操作場景

該任務指導您使用 C# 語言，透過應用認證來對您的 API 進行認證管理。

#### JSON 請求方式示例代碼

##### GET請求：

csharp

using System;

using System.Collections.Generic;

using System.IO;

using System.Linq;

using System.Net;

using System.Net.Http;

using System.Security.Cryptography;

using System.Text;

using System.Threading.Tasks;

using System.Web;

namespace ConsoleApp1

{

class Program

{

static void Main(string[] args)

{

Console.WriteLine("Start>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");

string HTTPMethod = "GET";

string Accept = "application/json";

string ContentType = "application/json";

// 應用 ApiAppKey

string ApiAppKey = "Your ApiAppKey";

//應用 ApiAppSecret

string ApiAppSecret = "Your ApiAppSecert";

string url = "https://xxxxxx.com/pudu-entry/data-open-platform-service/v1/api/healthCheck?b=${b}&a=${a}&c=${c}";

Uri uri = new Uri(url);

string host = uri.Host;

string path = uri.AbsolutePath;

Console.WriteLine("Url:{0}", url);

Console.WriteLine("Host:{0}", host);

// Without environmental information

if (path.StartsWith("/release"))

##### POST請求：

csharp

using System;

using System.Collections.Generic;

using System.IO;

using System.Linq;

using System.Net;

using System.Net.Http;

using System.Security.Cryptography;

using System.Text;

using System.Threading.Tasks;

using System.Web;

namespace ConsoleApp1

{

class Program

{

static void Main(string[] args)

{

Console.WriteLine("Start>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");

string HTTPMethod = "POST";

string Accept = "application/json";

string ContentType = "application/json";

// 應用 ApiAppKey

string ApiAppKey = "Your ApiAppKey";

//應用 ApiAppSecret

string ApiAppSecret = "Your ApiAppSecret";

string url = "https://xxxxxx.com/pudu-entry/data-open-platform-service/v1/api/healthCheck?b=${b}&a=${a}&c=${c}";

Uri uri = new Uri(url);

string host = uri.Host;

string path = uri.AbsolutePath;

Console.WriteLine("Url:{0}", url);

Console.WriteLine("Host:{0}", host);

// Without environmental information

if (path.StartsWith("/release"))

# 簽名生成和認證流程

## 前置條件

* 被呼叫的 API 的安全認證類型為“應用認證”。

* API 的呼叫方需要在呼叫 API 之前取得到對應 API 給應用的授權。

## 客戶端生成簽名

- 1.

  從原始請求中提取關鍵資料，得到一個用來簽名的字符串。

- 2.

  使用加密算法和 ApiAppSecret 對關鍵資料簽名串進行加密處理，得到簽名。

- 3.

  將簽名所相關的所有頭加入到原始 HTTP 請求中，得到最終 HTTP 請求。

## 計算簽名

客戶端從 HTTP 請求中提取出關鍵資料組裝成簽名串後，需要對簽名串進行加密及編碼處理，形成最終的簽名。步驟如下：

- 1.

  將簽名串（signing_str 簽名內容）使用 UTF-8 解碼後得到 Byte 數組。

- 2.

  使用加密算法對 Byte 數組進行加密。

- 3.

  使用 Base64 算法進行編碼，形成最終的簽名。

## 生成與傳遞簽名

### 提取簽名串

客戶端需要從 HTTP 請求中提取出關鍵資料，組合成一個簽名串。生成的簽名串的格式如下：

plain

Headers

HTTPMethod

Accept

Content-Type

Content-MD5

PathAndParameters

以上6個欄位構成整個簽名串，欄位之間使用 \n 間隔，Headers 必須包含 X-Date，PathAndParameters 後不需要加 \n，其他欄位如果為空都需要保留 \n。簽名大小寫敏感。每個欄位的提取規則如下：

* Headers：用戶可以選取指定的 Header 參與簽名。 參與簽名計算的 Header 的 Key 按照字典排序後使用如下方式拼接：

plain

HeaderKey1 + ": " + HeaderValue1 + "\n"\+

HeaderKey2 + ": " + HeaderValue2 + "\n"\+

...

HeaderKeyN + ": " + HeaderValueN + "\n"

Authorization 中 headers 位置填入的需要是參與計算簽名的 header 的名稱，並建議轉換為小寫，以 ascii 空格分隔。例如，參與計算的 header 為 date 和 source 時，此位置的形式為 headers="date source"；參與計算的 header 僅為 x-date 時，此位置的形式為 headers="x-date"。

* HTTPMethod：HTTP 的方法，全部大寫（如 POST）。

* Accept：請求中的 Accept 頭的值，可為空。建議顯示設置 Accept Header。當 Accept 為空時，部分 HTTP 客戶端會給 Accept 設置預設值為 */*，導致簽名校驗失敗。

* Content-Type：請求中的 Content-Type 頭的值，可為空。

* Content-MD5：請求中的 Content-MD5 頭的值，可為空只有在請求存在 Body 且 Body 為非 Form 形式時才計算Content-MD5 頭。Java 的 Content-MD5 值的參考計算方式如下：

plain

String content-MD5 = Base64.encodeBase64(MD5(bodyStream.getbytes("UTF-8")));

* PathAndParameters：包含 Path、Query 和 Form 中的所有參數，具體組織形式如下：

以一個普通的 HTTP 請求為例：

plain

POST / HTTP/1.1

host:service-3rmwxxxx-1255968888.cq.apigw.pudutech.com

accept:application/json

content-type:application/x-www-form-urlencoded

source:apigw test

x-date:Thu, 11 Mar 2021 08:29:58 GMT

content-length:8

p=test

生成的正確簽名串為：

plain

source: apigw test

x-date: Thu, 11 Mar 2021 08:29:58 GMT

POST

application/json

application/x-www-form-urlencoded

/?p=test

### 計算簽名

客戶端從 HTTP 請求中提取出關鍵資料組裝成簽名串後，需要對簽名串進行加密及編碼處理，形成最終的簽名。步驟如下：

- 1.

  將簽名串（signing_str 簽名內容）使用 UTF-8 解碼後得到 Byte 數組。

- 2.

  使用加密算法對 Byte 數組進行加密。

- 3.

  使用 Base64 算法進行編碼，形成最終的簽名。

### 傳輸簽名

客戶端需要將 Authorization 放在 HTTP 請求中傳輸給 API 網關，進行簽名校驗。  
Authorization header 格式如下：

plain

Authorization: hmac id="secret_id", algorithm="hmac-sha1", headers="date source", signature="Base64(HMAC-SHA1(signing_str, secret_key))"

Authorization 內各參數說明如下：

| 參數 | 說明 |
| --- | --- |
| hmac | 固定內容，用於標識計算方法 |
| ID | 其值為密鑰內的 secret_id 的值 |
| algorithm | 加密算法，當前支持的是 hmac-sha1 和 hmac-sha256 |
| headers | 參與簽名計算的 header |
| signature | 計算簽名後得到的簽名，signing_str 是簽名內容 |

攜帶簽名的完整 HTTP 請求的示例如下：

plain

POST / HTTP/1.1

host:service-3rmwxxxx-1255968888.cq.apigw.pudutech.com

accept:application/json

content-type:application/x-www-form-urlencoded

source:apigw test

x-date:Thu, 11 Mar 2021 08:29:58 GMT

Authorization:hmac id="xxxxxxx", algorithm="hmac-sha1", headers="source x-date", signature="xyxyxyxyxyxy"

content-length:8

p=test

## 簽名排錯方法

**問題描述：**  
API 網關簽名校驗失敗時，會將服務端的簽名串（StringToSign）放到 HTTP Response 的 Header 中回傳到客戶端，錯誤碼為401。

**解決方法：**

- 1.

  檢查本地計算的簽名串（StringToSign）與服務端回傳的簽名串是否一致。

- 2.

  檢查用於簽名計算的 ApiAppSecret 是否正確。  
  說明服務器的簽名是：

plain

source: apigw test

x-date: Thu, 11 Mar 2021 08:29:58 GMT

POST

application/json

application/x-www-form-urlencoded

/?p=test

# 呼叫機器呼叫範例

更新時間:2025-11-28 11:53:02

詳細介面、請求參數、回傳值含義請參考文檔：[【機器人任務】-【呼叫機器人】-【發起呼叫任務】](/zh/cloud-api/d5vkhidure8ibhw5a58bthp1)

## 以Go語言呼叫為例：

go

package main

import (

"crypto/hmac"

"crypto/md5"

"crypto/sha1"

"encoding/base64"

"encoding/hex"

"fmt"

"io/ioutil"

"log"

"net/http"

"net/url"

"sort"

"strings"

"time"

)

func main() {

// 應用 ApiAppKey

const ApiAppKey = "Your ApiAppKey"

//應用 ApiAppSecret

const ApiAppSecret = "Your ApiAppSecret"

// xxxxxx.com 請使用真實的普渡開放平台對外固定域名：比如測試環境 open-platform-test.pudutech.com

const Url = "https://xxxxxx.com/pudu-entry/open-platform-service/v1/custom_call"

const GmtFormat = "Mon, 02 Jan 2006 15:04:05 GMT"

const HTTPMethod = "POST"

const Accept = "application/json"

const ContentType = "application/json"

// 根據 Url 解析 Host 和 Path

u, err := url.Parse(Url)

if err != nil {

log.Fatal(err)

# 重點需替換為真實參數

go

// 應用 ApiAppKey

const ApiAppKey = "Your ApiAppKey"

//應用 ApiAppSecret

const ApiAppSecret = "Your ApiAppSecret"

const Url = "https://xxxxxx.com/pudu-entry/open-platform-service/v1/custom_call"

bodyStr := `{

"sn":"123",

"map_name":"map1",

"point":"table1",

"point_type":"table",

"call_device_name":"appKey",

"call_mode":"IMG",

"mode_data":{

"urls":["http://123.com/1.png","http://123.com/2.png"],

"switch_time":2,

"cancel_btn_time":1,

"show_timeout":30,

"qrcode":"",

"text":""

}

}`

# 呼叫抵達通知回呼示例

更新時間:2025-11-28 11:52:42

詳細介面、請求參數、回傳值含義請參考文檔:[【回呼通知】-【任務與執行回呼】-【notifyCustomCall-呼叫狀態通知】](/zh/cloud-api/a0btpzfq266i1z7658flbwnz)

普渡會呼叫用戶提供的地址，把呼叫狀態及時通知到用戶，具體就是發送以下資訊：

json

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

# 取得機器當前使用地圖呼叫範例

更新時間:2025-11-28 11:57:36

詳細介面、請求參數、回傳值含義請參考文檔：[【通用介面】-【地圖資訊】-【機器當前使用地圖】](/zh/cloud-api/bfqvp7meqi1wkjt3k4yitvuq)

## 以Go語言呼叫為例：

go

package main

import (

"crypto/hmac"

"crypto/md5"

"crypto/sha1"

"encoding/base64"

"encoding/hex"

"fmt"

"io/ioutil"

"log"

"net/http"

"net/url"

"sort"

"strings"

"time"

)

func main() {

// 應用 ApiAppKey

const ApiAppKey = "Your ApiAppKey"

//應用 ApiAppSecret

const ApiAppSecret = "Your ApiAppSecret"

// xxxxxx.com 請使用真實的普渡開放平台對外固定域名：比如測試環境 open-platform-test.pudutech.com

var Url = "https://xxxxxx.com/pudu-entry/map-service/v1/open/point?sn=${sn}&limit=${limit}&offset=${offset}"

Url = strings.ReplaceAll(Url, "${sn}", encode("123"))

Url = strings.ReplaceAll(Url, "${limit}", encode("10"))

Url = strings.ReplaceAll(Url, "${offset}", encode("0"))

const GmtFormat = "Mon, 02 Jan 2006 15:04:05 GMT"

const HTTPMethod = "GET"

const Accept = "application/json"

const ContentType = "application/json"

// 根據 Url 解析 Host 和 Path

# 重點需替換為真實參數

go

// 應用 ApiAppKey

const ApiAppKey = "Your ApiAppKey"

//應用 ApiAppSecret

const ApiAppSecret = "Your ApiAppSecret"

// xxxxxx.com 請使用真實的普渡開放平台對外固定域名：比如測試環境 open-platform-test.pudutech.com

var Url = "https://xxxxxx.com/pudu-entry/map-service/v1/open/point?sn=${sn}&limit=${limit}&offset=${offset}"

# 機器類型

更新時間:2025-11-07 14:31:02

| **機器類型** | **說明** |
| --- | --- |
| PuduBot | 歡樂送 |
| BellaBot | 貝拉 |
| HolaBot | 好啦 |
| Puductor | 歡樂消 |
| Puductor2 | 歡樂消 2 |
| KettyBot | 葫蘆 |
| FlashBot | 閃電匣 |
| CC1 | 出塵 |
| SwiftBot | 巧樂送 |
| PuduBot2 | 歡樂送 2 |
| PuduT300 | 瓦特 |
| KettyBotPro | 葫蘆 Pro |
| BellaBotPro | 貝拉 Pro |
| PuduSH1 | 獅虎 |
| MT1 | PUDU MT1 |
| MT1Vac | PUDU MT1 Vac |
| MT1Max | PUDU MT1 Max |
| CC1Pro | PUDU CC1 Pro |
| FlashBot2025 | 閃電匣2025 |
| FlashBotUltra | 閃電匣Ultra |
| FlashBotMax | 閃電匣Max |
| FlashBotPro | 閃電匣Pro |
| KettyBotPro(OSVersion) | 葫蘆Pro（OS版） |
| FlashBotLite | 閃電匣Lite |
| PuduT600 | T600 |
| PuduT600Underride | T600 潛伏版 |

# 資料中心指標定義

更新時間:2025-11-07 14:32:26

## 配送類各機器人支持的資料看板

基於各機器人的功能模式而定義

| 機器人/資料看板 Robot/Data Dashboard | 配送資料 Delivery data | 巡航資料 Cruise data | 領位資料 Escorting data | 互動資料 Interactive data | 攬客資料 Attract customer data | 宮格資料 Grid data | 廣告資料 Ad data | 回盤資料 Recycling dishes data |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 貝拉 BellaBot | √ | √ | √ | √ |  |  |  | √ |
| 葫蘆 KettyBot | √ | √ | √ | √ | √ | √ | √ | √ |
| 歡樂送 2 PuduBot 2 | √ | √ |  |  |  |  |  | √ |
| 歡樂送 PuduBot | √ | √ | √ |  |  |  |  | √ |
| 巧樂送 SwiftBot | √ | √ | √ |  |  |  |  |  |
| 好拉 PUDU HolaBot | √ | √ |  |  |  |  |  | √ |
| 閃電匣 FlashBot | √ |  | √ |  |  |  |  |  |

## 配送類機器人各個看板的資料欄位說明

### 巡航資料 Cruise data

| **欄位 Fields** | **看板報表解釋說明 Explanation** |
| --- | --- |
| 運行里程 Running Mileage(km) | 在日期範圍內，所選門市下所有綁定機器人的巡航運行總里程 Total mileage of cruise operations |
| 運行時長 Runtime(h) | 在日期範圍內，所選門市下所有綁定機器人的巡航運行總時長 Total duration of cruise operations |
| 互動人次 Interactive Visits | 在日期範圍內，所選門市下所有綁定機器人的互動總次數，包括：巡航時檢測到人時進入互動次數的次數、巡航時暫停進入互動次數 Total number of interactions during cruise |
| 互動時長 Interaction time(h) | 在日期範圍內，所選門市下所有綁定機器人的巡航過程中，發生的互動總時長 Total duration of interactions during the cruise process |

### 配送資料 Delivery data

| **欄位 Fields** | **看板報表解釋說明 Explanation** |
| --- | --- |
| 任務數 Number of tasks | 在日期範圍內，所選門市下所有綁定機器人的配送任務總數，從出發到達目的地，計為一次任務。返程不計為配送任務，計為返程任務 Total number of delivery tasks from departure to arrival at the destination |
| 運行里程 Running Mileage(km) | 在日期範圍內，所選門市下所有綁定機器人的配送運行總里程 Total mileage of delivery operations |
| 運行時長 Runtime(h) | 在日期範圍內，所選門市下所有綁定機器人的配送運行總時長 Total duration of delivery operations |
| 配送餐桌 Number of delivery tables | 在日期範圍內，所選門市下所有綁定機器人的配送餐桌數（即送達目的地數） Total number of tables delivered |
| 配送餐盤 Number of plates delivered | 在日期範圍內，所選門市下所有綁定機器人的配送餐盤數（即託盤數） Total number of trays delivered |

### 領位資料 Escorting data

| **欄位 Fields** | **看板報表解釋說明 Explanation** |
| --- | --- |
| 任務數 Number of tasks | 在日期範圍內，所選門市下所有綁定機器人的領位任務總數，從出發到達目的地，計為一次任務。返程不計為領位任務，計為返程任務 Total number of hostess tasks from departure to arrival at the destination |
| 運行里程 Running Mileage(km) | 在日期範圍內，所選門市下所有綁定機器人的領位運行總里程 Total mileage of hostess operations |
| 運行時長 Runtime(h) | 在日期範圍內，所選門市下所有綁定機器人的在日期範圍內，所選門市下所有綁定機器人的領位運行總時長 Total duration of hostess operations |
| 領位帶客次數 Number of tie-in passengers | 在日期範圍內，所選門市下所有綁定機器人的領位任務次數（即領位到達目的地數） Total number of hostess tasks reached their destination |

### 互動資料 Interactive data

| **欄位 Fields** | **看板報表解釋說明 Explanation** |
| --- | --- |
| 互動人次 Interactive Visits | 在日期範圍內，所選門市下所有綁定機器人的人機互動（觸摸、語音互動）的次數，包括：巡航攬客互動次數、定點攬客互動次數 Total number of human-robot interactions including cruise-based and fixed-point customer acquisition |
| 語音互動次數 voice interactions Number | 在日期範圍內，所選門市下所有綁定機器人的語音互動的次數 Total number of voice interactions |
| 語音互動時長 Voice interaction time(h) | 在日期範圍內，所選門市下所有綁定機器人的語音互動累計時長 Total accumulated duration of voice interactions |

### 攬客資料 Attract customer data

| **欄位 Fields** | **看板報表解釋說明 Explanation** |
| --- | --- |
| 任務數 Number of tasks | 在日期範圍內，所選門市下所有綁定機器人的攬客任務總數，從攬客開始到攬客結束，計為一次任務 Total number of customer acquisition tasks from start to end |
| 運行時長 Runtime(h) | 在日期範圍內，所選門市下所有綁定機器人的攬客運行總時長 Total duration of customer acquisition operations |
| 打招呼次數 greetings Number | 在日期範圍內，所選門市下所有綁定機器人的招攬話術播放次數 Total number of times the solicitation script was played |
| 觸達人次 reached people | 在日期範圍內，所選門市下所有綁定機器人的觸達用戶次數（即識別人腿數） Total number of user engagements (i.e., number of times people were detected) |
| 吸引人次 Attract people | 在日期範圍內，所選門市下所有綁定機器人的觸達用戶，且用戶駐足停留 5 秒及以上的人次數 Total number of instances where users stayed for 5 seconds or more after being reached |
| 互動人次 Interactive Visits | 在日期範圍內，所選門市下所有綁定機器人的被用戶喚醒的次數 Total number of times awakened by users |

### 宮格資料 Grid data

| **欄位 Fields** | **看板報表解釋說明 Explanation** |
| --- | --- |
| 帶我進店宮格 [Take me into the store] Number of clicks | 在日期範圍內，所選門市下所有綁定機器人的該類別功能被點擊的次數 Total number of times the feature in this category was clicked |
| 特色商品宮格 [featured item] number of clicks | 在日期範圍內，所選門市下所有綁定機器人的該類別功能被點擊的次數 Total number of times the feature in this category was clicked |
| 優惠活動宮格 [Promotions] Clicks | 在日期範圍內，所選門市下所有綁定機器人的該類別功能被點擊的次數 Total number of times the feature in this category was clicked |
| 領位宮格[Escorting] Clicks | 在日期範圍內，所選門市下所有綁定機器人的該類別功能被點擊的次數 Total number of times the feature in this category was clicked |
| 海報宮格[Poster] Clicks | 在日期範圍內，所選門市下所有綁定機器人的該類別功能被點擊的次數 Total number of times the feature in this category was clicked |
| 帶路宮格[Lead the way] Clicks | 在日期範圍內，所選門市下所有綁定機器人的該類別功能被點擊的次數 Total number of times the feature in this category was clicked |
| 跳舞宮格[Dance] Clicks | 在日期範圍內，所選門市下所有綁定機器人的該類別功能被點擊的次數 Total number of times the feature in this category was clicked |
| 視頻海報宮格[Video Poster] Clicks | 在日期範圍內，所選門市下所有綁定機器人的該類別功能被點擊的次數 Total number of times the feature in this category was clicked |

### 廣告資料 Ad data

| **欄位 Fields** | **看板報表解釋說明 Explanation** |
| --- | --- |
| 小屏廣告播放時長 Small screen play time(h) | 在日期範圍內，所選門市下所有綁定機器人的小屏廣告播放的時長 Total duration of small screen advertisements played |
| 小屏廣告播放次數 small screen plays | 在日期範圍內，所選門市下所有綁定機器人的小屏廣告播放的次數 Total number of times small screen advertisements were played |
| 大屏廣告播放時長 Large screen play time(h) | 在日期範圍內，所選門市下所有綁定機器人的大屏廣告播放的時長 Total duration of large screen advertisements played |
| 大屏廣告播放次數 Number of large screen plays | 在日期範圍內，所選門市下所有綁定機器人的大屏廣告播放的次數 Total number of times large screen advertisements were played |

### 回盤資料 Recycling dishes data

| **欄位 Fields** | **看板報表解釋說明 Explanation** |
| --- | --- |
| 任務數 Number of tasks | 在日期範圍內，所選門市下所有綁定機器人的回盤任務總數，從出發到最後一個達目的地，計為一次任務。返程不計為當前任務數，計為返程任務 Total number of return tasks from departure to the last destination reached. Return trips are not counted as current tasks, but rather as return tasks |
| 運行里程 Running Mileage(km) | 在日期範圍內，所選門市下所有綁定機器人的回盤運行總里程 Total mileage of return operations |
| 運行時長 Runtime(h) | 在日期範圍內，所選門市下所有綁定機器人的回盤運行總時長 Total duration of return operations |
| 清潔餐桌 Number of clean tables | 在日期範圍內，所選門市下所有綁定機器人的清潔回盤的餐桌次數 Total number of times tables were cleaned during return operations |

## 配送/回盤/領位任務明細欄位說明

| **Fields** | **Explanation** |
| --- | --- |
| Time 運行時間 | Start date of the robot's task execution 機器人開始任務的日期 |
| Product name 產品名稱 | Product name 機器人產品類型 |
| Robot nickname 機器暱稱 | Robot nickname 機器人產品暱稱 |
| SN/MAC | SN/MAC |
| Store name 門市名稱 | Store name to which the robot is assigned 機器人所綁定的門市名稱 |
| Store Installation Time 門市安裝時間 | Time when the robot was assigned to the store 機器人綁定在門市的時間 |
| Task start time 任務開始時間 | Time when the robot started the delivery task, recycling task, or escorting task. 機器人開始配送任務的時間 |
| Task destination 任務目的地 | The destination name(s) that the robot arrives at during task execution. If a task has multiple destinations, multiple destination names will be displayed. 機器人在當前任務中，到達的目的地名稱。如果一個任務有多個目的地，會顯示多條資料。 |
| Time of arrival at the destination 到達目的地時間 | The arrival time of the robot at each destination during the current task. ( If there is data in the "Task Destination" field but no data in the "Arrival Time at Destination" field, it indicates that the task was interrupted or halted before reaching the destination.) 1、機器人在當前任務中，到達目的地的時間 2、若存在“任務目的地”，但無“到達目的地時間”，則表示任務中途被中斷 |
| Duration of stay at the destination(s) 目的地逗留時長（S） | The duration of the robot's stay at the destination after reaching it in the current task. The duration is measured in seconds. ( The duration of the robot's stay at the destination after reaching it is only applicable for "Delivery Data" and "Return Data" fields.) 1、機器人在當前任務中，到達目的地後，停留時長。單位為秒。 2、只有“配送資料”和“回盤資料”存在該欄位。 |
| current destination travel duration(min) 到達目的地運行時長（min） | The running duration of the robot from the start of the current task to the arrival at the destination, measured in minutes. 機器人在當前任務中，開始任務時間至到達目的地的時長 |
| Current destination travel distance(m) 到達目的地運行里程（m） | The running distance of the robot from the starting position of the current task to the destination, measured in meters. 機器人在當前任務中，開始任務位置至到達目的地的運行里程 |

## 清潔資料報表欄位解釋說明

| **欄位 Fields** | **解釋說明 Explanation** |
| --- | --- |
| 清潔總面積 Total Cleaning Area (m²) | 單位（M2），選擇週期內綁定且激活的機器人清潔總面積，面積計算公式清潔時長（H）\*清潔寬度（M2）\*清潔速度（KM/H）。 The total cleaning area of robots bound and activated within the selected period is calculated using the formula: cleaning duration (H) \* cleaning width (M2) \* cleaning speed (KM/H). |
| 清潔總時長 Total Cleaning Time (h) | 單位（H），選擇週期內綁定且激活的機器人清潔總時長。 Total cleaning duration of robots bound and activated within the selected period. |
| 耗電情況 Power Consumption（KW\*H） | 單位（KW*H），選擇週期內的綁定且激活的機器人耗電情況，電量消耗 = 總百分比 \* 50AH \* 26V /1000 （KW*H）。 Power consumption of robots bound and activated within the selected period can be calculated using the formula: Energy consumption = total percentage \* 50AH \* 26V / 1000 (KW\*H). |
| 清潔任務數 Cleaning Task Count | 任務結束後，計為一次任務。任務按小時統計，當任務結束時候為非整點，則取結束任務時間的整點數。例如：任務結束時間是 18:06，即為 18:00 執行了一次完整的清潔任務。 After the completion of a task, it is counted as one task. Tasks are counted in hours, and if a task ends at a non-whole hour, the nearest whole hour is taken as the end time. For example, if a task ends at 18:06, it is considered as a complete cleaning task executed at 18:00. |
| 耗水量 Water Consumption(ml） | 洗地機器人特有資料項，單位（ML），不同模式的耗水量，下水模式的清潔時長（s）\*單位時間平均下水量（ML）。 Unique data item for floor scrubbing robots: water consumption in milliliters (ML). The water consumption for different modes is calculated by multiplying the cleaning duration in seconds for the mop mode by the average water consumption per unit time in milliliters (ML). |
| 清潔任務分佈 Distribution of Cleaning Task Execution | 選擇週期內固定拆分為 24 個小時，每個時間點包含執行任務的次數總和。例：1 號 1 點開始一個任務執行到了三點，那麼 1 號 1 點、2 點、3 點任務數各加一，2 號 1 點開始一個任務執行到 2 點，則 2 號 1 點、2 點任務數各加 1。可視化圖形 1 點任務數 2 個，2 點任務數 2 個，三點任務數 1 個。 Within the selected period, the fixed splitting is done into 24 hours, with each time point including the total sum of task executions. For example, if a task starts at 1:00 on the 1st and continues until 3:00, then the task count for 1:00, 2:00, and 3:00 is increased by one. If another task starts at 1:00 on the 2nd and continues until 2:00, then the task count for 1:00 and 2:00 on the 2nd is increased by one. The visualization graph would show 2 tasks at 1:00, 2 tasks at 2:00, and 1 task at 3:00. |

# 錯誤碼

更新時間:2025-11-28 11:43:01

## 鑑權常見錯誤提示

| **日誌中錯誤提示** | **說明** |
| --- | --- |
| HMAC signature does not match. | 簽名不一致。 |
| HMAC apikey is invalid for API. | APIKey 沒有綁定到該 API。 |
| HMAC signature cannot be verified, a valid x-date header is required for HMAC Authentication. | HMAC 認證時沒有在 header 中帶上 x-date，或者 HMAC 值非法。 |
| HMAC signature cannot be verified, the x-date header is out of date for HMAC Authentication. | x-date 時間戳超時，預設為 900s。 |
| HMAC signature cannot be verified, a valid date or x-date header is required. | 如果沒有 x-date，則 header 中包含 date。 |
| HMAC id or signature missing. | Authorization 中 ID 或者 signatrue 欄位缺失。 |
| HMAC do not support multiple HTTP header. | 不支持一個 header 包含多個值的形式。 |
| HMAC signature cannot be verified, a valid xxx header is required. | 請求中缺少 xxx header。 |
| HMAC algorithm xxx not supported. | HMAC 算法不支持 xxx，目前支持 hmac-sha1、hmac-sha256、hmac-sha384、hmac-sha512。 |
| HMAC authorization format error. | Authorization 格式錯誤。 |
| HMAC authorization headers is invalidate. | [Authorization 缺少足夠的參數，請參考 密鑰對認證-最終發送內容。] |
| HMAC signature cannot be verified. | 無法檢驗簽名，可能原因為 APIKey 無法識別，通常是 APIKey 沒有綁定到這個服務或者沒有綁定到這個 API。 |
| Oauth call authentication server fail. | 呼叫認證服務器失敗。 |
| Oauth found no related Oauth api. | 沒有查到關聯的 Oauth 認證 API，無法認證 id_token。 |
| Oauth miss Oauth id_token. | 請求缺少 id_token。 |
| Oauth signature cannot be verified, a validate authorization header is required. | 沒有認證頭部。 |
| Oauth authorization header format error. | Oauth 頭部格式錯誤。 |
| Oauth found no authorization header. | 沒有找到認證頭部。 |
| Oauth found no id_token. | 沒有找到 id_token。 |
| Oauth id_token verify error. | JWT 格式的 id_token 驗證失敗。 |
| Found no validate usage plan. | 沒有找到對應的使用計劃，禁止訪問（開啟使用計劃時可能出現的錯誤）。 |
| Cannot identify the client IP address, unix domain sockets are not supported. | 無法識別源 IP。 |
| Endpoint IP address is not allowed. | 禁止訪問的後端 IP。 |
| Get xxx params fail. | 從請求中取得參數出錯。 |
| need header Sec-WebSocket-Key. | 實際請求缺少 header Sec-WebSocket-Key，設定了 websocket 的 API 會檢驗。 |
| need header Sec-WebSocket-Version. | 實際請求缺少 header Sec-WebSocket-Version，設定了 websocket 的 API 會檢驗。 |
| header xxx is required. | 實際請求缺少 header xxx |
| path variable xxx is required. | 設定了路徑變量 {xxx} ，但是與實際請求的路徑不能匹配。 |
| querystring xxx is required. | 實際請求缺少 querystring xxx。 |
| req content type need application/x-www-form-urlencoded. | 設定了 body 參數的請求必須是表單格式。 |
| body param xxx is required. | 實際請求缺少 body 參數 xxx。 |
| Found no validate apiapp. | 當前 API 沒有綁定的應用認證密鑰。 |
| Not found micro service with key. | 沒有找到對應的微服務。 |
| Not Found Host. | 請求攜帶 host 欄位，該欄位值需要填服務器的域名，且為 String 類型。 |
| Get Host Fail. | 請求中攜帶的 host 欄位值不是 String 類型。 |
| Could not support method. | 並不支持該請求方法類型。 |
| There is no api match host[$host]. | 找不到請求服務器域名/地址。 |
| There is no api match env_mapping[$env_mapping]. | 自定義域名後的 env_mapping 欄位錯誤。 |
| There is no api match default env_mapping[$env_mapping]. | 預設域名後的 env_mapping 欄位需要是 test/prepub/release。 |
| There is no api match uri[$uri]. | 在該請求地址對應的服務下找不到對應 URI 匹配的 API。 |
| Not allow use HTTPS protocol 或者 Not allow use HTTP protocol. | 該請求地址對應的服務並不支持對應 HTTP 協議類型。 |
| Found no api. | 請求沒有匹配到 API。 |
| Method Not Allowed. | 不允許的 HTTP 請求方法。 |
| Not allow use HTTPS protocol. | 不允許用 HTTPS 協議。 |
| Not allow use HTTP protocol. | 不允許用 HTTP 協議。 |
| Not allow use xxx protocol. | 不允許用 xxx 協議。 |
| API rate limit exceeded. | 請求速率超過限速值，當前速率值可以查看請求的 header。 |
| API quota exceeded. | 設定超限，剩餘的配額可以透過請求的 header 查看。 |
| req is cross origin, api $uri need open cors flag on qcloud apigateway. | 該請求是跨域請求，但對應的 API 並未打開跨域開關。 |
| API config error. | API 設定錯誤。 |
| TSF config error. | TSF 相關設定錯誤。 |
| Get location of micro service info fail. | 沒有設定微服務名、微服務命名空間取得位置。 |
| Only support the map_from like method.req.{path}.{} | 設定了微服務名、微服務空間的拉取位置，但是位置格式非法。 |
| Found no valid cors config. | CORS 設定出錯。 |
| Oauth public key error. | 設定的公鑰證書錯誤。 |
| Oauth id_token location forbidden. | 不允許的 id_token 存放位置。 |
| path variable xxx is required. | 設定了路徑變量 {xxx} ，但是與實際請求的路徑不能匹配。 |
| querystring xxx is required. | 實際請求缺少 querystring xxx。 |
| req content type need application/x-www-form-urlencoded. | 設定了 body 參數的請求必須是表單格式。 |
| body param xxx is required. | 實際請求缺少 body 參數 xxx。 |
| Found no validate apiapp. | 當前 API 沒有綁定的應用認證密鑰。 |
| Not found micro service with key. | 沒有找到對應的微服務。 |
| Not Found Host. | 請求攜帶 host 欄位，該欄位值需要填服務器的域名，且為 String 類型。 |
| Get Host Fail. | 請求中攜帶的 host 欄位值不是 String 類型。 |
| Could not support method. | 並不支持該請求方法類型。 |
| There is no api match host[$host]. | 找不到請求服務器域名/地址。 |
| There is no api match env_mapping[$env_mapping]. | 自定義域名後的 env_mapping 欄位錯誤。 |
| There is no api match default env_mapping[$env_mapping]. | 預設域名後的 env_mapping 欄位需要是 test/prepub/release。 |
| There is no api match uri[$uri]. | 在該請求地址對應的服務下找不到對應 URI 匹配的 API。 |
| Not allow use HTTPS protocol 或者 Not allow use HTTP protocol. | 該請求地址對應的服務並不支持對應 HTTP 協議類型。 |
| Found no api. | 請求沒有匹配到 API。 |
| Method Not Allowed. | 不允許的 HTTP 請求方法。 |
| Not allow use HTTPS protocol. | 不允許用 HTTPS 協議。 |
| Not allow use HTTP protocol. | 不允許用 HTTP 協議。 |
| Not allow use xxx protocol. | 不允許用 xxx 協議。 |
| API rate limit exceeded. | 請求速率超過限速值，當前速率值可以查看請求的 header。 |
| API quota exceeded. | 設定超限，剩餘的配額可以透過請求的 header 查看。 |
| req is cross origin, api $uri need open cors flag on qcloud apigateway. | 該請求是跨域請求，但對應的 API 並未打開跨域開關。 |
| API config error. | API 設定錯誤。 |
| TSF config error. | TSF 相關設定錯誤。 |
| Get location of micro service info fail. | 沒有設定微服務名、微服務命名空間取得位置。 |
| Only support the map_from like method.req.{path}.{} | 設定了微服務名、微服務空間的拉取位置，但是位置格式非法。 |
| Found no valid cors config. | CORS 設定出錯。 |
| Oauth public key error. | 設定的公鑰證書錯誤。 |
| Oauth id_token location forbidden. | 不允許的 id_token 存放位置。 |
| Oauth found no oauth config. | 沒有找到 Oauth 設定。 |
| Oauth found no public key. | 沒有找到公鑰。 |
| Mock config error. | mock 的設定出錯。 |
| Client closed connection. | 客戶端主動中斷連接。 |
| ApiAppKey not relation company（OpenPlatform） | apiAppkey 沒有關聯代理商 |
| Forward address resolution failed（OpenPlatform） | 請求的 url 非法 |
| Illegal request URL（OpenPlatform） | 請求的 url 非法 |

## 開放介面常見錯誤碼

| **message** | **中文描述** |
| --- | --- |
| SUCCESS | 成功 |
| PARAM_ERROR | 參數錯誤 |
| SYSTEM_ERROR | 系統錯誤 |
| CLEANBOT_ROBOT_NO_EXISTS | 無法找到機器 |
| CLEANBOT_DB_ERROR | 資料庫出錯 |
| CLEANBOT_ROBOT_NOT_BIND | 機器沒綁定門市 |
| CLEANBOT_OPENPLATFORM_SERVER_ERROR | 呼叫雲中控服務出錯 |
| CLEANBOT_ROBOT_TIME_OUT | 機器回覆超時 |
| CLEANBOT_WAIT | 機器上個指令未處理完 |
| CLEANBOT_ROBOT_OFFLINE | 機器不在線 |
| CLEANBOT_ROBOT_MISMATCH | 機器不匹配無法調度 |
| CLEANBOT_MAC_ABNORMAL | mac 地址異常無法調度 |
| CLEANBOT_NO_SUCH_TASK_TYPE | 沒有該任務類型無法調度 |
| CLEANBOT_INVALID_OPERATION | 無效操作無法調度 |
| CLEANBOT_NOT_IN_THE_CHARGING_TASK | 不在任務中，無法調度 |
| CLEANBOT_CHARGING_TASK_CANNOT_BE_MODIFIED | 充電任務不可修改 |
| CLEANBOT_NOT_IN_THE_PAUSE_STATE | 不在暫停中無法調度 |
| CLEANBOT_TASK_IS_EMPTY | 任務為空無法調度 |
| CLEANBOT_TASK_NO_EXISTS | 機器沒有該任務無法調度 |
| CLEANBOT_INVALID_TASK_AREA | 任務區域不合法無法調度 |
| CLEANBOT_INSUFFICIENT_BATTERY_POWER | 電量不足無法調度 |
| CLEANBOT_FULL_DIRTY_WATER_OR_INSUFFICIENT_CONSUMABLES | 清水不足或者污水已滿或者耗材不足無法調度 |
| CLEANBOT_FAILED_TO_OBTAIN_CONSUMABLES | 耗材取得失敗無法調度 |
| CLEANBOT_INSUFFICIENT_CONSUMABLES | 耗材不足無法調度 |
| CLEANBOT_THE_CLEANING_MODE_IS_INCORRECT | 清潔模式不正確無法調度 |
| CLEANBOT_NOT_IN_THE_CLEANING_STATE | 不在清掃中無法調度 |
| CLEANBOT_MAP_LOST | 地圖丟失請重新保存任務 |
| CLEANBOT_NO_CLEANING_AREA | 沒有清潔區域 |
| CLEANBOT_CLEANING_AREA_LOST | 清潔區域丟失請進入編輯重新保存任務後再進行續掃任務 |
| CLEANBOT_CLEANING_AREA_ADDED | 清潔區域增加請重新保存任務 |
| CLEANBOT_CLEANING_AREA_CHANGED | 清潔區域變更請重新保存任務 |
| CLEANBOT_NO_LIFT_CONTROL | 沒有梯控無法進行跨樓層任務 |
| CLEANBOT_LIFT_CONTROL_LOST | 梯控丟失無法進行跨樓層任務 |
| CLEANBOT_RETURN_POINT_LOST | 返航點丟失 |
| CLEANBOT_ELEVATORS_CANNOT_BE_SHARED | 當前地圖與任務地圖存在無法共用的電梯,無法執行跨樓層任務！ |
| CLEANBOT_WORKSTATION/CHARGING_STATION_HAS_NOT_BEEN_ADDED | 該任務工作站/充電樁沒有添加請進入編輯重新保存任務後才能開始任務 |
| CLEANBOT_WORKSTATION/CHARGING_STATION_LOST | 工作站/充電樁丟失請進入編輯重新保存任務後才能開始任務 |
| CLEANBOT_LOST_LOCATION | 定位異常 |
| CLEANBOT_NORMAL | 空閒中 |
| CLEANBOT_GOTO_WORKSTATION_INIT | 前往工作站初始化 |
| CLEANBOT_GOTO_WORKSTATION_WAY | 前往工作站路上 |
| CLEANBOT_GOTO_WORKSTATION_PAUSE | 前往工作站暫停 |
| CLEANBOT_GOTO_WORKSTATION_CANCELED | 前往工作站取消 |
| CLEANBOT_GOTO_WORKSTATION_END | 前往工作站結束 |
| CLEANBOT_GOTO_WORKSTATION_GATE | 前往工作站過閘機 |
| CLEANBOT_GOTO_WORKSTATION_ELV | 前往工作站乘梯 |
| CLEANBOT_CHARGING_LINE | 充電中(插線) |
| CLEANBOT_CHARGING_STATION | 充電中(補給站) |
| CLEANBOT_DRAINING_IN_PROGRESS | 加排水中 |
| CLEANBOT_WORKSTATION_OTA_UPGRADE_IN_PROGRESS | 工作站 OTA 升級 |
| CLEANBOT_CLEANING_INIT_IN_PROGRESS | 清潔初始化 |
| CLEANBOT_CLEANING_PAUSED | 清潔暫停 |
| CLEANBOT_CLEANING_IN_PROGRESS | 清潔中 |
| CLEANBOT_CLEANING_CANCELED | 清潔取消 |
| CLEANBOT_CLEANING_EN_ROUTE | 清潔路上 |
| CLEANBOT_CLEANING_COMPLETED | 清潔完成 |
| CLEANBOT_CLEANING_IN_ELEVATOR | 清潔乘梯中 |
| CLEANBOT_CLEANING_IN_GATE | 清潔過閘機中 |
| CLEANBOT_CLEANING_AND_WATER_COLLECTION_PREPARATION_IN_PROGRESS | 清潔收水準備中 |
| CLEANBOT_CLEANING_AND_WATER_COLLECTION_IN_REVERSE | 清潔收水後退 |
| CLEANBOT_CLEANING_AND_WATER_COLLECTION_IN_FORWARD | 清潔收水前進 |
| CLEANBOT_CLEANING_AND_WATER_COLLECTION_IN_RECIPROCATING_MOTION | 清潔收水往復運動 |
| CLEANBOT_CLEANING_AND_WATER_COLLECTION_IN_PLACE | 清潔原地收水 |
| CLEANBOT_CLEANING_AND_WATER_COLLECTION_COMPLETED | 清潔收水完成 |
| CLEANBOT_RETURNING | 返航中 |
| CLEANBOT_RETURNING_CANCELLED | 返航取消 |
| CLEANBOT_RETURNING_PAUSED | 返航暫停 |
| CLEANBOT_RETURNING_INITIALIZATION | 返航初始化 |
| CLEANBOT_RETURNING_COMPLETED | 返航結束 |
| CLEANBOT_RETURN_THROUGH_THE_GATE | 返航過閘機中 |
| CLEANBOT_RETURN_THROUGH_THE_ELV | 返航乘梯中 |
| CLEANBOT_PILE_INIT | 對樁初始化 |
| CLEANBOT_PILE_OPERATION | 對樁中 |
| CLEANBOT_PILE_PAUSE | 對樁暫停 |
| CLEANBOT_PILE_CANCELLATION | 對樁取消 |
| CLEANBOT_PILE_END | 對樁結束 |
| CLEANBOT_PILE_REMOVAL_INIT | 脫樁初始化 |
| CLEANBOT_PILE_REMOVAL_PAUSE | 脫樁暫停 |
| CLEANBOT_PILE_REMOVAL_OPERATION | 脫樁中 |
| CLEANBOT_PILE_REMOVAL_CANCELLATION | 脫樁取消 |
| CLEANBOT_PILE_REMOVAL_END | 脫樁結束 |
| CLEANBOT_MANUAL_CLEANING_IN_PROGRESS | 手動清潔中 |
| CLEANBOT_MANUAL_DRAINAGE_IN_PROGRESS | 手動排污 |
| CLEANBOT_MANUAL_ROLLER_BRUSH_REPLACEMENT_IN_PROGRESS | 手動換滾刷 |
| CLEANBOT_SOFTWARE_OTA_UPGRADE_IN_PROGRESS | 軟件 OTA 升級 |
| CLEANBOT_MAPPING_IN_PROGRESS | 建圖中 |
| CLEANBOT_DEBUGGING_IN_PROGRESS | 調試 |
| CLEANBOT_CAN_DATA_LOSS | CAN 資料丟失 |
| CLEANBOT_ENCODER_DATA_LOSS | 編碼器資料丟失 |
| CLEANBOT_IMU_DATA_LOSS | IMU 資料丟失 |
| CLEANBOT_BATTERY_DATA_LOSS | 電池資料丟失 |
| CLEANBOT_LIDAR_DATA_LOSS | 激光雷達資料丟失 |
| CLEANBOT_MAKER_CAMERA_DATA_LOSS | maker 相機資料丟失 |
| CLEANBOT_FACE_CAMERA_DATA_LOSS | 人臉相機資料丟失 |
| CLEANBOT_RGBD_DATA_LOSS | RGBD 資料丟失 |
| CLEANBOT_ULTRASONIC_ANOMALY | 超聲波異常 |
| CLEANBOT_ULTRASONIC_DATA_LOSS | 超聲資料丟失 |
| CLEANBOT_REAR_RADAR_ANOMALY | 後視雷達異常 |
| CLEANBOT_MOTOR_PARAMETERS_ABNORMAL | 電機參數異常 |
| CLEANBOT_MOTOR_ROTATION_ABNORMAL | 電機轉動異常 |
| CLEANBOT_EMERGENCY_STOP_SWITCH_ABNORMAL | 急停開關異常 |
| CLEANBOT_MOTOR_COMMUNICATION_ABNORMAL | 電機通訊異常 |
| CLEANBOT_COLLISION_ABNORMAL | 碰撞異常 |
| CLEANBOT_LIFT_THE_HANDRAIL | 扶手抬起 |
| CLEANBOT_EMERGENCY_STOP_SWITCH_TRIGGERED | 急停開關觸發 |
| CLEANBOT_POSITIONING_ABNORMAL | 定位異常 |
| CLEANBOT_SOFTWARE_EXCEPTION | 軟件異常 |
| CLEANBOT_RUNTIME_EXCEPTION | 運行異常 |
| CLEANBOT_LOCATION_NOT_INITIALIZED | 定位未初始化 |
| CLEANBOT_TARGET_POINT_DOES_NOT_EXIST | 目標點不存在 |
| CLEANBOT_UNABLE_TO_PLAN_NAVIGATION_FOR_THE_TARGET_POINT | 目標點無法規劃導航 |
| CLEANBOT_ROBOT_UNKNOW_ERROR | 機器未知異常 |
| CLEANBOT_REPLANNING_FAILURE | 重規劃失敗... |
| CLEANBOT_RGBD_FALL_RISK | RGBD 跌落風險 |
| CLEANBOT_MAGNETIC_STRIP_FALL_RISK | 磁條跌落風險 |
| CLEANBOT_REFLECTIVE_PLATE_FALL_RISK | 反光板跌落風險 |
| CLEANBOT_SIDE_BRUSH_EXCEPTION | 邊刷異常 |
| CLEANBOT_ROLL_BRUSH_EXCEPTION | 滾刷異常 |
| CLEANBOT_FAN_EXCEPTION | 風機異常 |
| CLEANBOT_WATER_PUMP_EXCEPTION | 水泵異常 |
| CLEANBOT_ROLL_BRUSH_PUSH_ROD_EXCEPTION | 滾刷推杆異常 |
| CLEANBOT_DRAIN_VALVE_EXCEPTION | 排污閥異常 |
| CLEANBOT_CLEAR_WATER_VALVE_ABNORMAL | 清水閥異常 |
| CLEANBOT_DUST_PUSH_ROD_ABNORMAL | 塵推推杆異常 |
| CLEANBOT_CHARGING_ABNORMAL | 充電異常 |
| CLEANBOT_WORKSTATION_ABNORMAL | 工作站異常 |
| CLEANBOT_ELEVATOR_CONTROL_ABNORMAL | 梯控異常 |
| CLEANBOT_WORKSTATION_CONNECTION_ABNORMAL | 工作站連接異常 |
| CLEANBOT_THE_MAP_NAME_TO_SWITCH_TO_CANNOT_BE_EMPTY | 要切換的地圖名稱不能為空 |
| CLEANBOT_CURRENT_STATE_DOES_NOT_ALLOW_MAP_SWITCHING | 當前狀態不允許切換地圖 |
| CLEANBOT_CANNOT_SWITCH_TO_MAP | 非本機地圖，不支持切換 |
| CLEANBOT_RETURN_POINT_IS_EMPTY | 返航點為空，無法調度 |
| CLEANBOT_RETURN_POINT_THAT_IS_NOT_ON_THE_CURRENT_MAP | 非當前地圖返航點，無法調度 |
| CLEANBOT_MAP_HAS_NOT_ELEVATOR_CONTROL_UNABLE_TO_SWITCH_MAP | 當前地圖或者目標地圖未部署梯控，無法切換地圖 |
| CLEANBOT_CHARGING_PORT_ERROR | 充電口接觸不良，請重新插拔充電器 |
| CLEANBOT_CANNOT_REMOTE_TRIGGER_IN_DISTURB_MODE | 當前為勿擾時間段，不可遠程觸發任務 |
| CLOUD_OPEN_UNKNOW_ERROR | 未知錯誤 |
| CLOUD_OPEN_ROBOT_DB_ERROR | 資料庫出錯 |
| CLOUD_OPEN_ROBOT_PARAM_ERROR | 參數出錯 |
| CLOUD_OPEN_WAIT | 上個處理還未完成，需要等待 |
| CLOUD_OPEN_ROBOT_UNREGISTER | 機器未註冊到雲平台 |
| CLOUD_OPEN_TIMEOUT | 機器回覆超時 |
| CLOUD_OPEN_IOT_SEND_ERROR | 發送 iot 消息出錯 |
| CLOUD_OPEN_ROBOT_INFO_ERROR | 取得機器資訊出錯 |
| CLOUD_OPEN_ROBOT_NOT_EXISTS | 取得機器資訊為空，可能是沒綁定門市 |
| CLOUD_OPEN_GET_STATUS_ERROR | 取得機器狀態失敗 |
| CLOUD_OPEN_GET_ROBOT_MAC_ERROR | 取得機器 mac 失敗 |
| CLOUD_OPEN_ROBOT_OFFLINE | 機器不在線 |
| CLOUD_OPEN_CANNOT_SCHEDULE | 機器無法調度 |
| CLOUD_OPEN_ROBOT_IS_CHARGING | 機器充電中 |
| CLOUD_OPEN_NO_AVAILABLE_ROBOT | 無可用機器調度 |
| CLOUD_OPEN_ENTER_QUEUE_ERROR | 進入隊列出錯 |
| CLOUD_OPEN_CALL_ERROR | 呼叫機器出錯 |
| CLOUD_OPEN_ROBOT_EXEC_FAIL | 機器回覆無法執行任務 |
| CLOUD_OPEN_CHECK_QUEUE_FAIL | 檢測隊列出錯 |
| CLOUD_OPEN_CALL_WITCH_ROBOT | 隨即呼叫正在切換機器 |
| CLOUD_OPEN_QUEUE_OVER | 機器狀態轉為不可呼叫提前結束排隊任務 |
| CLOUD_OPEN_TASK_NOT_EXISTS | 任務不存在 |
| CLOUD_OPEN_TASK_BELONG_ERROR | 無權操作任務 |
| CLOUD_OPEN_UNABLE_CANCEL_TASK | 無法取消任務 |
| CLOUD_OPEN_QUEUE_CANCEL_FAIL | 取消任務出錯 |
| CLOUD_OPEN_QUEUE_LIMIT | 超出呼叫數量 |
| CLOUD_OPEN_TASK_EXPIRED | 任務超時自動結束 |
| CLOUD_OPEN_UNABLE_COMPLETE_TASK | 無法完成任務 |
| CLOUD_OPEN_ROBOT_RSP_ERROR | 機器應答消息結構錯誤 |
| CLOUD_OPEN_SCREEN_CONTENT_LEN_ERR | 設置頁面顯示內容參數長度有誤 |
| CLOUD_OPEN_ROBOT_BELONG_ERROR | 無權操作機器 |

## 清潔機器狀態碼

| **狀態** | **狀態值** | **支持的操作** | **是否可調度** | **是否工作** | **描述** |
| --- | --- | --- | --- | --- | --- |
| Error | -100 |  | 否 | true | 錯誤，具體異常 detail 欄位 |
| LostLoaction | -200 |  | 否 | false | 定位異常 |
| Notice | -300 |  | 否 | false | 提示警告 |
| Normal |  | 可下達指令 | 是 | false | 空閒中 |
| GotoPileIdle | 100 |  | 是 | true | 前往工作站初始化 |
| GotoPileWay | 102 | 可暫停 | 是 | true | 前往工作站路上 |
| GotoPilePause | 101 | 可恢復/可取消 | 是 | true | 前往工作站暫停 |
| GotoPileCancel | 104 |  | 是 | true | 前往工作站取消 |
| GotoPileEnd | 105 |  | 是 | true | 前往工作站結束 |
| GotoPileGate | 106 |  | 是 | true | 前往工作站過閘機 |
| GotoPileElv | 107 |  | 是 | true | 前往工作站乘梯 |
| ChargingLine | 201 |  | 是 | true | 充電中(插線) |
| ChargingPile | 202 | 可下達指令 | 是 | true | 充電中(補給站) |
| WorkSpaceWaterSupply | 203 |  | 是 | true | 加排水中 |
| PileOTA | 204 |  | 是 | true | 工作站 OTA 升級 |
| VacuumIdle | 300 |  | 是 | true | 清潔初始化 |
| VacuumPause | 301 | 可恢復/可取消 | 是 | true | 清潔暫停 |
| Vacuuming | 302 | 可暫停 | 是 | true | 清潔中 |
| VacuumCancel | 303 |  | 是 | true | 清潔取消 |
| VacuumWay | 304 |  | 是 | true | 清潔路上 |
| VacuumingEnd | 311 |  | 是 | true | 清潔完成 |
| VacuumElv | 312 |  | 是 | true | 清潔乘梯中 |
| VacuumGoGate | 313 |  | 是 | true | 清潔過閘機中 |
| FinishingPrepare | 305 |  | 是 | true | 清潔收水準備中 |
| FinishingBack | 306 | 可暫停 | 是 | true | 清潔收水後退 |
| FinishingForward | 307 | 可暫停 | 是 | true | 清潔收水前進 |
| FinishingShortLine | 308 | 可暫停 | 是 | true | 清潔收水往復運動 |
| FinishingFinishing | 309 |  | 是 | true | 清潔原地收水 |
| FinishingFinished | 310 |  | 是 | true | 清潔收水完成 |
| ReturnWay | 400 | 可暫停 | 是 | true | 返航中 |
| ReturnCancel | 401 |  | 是 | true | 返航取消 |
| ReturnPause | 402 | 可恢復/可取消 | 是 | true | 返航暫停 |
| ReturnIdle | 403 |  | 是 | true | 返航初始化 |
| ReturnEnd | 404 |  | 是 | true | 返航結束 |
| ReturnGate | 405 |  | 是 | true | 返航過閘機中 |
| ReturnElv | 406 |  | 是 | true | 返航乘梯中 |
| DockPileIdle | 500 |  | 是 | true | 對樁初始化 |
| DockPileing | 501 |  | 是 | true | 對樁中 |
| DockPilePause | 502 |  | 是 | true | 對樁暫停 |
| DockPileCancel | 503 |  | 是 | true | 對樁取消 |
| DockPileEnd | 504 |  | 是 | true | 對樁結束 |
| PileLeaveIdle | 600 |  | 是 | true | 脫樁初始化 |
| PileLeavePause | 601 |  | 是 | true | 脫樁暫停 |
| PileLeaving | 602 |  | 是 | true | 脫樁中 |
| PileLeaveCancel | 603 |  | 是 | true | 脫樁取消 |
| PileLeaveEnd | 604 |  | 是 | true | 脫樁結束 |
| ManualVacuuming | 710 |  | 是 | true | 手動清潔中 |
| HandDrainSwedge | 720 |  | 是 | true | 手動排污 |
| HandShiftBrush | 730 |  | 是 | true | 手動換滾刷 |
| AppOTA | 740 |  | 是 | true | 軟件 OTA 升級 |
| Mapping | 750 |  | 是 | true | 建圖中 |
| Testing | 760 |  | 是 | true | 調試 |

## 資料中心錯誤碼

| **錯誤碼** | **說明** |
| --- | --- |
| PARAM_ERROR | 參數錯誤，請根據 API 文檔檢查入參 |
| ACCOUNT_ERROR | 賬號異常，請檢查賬號和鑑權參數 |
| SYSTEM_ERROR | 系統異常，請稍後重試 |
| DATA_NOT_EXIST | 資料不存在 |
| DATABASE_ERROR | 資料庫異常，請稍後重試 |

# Locale枚舉

更新時間:2025-11-07 14:34:56

| **值** | **說明** |
| --- | --- |
| zh-CN | 中文 |
| zh-TW | 繁體中文 |
| en-US | 英語 |
| ja-JP | 日語 |
| ko-KR | 韓語 |
| de-DE | 德國 |
| fr-FR | 法國 |
| ru-RU | 俄羅斯 |
| es-ES | 西班牙語 |
| th-TH | 泰語 |

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

json

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

# 機器綁定門市通知-robotBinding

更新時間:2025-11-17 21:04:34

## 1、說明

### 功能描述

在雲平台操作機器綁定門市後，機器的生命週期狀態會由【unbind(未綁定)】更新為【unactivated(待激活)】的狀態，同時透過該回呼消息通知開發者。

### 適用範圍

* **支援機型**：ALL

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：robotBinding |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器sn |
| name | string | 機器暱稱 |
| shop_id | int32 | 門市id |
| timestamp | int64 | 通知時間，時間戳秒 |

## 3、呼叫範例

json

{

"callback_type": "robotBinding",

"data": {

"sn": "SV10111....",

"shop_id": 1001,

"timestamp": 1699364274

}

}

# 機器解綁門市通知-robotUnBinding

更新時間:2025-11-17 21:05:37

## 1、說明

### 功能描述

在雲平台上操作機器解綁門市後，機器的生命週期狀態會由【normal(待激活)】更新為【unbind(未綁定)】的狀態，同時透過該回呼消息通知開發者。

### 適用範圍

* **支援機型**：ALL

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：robotUnBinding |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器sn |
| timestamp | int64 | 通知時間，時間戳秒 |

## 3、呼叫範例

json

{

"callback_type": "robotUnBinding",

"data": {

"sn": "SV10111....",

"timestamp": 1699364274

}

}

# 機器激活通知-robotActivate

更新時間:2025-11-28 11:55:16

## 1、說明

### 功能描述

機器在綁定門市後，首次重啟，或者在機器的激活頁面上點擊【激活】按鈕之後，機器的生命週期狀態會由【unactivated(待激活)】更新為【normal(已激活)】的狀態，同時透過該回呼消息通知開發者。

### 適用範圍

* **支援機型**：ALL

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：robotActivate |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器sn |
| timestamp | int64 | 通知時間，時間戳秒 |

## 3、呼叫範例

json

{

"callback_type": "robotActivate",

"data": {

"sn": "SV10111....",

"timestamp": 1699364274

}

}

# 機器在線_離線狀態變更通知-robotStatus

更新時間:2025-11-17 21:05:27

## 1、說明

### 功能描述

機器連接上雲平台後，雲平台會給開發者推送機器在線的通知。

當機器斷網、斷電後，雲平台檢測到機器離線，會給開發者推送機器離線的通知。但是並非機器斷網後就立即通知，要取決於機器來不來得及主動和雲平台斷開連接，如果沒來得及斷開連接就需要等雲端檢測到機器的心跳超時，一般需要3-5分鐘。

### 適用範圍

* **支援機型**：ALL

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：robotStatus |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器sn |
| run_status | string | 機器運行狀態：online、offline |
| timestamp | int64 | 時間戳秒 |

## 3、呼叫範例

json

{

"callback_type": "robotStatus",

"data": {

"sn": "SV10111....",

"run_status": "online",

"timestamp": 1699364274

}

}

# 急停恢復通知-robotEmergencyRecover

更新時間:2025-12-17 10:07:31

## 1、說明

### 功能描述

機器按下急停按鈕之後，再恢復會透過該回呼通知開發者。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、BellaBot Pro、PuduT300

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：robotEmergencyRecover |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器sn |
| mac | string | 機器mac |
| timestamp | int64 | 時間戳秒 |

## 3、呼叫範例

json

{

"callback_type": "robotEmergencyRecover",

"data": {

"sn":"OP21321dsffsd",

"mac":"AA:AA:AA:AA:AA:AA",

"timestamp": 1764325632 // 當前時間戳，秒，

}

}

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

# 地圖資訊(元素點)上傳_變更_刪除-mapElementChange

更新時間:2025-12-29 17:17:12

## 1、說明

### 功能描述

機器端地圖管理工具，修改地圖後，點擊同步雲端，雲端檢測到地圖發生變化，則會透過該回呼通知開發者。

### 適用範圍

* **支援機型**：ALL

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：mapElementChange |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| timestamp | int32 | 通知時間，時間戳秒 |
| shop_id | int32 | 門市id |
| map_name | string | 地圖名稱 |

## 3、呼叫範例

json

{

"callback_type": "mapElementChange",

"data": {

"map_name": "map123",

"shop_id": 1001,

"timestamp": 1699364274

}

}

# 機器位置上報-notifyRobotPose

更新時間:2025-11-17 21:03:41

## 1、說明

### 功能描述

開發者透過開放介面[【控制指令】-【地圖與位置】-【通知機器上報位置】](/zh/cloud-api/cl4mlqsqsz5xo7lpos124se2)給機器下達上報指令後，機器會按參數的上報頻率和上報次數進行上報實時位置，機器上報後會透過該回呼通知開發者。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、KettyBot Pro、BellaBot Pro、PuduT300

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyRobotPose |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| x | float | x座標 |
| y | float | y座標 |
| yaw | float | 角度 |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int32 | 當前時間戳秒 |
| notify_timestamp | long | 機器上報的時間戳，毫秒，開發者可用於做亂序消息過濾 |

## 3、呼叫範例

json

{

"callback_type": "notifyRobotPose",

"data": {

"x":1.234,

"y":2.345,

"yaw":32.34,

"sn":"OP21321dsffsd",

"mac":"AA:AA:AA:AA:AA:AA",

"timestamp": 1764325632, // 當前時間戳，秒，

"notify_timestamp" :1764325632000 //機器上報的時間戳 毫秒

}

}

# 機器移動狀態通知-notifyRobotMoveState

更新時間:2025-12-24 10:16:27

## 1、說明

### 功能描述

機器做任務時會透過該回呼通知開發者機器的移動狀態

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、KettyBot Pro、BellaBot Pro、PuduT300

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
| state | string | 機器人的運動狀態通知： IDLE :空閒 MOVING :運動中 STUCK :被障礙物阻擋 APPROACHING ：快抵達目標點 ARRIVE ：抵達目標點 PAUSE ：暫停 AVOID ：與其他機器人進行調度 |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int32 | 當前時間戳秒 |
| notify_timestamp | long | 機器上報的時間戳，毫秒，開發者可用於做亂序消息過濾 |

## 3、呼叫範例

json

{

"callback_type": "notifyRobotMoveState",

"data": {

"state":"IDLE",

"sn":"OP21321dsffsd",

"mac":"AA:AA:AA:AA:AA:AA",

"timestamp": 1764325632, // 當前時間戳，秒，

"notify_timestamp" :1764325632000 //機器上報的時間戳 毫秒

}

}

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

json

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

# 訂單通知-notifyRobotOrderState

更新時間:2025-11-17 21:03:27

## 1、說明

### 功能描述

該介面是為了兼容舊開放平台(SDK微服務)的開放介面而提供，新版本機型不再支持該介面。

### 適用範圍

* **支援機型**：Flashbot

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyRobotOrderState |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| order_state | string | 分別會有三種狀態， START為開始送餐， CANCEL為取消任務， COMPLETED為完成任務 |
| employee_id | string | 下單員工 |
| ids | **Array<object>** | 訂單集合 |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 當前時間戳秒 |
| notify_timestamp | long | 機器上報的時間戳，毫秒，開發者可用於做亂序消息過濾 |

### Params.data.ids

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| id | string | 訂單的唯一id |
| spend_time | int32 | 開始到取消狀態或完成狀態花費的時間，單位：毫秒 |

## 3、呼叫範例

json

{

"callback_type": "notifyRobotOrderState",

"data": {

"order_state": "START",//START、CANCEL、COMPLETED

"employee_id": "PD001",

"ids": [{

"id":"order001", //orderId

"spend_time":1000 //ms

}],

"sn":"OP21321dsffsd",

"mac":"AA:AA:AA:AA:AA:AA",

"timestamp": 1764325632, // 當前時間戳，秒，

"notify_timestamp" :1764325632000 //機器上報的時間戳 毫秒

}

}

# 機器人點位配送通知-robotDeliveryStatus

更新時間:2025-11-17 21:04:44

## 1、說明

### 功能描述

歡樂送2定製功能，機器在執行任務時，會上報任務中每個點位的狀態。

### 適用範圍

* **支援機型**：Pudubot2

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：robotDeliveryStatus |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_id | string | 任務id |
| task_name | string | 任務名稱 |
| status | string | BEGIN:開始任務 INTERRUP:任務中斷 END:任務結束 |
| task_time | long | 發生任務變化時間，時間戳秒 |
| remark | string | 備註(eg:中斷原因) |
| map_name | string | 當前地圖名稱 |
| points | **Array<object>** | 地圖點位集合 |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 當前時間戳秒 |
| notify_timestamp | long | 機器上報的時間戳，毫秒，開發者可用於做亂序消息過濾 |

### Params.data.points

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| point_name | string | 點位名稱 |
| point_status | string | 點位狀態 AWAIT :等待中 ON_THE_WAY :當前前往中 ARRIVED :已配送到達 CANCEL :配送取消 COMPLETED ：已配送完成 |
| point_type | string | 點位類型 |

## 3、呼叫範例

json

{

"callback_type": "robotDeliveryStatus",

"data": {

"task_id": "taskId1",//START、CANCEL、COMPLETED

"task_name": "taskName",

"status": "BEGIN",//BEGIN:開始任務 INTERRUP:任務中斷 END:任務結束

"task_time": 1699364274,

"remark": "中斷原因",

"map_name": "map001",

"points": [{

"point_name": "pointName",

"point_status": "AWAIT",//點位狀態 AWAIT :等待中 ON_THE_WAY :當前前往中 ARRIVED :已配送到達 CANCEL :配送取消 COMPLETED ：已配送完成

"point_type": "pointType"

}],

"sn":"OP21321dsffsd",

"mac":"AA:AA:AA:AA:AA:AA",

"timestamp": 1764325632, // 當前時間戳，秒

"notify_timestamp" :1764325632000 //機器上報的時間戳 毫秒

}

}

# 工業場景運送通知-notifyTransportTask

更新時間:2025-11-17 21:04:16

## 1、說明

### 功能描述

歡2定製功能，主要用於工廠配送，開發者呼叫[【機器人任務】-【運送任務】](/zh/cloud-api/chzlhyuuf0p2giogmpmbxr8s)後，機器會透過該回呼通知任務的狀態。

### 適用範圍

* **支援機型**：Pudubot2

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyTransportTask |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **欄位** | **類型** | **描述** |
| --- | --- | --- |
|  | **Array<object>** | 任務起始點狀態資訊，結構同trays |
| delivery_mode | string | 配送模式： GENERAL(普通), DIRECT（直達）, BIRTHDAY（生日）, SEPECIAL（特殊） |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 當前時間戳秒 |
| notify_timestamp | long | 機器上報的時間戳，毫秒，開發者可用於做亂序消息過濾 |
| trays | **Array<object>** | 對應的託盤數組 |

### Params.data.start_point/trays

| **欄位** | **類型** | **描述** |
| --- | --- | --- |
| destinations | **Array<object>** | 每個託盤上的目標任務 |

### Params.data.trays.destination

| **欄位** | **類型** | **描述** |
| --- | --- | --- |
| destination | string | 目標點：該值是使用透過“取得機器人的地圖目標點”得到的目標點的name |
| type | string | 任務類型： REMOTE：遠程發送的任務 MANUAL：機器上手動編輯的任務 |
| id | string | 任務id，如果透過“給機器人發送配送任務”來執行機器人任務時帶有任務id，機器人會將就收到的id透過該欄位通知開發者 |
| status | string | 任務狀態 AWAIT: 等待執行 ON_THE_WAY：配送中 ARRIVED：抵達 CANCEL: 取消 COMPLETE：完成 |
| estimated_time | Long | 預估抵達花費時間，當任務開始狀態為ON_THE_WAY時，會計算當前執行任務的花費時間，單位：ms（該時是執行開始執行任務時根據距離與設定速度計算的，可能因為機器人運行中遇到的障礙物導致該值不準確） |
| spend_time | Long | 配送狀態改變一共花費的時間，從第一個任務的ON_THE_WAY開始計時，到該任務COMPLETE結束該任務計時。單位：ms |
| complete_type | string | 機器人完成任務有多種形式，該欄位會回傳機器人抵達後是怎麼完成任務的： TIMEOUT：抵達後超時完成任務 MANUAL：手動點擊操作完成 REMOTE：遠程控制完成 QRCODE：二維碼掃碼完成 TRAY_EMPTY：託盤檢測空自動完成 |
| timeout | bool | 在任意一點位，trays欄位裡面的items在每次ARRIVED狀態持續超過任務下達的時候的wait_time，此標識為true; start_point欄位裡的items在放置物品的時候是否超過wait_time的值 |

## 3、呼叫範例

json

{

"callback_type": "notifyTransportTask",

"data": {

"delivery_mode": "GENERAL",

"sn":"OP21321dsffsd",

"mac":"AA:AA:AA:AA:AA:AA",

"timestamp": 1764325632, // 當前時間戳，秒

"notify_timestamp" :1764325632000, //機器上報的時間戳 毫秒

"trays": [

{

"destinations": [

{

"destination": "A1",

"type": "REMOTE/MANUAL",

"id": "任務id，狀態同步時會回執",

"estimated_time": 60000,

"spend_time": 80000,

"status": "AWAIT/ON_THE_WAY/ARRIVED/CANCEL/COMPLETE",

"timeout": false,

"complete_type": "REMOTE"

}

]

}

],

"start_point": [

{

"destinations": [

{

"destination": "A1",

"type": "REMOTE/MANUAL",

"id": "任務id，狀態同步時會回執",

"estimated_time": 60000,

"spend_time": 80000,

"status": "AWAIT/ON_THE_WAY/ARRIVED/CANCEL/COMPLETE",

"timeout": false,

"complete_type": "REMOTE"

# 配送任務通知-notifyDeliveryTask

更新時間:2025-11-17 21:01:55

## 1、說明

### 功能描述

開發者呼叫[【機器人任務】-【配送任務】](/zh/cloud-api/rbhjd42vj0rt5h31ib195vfx)後，機器會透過該回呼通知上報任務狀態

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、KettyBot Pro、BellaBot Pro、PuduT300、BellaBot、Flashbot、Pudu Bot2

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyDeliveryTask |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **欄位** | **類型** | **描述** |
| --- | --- | --- |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 服務端推送出來的時間戳秒 |
| delivery_mode | string | 配送模式： GENERAL(普通), DIRECT（直達）, BIRTHDAY（生日）, SEPECIAL（特殊） |
| task_id | string | 任務id |
| notify_timestamp | long | 機器通知的時間戳，毫秒 |
| is_over_time | bool | 是否超時 true,false |
| spent_time | int | 任務花費時間 |
| trays | **Array<object>** | 對應的託盤數組 |

### Params.data.trays

| **欄位** | **類型** | **描述** |
| --- | --- | --- |
| destinations | **Array<object>** | 每個託盤上的目標任務 |

### Params.data.trays.destinations

| **欄位** | **類型** | **描述** |
| --- | --- | --- |
| destination | string | 目標點：該值是使用透過“取得機器人的地圖目標點”得到的目標點的name |
| type | string | 任務類型： REMOTE：遠程發送的任務 MANUAL：機器上手動編輯的任務 |
| id | string | 任務id，如果透過“給機器人發送配送任務”來執行機器人任務時帶有任務id，機器人會將就收到的id透過該欄位通知開發者 |
| status | string | 任務狀態 AWAIT: 等待執行 ON_THE_WAY：配送中 ARRIVED：抵達 CANCEL: 取消 COMPLETE：完成 |
| estimated_time | Long | 預估抵達花費時間，當任務開始狀態為ON_THE_WAY時，會計算當前執行任務的花費時間，單位：ms（該時是執行開始執行任務時根據距離與設定速度計算的，可能因為機器人運行中遇到的障礙物導致該值不準確） |
| spend_time | Long | 配送狀態改變一共花費的時間，從第一個任務的ON_THE_WAY開始計時，到該任務COMPLETE結束該任務計時。單位：ms |
| complete_type | string | 機器人完成任務有多種形式，該欄位會回傳機器人抵達後是怎麼完成任務的： TIMEOUT：抵達後超時完成任務 MANUAL：手動點擊操作完成 REMOTE：遠程控制完成 QRCODE：二維碼掃碼完成 TRAY_EMPTY：託盤檢測空自動完成 |
| timeout | bool | 在任意一點位，trays欄位裡面的items在每次ARRIVED狀態持續超過任務下達的時候的wait_time，此標識為true; start_point欄位裡的items在放置物品的時候是否超過wait_time的值 |
| map_info | **Object** | 點位所屬地圖 |

### Params.data.trays.destinations.map_info

| **欄位** | **類型** | **描述** |
| --- | --- | --- |
| map_name | string | 地圖名稱 |

## 3、呼叫範例

json

{

"callback_type": "notifyDeliveryTask",

"data": {

"delivery_mode": "GENERAL",

"sn":"SV1111.....",

"mac":"mac",

"timestamp": 1699364274,

"notify_timestamp": 1699364274000,

"is_over_time":false,

"spent_time":100,

"task_id":"111111111",

"trays": [

{

"destinations": [

{

"destination": "A1",

"type": "REMOTE/MANUAL",

"id": "任務id，狀態同步時會回執",

"estimated_time": 60000,

"spend_time": 80000,

"status": "AWAIT/ON_THE_WAY/ARRIVED/CANCEL/COMPLETE",

"timeout": false,

"complete_type": "REMOTE",

"map_info":{"map_name":"地圖名稱"}

}

]

},

{

"destinations": [

{

"destination": "A1",

"type": "REMOTE/MANUAL",

"id": "任務id，狀態同步時會回執",

"estimated_time": 60000,

"spend_time": 80000,

"status": "AWAIT/ON_THE_WAY/ARRIVED/CANCEL/COMPLETE",

# 跑腿任務通知-notifyErrandStatus

更新時間:2025-11-17 21:02:27

## 1、說明

### 功能描述

機器在進行跑腿任務時，會透過該回呼通知機器執行任務中的狀態。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyErrandStatus |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 當前時間戳秒 |
| session_id | string | 總任務id |
| auth | string | 授權碼，下達任務時指定 |
| task_type | string | 任務類型： REMOTE：遠程下達 MANUAL：本地手動下達 |
| task_time | int | 任務下達的時間戳，秒 |
| notify_timestamp | long | 機器上報的時間戳，毫秒，開發者可用於做亂序消息過濾 |
| tasks | **Array<object>** | 跑腿任務 |

### Params.data.tasks

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| task_id | string | 任務id |
| task_name | string | 子任務名稱,機器上報狀態時會用這個 |
| task_status | string | 子任務狀態： AWAIT:等待 ONGOING:進行中 CANCEL:取消 COMPLETE:完成 FAIL:失敗 OUT_OF_STOCK:缺貨 TAKE_ADVANCE:提前取出 RETURN_SUCCESS:退回成功 RETURN_FAIL:退回失敗 |
| point_list | **Array<object>** | 點位集合 |

### Params.data.tasks.point_list

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| map_name | string | 地圖名稱 |
| map_code | string | 地圖code |
| point | string | 點位id/名稱 |
| point_type | string | 點位類型，table.... |
| point_status | string | 點位狀態： AWAIT :等待中 ON_THE_WAY :前往中 ARRIVED :到達 CANCEL:取消 COMPLETE :完成 |
| verification_code | string | 點位驗證碼，下達任務時可以指定 |

## 3、呼叫範例

json

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

# 頂升任務通知-notifyLiftingTask

更新時間:2025-11-17 21:02:44

## 1、說明

### 功能描述

機器在執行頂升任務時，機器會透過該回呼通知任務狀態。

### 適用範圍

* **支援機型**：PuduT300

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyLiftingTask |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 服務推送通知的時間戳，秒 |
| notify_timestamp | long | 機器上報的時間戳，業務端可用於做亂序消息處理，毫秒 |
| task_id | string | 總任務id |
| task_status | string | 總任務狀態，ON_THE_WAY 機器執行任務中、CANCEL 取消任務、FAILED(機器回傳拒絕任務時，雲端自己更新)、COMPLETED 完成任務、PAUSE 任務暫停中、STARTING 正在給機器發送任務中 |
| tasks | **Array<object>** | 子任務集合 |

### Params.data.tasks

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| status | string | 子任務狀態AWAIT:等待執行ON_THE_WAY:執行中COMPLETE:已完成CANCEL:被取消 |
| points | **Array<object>** | 所有點位集合 |

### Params.data.tasks.points

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| map_info | **object** | 點位所屬地圖 |
| point_name | sting | 點位名稱 |
| point_type | string | 點位類型，點位和貨架組POINT、SECONDARY_GROUP |
| point_attr | string | 點位屬性：取貨點、途徑點、放貨點DROP_POINT 放貨點 LIFT_POINT 取貨點 STAY_POINT 逗留點 |
| point_status | string | 點位執行階段 - START：開始執行 - ACTIVE:更換點位 - MOVING：前往中 - APPROACHING：抵達中 - ARRIVED：抵達 - COMPLETE：完成 - LIFTING_IN_PROGRESS：頂起貨物中 - DROP_OFF_IN_PROGRESS：放貨中（1）對於頂升點：+ 開始前往：START+ 更換點位：ACTIVE+ 機器人前往頂升點中：MOVING+ 進入到後退抵達流程：APPROACHING+ 抵達點位：ARRIVED+ 頂升過程中：LIFTING_IN_PROGRESS+ 頂升完成：COMPLETE（2）對於途徑點+ 開始前往：START+ 機器人前往途徑點中：MOVING+ 進入到後退抵達流程：APPROACHING+ 抵達點位：ARRIVED+ 完成：COMPLETE（3）對於放貨點+ 開始前往：START+ 更換點位：ACTIVE+ 機器人前往放貨點中：MOVING+ 進入到後退抵達流程：APPROACHING+ 抵達點位：ARRIVED+ 放貨過程中：DROP_OFF_IN_PROGRESS+ 放貨完成：COMPLETE |

### Params.data.tasks.points.map_info

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| map_name | string | 地圖名稱 |

## 3、呼叫範例

json

{

"callback_type": "notifyLiftingTask",

"data": {

"is_overtime": false,

"mac": "90:03:71:42:9A:9A",

"notify_timestamp": 1760630481083,

"progress": 0,

"ratio": "0/1",

"sn": "8260047101A0007",

"spend_time": 0,

"task_id": "eee38b4016b74b8bbadc5e0c9ce3ea08",

"task_status": "PAUSE",

"task_type": "MANUAL",

"tasks": [

{

"desc_code": "",

"points": [

{

"point_attr": "LIFT_POINT",

"point_name": "原地頂升",

"point_status": "COMPLETE",

"point_type": "LIFT_IN_PLACE"

},

{

"map_info": {

"map_code": "3#3#333",

"map_name": "3#3#333"

},

"point_attr": "DROP_POINT",

"point_name": "3-點位4",

"point_status": "PAUSE",

"point_type": "POINT"

}

],

"status": "PAUSE",

"timestamp": 1760630481076

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

json

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

# 清潔任務狀態通知-notifyCleanStatus

更新時間:2025-11-17 21:01:36

## 1、說明

### 功能描述

機器做清潔任務時會透過該回呼通知開發者機器的任務狀態

### 適用範圍

* **支援機型**：CC1、CC1 Pro、MT1、MT1 Vac、MT1 Max

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyCleanStatus |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| 欄位名稱 | 類型 | 描述 |
| --- | --- | --- |
| task_id | string | 任務id |
| task_name | string | 任務名稱 |
| status | string | START_FAILED： 任務啟動失敗、BEGIN：任務開始END：任務結束INTERRUP：任務中斷 CANCEL：任務被取消 LONG_TERM_USED_CLEANING ：機器長時間執行掃地任務 LONG_TERM_USED_WASHING ：機器長時間執行洗滌任務 GO_MAINTENANCE： 機器正前往維護點ARRIVE_MAINTENANCE： 機器已到達維護點 WEATHER_WARNING_LOW_TEM：溫度過低 WEATHER_WARNING_HIGH_TEM：溫度過高 WEATHER_WARNING_SNOW：雪天 WEATHER_WARNING_RAIN：雨天 |
| task_time | int32 | 發生任務變化時間，時間戳秒 |
| remark | string | 備註(eg:中斷原因) |
| task_method | string | 任務除非方式：AUTOMATIC說明是機器上點擊任務執行觸發 |

## 3、呼叫範例

json

{

"callback_type": "notifyCleanStatus",

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

# 巡航任務狀態通知-notifyCruiseTask

更新時間:2025-12-04 14:26:05

## 1、說明

### 功能描述

機器呼叫[【機器人任務】-【巡航任務】-【發起巡航任務】](/zh/cloud-api/keclytvc5efrh0pwcygm0ct3)給機器下達指令後，機器巡航中會狀態變化透過這個回呼通知開發者。

### 適用範圍

* **支援機型**：PuduRobot2

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifCruiseTask |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **欄位** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 推送該消息的時間戳秒 |
| notify timestamp | long | 機器發生狀態變化的毫秒時間戳 |
| task_id | string | 任務id |
| task_type | string | REMOTE：遠程下達MANUAL：本地手動下達 |
| task_status | String | ON_THE_WAY(開始啟動巡航時報這個)、CANCEL、FAILED、COMPLETE、PAUSE |
| map_cruise_id | struct | 巡航路徑id |
| map_cruise_name | string | 巡航路徑名稱 |
| current_point | string | 當前點位名稱 |
| map_info | object | 當前地圖對像 |

### Params.data.map_info

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| map_name | string | 地圖名稱 |

## 3、呼叫範例

json

{

"callback_type": "notifyCruiseTask",

"data": {

"current_point": "A1",

"mac": "50:80:4A:F8:02:A8",

"map_cruise_id": "1764649613490",

"map_cruise_name": "chixz巡航1202",

"map_info": {

"map_name": "0#0#T600純激光地圖20250815"

},

"notify_timestamp": 1764770839934,

"sn": "6e0226270410014",

"task_id": "1764770838614695",

"task_status": "ON_THE_WAY",

"task_type": "REMOTE",

"timestamp": 1764770840

}

}

# 機器電量通知-notifyRobotPower

更新時間:2025-12-24 10:08:07

## 1、說明

### 功能描述

機器電量和電池狀態通知。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、KettyBot Pro、BellaBot Pro、PuduT300

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyRobotPower |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| charge_stage | string | 電池狀態： IDLE:空閒 CHARGING：充電中 CHARGE_FULL：充滿電 CHARGE_ERROR_CONTACT：充電連接異常 CHARGE_ERROR_ELECTRIC：電流異常 ERROR_BATTERY_PACK_COMM：通訊異常 ERROR_OVER_VOLT：電壓異常 ERROR_OVER_ELECTRIC：電流異常 ERROR_OVER_TEMPERATURE：溫度異常 ERROR_OVER_TIME：超時異常 |
| power | int32 | 電量百分⽐數，0～100 |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 服務推送通知的時間戳，秒 |
| notify_timestamp | long | 機器上報的時間戳，業務端可用於做亂序消息處理，毫秒 |

## 3、呼叫範例

json

{

"callback_type": "notifyRobotPower",

"data": {

"charge_stage": "IDLE",

"mac": "98:A1:4A:38:C4:6D",

"notify_timestamp": 1761705083466,

"power": 99,

"sn": "TS1732946965085",

"timestamp": 1761705082

}

}

# 艙門狀態通知-notifyDoorsState

更新時間:2025-11-17 21:02:04

## 1、說明

### 功能描述

機器艙門開關狀態變化時會透過該回呼通知開發者機器的艙門開關狀態

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyDoorsState |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| target_name | string | 目標點、當前所在抵達點 |
| door_states | **Array<object>** | 艙門狀態數組 |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 服務推送通知的時間戳，秒 |
| notify_timestamp | long | 機器上報的時間戳，業務端可用於做亂序消息處理，毫秒 |

### Params.data.door_states

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| state | string | 艙門狀態OPENING, 正在打開 OPENED, 打開成功 OPEN_FAILED, 打開失敗OPEN_TIMEOUT, 打開超時 CLOSING, 正在關閉 CLOSED, 關閉成功 CLOSE_FAILED, 關閉失敗 CLOSE_TIMEOUT; 關閉超時 |
| door_number | string | 艙門H_01 ， 1號艙門H_02 ， 2號艙門H_03， 3號艙門H_04 ， 4號艙門 |

## 3、呼叫範例

json

{

"callback_type": "notifyDoorsState",

"data": {

"target_name": "1",

"door_states": [{

"door_number": "H_01",

"state": "CLOSED"

}, {

"door_number": "H_03",

"state": "CLOSED"

}, {

"door_number": "H_02",

"state": "CLOSED"

}, {

"door_number": "H_04",

"state": "CLOSED"

}],

"sn":"OP21321dsffsd",

"mac":"AA:AA:AA:AA:AA:AA",

"notify_timestamp":1764325632001,//機器上報的時間戳，業務端可用於做亂序消息處理，毫秒

"timestamp": 1764325632 // 服務推送通知的時間戳，秒

}

}

# 機器梯控通知-notifyElevatorUtilizeState

更新時間:2025-12-24 10:14:14

## 1、說明

### 功能描述

機器乘坐電梯時，會回呼通知乘梯狀態。

### 適用範圍

* **支援機型**：PuduT300、FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyElevatorUtilizeState |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| elevator_utilize_state | string | 梯控狀態CALLING_ELEVATOR ：正在呼叫電梯 WAITING_ELEVATOR ：呼梯完成等待進梯 ENTERING_ELEVATOR ：進梯中 FINISH_ENTER_ELEVATOR：完成進梯 LEAVING_ELEVATOR：出梯中 FINISH_LEFT_ELEVATOR：出梯完成 OVERTIME_CALL_ELEVATOR ：呼叫電梯超時 OVERTIME_ENTER_ELEVATOR：進入電梯失敗 OVERTIME_ENTERED_ACK ：電梯回覆超時 OVERTIME_LEAVE_ELV：出梯超時 |
| elevator_event_param | **object** | 梯控參數 |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| timestamp | int | 服務推送通知的時間戳，秒 |
| notify_timestamp | long | 機器上報的時間戳，業務端可用於做亂序消息處理，毫秒 |

### Params.data.elevator_event_param

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| curr_floor | string | 當前樓層 |
| dst_floor | string | 目標樓層 |
| ele_id | string | 電梯ID |

## 3、呼叫範例

json

{

"callback_type": "notifyElevatorUtilizeState",

"data": {

"elevator_event_param": {

"curr_floor": "1",

"dst_floor": "1",

"ele_id": "865012064565160"

},

"elevator_utilize_state": "CALLING_ELEVATOR",

"env": "cxg-test-internal",

"mac": "00:D6:CB:4B:17:9D",

"notify_timestamp": 1761663939155,

"sn": "TS1732254968923",

"timestamp": 1761663938

}

}

# 二維碼消息通知-notifyQrCodeContent

更新時間:2025-11-17 21:02:53

## 1、說明

### 功能描述

該回呼介面是兼容SDK微服務的，新機型已經不再支持。

### 適用範圍

* **支援機型**：

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyQrCodeContent |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器sn |
| mac | string | 機器mac |
| content | string | 二位碼內容 |
| notify_timestamp | string | 機器上報的時間戳，業務端可用於做亂序消息處理，毫秒 |
| timestamp | int32 | 服務推送通知的時間戳，秒 |

## 3、呼叫範例

json

{

"callback_type":"notifyQrCodeContent",

"data":{

"mac": "00:D6:CB:4B:17:9D",

"sn": "TS1732254968923",

"content":"111111111111111",

"notify_timestamp":1764325632001,//(1.5.1版本支持)機器上報的時間戳，業務端可用於做亂序消息處理，毫秒

"timestamp": 1764325632 // 服務推送通知的時間戳，秒

}

}

# 頂升機構狀態通知-notifyLiftingStatus

更新時間:2025-11-17 21:02:36

## 1、說明

### 功能描述

機器頂升設備狀態發生變化時會透過該回呼進行通知

### 適用範圍

* **支援機型**：PuduT300

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyLiftingStatus |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| status | string | 頂升機構狀態+ RESET：頂升機構在復位位置+ LIFTING_IN_PROGRESS：頂升機構升起中+ LIFTED：頂升機構在上限位+ DROP_OFF_IN_PROGRESS：頂升機構放貨中 |
| mac | string | 機器mac |
| sn | string | 機器sn |
| timestamp | int | 服務推送通知的時間戳，秒 |
| notify_timestamp | long | (1.5.1版本支持)機器上報的時間戳，業務端可用於做亂序消息處理，毫秒 |

## 3、呼叫範例

json

{

"callback_type": "notifyLiftingStatus",

"data": {

"status": "RESET",

"mac": "90:03:71:42:9A:E0",

"sn": "8BROC20240902",

"notify_timestamp":1764325632001,//(1.5.1版本支持)機器上報的時間戳，業務端可用於做亂序消息處理，毫秒

"timestamp": 1764325632 // 服務推送通知的時間戳，秒

}

}

# 回充狀態通知-notifyRechargeStatus

更新時間:2025-11-17 21:03:02

## 1、說明

### 功能描述

在呼叫開放介面給機器下達回充指令後[【控制指令】-【機器人一鍵回充】-【機器人一鍵回充V2】](/zh/cloud-api/h517ik6b4gu8r8lz2teh7xex)，機器會將前端充電樁進行回充的過程狀態透過該回呼通知。

### 適用範圍

* **支援機型**：PuduT300、FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

## 2、回呼參數

POST <https://yourdomain.com/youruri>

【<https://yourdomain.com/youruri>】是由開發者提供接收回呼通知的介面地址，需要在申請APPKey的時候填到【回呼地址】那一欄裡，才能收到通知。

### 請求內容（Params）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| callback_type | string | 回呼消息類型，這裡：notifyRechargeStatus |
| data | **object** | 回呼的附加資料，根據callback_type不同，該結構不同 |

### Params.data

| **欄位** | **類型** | **描述** |
| --- | --- | --- |
| sn | string | 機器SN |
| mac | string | 機器MAC地址 |
| task_id | string | 任務id |
| status | string | ON_THE_WAY 機器執行任務中、CANCEL 取消任務、FAILED(機器回傳拒絕任務時，雲端自己更新)、COMPLETED 完成任務、PAUSE 任務暫停中 |
| map_name | string | 當前所在地圖 |
| point | string | 當前所處點位 |
| point_type | string | 點位類型 |
| timestamp | int | 服務推送通知的時間戳，秒 |
| notify_timestamp | long | 機器上報的時間戳，業務端可用於做亂序消息處理，毫秒 |

## 3、呼叫範例

json

{

"callback_type": "notifyRechargeStatus",

"data": {

"mac": "98:A1:4A:38:C4:DA",

"map_name": "0#0#Flashbot純激光",

"notify_timestamp": 1760440430417,

"point": "財務室門口充電樁",

"point_type": "ChargePile",

"sn": "OPG7jpSvFoA8cEdP",

"state": "COMPLETE",

"task_id": "07058bab9ef84625bcfc55d442c5766b",

"timestamp": 1760440431

}

}

# 取得門市列表

更新時間:2025-11-10 10:31:30

## 1. 介面說明

### 功能描述

取得門市列表。

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-open-platform-service/v1/api/shop |
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
| limit | int | N | 查詢限制的數量（預設為10） |
| offset | int | N | 偏移量（預設為0） |

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
| count | int | 總數量 |
| list | **Array<object>** | 門市列表 |

### Res.data.list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| shop_id | int | 門市id |
| shop_name | string | 門市名稱 |
| company_id | int | 門市所屬代理商id |
| company_name | string | 門市所屬代理商名稱 |

## 5.呼叫範例

### 請求範例

http

/data-open-platform-service/v1/api/shop?limit=100&offset=0

### 回傳範例

json

{

"data": {

"count": 110,

"list": [

{

"company_id": "13947",

"company_name": "chixzdls_internal02二級代理商",

"shop_id": "324100000",

"shop_name": "【10月08日】出塵門市"

},

{

"company_id": "13947",

"company_name": "chixzdls_internal02二級代理商",

"shop_id": "325300001",

"shop_name": "閃電匣和很多葫蘆"

}

]

},

"message": "SUCCESS",

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717"

}

# 門市機器列表

更新時間:2025-11-10 10:32:50

## 1. 介面說明

### 功能描述

取得機器列表,回傳機器mac、sn、產品類型等資訊。

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-open-platform-service/v1/api/robot |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |
| Language | string | N | 預設中文 （支援語系查看附錄） |

### 請求內容（Params）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| limit | int | N | 查詢限制的數量（預設為10） |
| offset | int | N | 偏移量（預設為0） |
| shop_id | int | N | 門市id |
| product_code | Array<string> | N | 產品類型集合，參考FAQ-機器類型 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | **object** | 查詢結果 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| count | int | 總數量 |
| list | **Array<object>** | 機器列表 |

### Res.data.list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器SN |
| mac | string | 機器mac |
| shop_id | int | 機器所屬門市id |
| shop_name | string | 機器所屬門市名稱 |
| product_code | string | 產品類型，參考FAQ-機器類型 |

## 5.呼叫範例

### 請求範例

http

/data-open-platform-service/v1/api/robot?limit=2&offset=0&shop_id=324100000

### 回傳範例

json

{

"data": {

"count": 4,

"list": [

{

"mac": "20:50:E7:3E:61:78",

"shop_id": 324100000,

"shop_name": "【10月08日】出塵門市",

"sn": "OP2023090702",

"product_code":"PuduBot"

},

{

"mac": "B4:ED:D5:75:6E:E8",

"shop_id": 324100000,

"shop_name": "【10月08日】出塵門市",

"sn": "8110A3802050003",

"product_code":"PuduBot"

}

]

},

"message": "success",

"trace_id": "YourApiAppKey_bd969310-9897-43c5-a37d-a4eab6825dbb"

}

# 門市下地圖列表

更新時間:2025-11-28 11:58:59

## 1. 介面說明

### 功能描述

取得門市下所有地圖名稱列表。

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-open-platform-service/v1/api/maps |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |
| Language | string | N | 預設中文 （支援語系查看附錄） |

### 請求內容（Params）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| shop_id | int | Y | 門市id |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | **object** | 查詢結果 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| count | int | 總數量 |
| list | **Array<object>** | 地圖列表 |

### Res.data.list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| map_name | string | 地圖名稱 |

## 5.呼叫範例

### 請求範例

http

/data-open-platform-service/v1/api/maps?shop_id=324100000

### 回傳範例

json

{

"data": {

"count": 2,

"list": [

{

"map_name": "2#2#地毯"

},

{

"map_name": "3#10#地圖yy"

}

]

},

"message": "SUCCESS",

"trace_id": "YourApiAppKey_bd969310-c98e-4182-a9bb-fa29b54bf07e"

}

# 機器可用地圖列表

更新時間:2025-11-28 12:00:56

## 1. 介面說明

### 功能描述

取得機器當前可用地圖列表。

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /map-service/v1/open/list |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |
| Language | string | N | 預設中文 （支援語系查看附錄） |

### 請求內容（Params）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| sn | string | Y | 機器sn |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | **object** | 查詢結果 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| list | **Array<object>** | 機器列表 |

### Res.data.list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| name | string | 地圖名稱 |
| floor | string | 地圖所在樓層 |

## 5.呼叫範例

### 請求範例

http

/map-service/v1/open/list?sn=123

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"list": [

{

"name": "-2#39#地圖qqqq",

"floor": "39"

},

{

"name": "4#103#bbd0bbd031302ttt",

"floor": "103"

}

]

}

}

# 機器當前使用地圖

更新時間:2025-11-28 11:55:03

## 1. 介面說明

### 功能描述

取得機器當前使用的地圖資料，正常情況下機器只會有一個正在使用的地圖，但是需要注意老閃電匣一些舊版本會上報多張的情況，這種情況會取第一張。

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /map-service/v1/open/current |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |
| Language | string | N | 預設中文 （支援語系查看附錄） |

### 請求內容（Params）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| sn | string | Y | 機器sn |
| need_element | bool | N | 是否需要回傳地圖的內部元素資料,這裡除非是需要渲染地圖纔會用到地圖的元素資料 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | object | 查詢結果 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| name | string | 地圖名稱 |
| floor | string | 地圖所在樓層 |
| elements | **Array<object>** | 地圖元素資料 |

### Res.data.elements

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| type | string | 元素類型 source 地圖中目標點。包括餐桌，回收櫃，洗碗點，取餐點，臨停點 track 地圖路徑，可透過該資料繪製地圖路徑 circle 巡航路徑 |
| id | string | 元素 id,type 為 source 時一般表示餐桌號 |
| name | string | 元素名稱，暫未用到 |
| mode | string | type 為 source 時欄位有效，表示為點位模式 table:  餐桌 dining_outlet:  取餐點/出餐口 transit:  回盤點/中轉點   dishwashing:  洗碗間   parking：臨停點/停靠點   usher: 門迎點 return_point: 返航點 clean_endpoint 清潔終點 |
| group | string | 點位分組 |
| width | float | 路徑寬度 |
| max_speed | float | 最大速度 |
| vector | Array<double> | 位置座標 |

## 5.呼叫範例

### 請求範例

http

/map-service/v1/open/current?sn=123&need_element=true

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"name": "-1#0#地圖1",

"floor": "0",

"elements": [

{

"type": "source",

"id": "7##return_point0B4EDD5756EE11698982688826",

"name": "返航點1",

"mode": "return_point",

"group": "",

"vector": [

0.12725049045409734, 0.008827563986179064, 0.10761558616086728

],

"width": 0,

"max_speed": 0

}

]

}

}

# 取得地圖詳情V2

更新時間:2025-12-03 14:27:48

## 1. 介面說明

### 功能描述

取得地圖詳情V2，原樣輸出機器地圖資料，不做單位轉換。

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /map-service/v1/open/map |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |
| Language | string | N | 預設中文 （支援語系查看附錄） |

### 請求內容（Params）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| shop_id | string | Y | 門市ID |
| map_name | string | Y | 地圖名稱（特別注意：地圖名稱需要轉義特殊字符，比如#、中文） |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | **object** | 查詢結果 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| map_name | string | 地圖名稱 |
| map_code | string | 地圖唯一碼 |
| url | string | 地圖圖片 |
| width | int | 地圖圖片寬度 |
| height | int | 地圖圖片高度 |
| resolution | float | 地圖的分辨率（物理世界尺寸（單位：米）：地圖圖片的像素尺寸） |
| origin_list | Array<float> | 地圖圖片在窗口座標系中的繪製座標 |
| element_list | **Array<object>** | 地圖點位、拓撲路徑、巡航路徑和區域的基礎資訊（類型，名稱，座標） |
| zone_list | **Array<object>** | 地圖點位、拓撲路徑、巡航路徑和區域的基礎資訊（類型，名稱，座標） |

### Res.data.elements

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| name | string | 元素名稱 |
| type | string | 地圖元素類型： source-具體點位類型，由Element.mode欄位來表示。 track-拓撲路徑，機器人能行走的路徑 circle-巡航路徑 virtual_wall-虛擬牆 elevator-電梯間 elev_waiter-電梯等待點 access_point-門禁點 charging_pile-充電樁 lslam_restarter-激光重定位點(開機點位) gate-閘機點 chargeWorkStation-(清潔)工作站 forbidden-（清潔）禁區 area-計劃清潔區域邊框 edge-手推類型的區域 |
| vector_list | Array<float> | 座標 |
| mode | string | 點位類型：table：餐桌、dining_outlet:取餐點/出餐口、transit:回盤點/中轉點、dishwashing:洗碗間、parking：臨停點/停靠點、usher:門迎點、return_point:返航點 |
| id | string | 元素id(點位名稱優先取這個id) |
| clean_path_list | **Array<object>** | 表示計劃清潔路線 |

### Res.data.zone_list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| type | string | 地圖區域類型： RGBDFunLinitArea-RGBD功能限制區域 elevator_area-電梯間區域 SpeedLimit-速度限制區 NoDetour-禁止繞行區 ExemptZone-豁免區 danger_area-危險區域 |
| id | string | 區域id |
| zone_node_list | **Array<object>** | 地圖區域座標節點 |

### Res.data.elements.clean_path_list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| x | float | x座標 |
| y | float | y座標 |
| z | float | z座標 |

### Res.data.zone_list.zone_node_list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| vector_list | Array<float> | 座標 |

## 5.呼叫範例

### 請求範例

http

/map-service/v1/open/map?shop_id=XXXXXX&map_name=2%234%232F_chixz

### 回傳範例

json

{

"data": {

"map_code": "ADAFDAFDAFDASFADFSDA",

"element_list": [

{

"clean_path_list": [],

"id": "7##return_point0EC1D9EA2821F1691742592683",

"mode": "return_point",

"name": "返航點2",

"type": "source",

"vector_list": [

-16.4842,

22.78,

]

},

{

"clean_path_list": [],

"id": "30EC1D9EA2821F1694516595756",

"mode": "",

"name": "充電樁0",

"type": "charging_pile",

"vector_list": [

310.62335,

-403.46823,

-72.81601

]

},

{

"clean_path_list": [],

"id": "190EC1D9EA2821F1694516595758",

"mode": "",

"name": "工作站0",

"type": "chargeWorkStation",

"vector_list": [

235.90141,

# 繪製解析後的地圖V2

更新時間:2025-11-28 11:55:54

<https://codesandbox.io/p/github/zayfen/OPEN_MAP_RENDER/main>

html

<iframe src="https://codesandbox.io/p/github/zayfen/OPEN_MAP_RENDER/draft/unruffled-oskar?embed=1"

style="width:100%; height: 500px; border:0; border-radius: 4px; overflow:hidden;"

title="zayfen/OPEN_MAP_RENDER/draft/unruffled-oskar"

allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking"

sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"

></iframe>

# 取得機器實時地圖位置

更新時間:2025-12-12 10:59:59

## 1. 介面說明

### 功能描述

取得機器當前所在地圖位置，需要注意該介面有頻率限制，每次取得位置後，位置資訊會緩存10秒，即10秒內再次取得到的位置資料是沒有變化的。如果要更實時的位置，可以透過【控制指令】-【地圖與位置】-【通知機器上報位置】的介面給機器下達上報位置的指令，然後透過【回呼通知】-【地圖與位置回呼】-【notifyRobotPose-機器位置上報】訂閱機器位置。

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/robot/get_position |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |
| Language | string | N | 預設中文（支援語系查看附錄） |

### 請求內容（Params）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| sn | string | Y | 機器sn |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | **object** | 查詢結果 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| name | string | 地圖名稱，取得不到位置則為空 |
| floor | string | 地圖所在樓層 |
| position | **object** | 機器位置 |

### Res.data.position

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| x | float | x座標 |
| y | float | y座標 |
| z | float | z座標 |

## 5.呼叫範例

### 請求範例

http

/open-platform-service/v1/robot/get_position?sn=xxx

### 回傳範例

json

{

"message": "SUCCESS",

"data": {

"map_name": "2#4#2F_chixz出塵20230811",

"floor": "2",

"position": {

"x": 0,

"y": -0,

"z": 0

}

},

"traceId": "YourApiAppKey_bd969310-1208-40c3-9495-e21ebd4ac7db"

}

# 取得機器當前使用地圖的點位

更新時間:2025-11-28 12:02:00

## 1. 介面說明

### 功能描述

取得機器當前使用的點位列表.

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /map-service/v1/open/point |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |
| Language | string | N | 預設中文 （支援語系查看附錄） |

### 請求內容（Params）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| sn | string | Y | 機器 sn |
| limit | int32 | N | 分頁參數，每頁行數，不傳預設所有 |
| offset | int32 | N | 分頁參數，跳過行數 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | **object** | 查詢結果 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| total | int32 | 地圖名稱 |
| list | **Array<object>** | 地圖所在樓層 |

### Res.data.list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| name | string | 點位 id，桌號 |
| type | string | 點位類型，對應地圖資料的 mode table:  餐桌 dining_outlet:  取餐點/出餐口 transit:  回盤點/中轉點 dishwashing:  洗碗間 parking：臨停點/停靠點 usher: 門迎點 return_point: 返航點 clean_endpoint 清潔終點 |
| x | double | 點位座標 X 軸 |
| y | double | 點位座標 Y 軸 |
| z | double | 點位座標 Z 軸 |

## 5.呼叫範例

### 請求範例

http

/map-service/v1/open/point?sn=123&limit=10&offset=0

### 回傳範例

json

{

"trace_id":""1111111111111111111111,

"message": "SUCCESS",

"data": {

"total": 1,

"list": [

{

"name": "返航點1",

"x": 0.12725049045409734,

"y": 0.008827563986179064,

"z": 0.10761558616086728,

"type": "return_point"

}

]

}

}

# 取得點位分組

更新時間:2025-11-10 19:43:44

## 1. 介面說明

### 功能描述

這裡僅puduT300的新版本建圖工具纔會支持二級分組,且二級分組就是貨架組名稱。

### 適用範圍

* **支援機型**：PuduT300

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /map-service/v1/open/group |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |

### 請求內容（Params）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| sn | string | Y | 機器 sn |
| map_name | string | Y | 地圖名 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | **object** | 查詢結果 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| group_list | **Array<object>** | 一級分組集合 |

### Res.data.group_list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| name | string | 一級分組名稱 |
| second_group_list | **Array<object>** | 二級分組集合 |

### Res.data.group_list.second_group_list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| name | string | 二級分組名稱 |
| point_list | Array<string> | 二級分組點位名稱列表 |

## 5.呼叫範例

### 請求範例

http

{

"sn":"OP0D412438B0CFE",

"map_name":"26#26#test"

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"group_list": [

{

"name": "26停靠點",

"second_group_list": [

{

"name": "",

"point_list": [

"26停靠點"

]

}

]

},

{

"name": "elevator-862195055876846",

"second_group_list": [

{

"name": "",

"point_list": [

"32"

]

}

]

},

{

"name": "",

"second_group_list": [

{

"name": "1",

"point_list": [

"26-1"

]

},

# 取得清潔機器狀態詳情

更新時間:2025-12-25 17:46:56

## 1. 介面說明

### 功能描述

取得機器詳情，回傳設備在線、電量、地圖、任務狀態、位置資訊等。

### 適用範圍

* **支援機型**：CC1、CC1 Pro、MT1、MT1 Vac、MT1 Max

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /cleanbot-service/v1/api/open/robot/detail |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | Y | application/json |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器 SN |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| message | string | SUCCESS 成功 |
| data | **object** | 機器詳情 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| mac | string | 設備 MAC |
| nickname | string | 機器暱稱 |
| battery | int32 | 電量（0-100） |
| map | **Object** | 地圖 |
| cleanbot | **Object** | 機器狀態及任務資訊 |
| shop | **Object** | 門市資訊 |
| position | Position | 位置 |
| sn | string | 機器 SN |

### Res.data.map

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| name | string | 地圖名稱 |
| lv | int32 | 樓層等級 |
| floor | string | 樓層 |

### Res.data.shop

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| id | int32 | 門市 ID |
| name | string | 門市名稱 |

### Res.data.Position

| **欄位** | **類型** | **說明** |
| --- | --- | --- |
| x | float | X |
| y | float | Y |
| z | float | Z |

### Res.data.cleanbot

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| rising | int32 | 上水箱餘量 |
| sewage | int32 | 污水箱餘量 |
| task | int32 | 任務狀態碼 |
| clean | **Object** | 當前清潔任務 |
| last_mode | int32 | 上一次工作模式 |
| detail | string | 任務詳情描述 |
| last_task | string | 上一次任務名稱 |

### Res.data.cleanbot.clean

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| mode | int32 | 工作模式：1手動 2自動 |
| report_id | string | 報告編號 |
| msg | string | 任務描述 |
| result | **Object** | 任務狀態和結果 |
| task | **Object** | 任務定義 |
| map | **Object** | 當前地圖 |
| config | **Object** | 清掃設定 |

### Res.data.cleanbot.clean.result

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| time | int32 | 用時（秒） |
| area | float | 面積 |
| status | int32 | 任務狀態：0未開始 1進行中 2暫停 3中斷 4結束 5異常 6取消 |
| break_point | **Object** | 斷點位置 |
| percentage | int32 | 進度百分比 |
| remaining_time | int32 | 剩餘時間（秒） |
| task_area | float | 任務實際清潔面積 |
| cost_water | int32 | 消耗水量 |
| cost_battery | int32 | 消耗電量 |
| charge_count | int32 | 充電次數 |

### Res.data.cleanbot.clean.task

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| task_id | long | 任務 ID |
| version | float | 任務版本 |
| name | string | 任務名稱 |

### Res.data.cleanbot.clean.map

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| name | string | 地圖名稱 |
| lv | int32 | 樓層等級 |
| floor | string | 樓層 |

### Res.data.cleanbot.clean.config

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| mode | int32 | 模式 |
| vacuum_speed | int32 | 吸塵速度 |
| vacuum_suction | int32 | 吸塵吸力 |
| wash_speed | int32 | 洗地速度 |
| wash_suction | int32 | 洗地吸力 |
| wash_water | int32 | 洗地用水量 |
| type | int32 | 類型：0自定義 1地毯 2靜音 |
| left_brush | int32 | 左邊刷（Monster 有）：1低 2中 3高 0關閉 |
| right_brush | int32 | 右邊刷（Monster & CC1）：1低 2中 3高 0關閉 |
| right_vacuum_suction | int32 | 掃地右吸力：1低 2中 3高 0關閉 |
| ai_adaptive_switch | bool | AI 自適應開關 |

### Res.data.cleanbot.clean.result.break_point

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| index | int32 | 斷點索引 |
| vector | **Object** | 斷點位置 |
| clean_type | int32 | 清掃類型 |
| start | **Object** | 沿邊開始位置 |

### Res.data.cleanbot.clean.result.break_point.vector/start

| **欄位** | **類型** | **說明** |
| --- | --- | --- |
| x | float | X |
| y | float | Y |
| z | float | Z |

## 5.呼叫範例

### 請求範例

http

/cleanbot-service/v1/api/open/robot/detail?sn=SN123

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"sn": "SN123",

"mac": "B4:ED:D5:75:6E:EB",

"nickname": "出塵111",

"online": true,

"battery": 89,

"map": {

"name": "4#120#地圖1",

"lv": 15,

"floor": ""

},

"cleanbot": {

"rising": 75,

"sewage": 5,

"task": 0,

"clean": {

"mode": 2,

"report_id": "896477585377857536",

"msg": "",

"result": {

"time": 0,

"area": 0,

"status": 3,

"break_point": {

"index": -1,

"vector": {

"x": 0,

"y": 0,

"z": 0

},

"clean_type": 1,

"start": null

},

# 取得指定機器人狀態

更新時間:2025-11-28 11:56:28

## 1. 介面說明

### 功能描述

這裡取得機器人工作狀態、在線狀態、電量等資訊，用於判斷是否能給機器下達任務，需要注意該介面已經廢棄，請使用【取得指定機器人狀態V2】。

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/status/get_by_sn |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |

### 請求內容（Params）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| sn | string | Y | 機器sn |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | **object** | 查詢結果 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| device_name | string | 設備名 |
| timestamp | long | 更新時間 |
| schedule_status | int32 | 調度狀態 1: 可調度 -1: 不可調度 |
| schedule_msg | string | 不可調度原因 |
| work_status | int32 | 工作狀態 1:工作中 -1:空閒 |
| work_msg | string | 工作內容 |
| battery | int32 | 電量 |
| is_online | int32 | 1:在線 -1:離線 |
| is_charging | int32 | 1:正在充電 -1 沒有充電 |
| map_name | string | 地圖名稱 |
| move_state | string | 僅支持T300 運動狀態 IDLE :空閒 MOVING :運動中 STUCK :被障礙物阻擋 APPROACHING ：快抵達目標點 ARRIVE ：抵達目標點 PAUSE ：暫停 AVOID ： 與其他機器人進行調度 |
| charge_stage | string | 僅支持T300 電池狀態 IDLE:空閒 CHARGING：充電中 CHARGE_FULL：充滿電 CHARGE_ERROR_CONTACT：充電連接異常 CHARGE_ERROR_ELECTRIC：電流異常 ERROR_BATTERY_PACK_COMM：通訊異常 ERROR_OVER_VOLT：電壓異常 ERROR_OVER_ELECTRIC：電流異常 ERROR_OVER_TEMPERATURE：溫度異常 ERROR_OVER_TIME：超時異常 |
| remain_time | int32 | 僅支持T300 機器剩餘使用時長，分鐘 |

## 5.呼叫範例

### 請求範例

http

/open-platform-service/v1/status/get_by_sn?sn=123

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message":"SUCCESS",

"data":{

"device_name":"mac地址",

"timestamp":1852342312,

"schedule_status":-1,

"schedule_msg":"電量低於2%",

"work_status":-1,

"work_msg":"空閒",

"battery":1,

"is_online":1,

"is_charging":1,

"map_name":"map",

"move_state":"MOVING",

"charge_stage":"CHARGING"

}

}

# 取得指定機器人狀態V2

更新時間:2025-12-25 17:44:41

## 1. 介面說明

### 功能描述

根據機器人序列號取得機器人的狀態資訊V2版本，將3個狀態(schedule_status,work_status,is_online)合併成一個(run_state)：OFFLINE、DISABLE、BUSY、IDLE。如果需要實時取得機器狀態可透過【[回呼通知】-【機器狀態與綁定】-【機器工作狀態通知-notifyRobotStatus】](/zh/cloud-api/rxyacnq8qr4i2qum6ek0c229)進行訂閱。

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v2/status/get_by_sn |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | N | 機器人SN和MAC兩個參數二選一 |
| mac | string | N | 機器人MAC地址 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息 |
| data | **object** | 機器人狀態資料V2 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器人序列號 |
| mac | string | 設備名 |
| timestamp | int32 | 更新時間 |
| battery | int32 | 電量 |
| is_charging | int32 | 充電狀態：1(正在充電)、-1(沒有充電) |
| move_state | string | 運動狀態：IDLE(空閒)、MOVING(運動中)、STUCK(被障礙物阻擋)、APPROACHING(快抵達目標點)、ARRIVE(抵達目標點)、PAUSE(暫停)、AVOID(與其他機器人進行調度) |
| charge_stage | string | 電池狀態：IDLE(空閒)、CHARGING(充電中)、CHARGE_FULL(充滿電)、CHARGE_ERROR_CONTACT(充電連接異常)、CHARGE_ERROR_ELECTRIC(電流異常)、ERROR_BATTERY_PACK_COMM(通訊異常)、ERROR_OVER_VOLT(電壓異常)、ERROR_OVER_ELECTRIC(電流異常)、ERROR_OVER_TEMPERATURE(溫度異常)、ERROR_OVER_TIME(超時異常) |
| remain_time | int32 | 機器剩餘時間(秒) |
| product_code | string | 產品代碼 |
| run_state | string | 運行狀態：OFFLINE：機器離線，一般是由於機器網絡問題或者呼叫開關沒有開啟; DISABLE：當前狀態不可用，機器電量太低無法執行任務或者設置了機器充電中無法被呼叫，注意當機器由IDLE變為該狀態時，所有在雲端排隊的呼叫任務都會提前結束; BUSY：機器正在執行任務，或者部分機器觸摸屏幕後10秒內都會時忙碌狀態，該狀態機器是可以呼叫，但是會進入雲端排隊(僅呼叫任務有排隊邏輯) ;IDLE：機器當前空閒，給機器發任務，機器會立即回應。 |
| charge_type | int32 | 充電類型：1(線充)、2(樁充) |

## 5.呼叫範例

### 請求範例

http

GET /open-platform-service/v2/status/get_by_sn?sn=SN-PD202405000001

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"sn": "SN-PD202405000001",

"mac": "機器人001",

"timestamp": 1640995200,

"battery": 85,

"is_charging": -1,

"move_state": "IDLE",

"charge_stage": "IDLE",

"remain_time": 0,

"product_code": "PD-001",

"run_state": "IDLE",

"charge_type": 2

}

}

# 取得組中機器人狀態

更新時間:2025-11-28 11:57:58

## 1. 介面說明

### 功能描述

這裡根據組ID取得機器人列表工作狀態、在線狀態、電量等資訊，用於判斷是否能給機器下達任務，需要注意該介面已經廢棄，請使用【取得指定組中機器人狀態V2】。

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/status/get_by_group_id |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| group_id | string | Y | 機器組id |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | **Array<object>** | 查詢結果 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| device_name | string | 設備名 |
| timestamp | long | 更新時間 |
| schedule_status | int32 | 調度狀態 1: 可調度 -1: 不可調度 |
| schedule_msg | string | 不可調度原因 |
| work_status | int32 | 工作狀態 1:工作中 -1:空閒 |
| work_msg | string | 工作內容 |
| battery | int32 | 電量 |
| is_online | int32 | 1:在線 -1:離線 |
| is_charging | int32 | 1:正在充電 -1 沒有充電 |
| map_name | string | 地圖名稱 |
| move_state | string | 僅支持T300 運動狀態 IDLE :空閒 MOVING :運動中 STUCK :被障礙物阻擋 APPROACHING ：快抵達目標點 ARRIVE ：抵達目標點 PAUSE ：暫停 AVOID ： 與其他機器人進行調度 |
| charge_stage | string | 僅支持T300 電池狀態 IDLE:空閒 CHARGING：充電中 CHARGE_FULL：充滿電 CHARGE_ERROR_CONTACT：充電連接異常 CHARGE_ERROR_ELECTRIC：電流異常 ERROR_BATTERY_PACK_COMM：通訊異常 ERROR_OVER_VOLT：電壓異常 ERROR_OVER_ELECTRIC：電流異常 ERROR_OVER_TEMPERATURE：溫度異常 ERROR_OVER_TIME：超時異常 |
| remain_time | int32 | 僅支持T300 機器剩餘使用時長，分鐘 |

## 5.呼叫範例

### 請求範例

http

/open-platform-service/v1/status/get_by_group_id?group_id=123

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message":"SUCCESS",

"data":[{

"device_name":"device",

"timestamp":1852342312,

"schedule_status":-1,

"schedule_msg":"電量低於2%",

"work_status":-1,

"work_msg":"空閒",

"battery":1,

"is_online":1,

"is_charging":1,

"map_name":"map",

"move_state":"MOVING",

"charge_stage":"CHARGING"

}]

}

# 取得組中機器人狀態V2

更新時間:2025-12-25 17:45:24

## 1. 介面說明

### 功能描述

根據機器人組ID取得組內所有機器人的狀態資訊V2版本，將3個狀態(schedule_status,work_status,is_online)合併成一個(run_state)：OFFLINE、DISABLE、BUSY、IDLE。

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v2/status/get_by_group_id |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| group_id | string | Y | 機器組id |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息 |
| data | **Array<object>** | 機器人狀態資料V2列表 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| sn | string | 機器人序列號 |
| mac | string | 設備名 |
| timestamp | int32 | 更新時間 |
| battery | int32 | 電量 |
| is_charging | int32 | 充電狀態：1(正在充電)、-1(沒有充電) |
| move_state | string | 運動狀態 |
| charge_stage | string | 電池狀態 |
| remain_time | int32 | 機器剩餘時間(秒) |
| product_code | string | 產品代碼 |
| run_state | string | 運行狀態：OFFLINE：機器離線，一般是由於機器網絡問題或者呼叫開關沒有開啟; DISABLE：當前狀態不可用，機器電量太低無法執行任務或者設置了機器充電中無法被呼叫，注意當機器由IDLE變為該狀態時，所有在雲端排隊的呼叫任務都會提前結束; BUSY：機器正在執行任務，或者部分機器觸摸屏幕後10秒內都會時忙碌狀態，該狀態機器是可以呼叫，但是會進入雲端排隊(僅呼叫任務有排隊邏輯) ;IDLE：機器當前空閒，給機器發任務，機器會立即回應。 |
| charge_type | int32 | 充電類型：1(線充)、2(樁充) |

## 5.呼叫範例

### 請求範例

http

GET /open-platform-service/v2/status/get_by_group_id?group_id=GROUP-001

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": [

{

"sn": "SN-PD202405000001",

"mac": "機器人001",

"timestamp": 1640995200,

"battery": 85,

"is_charging": -1,

"move_state": "IDLE",

"charge_stage": "IDLE",

"remain_time": 0,

"product_code": "PD-001",

"run_state": "IDLE",

"charge_type": 2

}

]

}

# 取得當前機器執行任務狀態

更新時間:2025-11-10 15:34:26

## 1. 介面說明

### 功能描述

取得當前機器執行任務的狀態資訊。該介面是兼容SDK微服務的舊開放介面，新版本機器不支持該介面

### 適用範圍

* **支援機型**：閃電匣

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/robot/task/state/get |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器sn |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | object | 查詢結果 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| code | integer | 機器回傳碼 |
| message | string | 機器回傳消息 |
| data | object | 機器回傳的任務詳情 |

### Res.data.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| tasks | **Array<object>** | 任務組 |

### Res.data.data.tasks

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| name | string | 目標點 |
| type | string | 類型：直達(Direct)、客房送(RoomDelivery)、閃電送(OrderDelivery)、回充(Charge)、返航(BackHome)、回傳門迎點(BackMeet)、巡航(Cruise)、呼叫(Call)、帶客(Guest) |
| state | string | 狀態：等待(Await)、進行中(Ongoing)、抵達(Arrive)、完成(Complete)、失敗(Fail)、取消(Cancel) |

## 5.呼叫範例

### 請求範例

http

GET /open-platform-service/v1/robot/task/state/get?sn=SN-PD202405000001

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"code": 0,

"message": "查詢成功",

"data": {

"tasks": [

{

"name": "TABLE-001",

"type": "Direct",

"state": "Ongoing"

}

]

}

}

}

# 取得綁定的機器人組

更新時間:2025-11-28 11:58:27

## 1. 介面說明

### 功能描述

取得根據門市id或者微服務的設備ID取得機器人組列表，該介面是為了兼容SDK微服務。

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/robot/group/list |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |

### 請求內容（Params）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| device | string | N | 設備id,舊SDK微服務可以傳device |
| shop_id | int32 | N | 門市id,新開放平台沒有device,則傳shop_id |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | **object** | 查詢結果 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| groups | **Array<object>** | 組列表 |

### Res.data.groups

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| group_id | string | 機器組 id |
| group_name | string | 機器組名稱 |
| shop_id | int32 | 門市 id |
| shop_name | string | 門市名稱 |

## 5.呼叫範例

### 請求範例

http

/open-platform-service/v1/robot/group/list?shop_id=123

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"groups": [

{

"group_id": "UWlBrDb4NmPhiorpHMiir",

"group_name": "分組1",

"shop_id:": 121562,

"shop_name": "門市"

}

]

}

}

# 取得機器人組中的機器人

更新時間:2025-11-28 11:56:58

## 1. 介面說明

### 功能描述

根據組id取得機器人列表和所在的門市名稱。

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/robot/list_by_device_and_group |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |

### 請求內容（Params）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| group_id | string | Y | 機器組id |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | **object** | 查詢結果 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| robots | **Array<object>** | 機器列表 |

### Res.data.groups

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| mac | string | mac |
| sn | string | sn |
| robot_name | string | 機器名稱 |
| shop_id | int32 | 門市 id |
| shop_name | string | 門市名稱 |

## 5.呼叫範例

### 請求範例

http

/open-platform-service/v1/robot/list_by_device_and_group?group_id=123

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"robots": [

{

"mac": "00:00:15:EF:A4:30",

"sn": "0OP10164655230",

"robot_name": "robot",

"shop_id": 121562,

"shop_name": "門市"

}

]

}

}

# 發起呼叫任務

更新時間:2025-12-08 10:45:55

## 1. 介面說明

### 功能描述

可指定呼叫一臺機器到某一個點位，也可以隨機呼叫一臺機器到某一個點位。根據【取得指定機器人狀態V2】介面中的狀態進行回應。以下是機器調度狀態對呼叫任務的回應邏輯：

• run_state=OFFLINE 機器離線中，不可呼叫；

• run_state=DISABLE 表示機器當前不可執行任務；

• run_state=BUSY表示機器當前忙碌中，呼叫呼叫介面後，服務端會將任務放進隊列中，等待機器空閒後再給下達任務；

• run_state=IDLE 表示機器當前空閒，呼叫呼叫介面後機器會立即回應；

該介面回傳成功時會一起回傳task_id，開發者自行緩存，有以下作用：

• 透過【呼叫任務狀態通知】的回呼介面監聽任務狀態；

• 透過呼叫【取消呼叫任務】介面取消任務

• 透過呼叫【完成呼叫任務】介面來提前完成任務並執行下一個任務

需要注意當滿足2個條件的其中1個就會走新開放介面鏈路進行呼叫機器，否則需要走舊開放平台，需要運行SDK微服務

• 機器已經升級P-ONE系統

• call_mode為空或者call_mode=CALL

任務創建30分鐘後就會直接超時失敗，但是該超時時間可能存在變化，需要留意文檔更新。

在發起任務後，可以到[【回呼通知】-【任務執行】-【notifyCustomCall-呼叫狀態通知】](/zh/cloud-api/a0btpzfq266i1z7658flbwnz)訂閱任務狀態

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、KettyBot Pro、BellaBot Pro、PuduT300、FlashBot、KettyBot、BellaBot、Pudu Bot2、HolaBot

* **前置準備**：需確認機器人狀態為在線且空閒

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/custom_call |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| 參數名 | 類型 | 示例值 | 說明 |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| sn | string | N | 指定機器呼叫,如果這個參數不傳，傳了shop_id,就會隨機呼叫門市下的一臺空閒機器，沒有空閒機器就會進入排隊 |
| shop_id | int32 | N | 機器所屬門市ID，和SN必須二選一 |
| map_name | string | Y | 地圖名稱 |
| point | string | Y | 目標點位 |
| point_type | string | Y | 點位類型，如table等 |
| call_mode | string | N | \*\*呼叫模式：\*\*空：非自定義呼叫(呼叫到達點位就結束任務)；IMG：圖片模式、QR_CODE：支付二維碼業務模式、VIDEO：視頻模式、CALL_CONFIRM：呼叫抵達確認模式、CALL：呼叫抵達結束模式備註：呼叫P-ONE機器可以支持該參數，呼叫非P-ONE機器，當call_mode不為CALL時需要透過機器支持舊開放平台鏈路 |
| mode_data | **object** | N | 自定義呼叫的附加內容，僅特定模式需要 |
| do_not_queue | bool | N | 如果傳true，則不需要進入排隊，一旦無法執行任務，則直接回傳失敗 |

### Params.mode_data

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| urls | Array<string> | N | 圖片的顯示地址或視頻播放的地址 |
| switch_time | int32 | N | 圖片模式：圖片切換的時間(秒) |
| play_count | int32 | N | 視頻模式：視頻播放輪詢次數 |
| cancel_btn_time | int32 | N | 內容取消按鈕顯示時間(秒) |
| show_timeout | int32 | N | 內容顯示超時時間(秒) |
| qrcode | string | N | 二維碼內容 |
| text | string | N | 二維碼模式下的文本內容 |

## 4.回傳參數

### 回傳內容（Response）

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| message | string | 回傳錯誤碼，成功SUCCESS |
| data | **object** | 呼叫結果資料 |

### Res.data

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| task_id | string | 任務ID |
| queue | int32 | 當前排隊號碼，如果當前機器忙碌會進入排隊，回傳的state=QUEUEING，僅當status=QUEUEING有效 |
| state | string | 當前狀態，"CALLING": 呼叫機器中,"CALL_SUCCESS": 機器回應成功,"QUEUEING": 排隊中,"CALL_FAILED": 呼叫失敗,"CALL_COMPLETE": 呼叫完成,"QUEUING_CANCEL": 取消排隊,"TASK_CANCEL": 任務被取消,"ROBOT_CANCEL": 機器端取消 |
| remark | string | 任務備註 |

## 5.呼叫範例

### 請求範例

http

POST /open-platform-service/v1/custom_call

json

{

"sn": "SN-PD202405000001",

"shop_id": 1001,

"map_name": "餐廳1樓",

"point": "TABLE-001",

"point_type": "table",

"call_device_name": "服務員終端001",

"call_mode": "IMG",

"mode_data": {

"urls": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],

"switch_time": 5,

"cancel_btn_time": 10,

"show_timeout": 30

},

"do_not_queue": false

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"task_id": "CALL-202405201234567890",

"queue": 1,

"state": "CALLING",

"remark": "呼叫任務已創建"

}

}

# 取消呼叫任務

更新時間:2025-11-11 20:14:00

## 1. 說明

### 功能描述

取消指定的自定義呼叫任務。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、KettyBot Pro、BellaBot Pro、PuduT300、FlashBot、KettyBot、BellaBot、Pudu Bot2、HolaBot

* **前置準備**：需確認呼叫任務存在且未完成

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/custom_call/cancel |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| task_id | string | N | 呼叫任務id，發起呼叫任務時回傳的task_id欄位，需要注意發起呼叫任務和取消呼叫任務必須時同一個APPKEY操作，否則會回傳CLOUD_OPEN_TASK_BELONG_ERROR錯誤 |
| sn | string | N | 如果沒傳task_id，但是傳了sn，則取消sn下的所有未完成任務 |
| is_auto_back | bool | N | 如果取消當前任務，機器是否自動返航 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 服務端回傳錯誤碼 |

## 5.呼叫範例

### 請求範例

http

POST /open-platform-service/v1/custom_call/cancel

json

{

"task_id": "CALL-202405201234567890",

"is_auto_back": true

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS"

}

# 完成呼叫任務

更新時間:2025-11-11 20:14:42

## **1. 完成自定義呼叫**

### **功能描述**

當呼叫任務非自動完成模式時，可調該介面完成指定的自定義呼叫任務，並可選擇執行下一個自定義任務。

### **適用範圍**

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、KettyBot Pro、BellaBot Pro、PuduT300

* **前置準備**：需確認呼叫任務存在且正在執行

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/custom_call/complete |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| task_id | string | Y | 呼叫任務id，需要注意發起呼叫任務和完成呼叫任務必須時同一個APPKEY操作，否則會回傳 |
| next_call_task | object | N | 下個自定義任務 |

### Params.next_call_task

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| shop_id | int32 | Y | 機器所屬門市ID |
| map_name | string | Y | 地圖名稱 |
| point | string | Y | 目標點位 |
| point_type | string | Y | 點位類型，如table等 |
| call_mode | string | N | 呼叫模式：空(非自定義呼叫)、IMG(圖片模式)、QR_CODE(支付二維碼業務模式)、VIDEO(視頻模式)、CALL_CONFIRM(呼叫抵達確認模式)、CALL(呼叫抵達結束模式) |
| mode_data | **object** | N | 自定義呼叫的附加內容，僅特定模式需要 |

### Params.next_call_task.mode_data

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| urls | Array<string> | N | 圖片的顯示地址或視頻播放的地址 |
| switch_time | int32 | N | 圖片模式：圖片切換的時間(秒) |
| play_count | int32 | N | 視頻模式：視頻播放輪詢次數 |
| cancel_btn_time | int32 | N | 內容取消按鈕顯示時間(秒) |
| show_timeout | int32 | N | 內容顯示超時時間(秒) |
| qrcode | string | N | 二維碼內容 |
| text | string | N | 二維碼模式下的文本內容 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 服務端回傳錯誤碼 |
| data | **object** | 完成結果資料 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| next_call_result | **object** | 下一個人任務直接執行結果 |

### Res.data.next_call_result

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| message | string | 下一個任務執行結果，SUCCESS成功 |
| task_id | string | 下一個任務id |

## 5.呼叫範例

### 請求範例

http

POST /open-platform-service/v1/custom_call/complete

json

{

"task_id": "CALL-202405201234567890",

"next_call_task": {

"shop_id": 1001,

"map_name": "餐廳1樓",

"point": "TABLE-001",

"point_type": "table",

"call_device_name": "服務員終端001",

"call_mode": "IMG",

"mode_data": {

"urls": [

"https://example.com/image1.jpg",

"https://example.com/image2.jpg"

],

"switch_time": 5,

"cancel_btn_time": 10,

"show_timeout": 30

},

"do_not_queue": false

}

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"next_call_result": {

"message": "SUCCESS",

"task_id": "CALL-202405201234567891"

}

}

}

# 發送自定義展示內容

更新時間:2025-11-11 20:13:07

發起呼叫任務(call_mode非空，且非呼叫抵達結束模式)之後，機器到達呼叫點，可向向指定機器人發送自定義展示內容，支持圖片、視頻、二維碼等多種展示模式。需要注意，該介面發送的任務參數只直接推送給機器，不會影響雲端的任務資料。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、BellaBot Pro、PuduT300、PuduBot2

* **前置準備**：需確認機器人正在執行自定義呼叫任務

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/custom_content |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |
| payload | **object** | Y | 自定義內容參數 |

### Params.payload

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| call_mode | string | Y | 呼叫模式：IMG(圖片模式)、QR_CODE(支付二維碼業務模式)、VIDEO(視頻模式)、CALL_CONFIRM(呼叫抵達確認模式)、CALL(呼叫抵達結束模式) |
| task_id | string | Y | 自定義呼叫任務的id |
| mode_data | **object** | N | 模式資料 |

### Params.payload.mode_data

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| urls | Array<string> | N | 圖片的顯示地址或視頻播放的地址 |
| switch_time | int32 | N | 圖片模式：圖片切換的時間(秒) |
| play_count | int32 | N | 視頻模式：視頻播放輪詢次數 |
| cancel_btn_time | int32 | N | 內容取消按鈕顯示時間(秒) |
| show_timeout | int32 | N | 內容顯示超時時間(秒) |
| qrcode | string | N | 二維碼內容 |
| text | string | N | 二維碼模式下的文本內容 |

## 4.回傳參數

### 回傳內容（Response）

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息 |
| data | **object** | 發送結果資料 |

### Res.data

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| code | int32 | 回傳碼 |
| message | string | 回傳消息 |

## 5.呼叫範例

### 請求範例

http

POST /open-platform-service/v1/custom_content

json

{

"sn": "SN-PD202405000001",

"payload": {

"call_mode": "IMG",

"task_id": "TASK-202405201234567890",

"mode_data": {

"urls": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],

"switch_time": 5,

"cancel_btn_time": 10,

"show_timeout": 30

}

}

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"code": 0,

"message": "內容發送成功"

}

}

# 取得呼叫列表

更新時間:2025-11-11 20:18:49

## 1. 說明

### 功能描述

取得指定機器人的呼叫任務列表。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、KettyBot Pro、BellaBot Pro、PuduT300、FlashBot、KettyBot、BellaBot、Pudu Bot2、HolaBot

* **前置準備**：

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/call/list |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| sn | string | N | 機器人序列號 |
| task_id | string | N | 任務ID |
| shop_id | int32 | N | 門市ID |
| status | Array<string> | N | 狀態列表，以上4個非必填參數都沒傳就會報錯 |
| offset | int32 | N | 偏移量 |
| limit | int32 | N | 限制數量，預設10 |

## 4.回傳參數

### 回傳內容（Response）

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息 |
| data | **Object** | 呼叫任務資料 |

### Res.data

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| total | int32 | 總數 |
| list | **Array<object>** | 呼叫任務列表 |

### Res.data.list

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| task_id | string | 任務ID |
| shop_id | int32 | 門市ID |
| map_name | string | 地圖名稱 |
| point | string | 目標點位 |
| sn | string | 機器人序列號 |
| queue | int32 | 排隊號碼，僅當status=QUEUEING有效 |
| create_time | int32 | 創建時間,秒時間戳 |
| finish_time | int32 | 完成時間，秒時間戳 |
| status | string | 狀態，"CALLING": 呼叫機器中,"CALL_SUCCESS": 機器回應成功,"QUEUEING": 排隊中,"CALL_FAILED": 呼叫失敗,"CALL_COMPLETE": 呼叫完成,"QUEUING_CANCEL": 取消排隊,"TASK_CANCEL": 任務被取消,"ROBOT_CANCEL": 機器端取消 |
| remark | string | 備註 |
| product_code | string | 產品代碼 |

## 5.呼叫範例

### 請求範例

http

GET /open-platform-service/v1/call/list?sn=SN-PD202405000001&limit=10

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"total": 5,

"list": [

{

"task_id": "CALL-202405201234567890",

"shop_id": 1001,

"map_name": "餐廳1樓",

"point": "TABLE-001",

"sn": "SN-PD202405000001",

"queue": 1,

"create_time": 1640995200,

"finish_time": 1640995800,

"status": "COMPLETE",

"remark": "呼叫任務",

"product_code": "PD-001"

}

]

}

}

# 配送任務

更新時間:2025-12-03 11:17:31

## 1. 說明

### 功能描述

向指定機器人發送配送任務，支持多託盤配送和自定義配送方式。在發起任務後，可以到[【回呼通知】-【任務執行】-【notifyDeliveryTask-配送任務通知】](/zh/cloud-api/nmaif4pbid8jsp9lw9xzec9j)訂閱任務狀態。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、KettyBot Pro、BellaBot Pro、PuduT300、BellaBot、Pudu Bot2

* **前置準備**：需確認機器人狀態為在線且空閒

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/delivery_task |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |
| payload | **object** | Y | 配送任務參數 |

### Params.payload

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| type | string | Y | NEW：為新的任務，在編輯任務界面可以接收該請求； MODIFY：為修改任務，在配送任務中的機器人可以強制修改配送任務 |
| delivery_sort | string | Y | AUTO：機器人自己根據最近目標點排序配送目標； FIXED：使用發送的任務順序配送 |
| execute_task | bool | Y | 是否直接執行任務： TRUE：在發送任務後，機器人接收成功會直接執行任務 FALSE: 在發送後，只會在機器人配送任務界面輸入相關任務，需要人工點擊出發或者呼叫“給機器發送操作指令”介面的 Start 指令來啟動 |
| trays | **Array<object>** | Y | 託盤列表 |

### Params.payload.trays

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| destinations | **Array<object>** | Y | 注意這裡，二維數組，即一層託盤放多個菜 |

### Params.payload.trays.destinations

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| destination | string | Y | 配送目的地名稱,該欄位原欄位名是points |
| id | string | Y | 訂單 id，在配送狀態通知時會回執該 id，可以不填 |
| phone_num | string | N | 電話號碼 |
| phone_code | string | N | 手機號碼區號 eg:+86 |
| map_info | **object** | N | 地圖資訊 |

### Params.payload.trays.destinations.map_info

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| map_name | string | 點位所屬的地圖名稱 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息，SUCCEESS成功 |
| data | **object** | 任務結果資料 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| code | int32 | 機器回傳碼 |
| message | string | 機器回傳消息 |
| task_id | string | 機器回傳的任務ID |

## 5.呼叫範例

### 請求範例

http

POST /open-platform-service/v1/delivery_task

json

{

"sn": "SN-PD202405000001",

"payload": {

"type": "NEW",

"delivery_sort": "AUTO",

"execute_task": true,

"trays": [

{

"destinations": [

{

"destination": "TABLE-001",

"id": "DELIVERY-001",

"phone_num": "13800138000",

"phone_code": "+86"

}

]

}

]

}

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"code": 0,

"message": "配送任務創建成功",

"task_id": "TASK-202405201234567890"

}

}

# 配送指令

更新時間:2025-12-03 11:01:13

## 1. 說明

### 功能描述

向指定機器人發送配送任務的操作指令，如開始、完成、取消等。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、KettyBot Pro、BellaBot Pro、PuduT300、BellaBot、Pudu Bot2

* **前置準備**：需確認機器人有正在執行的配送任務

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/delivery_action |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |
| payload | object | Y | 操作指令參數 |

### Params.payload

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| action | string | Y | START：開始配送任務，需要在配送任務界面時生效； COMPLETE：完成配送任務，需要抵達後顯示抵達界面時，指令才能生效； CANCEL_ALL_DELIVERY: 取消所有配送任務，機器人在執行配送任務過程中指令才生效（當抵達任務點沒有完成任務時，指令無效） |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息，SUCCESS說明成功 |
| data | **object** | 操作結果資料 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| code | int32 | 機器回傳碼 |
| message | string | 機器回傳消息 |
| task_id | string | 如果當前配送任務是在機器發起的，這裡發送操作指令後機器會再次回傳任務ID給開發者 |

## 5.呼叫範例

### 請求範例

http

POST /open-platform-service/v1/delivery_action

json

{

"sn": "SN-PD202405000001",

"payload": {

"action": "START"

}

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"code": 0,

"message": "操作指令執行成功",

"task_id": "TASK-202405201234567890"

}

}

# 運送任務

更新時間:2025-12-03 11:06:48

## 1. 說明

### 功能描述

向指定機器人發送運送任務，支持出發點、優先級以及3個以上目標點的複雜配送場景。在發起任務後，可以到[【回呼通知】-【任務執行】-【notifyDeliveryTask-配送任務通知】](/zh/cloud-api/eodjqzj382d1mskgwwuahjeu)訂閱任務狀態。

### 適用範圍

* **支援機型**：PuduBot2

* **前置準備**：需確認機器人狀態為在線且空閒

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/transport_task |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |
| payload | **object** | Y | 運送任務參數 |

### Params.payload

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| task_id | string | Y | 任務ID |
| type | string | Y | 任務類型：NEW(新任務)、MODIFY(修改任務) |
| delivery_sort | string | Y | 配送排序：AUTO：機器人自己根據最近目標點排序配送目標； FIXED：使用發送的任務順序配送 |
| execute_task | bool | Y | 是否直接執行任務： TRUE：在發送任務後，機器人接收成功會直接執行任務 FALSE: 在發送後，只會在機器人配送任務界面輸入相關任務，需要人工點擊出發或者呼叫“給機器發送操作指令”介面的 Start 指令來啟動 |
| trays | array | Y | 託盤列表 |
| start_point | **object** | N | 起始點資訊 |
| start_wait_time | int32 | N | 起始點超時時間(秒) |
| end_wait_time | int32 | N | 目標點超時時間(秒) |
| task_remark | string | N | 任務說明 |
| priority | int32 | N | 優先級(0-10，越小越優先) |
| extend1 | string | N | 擴展欄位1 |
| extend2 | string | N | 擴展欄位2 |
| extend3 | string | N | 擴展欄位3 |

### Params.payload.start_point

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| destination | string | Y | 目的地 |
| content_type | string | Y | 內容類型：IMG(圖片)、QR_CODE(二維碼)、VIDEO(視頻)、TEXT(文本) |
| content_data | string | Y | 內容資料 |

### Params.payload.trays

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| destinations | **Array<object>** | Y | 運送目標列表 |

### Params.payload.trays.destinations

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| points | string | Y | 目標點位 |
| id | string | Y | 運送ID |
| name | string | Y | 物品名稱 |
| amount | int32 | Y | 數量 |
| content_type | string | N | 內容類型：IMG、QR_CODE、VIDEO、TEXT |
| content_data | string | N | 內容資料 |
| tray_index | int32 | N | 託盤編號(從上到下1,2,3...) |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息 |
| data | **object** | 任務結果資料 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| code | int32 | 回傳碼 |
| message | string | 回傳消息 |
| task_id | string | 任務ID |

## 5.呼叫範例

### 請求範例

http

POST /open-platform-service/v1/transport_task

json

{

"sn": "SN-PD202405000001",

"payload": {

"task_id": "TRANSPORT-001",

"type": "NEW",

"delivery_sort": "AUTO",

"execute_task": true,

"trays": [

{

"destinations": [

{

"points": "TABLE-001",

"id": "ITEM-001",

"name": "咖啡",

"amount": 2,

"content_type": "IMG",

"content_data": "https://example.com/coffee.jpg",

"tray_index": 1

}

]

}

],

"start_point": {

"destination": "廚房",

"content_type": "TEXT",

"content_data": "請取餐"

},

"start_wait_time": 30,

"end_wait_time": 60,

"task_remark": "VIP客戶配送",

"priority": 1

}

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"code": 0,

"message": "運送任務創建成功",

"task_id": "TASK-202405201234567890"

}

}

# 運送指令

更新時間:2025-12-03 11:08:24

## 1. 給機器人發送運送操作指令

### 功能描述

向指定機器人發送運送任務的操作指令。

### 適用範圍

* **支援機型**：PuduBot2

* **前置準備**：需確認機器人有正在執行的運送任務

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/transport_action |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |
| payload | **object** | Y | 操作指令參數 |

### Params.payload

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| action | string | Y | START：開始配送任務，需要在配送任務界面時生效； COMPLETE：完成配送任務，需要抵達後顯示抵達界面時，指令才能生效； CANCEL_ALL_DELIVERY: 取消所有配送任務，機器人在執行配送任務過程中指令才生效（當抵達任務點沒有完成任務時，指令無效） |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息 |
| data | **object** | 操作結果資料 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| code | integer | 回傳碼 |
| message | string | 回傳消息 |
| task_id | string | 任務ID |

## 5.呼叫範例

### 請求範例

http

POST /open-platform-service/v1/transport_action

json

{

"sn": "SN-PD202405000001",

"payload": {

"action": "START"

}

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"code": 0,

"message": "操作指令執行成功",

"task_id": "TASK-202405201234567890"

}

}

# 跑腿任務

更新時間:2025-12-03 14:30:08

## 1. 說明

### 功能描述

向指定機器人發送跑腿任務。任務發送成功後可透過[【回呼通知】-【任務執行回呼】-【notifyErrandStatus-跑腿任務通知](/zh/cloud-api/l7iatjz5hvwuskbpi77zfgk7)】訂閱任務狀態。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

* **前置準備**：需確認機器人狀態為在線且空閒

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/task_errand |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |
| payload | **object** | Y | 跑腿任務參數 |

### Params.payload

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| tasks | **Array<object>** | Y | 任務列表 |
| auth | string | N | 任務下達授權資訊（如刷卡卡號、手動輸入的密碼） |
| back_mode | string | N | UNSPECIFIED(使用機器端設置)、RETURN(未取物時返航)、BACK_START(多個無人取物逐個回傳放物點) |

### Params.payload.tasks

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| task_name | string | Y | 子任務名稱,機器上報狀態時會用這個 |
| task_desc | string | Y | 子任務描述 |
| point_list | **Array<object>** | Y | 點位集合，目前機器只支持傳2個點位，一個放貨點，一個取貨點 |
| hatch_id | string | N | 艙門ID |

### Params.payload.tasks.point_list

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| map_name | string | Y | 地圖名稱 |
| map_code | string | N | 地圖code |
| point | string | Y | 點位id/名稱 |
| point_type | string | Y | 點位類型，table.... |
| verification_code | string | N | 驗證碼 |
| remark | string | N | 備註 |
| phone_num | string | N | 手機號 |
| phone_code | string | N | 手機號區號 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息 |
| data | **object** | 跑腿任務結果資料 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| code | int32 | 回傳碼 |
| message | string | 回傳消息 |
| session_id | string | 總任務id |

## 5.呼叫範例

### 請求範例

http

POST /open-platform-service/v1/task_errand

json

{

"sn": "SN-PD202405000001",

"payload": {

"tasks": [

{

"task_name": "跑腿任務001",

"task_desc": "送餐到1號桌",

"point_list": [

{

"map_name": "餐廳1樓",

"map_code": "R001",

"point": "TABLE-001",

"point_type": "table",

"phone_num": "13800138000",

"phone_code": "+86",

"remark": "這裡是放貨點"

},

{

"map_name": "餐廳1樓",

"map_code": "R001",

"point": "TABLE-002",

"point_type": "table",

"phone_num": "13800138000",

"phone_code": "+86",

"remark": "這裡是取貨點"

}

],

"hatch_id": "HATCH-001"

}

],

"auth": "CARD-123456",

"back_mode": "RETURN"

}

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"code": 0,

"message": "跑腿任務創建成功",

"session_id": "SESSION-202405201234567890"

}

}

# 跑腿任務控制指令

更新時間:2025-11-11 20:24:53

## 1. 發送跑腿指令

### 功能描述

向指定機器人發送跑腿操作指令。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

* **前置準備**：需確認機器人有正在執行的跑腿任務

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/errand_action |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |
| payload | **object** | Y | 跑腿指令參數 |

### Params.payload

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| session_id | string | Y | 總任務id，下達跑腿任務時機器回傳的，或者機器端發起的跑腿任務也會透過回呼通知裡回傳總任務id |
| action | string | Y | 操作類型：CANCEL(取消配送任務)、RETRY(重新配送) |
| auth | string | N | 任務下達授權資訊（如刷卡卡號、手動輸入的密碼） |
| hatch_id | string | N | 艙門id |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息 |
| data | **object** | 操作結果資料 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| code | int32 | 回傳碼 |
| message | string | 回傳消息 |
| session_id | string | 會話ID |

## 5.呼叫範例

### 請求範例

http

POST /open-platform-service/v1/errand_action

json

{

"sn": "SN-PD202405000001",

"payload": {

"session_id": "SESSION-202405201234567890",

"action": "CANCEL",

"auth": "CARD-123456",

"hatch_id": "HATCH-001"

}

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"code": 0,

"message": "跑腿指令執行成功",

"session_id": "SESSION-202405201234567890"

}

}

# 頂升任務

更新時間:2025-12-24 11:16:21

## 1. 給機器發送頂升任務

### 功能描述

向指定機器人發送頂升任務。任務發送成功後可透過[【回呼通知】-【任務執行回呼】-【notifyLiftingStatus-頂升任務通知】](/zh/cloud-api/rkyh9t3ck9tkxunegsk5j9pk)訂閱任務狀態。

### 適用範圍

* **支援機型**：PuduT300

* **前置準備**：需確認機器人狀態為在線且空閒

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/lifting_task |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |
| payload | **object** | Y | 頂升任務參數 |

### Params.payload

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| tasks | **Array<object>** | Y | 頂升任務列表 |
| type | string | Y | 配送方式：DISTINCE(機器人根據自己最近目標點排序途徑點)、DEFAULT(按途徑點順序進行運送) |

### Params.payload.tasks

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| point_list | **Array<object>** | Y | 點位資訊集合 |

### Params.payload.tasks.point_list

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| point_name | string | Y | 點位名稱 |
| point_type | string | Y | 點位類型，點位和貨架組：POINT、SECONDARY_GROUP |
| point_attr | string | Y | 點位屬性：放貨點、取貨點、逗留點 DROP_POINT 放貨點 LIFT_POINT 取貨點 STAY_POINT 逗留點 一個子任務必須有取貨點和放貨點，逗留點非必須 |
| map_info | **object** | Y | 地圖資訊 |
| fail_action | **object** | N | 失敗時做什麼動作 |

### Params.payload.tasks.point_list.map_info

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| map_name | string | Y | 地圖名稱 |
| map_code | string | N | 地圖代碼 |

### Params.payload.tasks.point_list.fail_action

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| action | string | Y | 失敗後動作枚舉：STAY(停在原地)、RETRY(重試)、SKIP(跳過)、GO_BACK_LIFT_POINT(回傳取貨點)、SPEC_POINT(前往指定位置) |
| data | **object** | N | action=SPEC_POINT時，需要帶上以下資訊 |

### Params.payload.tasks.point_list.fail_action.data

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| point_name | string | Y | 點位名稱 |
| point_type | string | Y | 點位類型，點位和貨架組：POINT、SECONDARY_GROUP |
| point_attr | string | Y | 點位屬性：放貨點、取貨點、逗留點 DROP_POINT 放貨點 LIFT_POINT 取貨點 STAY_POINT 逗留點 一個子任務必須有取貨點和放貨點，逗留點非必須 |
| map_info | **object** | Y | 地圖資訊,同【Params.payload.tasks.point_list.map_info】結構 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息 |
| data | **object** | 頂升任務結果資料 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_id | string | 任務ID |
| code | int32 | 回傳碼 |
| message | string | 回傳消息 |

## 5.呼叫範例

### 請求範例

http

POST /open-platform-service/v1/lifting_task

json

{

"sn": "SN-PD202405000001",

"payload": {

"tasks": [

{

"point_list": [

{

"point_name": "PICK-001",

"point_type": "POINT",

"point_attr": "DROP_POINT",

"map_info": {

"map_name": "倉庫1樓",

"map_code": "WH001"

},

"fail_action": {

"action": "RETRY"

}

}

]

}

],

"type": "DEFAULT"

}

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"task_id": "LIFTING-202405201234567890",

"code": 0,

"message": "頂升任務創建成功"

}

}

# 頂升任務控制指令

更新時間:2025-11-10 19:19:40

## 1. 給機器發送頂升指令

### 功能描述

向指定機器人發送頂升操作指令。

### 適用範圍

* **支援機型**：PuduT300

* **前置準備**：需確認機器人有正在執行的頂升任務

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/lifting_action |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |
| task_id | string | Y | 任務ID,下達任務時機器回傳的，或者機器端發起的任務也會透過回呼通知裡回傳總任務id |
| action | string | Y | 操作類型：PAUSE(暫停)、RESUME(恢復任務)、FINISH_ONE(使機器在途徑點結束逗留)、CANCEL_ALL_LIFTIONG(取消所有頂升任務) |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息 |
| data | **object** | 操作結果資料 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| code | int32 | 機器回傳碼 |
| message | string | 機器回傳消息 |

## 5.呼叫範例

### 請求範例

http

POST /open-platform-service/v1/lifting_action

json

{

"sn": "SN-PD202405000001",

"task_id": "LIFTING-202405201234567890",

"action": "PAUSE"

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"code": 0,

"message": "頂升指令執行成功"

}

}

# 清潔任務列表

更新時間:2025-11-11 20:23:09

## 1. 介面說明

### 功能描述

取得任務列表，用於查詢指定設備可用的清潔任務及其設定詳情。

### 適用範圍

* **支援機型**：CC1、CC1 Pro、MT1、MT1 Vac、MT1 Max

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /cleanbot-service/v1/api/open/task/list |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | Y | application/json |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | N | 機器 SN，機器SN和店鋪編號二選一 |
| shop_id | int32 | N | 門市 ID，機器SN和店鋪編號二選一 |
| mode | Array<int32> | N | 任務類型，1:手動任務，2.自動任務，3.巡檢任務&混合任務，不傳預設2 |
| product | Array<string> | N | 產品類型，不傳預設cleanbot,可傳cleanbot,mt1,mt1Pro,mt1Max |
| collaborative | int32 | N | 協同任務，1：先掃後洗，不傳該參數不生效 |

## 4.回傳參數

### 回傳內容（Response）

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS 成功 |
| data | **object** | 查詢結果 |

### Res.data

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| count | int32 | 任務總數 |
| item | **Array<object>** | 任務列表 |

### Res.data.item

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_id | string | 任務 ID |
| version | double | 任務版本 |
| name | string | 任務名稱 |
| desc | string | 任務描述 |
| config | **object** | 任務的清掃設定 |
| floor_list | **Array<object>** | 樓層列表 |
| status | int32 | 任務狀態 1:正常,-1:被刪除 |
| is_single_task | bool | 是否是單樓層 |
| task_count | int32 | 任務循環次數 0自定義,1 一次,2兩次 |
| task_mode | int32 | 任務模式 0 執行區域，不執行手路徑 1 區域+手推 2手推 |
| back_point | **object** | 返航點 |
| pre_clean_time | int32 | 預計清掃時間，單位秒 |
| is_area_connect | bool | 是否是連通域清潔 |
| station_config | **object** | 工作站/充電樁設定 |
| cleanagent_config | **object** | 清潔劑設定 |
| is_hand_sort | bool | 是否手動排序 |
| mode | int32 | 任務類型：1手動，2自動（0預設），3巡檢，4巡檢&自動混合 |
| temporary_point | **object** | 臨時停靠點 |
| product | string | 機器類型（如cleanbot、mt1、mt1Pro、mt1Max） |
| move_speed | double | 移動速度 |
| cleaning_speed | double | 清潔速度 |
| collaborative | int32 | 協同工作類型：1前掃後洗 |
| coll_list | **Array<object>** | 協同設備列表 |
| rgbd_recognition | int32 | RGBD 障礙物識別高度（mm，30-100） |
| device_name | string | 任務創建/更新者 |
| extend | string | 擴展欄位（JSON 字符串） |

### Res.data.item.config

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| mode | int32 | 清掃模式 1: 洗地,2: 掃地 |
| vacuum_speed | int32 | 掃地滾刷速度 0:關閉,1: 節能,2: 標準,3: 強勁 |
| vacuum_suction | int32 | 掃地吸力 0:關閉,1: 低,2: 中,3: 高 |
| wash_speed | int32 | 洗地滾刷速 0:關閉,1: 節能,2: 標準,3: 強勁 |
| wash_suction | int32 | 洗地吸力 0:關閉,1: 低,2: 中,3: 高 |
| wash_water | int32 | 洗地下水速度 0:關閉,1: 低,2: 中,3: 高 |
| type | int32 | 類型 0 自定義,1 地毯吸塵,2靜音塵推 |
| left_brush | int32 | 左邊刷（Monster 有）：1低 2中 3高 0關閉 |
| right_brush | int32 | 右邊刷（Monster & CC1）：1低 2中 3高 0關閉 |
| right_vacuum_suction | int32 | 掃地右吸力：1低 2中 3高 0關閉 |
| ai_adaptive_switch | bool | AI 自適應開關 |

### Res.data.item.floor_list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| map | **object** | 地圖資訊 |
| area_list | Array<string> | 區域 ID 列表 |
| area_array | **Array<object>** | 區域對象列表 |
| elv_array | **Array<object>** | 梯控對象列表 |

### Res.data.item.back_point

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| floor | string | 樓層 |
| map_name | string | 地圖名稱 |
| point_name | string | 點位名稱 |
| point_id | string | 點位 ID |

### Res.data.item.station_config

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| id | string | 工作站/充電樁 ID |
| station_name | string | 名稱 |
| station_type | int32 | 類型：1充電樁；2工作站 |
| station_funtion | int32 | 功能：1充電+換水；2僅充電 |
| map_name | string | 工作站地圖名稱 |
| station_mac | string | 工作站藍牙 MAC |

### Res.data.item.cleanagent_config

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| isopen | bool | 是否打開 |
| scale | int32 | 比例（例：1:50，填 50） |

### Res.data.item.temporary_point

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| floor | string | 樓層 |
| map_name | string | 地圖名稱 |
| point_name | string | 點位名稱 |
| point_id | string | 點位 ID |

### Res.data.item.coll_list

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| coll_mac | string | 協同設備 MAC |
| coll_config | **object** | 協同設備清潔設定,資料結構同【Res.data.item.config】 |
| coll_station_config | **object** | 協同設備基站設定【Res.data.item.station_config】 |
| coll_back_point | **object** | 協同設備返航點，資料結構同【Res.data.item.back_point】 |
| coll_temporary_point | **object** | 協同設備維護點，資料結構同【Res.data.item.temporary_point】 |

### Res.data.item.floor_list.map

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| name | string | 地圖名稱 |
| lv | int32 | 樓層等級 |
| floor | string | 樓層 |

### Res.data.item.floor_list.area_array

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| area_id | string | 區域 ID |
| clean_count | int32 | 清掃次數 |
| type | int32 | 0區域清掃，1施教路徑 |
| area | float | 區域面積 |
| area_name | string | 區域名稱 |

### Res.data.item.floor_list.elv_array

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| elv_id | string | 梯控 ID |
| elv_name | string | 梯控名稱 |

## 5.呼叫範例

### 請求範例

http

/cleanbot-service/v1/api/open/task/list?sn=SN123&shop_id=1&mode=2&product=cleanbot&collaborative=1

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"count": 1,

"item": [

{

"task_id": "1234567890",

"version": 1,

"name": "大廳一層清掃",

"desc": "一層全覆蓋清掃",

"config": {

"mode": 2,

"vacuum_speed": 2,

"vacuum_suction": 3,

"wash_speed": 2,

"wash_suction": 2,

"wash_water": 3,

"type": 0,

"left_brush": 2,

"right_brush": 2,

"right_vacuum_suction": 2,

"ai_adaptive_switch": true

},

"floor_list": [

{

"map": {

"name": "F1",

"lv": 1,

"floor": "1F"

},

"area_list": [

"area-001",

"area-002"

],

"area_array": [

# 清潔指令

更新時間:2025-11-11 20:22:56

## 1. 介面說明

### 功能描述

下達指令至設備（執行任務/動作），支持透過任務定義或點位進行控制。

### 適用範圍

* **支援機型**：CC1、CC1 Pro、MT1、MT1 Vac、MT1 Max

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /cleanbot-service/v1/api/open/task/exec |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON Body |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | Y | application/json |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 設備 SN |
| mac | string | N | 設備 MAC（開放平台通常使用 SN） |
| type | int32 | Y | 任務類型 1: 充電任務 2: 加排水任務 3: 清掃任務 4: 補給任務（充電+換水） 5:一鍵返航(有工作站回工作站，沒有工作站回返航點) 6:回返航點 9:切換地圖 10:控制定時任務開關 |
| clean | **object** | N | 任務定義 |

#### Params.clean

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| task_id | string | N | 任務 ID,當type=3時，該欄位有效 |
| version | float | N | 任務版本,當type=3時，該欄位有效 |
| name | string | N | 任務名稱,當type=3時，該欄位有效 |
| status | int32 | Y | 任務狀態 1:開始任務 3:暫停 4:取消 |
| cleanagent_scale | int32 | N | 清潔劑比例 。1:50傳50,當type=3時，該欄位有效 |
| point_id | string | N | 去充電/工作站/返航點（type 是 1，2,4,6）時下達，有則去指定點位，無則機器隨機 |
| map_name | string | N | type=9 時，切換地圖需要下達地圖名字 |
| cron_id | string | N | 當前type為10的時候，這個是定時任務id |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS 成功 |
| data | **object** | 執行結果 |

### Res.data（TaskExecuteReplyData）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_id | string | 任務 ID |

## 5.呼叫範例

### 請求範例

http

{

"sn": "SN123",

"type": 3,

"clean": {

"task_id": "T123",

"version": 1.0,

"name": "日常清潔",

"status":1

}

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"task_id": "T123"

}

}

# 定時任務

更新時間:2025-11-10 19:34:51

## 1. 說明

### 功能描述

取得定時任務列表，用於查看設備的定時清潔計劃。

### 適用範圍

* **支援機型**：清潔類型的機器

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /cleanbot-service/v1/api/open/cron/list |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | Y | application/json |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 設備 SN |
| limit | int32 | N | 分頁大小，每頁數量 預設10 |
| offset | int32 | N | 偏移量 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS 成功 |
| data | **object** | 定時任務列表 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| count | int32 | 總數 |
| list | **Array<object>** | 定時任務列表 |

### Res.data.list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| cron_id | string | 定時任務 ID |
| hour | int32 | 任務執行時間，小時：24小時制 |
| minute | int32 | 任務執行時間，分鐘 |
| weeks | Array<int32> | 任務執行時間，1週一，2週二，7周天 |
| task_list | **Array<object>** | 清潔任務計劃集合 |
| create_time | long | 創建時間戳 秒 |
| update_time | long | 更新時間戳 秒 |
| cron_status | string | 定時器任務 枚舉："close","open" |
| keep_time | int32 | 例如30分鐘，填30，表示定時任務時間倒後30分鐘內都可以在啟動 |
| repeat_clean_time | int32 | 重複清潔時間 |

### Res.data.list.task_list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_id | string | 任務 ID |
| task_version | long | 任務版本號 |
| name | string | 任務名稱 |
| task_desc | string | 任務描述 |
| pre_clean_time | int32 | 預計清掃時間（分鐘） |
| clean_area | double | 清掃面積 |
| map | **Array<object>** | 地圖名稱列表 |
| clean_mode | int32 | 1洗地；2掃地 |
| back_point | **object** | 返航點 |
| clean_type | int32 | 0自定義 1地毯吸塵 2靜音塵推 |
| mode | int32 | 任務類型：2覆蓋清潔（手動），3巡航清潔（自動） |
| product | string | 機器類型：cleanbot、cc1Pro、mt1Pro、mt1 |

### Res.data.list.task_list.map

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| name | string | 地圖名稱 |
| lv | int32 | 地圖版本 |
| floor | string | 樓層 |

### Res.data.list.task_list.back_point

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| floor | string | 樓層 |
| map_name | string | 返航點的地圖名稱 |
| point_name | string | 返航點名字 |
| point_id | string | 返航點位ID |

## 5.呼叫範例

### 請求範例

http

/cleanbot-service/v1/api/open/cron/list?sn=SN123&limit=10&offset=0

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"count": 49,

"list": [

{

"cron_id": "923623891597787136",

"device_name": "04:86:80:5F:17:62",

"pid": "OPUGRFU8O7NAQZCP",

"hour": 16,

"minute": 37,

"weeks": [

1,

2,

3,

4,

5,

6,

],

"task_list": [

{

"task_id": "1112889525015166976",

"task_version": 1747136609664,

"name": "舊1",

"task_desc": "",

"pre_clean_time": 1637,

"clean_area": 227.42,

"map": [

{

"name": "4#132#4樓-401-洗地",

"lv": 3,

"floor": "4"

}

],

# 給機器發送託盤推送任務

更新時間:2025-11-10 19:39:14

## 1. 說明

### 功能描述

向指定機器人的託盤推送訂單資訊。該介面為兼容SDK微服務的舊開放介面，新版本機器已經不支持。

### 適用範圍

* **支援機型**：Flashbot

* **前置準備**：需確認機器人狀態為在線

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/tray_order |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |
| payload | **object** | Y | 訂單推送參數 |

### Params.payload

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| orders | **Array<object>** | Y | 訂單列表 |
| tray_index | int32 | N | 指定第幾層託盤設置訂單，機器人託盤輸入界面從上向下1開始。0為不指定託盤，預設選擇界面託盤選中的託盤 |

### Params.payload.orders

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| table_no | string | Y | 桌編號（該協議列表中的目標必須一樣） |
| table_name | string | Y | 桌名稱，必須與機器人上地圖目標點一致（該協議列表中的目標必須一樣） |
| name | string | Y | 菜名 |
| amount | int32 | Y | 數量 |
| id | string | Y | 訂單唯一id。機器在運行中會將訂單狀態同步，使用的是該id |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | **object** | 推送結果資料 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| code | int32 | 機器回傳碼 |
| message | string | 機器回傳消息 |

## 5.呼叫範例

### 請求範例

http

POST /open-platform-service/v1/tray_order

json

{

"sn": "SN-PD202405000001",

"payload": {

"orders": [

{

"table_no": "T001",

"table_name": "1號桌",

"name": "宮保雞丁",

"amount": 1,

"id": "ORDER-001"

}

],

"tray_index": 1

}

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"code": 0,

"message": "訂單推送成功"

}

}

# 取得廣告列表

更新時間:2025-11-11 20:19:21

## 1. 說明

### 功能描述

取得根據門市id取得廣告列表

### 適用範圍

* **支援機型**：Flashbot、FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /biz-service/openPlatform/api/v1/gg/list |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |

### 請求參數（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| shop_id | int3232 | Y | 門市id |
| sn | string | Y | 偏移量（預設為0） |
| kind | int3232 | N | 1普通場景 2高級場景 3 小屏廣告 |
| limit | int3232 | N | 單頁條數 |
| offset | int3232 | N | 查詢限制的數量） offset = page\*limit |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | **object** | 查詢結果 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| count | int3232 | 總數 |
| items | **Array<object>** | 列表項 |

### Res.data.items

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| id | long | 廣告 ID |
| name | string | 廣告名稱 |
| shop_id | int32 | 門市 ID |
| start_time | int32 | 生效開始時間戳（秒） |
| end_time | int32 | 生效結束時間戳（秒） |
| second | int32 | 輪播間隔秒，1-60 |
| ad_list | **Array<object>** | 媒資列表 |
| status | int32 | 狀態：1生效 2停用 3下架 |
| create_time | string | 創建時間 |
| update_time | string | 更新時間 |
| times | int32 | 播放次數或輪次 |
| mac | string | 設備 MAC |
| sn | string | 設備 SN |
| is_expired | bool | 是否已過期 |
| show_type | int32 | 顯示類型：1單屏，3三屏 |
| scenes | Array<string> | 生效場景集合 |
| kind | int32 | 廣告類型：1普通 2高級 3輕量 |
| map_name | string | 地圖名稱 |
| map_point32s | Array<string> | 地圖點位集合 |
| media_type | int32 | 媒體類型：1圖片 2視頻 |

### Res.data.items.ad_list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| md5 | string | 文件 MD5 |
| type | int32 | 0圖片 1視頻 |
| url | string | 資源 URL |

## 5.呼叫範例

### 請求範例

json

{

"shop_id": 1001,

"sn": "SN-PD202405000001",

"kind": 1,

"limit": 10,

"offset": 0

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_bd969310-1208-40c3-9495-e21ebd4ac7db",

"message": "success",

"data": {

"count": 2,

"items": [

{

"id": "63358973",

"name": "509600002-00:01:21:C2:5B:3D-1745493328346",

"shop_id": 352400007,

"start_time": "1745424000000",

"end_time": "1748015999000",

"second": 5,

"ad_list": [

{

"md5": "98fe2eb98e3775b28205d69ce408ab8e",

"size": 0,

"type": 0,

"url": "https://download.pudutech.com/puduLink_axpp/wx/otherOs/chixzdls_int32ernal02/31373435343933333237343736666166.png"

}

],

"status": 1,

"create_time": "1745499499",

"update_time": "1745499499",

"times": 0,

"creator": "",

"mac": "94:A1:A2:84:06:B6",

"sn": "",

"is_expired": false,

"show_type": 3,

"scenes": [

"cruise_on_arrival"

],

"kind": 2,

"map_name": "",

"map_point32s": [],

# 取得廣告詳情

更新時間:2025-11-11 20:20:20

## 1. 說明

### 功能描述

取得單條廣告詳情。

### 適用範圍

* **支援機型**：Flashbot、FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /biz-service/openPlatform/api/v1/gg/get |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3. 請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 建議固定值 |

### 請求參數（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| id | long | Y | 廣告 ID |
| shop_id | int32 | Y | 門市 ID |

## 4. 回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 提示資訊 |
| data | **object** | 廣告詳情 |

### Res.data（AdModel）

| **欄位** | **類型** | **說明** |
| --- | --- | --- |
| id | long | 廣告 ID |
| name | string | 廣告名稱 |
| shop_id | int32 | 門市 ID |
| start_time | int32 | 生效開始時間戳（秒） |
| end_time | int32 | 生效結束時間戳（秒） |
| second | int32 | 輪播間隔秒，1-60 |
| ad_list | **Array<object>** | 媒資列表 |
| status | int32 | 狀態：1生效 2停用 3下架 |
| create_time | string | 創建時間 |
| update_time | string | 更新時間 |
| times | int32 | 播放次數或輪次 |
| mac | string | 設備 MAC |
| sn | string | 設備 SN |
| is_expired | bool | 是否已過期 |
| show_type | int32 | 顯示類型：1單屏，3三屏 |
| scenes | Array<string> | 生效場景集合 |
| kind | int32 | 廣告類型：1普通 2高級 3輕量 |
| map_name | string | 地圖名稱 |
| map_point32s | Array<string> | 地圖點位集合 |
| media_type | int32 | 媒體類型：1圖片 2視頻 |

### Res.data.items.ad_list

| **欄位** | **類型** | **說明** |
| --- | --- | --- |
| md5 | string | 文件 MD5 |
| type | int32 | 0圖片 1視頻 |
| url | string | 資源 URL |

## 5. 呼叫範例

### 請求範例

http

GET /biz-service/openPlatform/api/v1/gg/get?id=10001&shop_id=1001

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"id": 10001,

"name": "門市開業促銷",

"shop_id": 1001,

"start_time": 1730208000,

"end_time": 1732813200,

"second": 8,

"ad_list": [

{ "md5": "abc123", "type": 0, "url": "https://cdn.example.com/a1.jpg" }

],

"status": 1,

"create_time": "2025-10-01 10:00:00",

"update_time": "2025-10-02 12:00:00",

"times": 3,

"mac": "00:11:22:33:44:55",

"sn": "SN-PD202405000001",

"is_expired": false,

"show_type": 1,

"scenes": ["大廳", "收銀臺"],

"kind": 1,

"map_name": "一樓",

"map_point32s": ["A1", "A2"],

"media_type": 1

}

}

# 新增廣告

更新時間:2025-11-11 20:15:33

## 1. 說明

### 功能描述

新增廣告設定。

### 適用範圍

* **支援機型**：Flashbot、FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /biz-service/openPlatform/api/v1/gg/create |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3. 請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值 |

### 請求參數（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| name | string | Y | 名稱（2-255） |
| shop_id | int32 | Y | 門市 ID（>0） |
| start_time | long | Y | 開始時間戳（秒） |
| end_time | long | Y | 結束時間戳（秒） |
| show_type | int32 | N | 顯示類型：1單屏 3三屏 |
| ad_list | **Array<object>** | N | 媒資列表 |
| times | int32 | N | 播放輪次 |
| second | int32 | N | 輪播間隔秒 |
| sn | string | Y | 設備 SN（非空） |
| scenes | Array<string> | N | 生效場景 |
| kind | int32 | N | 類型：1普通 2高級 3輕量 |
| map_name | string | N | 地圖名稱 |
| map_point32s | Array<string> | N | 地圖點位集合 |
| media_type | int32 | N | 媒體類型：1圖片 2視頻 |

#### Params.ad_list

| **欄位** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| md5 | string | N | 文件 MD5 |
| type | int32 | N | 0圖片 1視頻 |
| url | string | Y | 資源 URL（非空） |

## 4. 回傳參數

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 提示資訊,SUCCESS成功 |
| data | object | 新建結果 |

## 5. 呼叫範例

### 請求範例

json

{

"shop_id": 352400007,

"sn": "BLBLEFGBOT00002",

"kind": 3,

"map_name": "",

"start_time": 1745993238671,

"end_time": 1748585238671,

"second": 10,

"show_type": 3,

"ad_list": [

{

"type": 1,

"size": 0,

"url": "https://download.pudutech.com/puduLink_axpp/wx/otherOs/chixzdls_int32ernal02/31373435343933333237343736666166.png",

"md5": "98fe2eb98e3775b28205d69ce408ab8e"

},

{

"type": 1,

"size": 0,

"url": "https://download.pudutech.com/puduLink_axpp/wx/otherOs/chixzdls_int32ernal02/3137343534393333323738343478556c.png",

"md5": "98fe2eb98e3775b28205d69ce408ab8e"

}

],

"map_point32s": [

],

"scenes": [

"soliciting_passengers_mode",

"cruise_mode"

],

"media_type": 1

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_bd969310-1208-40c3-9495-e21ebd4ac7db",

"message": "SUCCESS"

}

# 更新廣告

更新時間:2025-11-11 20:16:01

## 1. 介面說明

### 功能描述

更新廣告設定。

### 適用範圍

* **支援機型**：Flashbot、FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /biz-service/openPlatform/api/v1/gg/update |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3. 請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值 |

### 請求參數（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| id | long | Y | 廣告 ID |
| name | string | N | 名稱 |
| start_time | long | N | 開始時間戳（>0 則校驗） |
| end_time | long | N | 結束時間戳（>0 則校驗） |
| show_type | int32 | N | 顯示類型 |
| ad_list | **Array<object>** | N | 媒資列表 |
| status | int32 | N | 狀態：1生效 2停用 3下架 |
| times | int32 | N | 輪次 |
| second | int32 | N | 輪播間隔秒 |
| shop_id | int32 | Y | 門市 ID（>0） |
| sn | string | N | 設備 SN |
| scenes | Array<string> | N | 生效場景 |
| map_name | string | N | 地圖名稱 |
| map_point32s | Array<string> | N | 地圖點位集合 |
| media_type | int32 | N | 1圖片 2視頻 |

#### Params.ad_list

| **欄位** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| md5 | string | N | 文件 MD5 |
| type | int32 | N | 0圖片 1視頻 |
| url | string | Y | 資源 URL（非空） |

## 4. 回傳參數

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 提示資訊 |

## 5. 呼叫範例

### 請求範例

json

{

"id": "63358970",

"shop_id": 509600002,

"mac": "00:01:21:C2:5B:3D",

"scenes": [

"cruise_on_arrival"

],

"mapName": "",

"map_point32s": [],

"show_type": 3,

"second": 5,

"ad_list": [

{

"md5": "98fe2eb98e3775b28205d69ce408ab8e",

"size": 0,

"type": 0,

"url": "https://download.pudutech.com/puduLink_axpp/wx/otherOs/chixzdls_int32ernal02/31373435343933333237343736666166.png",

"duration": 0

},

{

"md5": "98fe2eb98e3775b28205d69ce408ab8e",

"size": 0,

"type": 0,

"url": "https://download.pudutech.com/puduLink_axpp/wx/otherOs/chixzdls_int32ernal02/3137343534393333323738343478556c.png",

"duration": 0

},

{

"md5": "98fe2eb98e3775b28205d69ce408ab8e",

"size": 0,

"type": 0,

"url": "https://download.pudutech.com/puduLink_axpp/wx/otherOs/chixzdls_int32ernal02/313734353439333332383135384a6670.png",

"duration": 0

}

],

"start_time": 1745424000000,

"end_time": 1779551999000,

### 回傳範例

json

{

"trace_id": "YourApiAppKey_bd969310-1208-40c3-9495-e21ebd4ac7db",

"message": "success"

}

# 刪除廣告

更新時間:2025-11-11 20:07:40

## 1. 介面說明

### 功能描述

刪除廣告。

### 適用範圍

* **支援機型**：Flashbot、FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /biz-service/openPlatform/api/v1/gg/delete |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3. 請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值 |

### 請求參數（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| id | long | Y | 廣告 ID |
| shop_id | int32 | Y | 門市 ID（>0） |

## 4. 回傳參數

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 提示資訊 |

## 5. 呼叫範例

### 請求範例

json

{

"shop_id": 352400007,

"id": "63358973"

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_bd969310-1208-40c3-9495-e21ebd4ac7db",

"message": "success"

}

# 取得廣告場景

更新時間:2025-11-11 20:19:47

## 1. 介面說明

### 功能描述

取得廣告場景列表（按菜單模式組織）。

### 適用範圍

* **支援機型**：Flashbot、FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /biz-service/openPlatform/api/v1/gg/scenesMenu/list |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3. 請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值 |

### 請求參數（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| lang | string | N | 預設中文（支援語系查看附錄） |
| kind | int32 | Y | 廣告種類 1普通場景廣告 2高級場景廣告 3小屏廣告 |
| product_name | string | N | 產品名稱 詳見FAQ |

## 4. 回傳參數

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 提示資訊 |
| data | **object** | 場景資料 |

#### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| scenes_list | **Array<object>** | 場景菜單列表 |

#### Res.data.scenes_list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| menu_name | string | 菜單名稱 |
| title | string | 菜單標題 |
| order_weight | float | 排序權重 |
| scenes_model_list | **Array<object>** | 場景集合 |

##### Res.data.scenes_model_list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| id | long | 場景 ID |
| name | string | 場景名稱 |
| title | string | 場景標題 |
| belong_mode | string | 歸屬模式 |
| order_weight | float | 排序權重 |
| need_map | bool | 是否需要地圖 |

## 5. 呼叫範例

### 請求範例

json

{

"kind": 2,

"lang": "en-US",

"product_name": "KettyBot"

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_bd969310-1208-40c3-9495-e21ebd4ac7db",

"message": "SUCCESS",

"data": {

"scenes_list": [

{

"menu_name": "deliver_food_mode_menu",

"title": "送餐模式",

"order_weight": 0,

"scenes_model_list": [

{

"id": "12",

"name": "deliver_food_mode",

"title": "送餐到達",

"belong_mode": "deliver_food_mode_menu",

"order_weight": 0,

"need_map": true

},

{

"id": "27",

"name": "waiting_for_delivery_mode",

"title": "等待取餐",

"belong_mode": "deliver_food_mode_menu",

"order_weight": 0,

"need_map": true

},

{

"id": "28",

"name": "pick_up_completed_mode",

"title": "取餐完成",

"belong_mode": "deliver_food_mode_menu",

"order_weight": 0,

"need_map": true

}

]

},

# 取得巡航路徑

更新時間:2025-12-04 16:29:15

## 1. 介面說明

### 功能描述

發起巡航任務時需要執行巡航路徑，可透過該介面取得巡航路徑列表

### 適用範圍

* **支援機型**：PuduBot2

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/get_cruise_line |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | QUERY PARAM |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器pid |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | **object** | 查詢結果 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| line_list | **Array<Object>** | 巡航路徑列表 |

### Res.data.line_list

| 參數名 | **類型** | **說明** |
| --- | --- | --- |
| map_cruise_id | string | 巡航路徑id |
| map_cruise_name | string | 巡航路徑名稱 |

## 5.呼叫範例

### 請求範例

http

GET /open-platform-service/v1/get_cruise_line?sn=11111111

### 回傳範例

json

{

"data": {

"line_list": [

{

"map_cruise_id": "1764649613490",

"map_cruise_name": "chixz巡航1202"

}

]

},

"message": "SUCCESS",

"trace_id": "APID1ieaq9SZfpBYvf5aPL4hzvnDzO90NTMDnR_084ae6e8-80b9-4850-8ff7-461a0b445603"

}

# 發起巡航任務

更新時間:2025-12-04 14:22:46

## 1. 介面說明

### 功能描述

發送指令讓機器進行巡航，機器巡航過程會透過[【回呼通知】-【任務執行】-【巡航任務狀態通知-notifyCruiseTask】](/zh/cloud-api/k15hrozhp0kph3s6mywtzbx5)推送巡航狀態。

### 適用範圍

* **支援機型**：PuduBot2

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/cruise_task |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器pid |
| map_cruise_id | string | Y | 巡航路徑id |
| map_cruise_name | string | Y | 巡航路徑名稱 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | **object** | 查詢結果 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| code | int32 | 機器回傳的code |
| message | string | 機器回傳的message |
| task_id | string | 巡航任務id |

## 5.呼叫範例

### 請求範例

http

{

"sn":""1111111111111111,

"map_cruise_id": "fafadfadsf"，

"map_cruise_name":"巡航路徑1"

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"task_id": "1760617692540913",

"code": 0,

"message": "ok"

}

}

# 發送巡航指令

更新時間:2025-12-04 14:07:32

## 1. 介面說明

### 功能描述

在發起巡航任務之後，機器會回傳巡航任務id，後續可透過該任務id控制任務的暫停、取消和恢復。

### 適用範圍

* **支援機型**：PuduBot2

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/cruise_action |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |

### 請求內容（Params）

| 參數明 | 類型 | 必填 | 備註 |
| --- | --- | --- | --- |
| sn | string | Y | 機器pid |
| task_id | string | Y | 當前的巡航任務id |
| action | string | Y | PAUSE：暫停RESUME：恢復任務CANCEL：取消任務 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | **object** | 機器回傳結果 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| code | int32 | 機器回傳的code |
| message | string | 機器回傳的message |
| task_id | string | 巡航任務id |

## 5.呼叫範例

### 請求範例

http

{

"sn":""1111111111111111,

"task_id": "fafadfadsf"，

"action":"PAUSE"

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"task_id": "1760617692540913",

"code": 0,

"message": "ok"

}

}

# 機器人一鍵回充V2

更新時間:2025-11-12 11:57:15

## 1. 機器人一鍵回充V2

### 功能描述

控制機器人執行一鍵回充操作V2版本。機器回覆之後可透過[【回呼通知】-【硬件控制與感知】-【notifyRechargeStatus-回充狀態通知】](/zh/cloud-api/dgnbdp5ju78ziokwiztgvs54)訂閱任務狀態。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra，PuduT300

* **前置準備**：需確認機器人狀態為在線

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v2/recharge |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | Query Params |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息 |
| data | **object** | 回充結果資料 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| desc | string | 描述資訊 |
| task_id | string | 機器回傳了task_id |

## 5.呼叫範例

### 請求範例

http

GET /open-platform-service/v2/recharge?sn=SN-PD202405000001

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"desc": "回充任務已啟動",

"task_id": "RECHARGE-202405201234567890"

}

}

# 取得艙門狀態

更新時間:2025-11-11 20:23:55

## 1. 取得指定機器人艙門狀態(閃電匣)

### 功能描述

取得指定機器人的艙門狀態資訊，包括各艙門的開關狀態。

### 適用範圍

* **支援機型**：Flashbot、FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

* **前置準備**：需確認機器人狀態為在線

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/door_state |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息 |
| data | **object** | 艙門狀態資料 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| door_states | **Array<object>** | 艙門狀態列表 |

### Res.data.door_states

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| door_number | string | 艙門編號 |
| state | string | 艙門狀態：OPENING(開啟中)、OPENED(已開啟)、OPEN_FAILED(開啟失敗)、OPEN_TIMEOUT(開啟超時)、CLOSING(關閉中)、CLOSED(已關閉)、CLOSE_FAILED(關閉失敗)、CLOSE_TIMEOUT(關閉超時) |

## 5.呼叫範例

### 請求範例

http

GET /open-platform-service/v1/door_state?sn=SN-PD202405000001

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"door_states": [

{

"door_number": "1",

"state": "CLOSED"

},

{

"door_number": "2",

"state": "OPENED"

}

]

}

}

# 艙門控制

更新時間:2025-11-11 20:18:00

## 1. 說明

### 功能描述

控制指定機器人的艙門開關操作。

### 適用範圍

* **支援機型**：Flashbot、FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

* **前置準備**：需確認機器人狀態為在線且空閒

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/control_doors |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |
| payload | **object** | Y | 控制參數 |

### Params.payload

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| control_states | **Array<object>** | Y | 控制狀態列表 |

### Params.payload.control_states

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| operation | bool | Y | true:開啟, false:關閉 |
| door_number | string | Y | 艙門編號 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息 |
| data | **object** | 控制結果資料 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| door_states | **Array<object>** | 艙門狀態集合 |

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| door_number | string | 艙門號 |
| state | string | 狀態：OPENED,CLOSED |

## 5.呼叫範例

### 請求範例

http

POST /open-platform-service/v1/control_doors

json

{

"sn": "SN-PD202405000001",

"payload": {

"control_states": [

{

"operation": true,

"door_number": "1"

}

]

}

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"door_states": [

{

"door_number": "1",

"state": "OPENING"

}

]

}

}

# 取得艙門拍照

更新時間:2025-11-11 20:21:47

## 1. 說明

### 功能描述

透過sn取得機器艙門拍照資訊。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /biz-open-service/v1/robotDoor/task_list |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| pid | string | Y | 機器sn |
| offset | int32 | N | 不填預設為0 |
| limit | int32 | N | 不填預設為10 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS為成功 |
| data | **object** | 照片資料 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| count | integer | 總條目數 |
| shop_id | integer | 門市id |
| shop_name | string | 門市名稱 |
| pid | string | 機器sn |
| mac | string | 機器mac |
| items | **Array<object>** | 詳細資料 |

### Res.data.items

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| mac | string | 機器mac |
| task_name | string | 任務名稱 |
| task_id | string | 任務id |
| auth_code | string | 授權code-只有配送模式有 |
| door_index | int32 | 艙門位置 |
| door_type | string | 艙門類型 |
| put_in | **object** | 放物 |
| take_out | **object** | 取物 |
| task_type | string | 任務類型（legwork跑腿、delivery配送） |
| create_time | string | 創建時間，時間戳秒 |
| update_time | string | 更新時間，時間戳秒 |

### Res.data.items.put_in

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| auth_code | string | 放物授權碼 |
| time | string | 放物授權碼時間 |

### Res.data.items.take_out

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| auth_code | string | 取物授權碼 |
| time | string | 取物授權碼時間 |

### 請求範例

http

{

"pid": "xxxCDEFGBOT01032",

"limit": 10,

"offset": 0

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"count": 19,

"shop_id": 412200005,

"shop_name": "TZYL1A0319Shopalter",

"pid": "xxxxT01032",

"mac": "xxx:xx:EF:11:10:32",

"items": [

{

"mac": "",

"task_name": "5- t7",

"task_id": "abd5230a4fcc4a9ca28a2846fc13c482",

"auth_code": "0000",

"door_index": 3,

"door_type": "ThreeHatchBottom1",

"image_list": [

{

"phone_time": "2025.03.31 15:46:17",

"url": "http://xxxx.com/pudu_cloud_platform/img/00D6CB4B1BF8/74cc153817523948a8875453d32b9113.jpeg",

"op_type": "take_out",

"op_type_value": ""

},

{

"phone_time": "2025.03.31 15:56:18",

"url": "xxxx.com/pudu_cloud_platform/img/00D6CB4B1BF8/2918043bf233f8c4345e13c4ca2fb3e5.jpeg",

"op_type": "take_out",

"op_type_value": ""

},

{

"phone_time": "2025.03.31 15:56:30",

"url": "xxxx.com/pudu_cloud_platform/img/00D6CB4B1BF8/c44855a16efc4e0a2438623e9feeb413.jpeg",

"op_type": "take_out",

"op_type_value": ""

}

# 設置頁面顯示內容

更新時間:2025-11-11 10:26:37

## 1. 設置頁面顯示內容(閃電匣)

### 功能描述

設置機器人屏幕顯示的內容。該介面是兼容SDK微服務的舊開放介面，新版機器不支持。

### 適用範圍

* **支援機型**：Flashbot

* **前置準備**：需確認機器人狀態為在線

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/robot/screen/set |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |
| payload | **object** | Y | 顯示內容參數 |

### Params.payload

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| info | **object** | Y | 顯示資訊 |

### Params.payload.info

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| content | string | Y | 內容，3-50個字符 |
| show | bool | Y | true 顯示，false 隱藏 |

## 4.回傳參數

### 回傳內容（Response）

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息 |
| data | **object** | 設置結果資料 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| code | int32 | 回傳碼：80001(參數不正確) |
| message | string | 回傳消息 |

## 5.呼叫範例

### 請求範例

http

POST /open-platform-service/v1/robot/screen/set

json

{

"sn": "SN-PD202405000001",

"payload": {

"info": {

"content": "歡迎光臨",

"show": true

}

}

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"code": 0,

"message": "屏幕內容設置成功"

}

}

# 取消任務

更新時間:2025-11-11 10:26:00

## 1. 取消任務(閃電匣)

### 功能描述

取消指定機器人的任務。該介面是兼容SDK微服務的舊開放介面，新版機器不支持。

### 適用範圍

* **支援機型**：Flashot

* **前置準備**：需確認機器人有正在執行的任務

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/cancel_task |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |
| payload | **object** | Y | 取消任務參數 |

### Params.payload

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| tasks | **Array<object>** | Y | 任務組 |

### Params.payload.tasks

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| name | string | Y | 目標點 |
| type | string | Y | 類型 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息 |
| data | **object** | 取消結果資料 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| code | int32 | 機器回傳碼 |
| message | string | 機器回傳消息 |
| data | **object** | 任務取消詳情 |

### Res.data.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| tasks | **Array<object>** | 任務取消結果列表 |

### Res.data.data.tasks

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| name | string | 目標點 |
| type | string | 類型 |
| success | boolean | 是否成功 true false |
| failure_code | integer | 失敗原因回應碼：11001(任務不存在)、11002(取消失敗) |

## 5.呼叫範例

### 請求範例

http

POST /open-platform-service/v1/cancel_task

json

{

"sn": "SN-PD202405000001",

"payload": {

"tasks": [

{

"name": "TABLE-001",

"type": "DELIVERY"

}

]

}

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"code": 0,

"message": "任務取消成功",

"data": {

"tasks": [

{

"name": "TABLE-001",

"type": "DELIVERY",

"success": true,

"failure_code": 0

}

]

}

}

}

# 電梯內切換當前使用的樓層地圖

更新時間:2025-11-11 20:17:29

## 1.說明

### 功能描述

在電梯內切換指定機器人當前使用的樓層地圖。

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、PuduT300

* **前置準備**：需確認機器人支持梯控功能

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/robot/map/switch_in_elevator |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |
| payload | **object** | Y | 地圖切換參數 |

### Params.payload

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| map | **object** | Y | 地圖資訊 |

### Params.payload.map

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| name | string | Y | 地圖名稱 |
| floor | string | Y | 地圖所在樓層 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息 |
| data | **object** | 切換結果資料 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| code | int | 回傳碼：70001(地圖不存在)、70002(地圖名稱與樓層不匹配)、70003(當前不允許切換地圖)、70004(切換地圖失敗) |
| message | string | 回傳消息 |

## 5.呼叫範例

### 請求範例

http

POST /open-platform-service/v1/robot/map/switch_in_elevator

json

{

"sn": "SN-PD202405000001",

"payload": {

"map": {

"name": "餐廳2樓",

"floor": "2F"

}

}

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"code": 0,

"message": "地圖切換成功"

}

}

# 通知機器上報位置

更新時間:2025-11-12 11:58:27

## 1. 說明

### 功能描述

命令指定機器人上報位置資訊，並指定上報頻次和頻率。機器回傳成功後，透過[【回呼通知】-【地圖與位置回呼】-【notifyRobotPose-機器位置上報】](/zh/cloud-api/c8eh4ez35tgdjqk3zofj1l98)

### 適用範圍

* **支援機型**：FlashBot 2025、FlashBot Pro、FlashBot Max、FlashBot Ultra、KettyBot Pro、BellaBot Pro、PuduT300

* **前置準備**：需確認機器人狀態為在線

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/position_command |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **示例值** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |
| payload | **object** | Y | 位置上報參數 |

### Params.payload

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| interval | int32 | Y | 最小間隔時間(秒)，最小值為1秒 |
| times | int32 | Y | 連續推送次數，最大1000次 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | 回傳消息 |

## 5.呼叫範例

### 請求範例

http

POST /open-platform-service/v1/position_command

json

{

"sn": "SN-PD202405000001",

"payload": {

"interval": 5,

"times": 100

}

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS"

}

# 切換地圖

更新時間:2025-11-12 11:58:59

## 1. 介面說明

### 功能描述

發送指令讓機器切換地圖，機器接收指令後會回傳成功，但這是並不是切換完成，需要透過[【回呼通知】-【地圖與位置】-【notifySwitchMap- 切換地圖的任務通知】](/zh/cloud-api/on2um5t36ke3gt0jnz0mgqsm)訂閱切換結果。

### 適用範圍

* **支援機型**：PuduT300

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/switch_map |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3.請求參數

### 請求頭（Headers）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| Content-Type | string | Y |  |

### 請求內容（Params）

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| sn | string | Y | 機器pid |
| map_info | object | Y | 地圖資訊 |

#### Params.map_info

| **參數名** | **類型** | **必填** | **說明** |
| --- | --- | --- | --- |
| map_name | string | Y | 地圖名稱 |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| trace_id | string | 此次請求的唯一id |
| message | string | SUCCESS成功 |
| data | **object** | 查詢結果 |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_id | string | 任務id，和notify回呼的一致 |
| code | string | 機器回傳的錯誤碼，70001 地圖不存在，70002 地圖名稱與樓層不匹配，70003 當前不允許切換地圖，70004 切換地圖失敗，70005 當前正在切換地圖中，不允許拒絕執行新的切換地圖指令 |
| message | string | 發送成功後會回傳：Sent successfully, please pay attention to the callback message[notifySwitchMap] |

## 5.呼叫範例

### 請求範例

http

{

"sn": "OP890807789769"，

"map_info":{"map_name":"地圖名稱"}

}

### 回傳範例

json

{

"trace_id": "YourApiAppKey_405eb004-7f09-4d86-bff1-4657cdec2717",

"message": "SUCCESS",

"data": {

"task_id": "1760617692540913",

"code": 0,

"message": "Sent successfully, please pay attention to the callback message[notifySwitchMap]"

}

}

# 取得音頻列表

更新時間:2025-12-22 19:55:41

## 1 介面說明

### 功能描述

取得指定機器人可用的語音列表。

### 適用範圍

* **支援機型**：Kettybot

* **前置準備**：需確認機器人狀態為在線

## 2 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/voice/list |
| --- | --- |
| 請求方法（Method） | GET |
| 資料格式 | JSON |

## 3 請求參數

### 請求頭（Headers）

| 參數名 | 類型 | 示例值 | 說明 |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |

### 請求參數（Query）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |

## 4 回傳參數

### 回傳內容（Response）

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| message | string | 回傳錯誤碼，成功SUCCESS |
| data | object | 音頻列表資料 |

### Res.data

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| voice_list | **Array[Object]** | 音頻列表 |

### Res.data.voice_list

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| name | string | 音頻名稱 |

## 5 呼叫範例

### 請求範例

http

GET /open-platform-service/v1/voice/list?sn=SN-PD202405000001

### 回傳範例

json

{

"message": "SUCCESS",

"data": {

"voice_list": [

{

"name": "歡迎語音"

},

{

"name": "到達提示"

}

]

}

}

# 播放音頻

更新時間:2025-12-22 20:00:02

## 1 介面說明

### 功能描述

控制指定機器人播放指定的語音，支持單次播放和循環播放。

### 適用範圍

* **支援機型**：Kettybot

* **前置準備**：需確認機器人狀態為在線，且語音名稱存在於語音列表中

## 2 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/voice/play |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3 請求參數

### 請求頭（Headers）

| 參數名 | 類型 | 示例值 | 說明 |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |
| X-Platform-Token | string | Token-202405ABC123DEF | 平台訪問令牌，從開發者後臺"API密鑰管理"模組取得 |

### 請求內容（Params）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |
| name | string | Y | 音頻名稱，需在音頻列表中存在 |
| is_loop | boolean | Y | 是否循環播放，true為循環播放，false為單次播放 |

## 4 回傳參數

### 回傳內容（Response）

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| message | string | 回傳錯誤碼，成功SUCCESS |
| data | object | 播放結果資料 |

### Res.data

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| code | integer | 機器回傳的錯誤碼 |
| message | string | 機器回傳的錯誤資訊 |

## 5 呼叫範例

### 請求範例

http

POST /open-platform-service/v1/voice/play

json

{

"sn": "SN-PD202405000001",

"name": "歡迎語音",

"is_loop": false

}

### 回傳範例

json

{

"message": "SUCCESS",

"data": {

"code": 0,

"message": "播放成功"

}

}

# 播放控制

更新時間:2025-12-22 20:02:41

## 1 介面說明

### 功能描述

對指定機器人當前正在播放的音頻進行控制操作，包括暫停、恢復和取消播放。

### 適用範圍

* **支援機型**：Kettybot

* **前置準備**：需確認機器人狀態為在線，且有正在播放的音頻

## 2 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/voice/action |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3 請求參數

### 請求頭（Headers）

| 參數名 | 類型 | 示例值 | 說明 |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |
| X-Platform-Token | string | Token-202405ABC123DEF | 平台訪問令牌，從開發者後臺"API密鑰管理"模組取得 |

### 請求內容（Params）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |
| action | string | Y | 操作類型：PAUSE（暫停播放）、RESUME（恢復播放）、CANCEL（取消播放） |

## 4 回傳參數

### 回傳內容（Response）

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| message | string | 回傳錯誤碼，成功SUCCESS |
| data | object | 操作結果資料 |

### Res.data

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| code | integer | 機器回傳的錯誤碼 |
| message | string | 機器回傳的錯誤資訊 |

## 5 呼叫範例

### 請求範例

http

POST /open-platform-service/v1/voice/action HTTP/1.1

Host: open.pudurobot.com

Content-Type: application/json

X-Platform-Token: Token-202405ABC123DEF

json

{

"sn": "SN-PD202405000001",

"action": "PAUSE"

}

### 回傳範例

json

{

"message": "SUCCESS",

"data": {

"code": 0,

"message": "操作成功"

}

}

# 音量設置

更新時間:2025-12-22 20:17:42

## 1 介面說明

### 功能描述

設置指定機器人的音量大小。

### 適用範圍

* **支援機型**：Kettybot

* **前置準備**：需確認機器人狀態為在線

## 2 基本資訊

| 請求路徑（Path） | /open-platform-service/v1/volume/set |
| --- | --- |
| 請求方法（Method） | POST |
| 資料格式 | JSON |

## 3 請求參數

### 請求頭（Headers）

| 參數名 | 類型 | 示例值 | 說明 |
| --- | --- | --- | --- |
| Content-Type | string | application/json | 固定值，指定請求內容資料格式為JSON |
| X-Platform-Token | string | Token-202405ABC123DEF | 平台訪問令牌，從開發者後臺"API密鑰管理"模組取得 |

### 請求內容（Params）

| 參數名 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| sn | string | Y | 機器人序列號 |
| volume | integer | Y | 音量值，0-100 |

## 4 回傳參數

### 回傳內容（Response）

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| message | string | 回傳錯誤碼，成功SUCCESS |
| data | object | 設置結果資料 |

### Res.data

| 參數名 | 類型 | 說明 |
| --- | --- | --- |
| code | integer | 機器回傳的錯誤碼 |
| message | string | 機器回傳的錯誤資訊 |

## 5 呼叫範例

### 請求範例

http

POST /open-platform-service/v1/volume/set

json

{

"sn": "SN-PD202405000001",

"volume": 50

}

### 回傳範例

json

{

"message": "SUCCESS",

"data": {

"code": 0,

"message": "設置成功"

}

}

# 機器概覽

更新時間:2025-11-28 14:01:00

## 1. 介面說明

### 功能描述

查詢週期內的機器總數：開機、綁定、激活機器數

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/brief/robot |
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
| summary | **object** | 本週期資料概覽 |
| qoq | **object** | 上週期環比資料概覽 |
| chart | **map<string, object>** | 繪圖(本期綁定的機型佔比,餅圖)用的資料 |

### Res.data.summary

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| boot_count | integer | 開機機器數 |
| total_count | integer | 累計機器數 |
| bind_count | integer | 綁定機器數 |
| active_count | integer | 綁定機器數 |
| lively_rate | double | 活躍率(開機機器數/累計機器數) |

### Res.data.qoq

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| boot_count | integer | 開機機器數 |
| total_count | integer | 累計機器數 |
| bind_count | integer | 綁定機器數 |
| active_count | integer | 綁定機器數 |
| lively_rate | double | 活躍率(開機機器數/累計機器數) |

### Res.data.chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| product_code | integer | 機器類型編碼，詳見【枚舉】 |
| bind_count | integer | 綁定機器數 |
| active_count | integer | 激活機器數 |
| bind_rate | double | 綁定佔比 |
| active_rate | double | 激活佔比 |

## 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/brief/robot?timezone_offset=8&start_time=1692892800&end_time=1693929599&shop_id=331300000

### 回傳範例

json

{

"message": "ok",

"data": {

"summary": {

"boot_count": 0,

"total_count": 3,

"bind_count": 3,

"active_count": 2,

"lively_rate": 0

},

"qoq": {

"boot_count": 0,

"total_count": 2,

"bind_count": 0,

"active_count": 0,

"lively_rate": 0

},

"chart": {

"61": {

"product_code": "61",

"bind_count": 1,

"active_count": 1,

"bind_rate": 33.33,

"active_rate": 50

},

"62": {

"product_code": "62",

"bind_count": 2,

"active_count": 1,

"bind_rate": 66.67,

"active_rate": 50

}

}

}

}

# 機器運行概覽

更新時間:2025-11-28 15:40:41

## 1. 介面說明

### 功能描述

查詢週期內的運行總數：里程、時長、任務數、清潔面積

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/brief/run |
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
| summary | **object** | 本週期資料概覽 |
| qoq | **object** | 上週期環比資料概覽 |

### Res.data.summary

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| duration | double | 工作時長(h) |
| mileage | double | 運行里程(km) |
| task_count | integer | 執行任務次數 |
| area | double | 清潔總面積(m²) |

### Res.data.qoq

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| duration | double | 工作時長(h) |
| mileage | double | 運行里程(km) |
| task_count | integer | 執行任務次數 |
| area | double | 清潔總面積(m²) |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/brief/run?timezone_offset=8&start_time=1692892800&end_time=1693929599&shop_id=331300000

### 回傳範例

json

{

"message": "ok",

"data": {

"summary": {

"duration": 77.49,

"mileage": 1.52,

"task_count": 40969,

"area": 0

},

"qoq": {

"duration": 0,

"mileage": 0,

"task_count": 0,

"area": 0

}

}

}

# 門市概覽

更新時間:2025-11-28 15:44:40

## 1. 介面說明

### 功能描述

查詢週期內的門市總數：活躍、新增、累計門市數 + TOP10門市運行時長

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/brief/shop |
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
| summary | **object** | 本週期資料概覽 |
| qoq | **object** | 上週期環比資料概覽 |
| lively_top10 | **object[]** | 活躍門市TOP10 |
| silent_top10 | **object[]** | 沉默門市TOP10 |

### Res.data.summary

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| lively_count | integer | 活躍門市數 |
| total_count | integer | 累計門市數 |
| new_count | integer | 新增門市數 |
| lively_rate | double | 活躍率(活躍門市數/累計門市數) |

### Res.data.qoq

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| lively_count | integer | 活躍門市數 |
| total_count | integer | 累計門市數 |
| new_count | integer | 新增門市數 |
| lively_rate | double | 活躍率(活躍門市數/累計門市數) |

### Res.data.lively_top10

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| shop_id | integer | 門市ID |
| shop_name | string | 門市名稱 |
| run_count | integer | 運行機器人數 |
| bind_count | integer | 綁定機器人數 |
| duration | double | 運行時長(h) |
| stop_duration | double | 停運時長(h) |

### Res.data.silent_top10

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| shop_id | integer | 門市ID |
| shop_name | string | 門市名稱 |
| run_count | integer | 運行機器人數 |
| bind_count | integer | 綁定機器人數 |
| duration | double | 運行時長(h) |
| stop_duration | double | 停運時長(h) |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/brief/shop?timezone_offset=8&start_time=1693497600&end_time=1693670399&shop_id=331300000

### 回傳範例

json

{

"message": "ok",

"data": {

"summary": {

"lively_count": 1,

"total_count": 1,

"new_count": 0,

"lively_rate": 100

},

"qoq": {

"lively_count": 1,

"total_count": 1,

"new_count": 0,

"lively_rate": 0

},

"lively_top10": [

{

"shop_id": 331300000,

"shop_name": "前德median門市",

"run_count": 1,

"bind_count": 4,

"duration": 0.89,

"stop_duration": 191.11

}

],

"silent_top10": []

}

}

# 機器運行分析-折線|柱狀圖資料

更新時間:2025-11-28 15:40:09

## 1. 介面說明

### 功能描述

查詢週期內的機器運行資料，可用於繪圖

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/run |
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
| time_unit | string | N | 時間單位(繪圖座標點)：day|hour，表示 按天|按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |

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
| chart | **object[]** | 本週期折線圖的資料 |
| qoq_chart | **object[]** | 上週期環比折線圖的資料 |

### Res.data.chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour 時用 0-24 小時，day 時用 Y-m-d 日期） |
| run_count | integer | 運行機器數 |
| list | object [] | 機型分佈資料 |

### Res.data.chart.list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour 時用 0-24 小時，day 時用 Y-m-d 日期） |
| product_code | string | 機器類型編碼，詳見【枚舉】 |
| run_count | integer | 運行機器數 |

### Res.data.qoq_chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour 時用 0-24 小時，day 時用 Y-m-d 日期） |
| run_count | integer | 運行機器數 |
| list | object [] | 機型分佈資料 |

### Res.data.qoq_chart.list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour 時用 0-24 小時，day 時用 Y-m-d 日期） |
| product_code | string | 機器類型編碼，詳見【枚舉】 |
| run_count | integer | 運行機器數 |

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/run?timezone_offset=8&start_time=1693497600&end_time=1693670399&shop_id=331300000&time_unit=day

### 回傳範例

json

{

"message": "ok",

"data": {

"chart": [

{

"task_time": "2023-09-01",

"run_count": 1,

"list": [

{

"task_time": "2023-09-01",

"product_code": "67",

"run_count": 1

}

]

},

{

"task_time": "2023-09-02",

"run_count": 0,

"list": []

}

],

"qoq_chart": [

{

"task_time": "2023-08-30",

"run_count": 1,

"list": [

{

"task_time": "2023-08-30",

"product_code": "67",

"run_count": 1

}

]

},

{

"task_time": "2023-08-31",

"run_count": 3,

# 門市分析-折線|柱狀圖資料

更新時間:2025-11-28 15:42:36

## 1. 介面說明

### 功能描述

查詢週期內的門市機器資料，可用於繪圖

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/shop |
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
| time_unit | string | N | 時間單位(繪圖座標點)：day|hour，表示 按天|按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |

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
| summary | **object** | 本週期資料概覽 |
| qoq | **object** | 上週期環比資料概覽 |
| chart | **object[]** | 本週期折線圖的資料 |
| qoq_chart | **object[]** | 上週期環比折線圖的資料 |

### Res.data.summary

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| lively_count | integer | 活躍門市數 |
| silent_count | integer | 沉默門市數 |
| new_count | integer | 新增門市數 |
| total_count | integer | 累計門市數 |

### Res.data.qoq

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| lively_count | integer | 活躍門市數 |
| silent_count | integer | 沉默門市數 |
| new_count | integer | 新增門市數 |
| total_count | integer | 累計門市數 |

### Res.data.chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour 時用 0-24 小時，day 時用 Y-m-d 日期） |
| lively_count | integer | 活躍門市數 |
| silent_count | integer | 沉默門市數 |
| new_count | integer | 新增門市數 |
| total_count | integer | 累計門市數 |

### Res.data.qoq_chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour 時用 0-24 小時，day 時用 Y-m-d 日期） |
| lively_count | integer | 活躍門市數 |
| silent_count | integer | 沉默門市數 |
| new_count | integer | 新增門市數 |
| total_count | integer | 累計門市數 |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/shop?timezone_offset=8&start_time=1693497600&end_time=1693670399&shop_id=331300000&time_unit=day

### 回傳範例

json

{

"message": "ok",

"data": {

"summary": {

"lively_count": 1,

"silent_count": 0,

"new_count": 0,

"total_count": 1

},

"qoq": {

"lively_count": 1,

"silent_count": 0,

"new_count": 0,

"total_count": 1

},

"chart": [

{

"task_time": "2023-09-01",

"lively_count": 1,

"silent_count": 0,

"new_count": 0,

"total_count": 1

},

{

"task_time": "2023-09-02",

"lively_count": 0,

"silent_count": 1,

"new_count": 0,

"total_count": 1

}

],

"qoq_chart": [

{

"task_time": "2023-08-30",

"lively_count": 1,

"silent_count": 0,

# 機器運行分析-列表分頁查詢

更新時間:2025-11-28 15:35:17

## 1. 介面說明

### 功能描述

查詢範圍內的機器運行資料，最小時間粒度=小時

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/run/paging |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |
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
| total | **integer** | 總條目數 |
| offset | **integer** | 偏移量 |
| limit | **integer** | 每頁條目數 |
| list | **object[]** | 當前頁詳細資料 |

### Res.data.list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 任務結束時歸屬時段（hour 時用 Y-m-d H:i:s 時間，day 時用 Y-m-d 日期） |
| product_code | string | 機器類型編碼，詳見【枚舉】 |
| mac | integer | 活躍排名 |
| shop_id | integer | 門市 ID |
| shop_name | string | 門市名稱 |
| duration | double | 運行時長(h) |
| mileage | double | 運行里程(km) |
| task_count | integer | 任務次數 |
| already_unbind | boolean | 機器是否已從該門市解綁 |
| sn | string | 機器 sn |

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/run/paging?timezone_offset=8&start_time=1693497600&end_time=1693670399&shop_id=331300000

### 回傳範例

json

{

"message": "ok",

"data": {

"total": 1,

"offset": 0,

"limit": 100,

"list": [

{

"task_time": "2023-09-01",

"product_code": "67",

"mac": "20:50:E7:3E:61:36",

"shop_id": 331300000,

"shop_name": "前德median門市",

"duration": 0.89,

"mileage": 0,

"task_count": 640,

"already_unbind": false,

"sn": "OP2050E73E6136"

}

]

}

}

# 門市分析-列表分頁查詢

更新時間:2025-11-28 15:42:08

## 1. 介面說明

### 功能描述

查詢範圍內的機器運行資料，最小時間粒度=小時

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/shop/paging |
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
| total | **integer** | 總條目數 |
| offset | **integer** | 偏移量 |
| limit | **integer** | 每頁條目數 |
| list | **object[]** | 當前頁詳細資料 |

### Res.data.list

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| rank | integer | 活躍排名 |
| shop_id | integer | 門市 ID |
| shop_name | string | 門市名稱 |
| run_count | integer | 運行機器人數 |
| bind_count | integer | 綁定機器人數 |
| duration | double | 運行時長(h) |
| mileage | double | 運行里程(km) |
| task_count | integer | 任務次數 |
| create_time | string | 門市創建時間（Y-m-d H:i:s） |

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/shop/paging?timezone_offset=8&start_time=1693497600&end_time=1693670399&shop_id=331300000

### 回傳範例

json

{

"message": "ok",

"data": {

"total": 1,

"offset": 0,

"limit": 100,

"list": [

{

"rank": 1,

"shop_id": 331300000,

"shop_name": "前德median門市",

"run_count": 1,

"bind_count": 4,

"duration": 0.89,

"mileage": 0,

"task_count": 640,

"create_time": "2023-08-02 18:57:23"

}

],

"export_url": ""

}

}

# 廣告-總數|折線|柱狀圖資料

更新時間:2025-11-28 17:20:55

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/ad |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |

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
| summary | **object[]** | 本週期資料彙總 |
| qoq | **object[]** | 上週期資料彙總 |
| chart | **object[]** | 本週期折線圖的資料 |
| qoq_chart | **object[]** | 上週期環比折線圖的資料 |

### Res.data.summary

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| tiny_play_duration | double | 小屏廣告播放時長(h) |
| tiny_play_times | integer | 小屏廣告播放次數 |
| big_play_duration | double | 大屏廣告播放時長(h) |
| big_play_times | integer | 大屏廣告播放次數 |

### Res.data.qoq

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| tiny_play_duration | double | 小屏廣告播放時長(h) |
| tiny_play_times | integer | 小屏廣告播放次數 |
| big_play_duration | double | 大屏廣告播放時長(h) |
| big_play_times | integer | 大屏廣告播放次數 |

### Res.data.chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| tiny_play_duration | double | 小屏廣告播放時長(h) |
| tiny_play_times | integer | 小屏廣告播放次數 |
| big_play_duration | double | 大屏廣告播放時長(h) |
| big_play_times | integer | 大屏廣告播放次數 |

### Res.data.qoq_chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| tiny_play_duration | double | 小屏廣告播放時長(h) |
| tiny_play_times | integer | 小屏廣告播放次數 |
| big_play_duration | double | 大屏廣告播放時長(h) |
| big_play_times | integer | 大屏廣告播放次數 |

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/ad?timezone_offset=8&start_time=1693497600&end_time=1693670399&shop_id=331300000&time_unit=day

### 回傳範例

json

{

"message": "ok",

"data": {

"summary": {

"tiny_play_duration": 0,

"tiny_play_times": 0,

"big_play_duration": 0.89,

"big_play_times": 640

},

"qoq": {

"tiny_play_duration": 0,

"tiny_play_times": 0,

"big_play_duration": 15.99,

"big_play_times": 8628

},

"chart": [

{

"task_time": "2023-09-01",

"tiny_play_duration": 0,

"tiny_play_times": 0,

"big_play_duration": 0.89,

"big_play_times": 640

},

{

"task_time": "2023-09-02",

"tiny_play_duration": 0,

"tiny_play_times": 0,

"big_play_duration": 0,

"big_play_times": 0

}

],

"qoq_chart": [

{

"task_time": "2023-08-30",

"tiny_play_duration": 0,

"tiny_play_times": 0,

# 呼叫-總數|折線|柱狀圖資料

更新時間:2025-11-28 18:18:03

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/call |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |

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
| summary | **object[]** | 本週期資料彙總 |
| qoq | **object[]** | 上週期資料彙總 |
| chart | **object[]** | 本週期折線圖的資料 |
| qoq_chart | **object[]** | 上週期環比折線圖的資料 |

### Res.data.summary

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| task_count | integer | 任務數 |
| destination_count | integer | 目的地數 |
| finished_destination_count | integer | 完成目的地數 |

### Res.data.qoq

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| task_count | integer | 任務數 |
| destination_count | integer | 目的地數 |
| finished_destination_count | integer | 完成目的地數 |

### Res.data.chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| task_count | integer | 任務數 |
| destination_count | integer | 目的地數 |
| finished_destination_count | integer | 完成目的地數 |

### Res.data.qoq_chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| task_count | integer | 任務數 |
| destination_count | integer | 目的地數 |
| finished_destination_count | integer | 完成目的地數 |

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/call?timezone_offset=8&start_time=1694707200&end_time=1694793599&shop_id=331300000&time_unit=day

### 回傳範例

json

{

"message": "ok",

"data": {

"summary": {

"mileage": 0.01,

"duration": 0.03,

"task_count": 4,

"destination_count": 4,

"finished_destination_count": 0

},

"qoq": {

"mileage": 0.01,

"duration": 0.22,

"task_count": 8,

"destination_count": 8,

"finished_destination_count": 8

},

"chart": [

{

"task_time": "2023-09-15",

"mileage": 0.01,

"duration": 0.03,

"task_count": 4,

"destination_count": 4,

"finished_destination_count": 0

}

],

"qoq_chart": [

{

"task_time": "2023-09-14",

"mileage": 0.01,

"duration": 0.22,

"task_count": 8,

"destination_count": 8,

"finished_destination_count": 8

}

# 巡航-總數|折線|柱狀圖資料

更新時間:2025-11-28 18:32:49

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/cruise |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |

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
| summary | **object[]** | 本週期資料彙總 |
| qoq | **object[]** | 上週期資料彙總 |
| chart | **object[]** | 本週期折線圖的資料 |
| qoq_chart | **object[]** | 上週期環比折線圖的資料 |

### Res.data.summary

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| interactive_count | integer | 互動人次 |
| interactive_duration | integer | 互動時長 |
| task_count | integer | 任務數 |

### Res.data.qoq

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| interactive_count | integer | 互動人次 |
| interactive_duration | integer | 互動時長 |
| task_count | integer | 任務數 |

### Res.data.chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| interactive_count | integer | 互動人次 |
| interactive_duration | integer | 互動時長 |
| task_count | integer | 任務數 |

### Res.data.qoq_chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| interactive_count | integer | 互動人次 |
| interactive_duration | integer | 互動時長 |
| task_count | integer | 任務數 |

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/cruise?timezone_offset=8&start_time=1693497600&end_time=1693670399&shop_id=331300000&time_unit=day

### 回傳範例

json

{

"message": "ok",

"data": {

"summary": {

"mileage": 0,

"duration": 0,

"interactive_count": 0,

"interactive_duration": 0,

"task_count": 0

},

"qoq": {

"mileage": 0.17,

"duration": 12.87,

"interactive_count": 0,

"interactive_duration": 0,

"task_count": 14

},

"chart": [

{

"task_time": "2023-09-01",

"mileage": 0,

"duration": 0,

"interactive_count": 0,

"interactive_duration": 0,

"task_count": 0

},

{

"task_time": "2023-09-02",

"mileage": 0,

"duration": 0,

"interactive_count": 0,

"interactive_duration": 0,

"task_count": 0

}

],

"qoq_chart": [

# 配送-總數|折線|柱狀圖資料

更新時間:2025-11-28 17:38:56

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/delivery |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |

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
| summary | **object[]** | 本週期資料彙總 |
| qoq | **object[]** | 上週期資料彙總 |
| chart | **object[]** | 本週期折線圖的資料 |
| qoq_chart | **object[]** | 上週期環比折線圖的資料 |

### Res.data.summary

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| table_count | integer | 配送桌數 |
| tray_count | integer | 配送餐盤數 |
| task_count | integer | 任務數 |

### Res.data.qoq

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| table_count | integer | 配送桌數 |
| tray_count | integer | 配送餐盤數 |
| task_count | integer | 任務數 |

### Res.data.chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| table_count | integer | 配送桌數 |
| tray_count | integer | 配送餐盤數 |
| task_count | integer | 任務數 |

### Res.data.qoq_chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| table_count | integer | 配送桌數 |
| tray_count | integer | 配送餐盤數 |
| task_count | integer | 任務數 |

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/delivery?timezone_offset=8&start_time=1693497600&end_time=1693670399&shop_id=331300000&time_unit=day

### 回傳範例

json

{

"message": "ok",

"data": {

"summary": {

"mileage": 0,

"duration": 0,

"table_count": 0,

"tray_count": 0,

"task_count": 0

},

"qoq": {

"mileage": 0.01,

"duration": 0.12,

"table_count": 10,

"tray_count": 10,

"task_count": 10

},

"chart": [

{

"task_time": "2023-09-01",

"mileage": 0,

"duration": 0,

"table_count": 0,

"tray_count": 0,

"task_count": 0

},

{

"task_time": "2023-09-02",

"mileage": 0,

"duration": 0,

"table_count": 0,

"tray_count": 0,

"task_count": 0

}

],

"qoq_chart": [

# 領位-總數|折線|柱狀圖資料

更新時間:2025-11-28 18:09:34

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/greeter |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |

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
| summary | **object[]** | 本週期資料彙總 |
| qoq | **object[]** | 上週期資料彙總 |
| chart | **object[]** | 本週期折線圖的資料 |
| qoq_chart | **object[]** | 上週期環比折線圖的資料 |

### Res.data.summary

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| destination_count | integer | 領位帶客次數(目的地數) |
| task_count | integer | 任務數 |

### Res.data.qoq

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| destination_count | integer | 領位帶客次數(目的地數) |
| task_count | integer | 任務數 |

### Res.data.chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| destination_count | integer | 領位帶客次數(目的地數) |
| task_count | integer | 任務數 |

### Res.data.qoq_chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| destination_count | integer | 領位帶客次數(目的地數) |
| task_count | integer | 任務數 |

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/greeter?timezone_offset=8&start_time=1693497600&end_time=1693670399&shop_id=331300000&time_unit=day

### 回傳範例

json

{

"message": "ok",

"data": {

"summary": {

"mileage": 0,

"duration": 0,

"destination_count": 0,

"task_count": 0

},

"qoq": {

"mileage": 0.02,

"duration": 0.04,

"destination_count": 8,

"task_count": 9

},

"chart": [

{

"task_time": "2023-09-01",

"mileage": 0,

"duration": 0,

"destination_count": 0,

"task_count": 0

},

{

"task_time": "2023-09-02",

"mileage": 0,

"duration": 0,

"destination_count": 0,

"task_count": 0

}

],

"qoq_chart": [

{

"task_time": "2023-08-30",

"mileage": 0.02,

"duration": 0.04,

# 宮格-總數|折線|柱狀圖資料

更新時間:2025-11-28 18:23:43

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/grid |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |

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
| summary | **object[]** | 本週期資料彙總 |
| qoq | **object[]** | 上週期資料彙總 |
| chart | **object[]** | 本週期折線圖的資料 |
| qoq_chart | **object[]** | 上週期環比折線圖的資料 |

### Res.data.summary

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| take_me_in_count | integer | 點擊次數:帶我進店 |
| featured_item_count | integer | 點擊次數:特色商品 |
| favorable_promotions_count | integer | 點擊次數:優惠活動 |
| guide_to_menu_count | integer | 點擊次數:領位 |
| poster_count | integer | 點擊次數:海報 |
| usher_count | integer | 點擊次數:帶路 |
| dance_count | integer | 點擊次數:跳舞 |
| video_poster_count | integer | 點擊次數:視頻 |

### Res.data.qoq

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| take_me_in_count | integer | 點擊次數:帶我進店 |
| featured_item_count | integer | 點擊次數:特色商品 |
| favorable_promotions_count | integer | 點擊次數:優惠活動 |
| guide_to_menu_count | integer | 點擊次數:領位 |
| poster_count | integer | 點擊次數:海報 |
| usher_count | integer | 點擊次數:帶路 |
| dance_count | integer | 點擊次數:跳舞 |
| video_poster_count | integer | 點擊次數:視頻 |

### Res.data.chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| take_me_in_count | integer | 點擊次數:帶我進店 |
| featured_item_count | integer | 點擊次數:特色商品 |
| favorable_promotions_count | integer | 點擊次數:優惠活動 |
| guide_to_menu_count | integer | 點擊次數:領位 |
| poster_count | integer | 點擊次數:海報 |
| usher_count | integer | 點擊次數:帶路 |
| dance_count | integer | 點擊次數:跳舞 |
| video_poster_count | integer | 點擊次數:視頻 |

### Res.data.qoq_chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| take_me_in_count | integer | 點擊次數:帶我進店 |
| featured_item_count | integer | 點擊次數:特色商品 |
| favorable_promotions_count | integer | 點擊次數:優惠活動 |
| guide_to_menu_count | integer | 點擊次數:領位 |
| poster_count | integer | 點擊次數:海報 |
| usher_count | integer | 點擊次數:帶路 |
| dance_count | integer | 點擊次數:跳舞 |
| video_poster_count | integer | 點擊次數:視頻 |

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/grid?timezone_offset=8&start_time=1693497600&end_time=1693670399&shop_id=331300000&time_unit=day

### 回傳範例

json

{

"message": "ok",

"data": {

"summary": {

"take_me_in_count": 0,

"featured_item_count": 0,

"favorable_promotions_count": 0,

"guide_to_menu_count": 0,

"poster_count": 0,

"usher_count": 0,

"dance_count": 0,

"video_poster_count": 0

},

"qoq": {

"take_me_in_count": 0,

"featured_item_count": 8,

"favorable_promotions_count": 2,

"guide_to_menu_count": 5,

"poster_count": 1,

"usher_count": 0,

"dance_count": 0,

"video_poster_count": 0

},

"chart": [

{

"task_time": "2023-09-01",

"take_me_in_count": 0,

"featured_item_count": 0,

"favorable_promotions_count": 0,

"guide_to_menu_count": 0,

"poster_count": 0,

"usher_count": 0,

"dance_count": 0,

"video_poster_count": 0

},

{

# 互動-總數|折線|柱狀圖資料

更新時間:2025-11-28 18:13:27

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/interactive |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |

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
| summary | **object[]** | 本週期資料彙總 |
| qoq | **object[]** | 上週期資料彙總 |
| chart | **object[]** | 本週期折線圖的資料 |
| qoq_chart | **object[]** | 上週期環比折線圖的資料 |

### Res.data.summary

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| interactive_count | integer | 互動人次 |
| voice_count | integer | 語音互動人次 |
| voice_duration | double | 語音互動時長(h) |

### Res.data.qoq

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| interactive_count | integer | 互動人次 |
| voice_count | integer | 語音互動人次 |
| voice_duration | double | 語音互動時長(h) |

### Res.data.chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| interactive_count | integer | 互動人次 |
| voice_count | integer | 語音互動人次 |
| voice_duration | double | 語音互動時長(h) |

### Res.data.qoq_chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| interactive_count | integer | 互動人次 |
| voice_count | integer | 語音互動人次 |
| voice_duration | double | 語音互動時長(h) |

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/interactive?timezone_offset=8&start_time=1693497600&end_time=1693670399&shop_id=331300000&time_unit=day

### 回傳範例

json

{

"message": "ok",

"data": {

"summary": {

"interactive_count": 0,

"voice_count": 0,

"voice_duration": 0

},

"qoq": {

"interactive_count": 5,

"voice_count": 0,

"voice_duration": 0

},

"chart": [

{

"task_time": "2023-09-01",

"interactive_count": 0,

"voice_count": 0,

"voice_duration": 0

},

{

"task_time": "2023-09-02",

"interactive_count": 0,

"voice_count": 0,

"voice_duration": 0

}

],

"qoq_chart": [

{

"task_time": "2023-08-30",

"interactive_count": 5,

"voice_count": 0,

"voice_duration": 0

},

{

"task_time": "2023-08-31",

# 回盤-總數|折線|柱狀圖資料

更新時間:2025-11-28 18:22:49

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/recovery |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |

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
| summary | **object[]** | 本週期資料彙總 |
| qoq | **object[]** | 上週期資料彙總 |
| chart | **object[]** | 本週期折線圖的資料 |
| qoq_chart | **object[]** | 上週期環比折線圖的資料 |

### Res.data.summary

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| table_count | integer | 餐桌數 |
| task_count | integer | 任務數 |

### Res.data.qoq

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| table_count | integer | 餐桌數 |
| task_count | integer | 任務數 |

### Res.data.chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| table_count | integer | 餐桌數 |
| task_count | integer | 任務數 |

### Res.data.qoq_chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| table_count | integer | 餐桌數 |
| task_count | integer | 任務數 |

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/recovery?timezone_offset=8&start_time=1693497600&end_time=1693670399&shop_id=331300000&time_unit=day

### 回傳範例

json

{

"message": "ok",

"data": {

"summary": {

"mileage": 0,

"duration": 0,

"table_count": 0,

"task_count": 0

},

"qoq": {

"mileage": 0,

"duration": 0,

"table_count": 0,

"task_count": 1

},

"chart": [

{

"task_time": "2023-09-01",

"mileage": 0,

"duration": 0,

"table_count": 0,

"task_count": 0

},

{

"task_time": "2023-09-02",

"mileage": 0,

"duration": 0,

"table_count": 0,

"task_count": 0

}

],

"qoq_chart": [

{

"task_time": "2023-08-30",

"mileage": 0,

"duration": 0,

# 攬客-總數|折線|柱狀圖資料

更新時間:2025-11-28 18:12:06

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/solicit |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |

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
| summary | **object[]** | 本週期資料彙總 |
| qoq | **object[]** | 上週期資料彙總 |
| chart | **object[]** | 本週期折線圖的資料 |
| qoq_chart | **object[]** | 上週期環比折線圖的資料 |

### Res.data.summary

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| duration | double | 運行時長(h) |
| play_count | integer | 打招呼次數 |
| attach_persons | integer | 觸達人次 |
| attract_persons | integer | 吸引人次 |
| interactive_count | integer | 互動人次 |
| task_count | integer | 任務數 |

### Res.data.qoq

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| duration | double | 運行時長(h) |
| play_count | integer | 打招呼次數 |
| attach_persons | integer | 觸達人次 |
| attract_persons | integer | 吸引人次 |
| interactive_count | integer | 互動人次 |
| task_count | integer | 任務數 |

### Res.data.chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| duration | double | 運行時長(h) |
| play_count | integer | 打招呼次數 |
| attach_persons | integer | 觸達人次 |
| attract_persons | integer | 吸引人次 |
| interactive_count | integer | 互動人次 |
| task_count | integer | 任務數 |

### Res.data.qoq_chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| duration | double | 運行時長(h) |
| play_count | integer | 打招呼次數 |
| attach_persons | integer | 觸達人次 |
| attract_persons | integer | 吸引人次 |
| interactive_count | integer | 互動人次 |
| task_count | integer | 任務數 |

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/solicit?timezone_offset=8&start_time=1693497600&end_time=1693670399&shop_id=331300000&time_unit=day

### 回傳範例

json

{

"message": "ok",

"data": {

"summary": {

"duration": 0,

"play_count": 0,

"attach_persons": 0,

"attract_persons": 0,

"interactive_count": 0,

"task_count": 0

},

"qoq": {

"duration": 0.16,

"play_count": 6,

"attach_persons": 2,

"attract_persons": 1,

"interactive_count": 5,

"task_count": 10

},

"chart": [

{

"task_time": "2023-09-01",

"duration": 0,

"play_count": 0,

"attach_persons": 0,

"attract_persons": 0,

"interactive_count": 0,

"task_count": 0

},

{

"task_time": "2023-09-02",

"duration": 0,

"play_count": 0,

"attach_persons": 0,

"attract_persons": 0,

"interactive_count": 0,

# 頂升-總數|折線|柱狀圖資料

更新時間:2025-11-28 17:39:47

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/lifting |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |

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
| summary | **object[]** | 本週期資料彙總 |
| qoq | **object[]** | 上週期資料彙總 |
| chart | **object[]** | 本週期折線圖的資料 |
| qoq_chart | **object[]** | 上週期環比折線圖的資料 |

### Res.data.summary

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| task_count | integer | 任務數 |
| destination_count | integer | 運貨次數 |

### Res.data.qoq

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| task_count | integer | 任務數 |
| destination_count | integer | 運貨次數 |

### Res.data.chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| task_count | integer | 任務數 |
| destination_count | integer | 目的地數 |

### Res.data.qoq_chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| task_count | integer | 任務數 |
| destination_count | integer | 目的地數 |
| duration | double | 運行時長(h) |
| table_count | integer | 配送桌數 |
| tray_count | integer | 配送餐盤數 |
| task_count | integer | 任務數 |

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/lifting?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=324100000&time_unit=day

### 回傳範例

json

{

"data": {

"chart": [

{

"destination_count": 61,

"duration": 0.32,

"mileage": 0.08,

"task_count": 61,

"task_time": "2024-09-09"

},

{

"destination_count": 1,

"duration": 0,

"mileage": 0,

"task_count": 1,

"task_time": "2024-09-10"

}

],

"qoq": {

"destination_count": 3,

"duration": 0.01,

"mileage": 0,

"task_count": 3

},

"qoq_chart": [

{

"destination_count": 3,

"duration": 0.01,

"mileage": 0,

"task_count": 3,

"task_time": "2024-09-07"

},

{

"destination_count": 0,

"duration": 0,

"mileage": 0,

# 清潔(洗地|掃地)-折線|柱狀圖資料

更新時間:2025-12-01 10:58:56

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/clean/mode |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |
| clean_mode | integer | N | 清潔模式過濾（0全部，1洗地，2掃地） |
| sub_mode | integer | N | 子模式過濾，目前只有掃地模式使用(-1全部，0自定義、1地毯吸塵、3靜音塵推) |

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
| summary | **object[]** | 本週期資料彙總 |
| qoq | **object[]** | 上週期資料彙總 |
| chart | **object[]** | 本週期折線圖的資料 |
| qoq_chart | **object[]** | 上週期環比折線圖的資料 |

### Res.data.summary

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| area | double | 清潔總面積(m²) |
| duration | double | 清潔總時長(h) |
| task_count | integer | 清潔任務數 |
| power_consumption | double | 耗電情況(Kw/h) |
| water_consumption | double | 耗水情況(ML) |

### Res.data.qoq

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| area | double | 清潔總面積(m²) |
| duration | double | 清潔總時長(h) |
| task_count | integer | 清潔任務數 |
| power_consumption | double | 耗電情況(Kw/h) |
| water_consumption | double | 耗水情況(ML) |

### Res.data.chart

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（hour時用0-24小時，day時用Y-m-d日期） |
| area | double | 清潔總面積(m²) |
| duration | double | 清潔總時長(h) |
| task_count | integer | 清潔任務數 |
| power_consumption | double | 耗電情況(Kw/h) |
| water_consumption | double | 耗水情況(ML) |

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/clean/mode?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=324100000&time_unit=day&clean_mode=2&sub_mode=-1

### 回傳範例

json

{

"message": "ok",

"data": {

"summary": {

"area": 88.02,

"duration": 0.19,

"power_consumption": 0.09,

"water_consumption": 0,

"task_count": 21

},

"qoq": {

"area": 119.31,

"duration": 0.26,

"power_consumption": 0.18,

"water_consumption": 0,

"task_count": 21

},

"chart": [

{

"task_time": "2023-08-30",

"area": 56.69,

"duration": 0.12,

"power_consumption": 0.04,

"water_consumption": 0,

"task_count": 13

},

{

"task_time": "2023-08-31",

"area": 31.33,

"duration": 0.07,

"power_consumption": 0.05,

"water_consumption": 0,

"task_count": 8

}

],

"qoq_chart": [

# 清潔(洗地|掃地)-24小時運行分佈

更新時間:2025-11-28 17:26:32

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/clean/detail |
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
| clean_mode | integer | N | 清潔模式過濾（0全部，1洗地，2掃地） |
| sub_mode | integer | N | 子模式過濾，目前只有掃地模式使用(-1全部，0自定義、1地毯吸塵、3靜音塵推) |

## 4.回傳參數

### 回傳內容（Response）

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| message | string | 回傳錯誤碼，成功SUCCESS |
| chart | **object[]** | 請求結果資料 |
| trace_id | string | 此次請求的唯一id |

### Res.data

| **參數名** | **類型** | **說明** |
| --- | --- | --- |
| task_time | string | 橫座標時間（H:i:s) |
| running_task_count | integer | 任務的個數 |

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/clean/detail?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=324100000&clean_mode=2&sub_mode=-1

### 回傳範例

json

{

"message": "ok",

"chart": [

{

"task_time": "10:30:00",

"running_task_count": 1

},

{

"task_time": "10:40:00",

"running_task_count": 2

},

{

"task_time": "10:50:00",

"running_task_count": 3

},

{

"task_time": "11:00:00",

"running_task_count": 1

},

{

"task_time": "11:10:00",

"running_task_count": 0

},

{

"task_time": "11:20:00",

"running_task_count": 0

}

]

}

# 廣告-列表分頁查詢

更新時間:2025-11-28 17:19:15

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/ad/paging |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |
| group_by | string | N | 分組方式：robot | shop，表示 按機器 | 按門市 |
| offset | integer | N | 偏移量，從0開始 |
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
| task_time | string | 任務結束時歸屬時段（hour時用Y-m-d H:i:s時間，day時用Y-m-d日期） |
| mac | string | MAC；注：按機器分組時有效 |
| shop_id | integer | 門市ID |
| shop_name | string | 門市名稱 |
| product_code | string | 機器類型編碼，詳見【枚舉】； 注：按機器分組時有效 |
| tiny_play_duration | integer | 小屏廣告播放時長(h) |
| tiny_play_times | double | 小屏廣告播放次數 |
| big_play_duration | double | 大屏廣告播放時長(h) |
| big_play_times | integer | 大屏廣告播放次數 |
| sn | string | 機器SN；注：按機器分組時有效 |
| task_count | integer | 任務數 |
| speed | double | 平均速度m/s |
| run_count | integer | 運行機器人數；注：按門市分組時有效 |
| bind_count | integer | 綁定機器人數；注：按門市分組時有效 |
| robot_name | string | 機器人暱稱；注：按機器分組時有效 |
| work_days | integer | 工作天數(僅all彙總時有效) |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/ad/paging?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=331300000&time_unit=day&group_by=robot

### 回傳範例

json

{

"message": "ok",

"data": {

"total": 1,

"limit": 100,

"list": [

{

"task_time": "2023-09-01",

"mac": "20:50:E7:3E:61:36",

"shop_id": 331300000,

"shop_name": "【勿動】【前德median】",

"product_code": "67",

"product_name": "kettybot",

"bind_time": "2023-08-28 10:45:28",

"tiny_play_duration": 0,

"tiny_play_times": 0,

"big_play_duration": 0.89,

"big_play_times": 640,

"already_unbind": false,

"sn": "OP2050E73E6136",

"run_count": 0,

"bind_count": 3,

"robot_name": "潮汕美食",

"work_days": 0,

"primary_industry_code": "7c8ca6dd-cea1-4149-9a29-693cffb815ee",

"secondary_industry_code": "fae6fad3-857a-458f-95f0-ebac5d9c4494",

"country_code": "20000",

"province_code": "0",

"city_code": "0",

"primary_industry": "",

"secondary_industry": "",

"country": "Singapore",

"province": "",

"city": ""

}

],

# 呼叫-列表分頁查詢

更新時間:2025-11-28 18:15:24

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/call/paging |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |
| group_by | string | N | 分組方式：robot | shop，表示 按機器 | 按門市 |
| offset | integer | N | 偏移量，從0開始 |
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
| task_time | string | 任務結束時歸屬時段（hour時用Y-m-d H:i:s時間，day時用Y-m-d日期） |
| mac | string | MAC；注：按機器分組時有效 |
| shop_id | integer | 門市ID |
| shop_name | string | 門市名稱 |
| product_code | string | 機器類型編碼，詳見【枚舉】； 注：按機器分組時有效 |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| destination_count | integer | 目的地數 |
| finished_destination_count | integer | 完成目的地數 |
| sn | string | 機器SN；注：按機器分組時有效 |
| task_count | integer | 任務數 |
| speed | double | 平均速度m/s |
| run_count | integer | 運行機器人數；注：按門市分組時有效 |
| bind_count | integer | 綁定機器人數；注：按門市分組時有效 |
| robot_name | string | 機器人暱稱；注：按機器分組時有效 |
| work_days | integer | 工作天數(僅all彙總時有效) |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/call/paging?timezone_offset=8&start_time=1694707200&end_time=1694793599&shop_id=331300000&time_unit=day&group_by=robot

### 回傳範例

json

{

"message": "ok",

"data": {

"total": 1,

"limit": 100,

"list": [

{

"task_time": "2023-09-15",

"mac": "20:50:E7:3E:61:36",

"shop_id": 331300000,

"shop_name": "【勿動】【前德median】",

"product_code": "67",

"product_name": "kettybot",

"bind_time": "2023-08-28 10:45:28",

"mileage": 0.01,

"duration": 0.03,

"already_unbind": false,

"sn": "OP2050E73E6136",

"run_count": 0,

"bind_count": 3,

"task_count": 4,

"robot_name": "潮汕美食",

"destination_count": 4,

"finished_destination_count": 0,

"work_days": 0,

"primary_industry_code": "7c8ca6dd-cea1-4149-9a29-693cffb815ee",

"secondary_industry_code": "fae6fad3-857a-458f-95f0-ebac5d9c4494",

"country_code": "20000",

"province_code": "0",

"city_code": "0",

"primary_industry": "",

"secondary_industry": "",

"country": "Singapore",

"province": "",

"city": ""

}

# 巡航-列表分頁查詢

更新時間:2025-11-28 18:28:34

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/cruise/paging |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |
| group_by | string | N | 分組方式：robot | shop，表示 按機器 | 按門市 |
| offset | integer | N | 偏移量，從0開始 |
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
| task_time | string | 任務結束時歸屬時段（hour時用Y-m-d H:i:s時間，day時用Y-m-d日期） |
| mac | string | MAC；注：按機器分組時有效 |
| shop_id | integer | 門市ID |
| shop_name | string | 門市名稱 |
| product_code | string | 機器類型編碼，詳見【枚舉】； 注：按機器分組時有效 |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| interactive_count | integer | 互動人次 |
| interactive_duration | double | 互動時長(h) |
| sn | string | 機器SN；注：按機器分組時有效 |
| task_count | integer | 任務數 |
| speed | double | 平均速度m/s |
| run_count | integer | 運行機器人數；注：按門市分組時有效 |
| bind_count | integer | 綁定機器人數；注：按門市分組時有效 |
| robot_name | string | 機器人暱稱；注：按機器分組時有效 |
| work_days | integer | 工作天數(僅all彙總時有效) |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/cruise/paging?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=332200002&time_unit=day&group_by=robot

### 回傳範例

json

{

"message": "ok",

"data": {

"total": 1,

"limit": 100,

"list": [

{

"task_time": "2023-09-01",

"mac": "08:E9:F6:CF:71:26",

"shop_id": 332200002,

"shop_name": "peng_internal_門市#",

"product_code": "67",

"product_name": "kettybot",

"bind_time": "2023-08-18 13:56:49",

"mileage": 0.01,

"duration": 0.03,

"interactive_count": 0,

"interactive_duration": 0,

"already_unbind": true,

"sn": "8TUAOCH91GIQSLM",

"run_count": 0,

"bind_count": 1,

"task_count": 3,

"robot_name": "葫蘆機器人PNT標準機型國內版（白黃）2023",

"work_days": 0,

"primary_industry_code": "65f2c092-2093-4225-8ffd-f49bd55b98c3",

"secondary_industry_code": "24e33544-8ebd-4750-8367-8a58d7a7d93d",

"country_code": "1",

"province_code": "440000",

"city_code": "440300",

"primary_industry": "",

"secondary_industry": "",

"country": "China",

"province": "廣東省",

"city": "深圳市"

}

# 配送-列表分頁查詢

更新時間:2025-11-28 17:34:14

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/delivery/paging |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |
| group_by | string | N | 分組方式：robot | shop，表示 按機器 | 按門市 |
| offset | integer | N | 偏移量，從0開始 |
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
| task_time | string | 任務結束時歸屬時段（hour時用Y-m-d H:i:s時間，day時用Y-m-d日期） |
| mac | string | MAC；注：按機器分組時有效 |
| shop_id | integer | 門市ID |
| shop_name | string | 門市名稱 |
| product_code | string | 機器類型編碼，詳見【枚舉】； 注：按機器分組時有效 |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| table_count | integer | 配送桌數 |
| tray_count | integer | 配送餐盤數 |
| sn | string | 機器SN；注：按機器分組時有效 |
| task_count | integer | 任務數 |
| speed | double | 平均速度m/s |
| run_count | integer | 運行機器人數；注：按門市分組時有效 |
| bind_count | integer | 綁定機器人數；注：按門市分組時有效 |
| robot_name | string | 機器人暱稱；注：按機器分組時有效 |
| work_days | integer | 工作天數(僅all彙總時有效) |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/delivery/paging?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=331300000&time_unit=day&group_by=robot

### 回傳範例

json

{

"message": "ok",

"data": {

"total": 2,

"offset": 0,

"limit": 100,

"list": [

{

"task_time": "2023-08-31",

"mac": "C0:84:7D:18:A8:4E",

"shop_id": 331300000,

"shop_name": "前德median門市",

"product_code": "61",

"product_name": "pudubot",

"bind_time": "2023-08-02 23:56:16",

"mileage": 0.01,

"duration": 0.07,

"table_count": 2,

"tray_count": 2,

"already_unbind": false,

"sn": "PD9102211844055",

"task_count": 2,

"speed": 0.02,

"run_count": 0,

"bind_count": 4

},

{

"task_time": "2023-08-30",

"mac": "20:50:E7:3E:61:36",

"shop_id": 331300000,

"shop_name": "前德median門市",

"product_code": "67",

"product_name": "kettybot",

"bind_time": "2023-08-28 10:45:28",

"mileage": 0.01,

"duration": 0.05,

# 領位-列表分頁查詢

更新時間:2025-11-28 17:58:34

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/greeter/paging |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |
| group_by | string | N | 分組方式：robot | shop，表示 按機器 | 按門市 |
| offset | integer | N | 偏移量，從0開始 |
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
| task_time | string | 任務結束時歸屬時段（hour時用Y-m-d H:i:s時間，day時用Y-m-d日期） |
| mac | string | MAC；注：按機器分組時有效 |
| shop_id | integer | 門市ID |
| shop_name | string | 門市名稱 |
| product_code | string | 機器類型編碼，詳見【枚舉】； 注：按機器分組時有效 |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| destination_count | integer | 領位帶客次數(目的地數) |
| sn | string | 機器SN；注：按機器分組時有效 |
| task_count | integer | 任務數 |
| speed | double | 平均速度m/s |
| run_count | integer | 運行機器人數；注：按門市分組時有效 |
| bind_count | integer | 綁定機器人數；注：按門市分組時有效 |
| robot_name | string | 機器人暱稱；注：按機器分組時有效 |
| work_days | integer | 工作天數(僅all彙總時有效) |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/greeter/paging?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=331300000&time_unit=day&group_by=robot

### 回傳範例

json

{

"message": "ok",

"data": {

"total": 1,

"limit": 100,

"list": [

{

"task_time": "2023-09-01",

"mac": "08:E9:F6:CF:71:26",

"shop_id": 332200002,

"shop_name": "peng_internal_門市#",

"product_code": "67",

"product_name": "kettybot",

"bind_time": "2023-08-18 13:56:49",

"mileage": 0,

"duration": 0.03,

"destination_count": 2,

"already_unbind": true,

"sn": "8TUAOCH91GIQSLM",

"run_count": 0,

"bind_count": 1,

"task_count": 4,

"robot_name": "葫蘆機器人PNT標準機型國內版（白黃）2023",

"work_days": 0,

"primary_industry_code": "65f2c092-2093-4225-8ffd-f49bd55b98c3",

"secondary_industry_code": "24e33544-8ebd-4750-8367-8a58d7a7d93d",

"country_code": "1",

"province_code": "440000",

"city_code": "440300",

"primary_industry": "",

"secondary_industry": "",

"country": "China",

"province": "廣東省",

"city": "深圳市"

}

],

# 宮格-列表分頁查詢

更新時間:2025-11-28 18:23:15

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/grid/paging |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |
| group_by | string | N | 分組方式：robot | shop，表示 按機器 | 按門市 |
| offset | integer | N | 偏移量，從0開始 |
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
| task_time | string | 任務結束時歸屬時段（hour時用Y-m-d H:i:s時間，day時用Y-m-d日期） |
| mac | string | MAC；注：按機器分組時有效 |
| shop_id | integer | 門市ID |
| shop_name | string | 門市名稱 |
| product_code | string | 機器類型編碼，詳見【枚舉】； 注：按機器分組時有效 |
| take_me_in_count | integer | 點擊次數:帶我進店 |
| featured_item_count | integer | 點擊次數:特色商品 |
| favorable_promotions_count | integer | 點擊次數:優惠活動 |
| guide_to_menu_count | integer | 點擊次數:領位 |
| poster_count | integer | 點擊次數:海報 |
| usher_count | integer | 點擊次數:帶路 |
| dance_count | integer | 點擊次數:跳舞 |
| video_poster_count | integer | 點擊次數:視頻 |
| sn | string | 機器SN；注：按機器分組時有效 |
| task_count | integer | 任務數 |
| speed | double | 平均速度m/s |
| run_count | integer | 運行機器人數；注：按門市分組時有效 |
| bind_count | integer | 綁定機器人數；注：按門市分組時有效 |
| robot_name | string | 機器人暱稱；注：按機器分組時有效 |
| work_days | integer | 工作天數(僅all彙總時有效) |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/grid/paging?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=332200002&time_unit=day&group_by=robot

### 回傳範例

json

{

"message": "ok",

"data": {

"total": 1,

"limit": 100,

"list": [

{

"task_time": "2023-09-01",

"mac": "08:E9:F6:CF:71:26",

"shop_id": 332200002,

"shop_name": "peng_internal_門市#",

"product_code": "67",

"product_name": "kettybot",

"bind_time": "2023-08-18 13:56:49",

"take_me_in_count": 2,

"featured_item_count": 1,

"favorable_promotions_count": 1,

"guide_to_menu_count": 0,

"poster_count": 0,

"usher_count": 0,

"dance_count": 0,

"video_poster_count": 0,

"already_unbind": true,

"sn": "8TUAOCH91GIQSLM",

"run_count": 0,

"bind_count": 1,

"robot_name": "葫蘆機器人PNT標準機型國內版（白黃）2023",

"work_days": 0,

"primary_industry_code": "65f2c092-2093-4225-8ffd-f49bd55b98c3",

"secondary_industry_code": "24e33544-8ebd-4750-8367-8a58d7a7d93d",

"country_code": "1",

"province_code": "440000",

"city_code": "440300",

"primary_industry": "",

"secondary_industry": "",

"country": "China",

# 互動-列表分頁查詢

更新時間:2025-11-28 18:12:55

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/interactive/paging |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |
| group_by | string | N | 分組方式：robot | shop，表示 按機器 | 按門市 |
| offset | integer | N | 偏移量，從0開始 |
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
| task_time | string | 任務結束時歸屬時段（hour時用Y-m-d H:i:s時間，day時用Y-m-d日期） |
| mac | string | MAC；注：按機器分組時有效 |
| shop_id | integer | 門市ID |
| shop_name | string | 門市名稱 |
| product_code | string | 機器類型編碼，詳見【枚舉】； 注：按機器分組時有效 |
| interactive_count | integer | 互動人次 |
| voice_count | integer | 語音互動人次 |
| voice_duration | double | 語音互動時長(h) |
| sn | string | 機器SN；注：按機器分組時有效 |
| task_count | integer | 任務數 |
| speed | double | 平均速度m/s |
| run_count | integer | 運行機器人數；注：按門市分組時有效 |
| bind_count | integer | 綁定機器人數；注：按門市分組時有效 |
| robot_name | string | 機器人暱稱；注：按機器分組時有效 |
| work_days | integer | 工作天數(僅all彙總時有效) |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/interactive/paging?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=332200002&time_unit=day&group_by=robot

### 回傳範例

json

{

"message": "ok",

"data": {

"total": 1,

"limit": 100,

"list": [

{

"task_time": "2023-09-01",

"mac": "08:E9:F6:CF:71:26",

"shop_id": 332200002,

"shop_name": "peng_internal_門市#",

"product_code": "67",

"product_name": "kettybot",

"bind_time": "2023-08-18 13:56:49",

"interactive_count": 2,

"voice_count": 0,

"voice_duration": 0,

"already_unbind": true,

"sn": "8TUAOCH91GIQSLM",

"run_count": 0,

"bind_count": 1,

"robot_name": "葫蘆機器人PNT標準機型國內版（白黃）2023",

"work_days": 0,

"primary_industry_code": "65f2c092-2093-4225-8ffd-f49bd55b98c3",

"secondary_industry_code": "24e33544-8ebd-4750-8367-8a58d7a7d93d",

"country_code": "1",

"province_code": "440000",

"city_code": "440300",

"primary_industry": "",

"secondary_industry": "",

"country": "China",

"province": "廣東省",

"city": "深圳市"

}

],

"offset": 0

# 回盤-列表分頁查詢

更新時間:2025-11-28 18:20:25

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/recovery/paging |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |
| group_by | string | N | 分組方式：robot | shop，表示 按機器 | 按門市 |
| offset | integer | N | 偏移量，從0開始 |
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
| task_time | string | 任務結束時歸屬時段（hour時用Y-m-d H:i:s時間，day時用Y-m-d日期） |
| mac | string | MAC；注：按機器分組時有效 |
| shop_id | integer | 門市ID |
| shop_name | string | 門市名稱 |
| product_code | string | 機器類型編碼，詳見【枚舉】； 注：按機器分組時有效 |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| table_count | integer | 餐桌數 |
| sn | string | 機器SN；注：按機器分組時有效 |
| task_count | integer | 任務數 |
| speed | double | 平均速度m/s |
| run_count | integer | 運行機器人數；注：按門市分組時有效 |
| bind_count | integer | 綁定機器人數；注：按門市分組時有效 |
| robot_name | string | 機器人暱稱；注：按機器分組時有效 |
| work_days | integer | 工作天數(僅all彙總時有效) |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/recovery/paging?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=331300000&time_unit=day&group_by=robot

### 回傳範例

json

{

"message": "ok",

"data": {

"total": 1,

"limit": 100,

"list": [

{

"task_time": "2023-08-31",

"mac": "C0:84:7D:18:A8:4E",

"shop_id": 331300000,

"shop_name": "【勿動】【前德median】",

"product_code": "61",

"product_name": "pudubot",

"bind_time": "2023-08-02 23:56:16",

"mileage": 0,

"duration": 0,

"table_count": 0,

"already_unbind": false,

"sn": "PD9102211844055",

"run_count": 0,

"bind_count": 3,

"task_count": 1,

"robot_name": "1",

"work_days": 0,

"primary_industry_code": "7c8ca6dd-cea1-4149-9a29-693cffb815ee",

"secondary_industry_code": "fae6fad3-857a-458f-95f0-ebac5d9c4494",

"country_code": "20000",

"province_code": "0",

"city_code": "0",

"primary_industry": "",

"secondary_industry": "",

"country": "Singapore",

"province": "",

"city": "",

"speed": 0

}

# 攬客-列表分頁查詢

更新時間:2025-11-28 18:11:33

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/solicit/paging |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |
| group_by | string | N | 分組方式：robot | shop，表示 按機器 | 按門市 |
| offset | integer | N | 偏移量，從0開始 |
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
| task_time | string | 任務結束時歸屬時段（hour時用Y-m-d H:i:s時間，day時用Y-m-d日期） |
| mac | string | MAC；注：按機器分組時有效 |
| shop_id | integer | 門市ID |
| shop_name | string | 門市名稱 |
| product_code | string | 機器類型編碼，詳見【枚舉】； 注：按機器分組時有效 |
| duration | double | 運行時長(h) |
| play_count | integer | 打招呼次數 |
| attach_persons | integer | 觸達人次 |
| attract_persons | integer | 吸引人次 |
| interactive_count | integer | 互動人次 |
| sn | string | 機器SN；注：按機器分組時有效 |
| task_count | integer | 任務數 |
| speed | double | 平均速度m/s |
| run_count | integer | 運行機器人數；注：按門市分組時有效 |
| bind_count | integer | 綁定機器人數；注：按門市分組時有效 |
| robot_name | string | 機器人暱稱；注：按機器分組時有效 |
| work_days | integer | 工作天數(僅all彙總時有效) |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/solicit/paging?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=331300000&time_unit=day&group_by=robot

### 回傳範例

json

{

"message": "ok",

"data": {

"total": 1,

"limit": 100,

"list": [

{

"task_time": "2023-09-01",

"mac": "08:E9:F6:CF:71:26",

"shop_id": 332200002,

"shop_name": "peng_internal_門市#",

"product_code": "67",

"product_name": "kettybot",

"bind_time": "2023-08-18 13:56:49",

"duration": 0.01,

"play_count": 0,

"attach_persons": 0,

"attract_persons": 1,

"interactive_count": 2,

"already_unbind": true,

"sn": "8TUAOCH91GIQSLM",

"run_count": 0,

"bind_count": 1,

"task_count": 3,

"robot_name": "葫蘆機器人PNT標準機型國內版（白黃）2023",

"work_days": 0,

"primary_industry_code": "65f2c092-2093-4225-8ffd-f49bd55b98c3",

"secondary_industry_code": "24e33544-8ebd-4750-8367-8a58d7a7d93d",

"country_code": "1",

"province_code": "440000",

"city_code": "440300",

"primary_industry": "",

"secondary_industry": "",

"country": "China",

"province": "廣東省",

"city": "深圳市"

# 頂升-列表分頁查詢

更新時間:2025-11-28 17:39:25

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/task/lifting/paging |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |
| group_by | string | N | 分組方式：robot | shop，表示 按機器 | 按門市 |
| offset | integer | N | 偏移量，從0開始 |
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
| task_time | string | 任務結束時歸屬時段（hour時用Y-m-d H:i:s時間，day時用Y-m-d日期） |
| mac | string | MAC；注：按機器分組時有效 |
| shop_id | integer | 門市ID |
| shop_name | string | 門市名稱 |
| product_code | string | 機器類型編碼，詳見【枚舉】； 注：按機器分組時有效 |
| sn | string | 機器SN；注：按機器分組時有效 |
| run_count | integer | 運行機器人數；注：按門市分組時有效 |
| bind_count | integer | 綁定機器人數；注：按門市分組時有效 |
| mileage | double | 運行里程(km) |
| duration | double | 運行時長(h) |
| destination_count | integer | 運貨次數 |
| task_count | integer | 任務數 |
| speed | double | 平均速度m/s |
| run_count | integer | 運行機器人數；注：按門市分組時有效 |
| bind_count | integer | 綁定機器人數；注：按門市分組時有效 |
| robot_name | string | 機器人暱稱；注：按機器分組時有效 |
| work_days | integer | 工作天數(僅all彙總時有效) |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/task/lifting/paging?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=331300000&time_unit=day&group_by=robot

### 回傳範例

json

{

"data": {

"limit": 10,

"list": [

{

"bind_count": 4,

"destination_count": 1,

"duration": 0,

"mac": "",

"mileage": 0,

"sn": "",

"product_code": "",

"robot_name": "",

"shop_id": 341200000,

"shop_name": "尹路門市",

"task_count": 1,

"task_time": "2024-09-10",

"work_days": 0

},

{

"bind_count": 4,

"destination_count": 61,

"duration": 0.32,

"mac": "",

"mileage": 0.08,

"sn": "",

"product_code": "",

"robot_name": "",

"shop_id": 341200000,

"shop_name": "尹路門市",

"task_count": 61,

"task_time": "2024-09-09",

"work_days": 0

}

],

"offset": 0,

# 清潔(洗地|掃地)-列表分頁查詢

更新時間:2025-11-28 15:55:56

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/analysis/clean/paging |
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
| time_unit | string | N | 時間單位：day | hour，表示 按天 | 按小時 預設值：day(時間跨度>24 小時) ，hour(時間跨度<24 小時) |
| group_by | string | N | 分組方式：robot | shop，表示 按機器 | 按門市 |
| offset | integer | N | 偏移量，從0開始 |
| limit | integer | N | 每頁條目數，1 ~ 20 |
| clean_mode | integer | N | 清潔模式過濾（0全部，1洗地，2掃地） |
| sub_mode | integer | N | 子模式過濾，目前只有掃地模式使用(-1全部，0自定義、1地毯吸塵、3靜音塵推) |

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
| task_time | string | 任務結束時歸屬時段（hour時用Y-m-d H:i:s時間，day時用Y-m-d日期） |
| mac | string | MAC；注：按機器分組時有效 |
| shop_id | integer | 門市ID |
| shop_name | string | 門市名稱 |
| product_code | string | 機器類型編碼，詳見【枚舉】； 注：按機器分組時有效 |
| product_name | string | 機器類型；注：按機器分組時有效 |
| area | double | 清潔總面積(m²) |
| duration | double | 清潔總時長(h) |
| sn | string | 機器SN；注：按機器分組時有效 |
| task_count | integer | 任務數 |
| speed | double | 平均速度m/s |
| run_count | integer | 運行機器人數；注：按門市分組時有效 |
| bind_count | integer | 綁定機器人數；注：按門市分組時有效 |
| power_consumption | double | 耗電量（kw/h） |
| water_consumption | double | 耗水量（ML） |
| task_count | integer | 任務數 |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/analysis/clean/paging?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=324100000&time_unit=day&group_by=shop&clean_mode=2&sub_mode=-1&offset=0&limit=10

### 回傳範例

json

{

"message": "ok",

"data": {

"total": 2,

"offset": 0,

"limit": 10,

"list": [

{

"task_time": "2023-08-31",

"mac": "",

"shop_id": 324100000,

"shop_name": "二級dls創建的出塵清潔門市",

"product_code": "",

"product_name": "",

"bind_time": "",

"area": 31.33,

"duration": 0.07,

"already_unbind": false,

"sn": "",

"run_count": 2,

"bind_count": 5,

"power_consumption": 0.05,

"water_consumption": 0,

"task_count": 8

},

{

"task_time": "2023-08-30",

"mac": "",

"shop_id": 324100000,

"shop_name": "二級dls創建的出塵清潔門市",

"product_code": "",

"product_name": "",

"bind_time": "",

"area": 56.69,

"duration": 0.12,

"already_unbind": false,

# 呼叫-目的地執行明細

更新時間:2025-11-28 18:35:24

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/task/call |
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
| offset | integer | N | 偏移量，從0開始 |
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
| task_time | string | 任務結束時歸屬時段（hour時用Y-m-d H:i:s時間，day時用Y-m-d日期） |
| product_code | string | 機器類型編碼，詳見【枚舉】； 注：按機器分組時有效 |
| mac | string | MAC；注：按機器分組時有效 |
| sn | string | 機器SN |
| shop_id | integer | 門市ID |
| shop_name | string | 門市名稱 |
| begin_time | string | 任務開始時間（Y-m-d H:i:s格式） |
| destination | string | 任務目的地 |
| arrival_time | string | 到達目的地時間（Y-m-d H:i:s格式） |
| stay_duration | double | 目的地逗留時長（s） |
| cur_duration | double | 當前目的地運行時長（min） |
| cur_mileage | double | 當前目的地運行里程（m） |
| robot_name | string | 機器人暱稱；注：按機器分組時有效 |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/task/call?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=331300000&time_unit=day&group_by=robot

### 回傳範例

json

{

"data": {

"limit": 10,

"list": [

{

"arrival_time": "",

"begin_time": "2024-09-12 14:10:08",

"cur_duration": 0,

"cur_mileage": 0,

"destination": "26樓抵達點",

"mac": "08:E9:F6:B1:93:34",

"sn": "OPA202311030123",

"product_code": "68",

"robot_name": "08:E9:F6:B1:93:34",

"shop_id": 415100008,

"shop_name": "jaden的門市",

"stay_duration": 0,

"task_time": "2024-09-12"

},

{

"arrival_time": "",

"begin_time": "2024-09-12 11:02:33",

"cur_duration": 0,

"cur_mileage": 0,

"destination": "25樓出餐",

"mac": "08:E9:F6:B1:93:34",

"sn": "OPA202311030123",

"product_code": "68",

"robot_name": "08:E9:F6:B1:93:34",

"shop_id": 415100008,

"shop_name": "jaden的門市",

"stay_duration": 0,

"task_time": "2024-09-12"

}

],

"offset": 0,

# 配送-目的地執行明細

更新時間:2025-11-28 18:39:32

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/task/delivery |
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
| offset | integer | N | 偏移量，從0開始 |
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
| task_time | string | 任務結束時歸屬時段（hour時用Y-m-d H:i:s時間，day時用Y-m-d日期） |
| product_code | string | 機器類型編碼，詳見【枚舉】； 注：按機器分組時有效 |
| mac | string | MAC；注：按機器分組時有效 |
| sn | string | 機器SN |
| shop_id | integer | 門市ID |
| shop_name | string | 門市名稱 |
| begin_time | string | 任務開始時間（Y-m-d H:i:s格式） |
| destination | string | 任務目的地 |
| arrival_time | string | 到達目的地時間（Y-m-d H:i:s格式） |
| stay_duration | double | 目的地逗留時長（s） |
| cur_duration | double | 當前目的地運行時長（min） |
| cur_mileage | double | 當前目的地運行里程（m） |
| robot_name | string | 機器人暱稱；注：按機器分組時有效 |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/task/delivery?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=331300000&time_unit=day&group_by=robot

### 回傳範例

json

{

"data": {

"limit": 10,

"list": [

{

"arrival_time": "",

"begin_time": "2024-09-12 14:10:08",

"cur_duration": 0,

"cur_mileage": 0,

"destination": "26樓抵達點",

"mac": "08:E9:F6:B1:93:34",

"sn": "OPA202311030123",

"product_code": "68",

"robot_name": "08:E9:F6:B1:93:34",

"shop_id": 415100008,

"shop_name": "jaden的門市",

"stay_duration": 0,

"task_time": "2024-09-12"

},

{

"arrival_time": "",

"begin_time": "2024-09-12 11:02:33",

"cur_duration": 0,

"cur_mileage": 0,

"destination": "25樓出餐",

"mac": "08:E9:F6:B1:93:34",

"sn": "OPA202311030123",

"product_code": "68",

"robot_name": "08:E9:F6:B1:93:34",

"shop_id": 415100008,

"shop_name": "jaden的門市",

"stay_duration": 0,

"task_time": "2024-09-12"

}

],

"offset": 0,

# 領位-目的地執行明細

更新時間:2025-11-28 18:43:54

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/task/greeter |
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
| offset | integer | N | 偏移量，從0開始 |
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
| task_time | string | 任務結束時歸屬時段（hour時用Y-m-d H:i:s時間，day時用Y-m-d日期） |
| product_code | string | 機器類型編碼，詳見【枚舉】； 注：按機器分組時有效 |
| mac | string | MAC；注：按機器分組時有效 |
| sn | string | 機器SN |
| shop_id | integer | 門市ID |
| shop_name | string | 門市名稱 |
| begin_time | string | 任務開始時間（Y-m-d H:i:s格式） |
| destination | string | 任務目的地 |
| arrival_time | string | 到達目的地時間（Y-m-d H:i:s格式） |
| stay_duration | double | 目的地逗留時長（s） |
| cur_duration | double | 當前目的地運行時長（min） |
| cur_mileage | double | 當前目的地運行里程（m） |
| robot_name | string | 機器人暱稱；注：按機器分組時有效 |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/task/greeter?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=331300000&time_unit=day&group_by=robot

### 回傳範例

json

{

"data": {

"limit": 10,

"list": [

{

"arrival_time": "",

"begin_time": "2024-09-12 14:10:08",

"cur_duration": 0,

"cur_mileage": 0,

"destination": "26樓抵達點",

"mac": "08:E9:F6:B1:93:34",

"sn": "OPA202311030123",

"product_code": "68",

"robot_name": "08:E9:F6:B1:93:34",

"shop_id": 415100008,

"shop_name": "jaden的門市",

"stay_duration": 0,

"task_time": "2024-09-12"

},

{

"arrival_time": "",

"begin_time": "2024-09-12 11:02:33",

"cur_duration": 0,

"cur_mileage": 0,

"destination": "25樓出餐",

"mac": "08:E9:F6:B1:93:34",

"sn": "OPA202311030123",

"product_code": "68",

"robot_name": "08:E9:F6:B1:93:34",

"shop_id": 415100008,

"shop_name": "jaden的門市",

"stay_duration": 0,

"task_time": "2024-09-12"

}

],

"offset": 0,

# 頂升-目的地執行明細

更新時間:2025-11-28 18:45:17

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/task/lifting |
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
| offset | integer | N | 偏移量，從0開始 |
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
| task_time | string | 任務結束時歸屬時段（hour時用Y-m-d H:i:s時間，day時用Y-m-d日期） |
| mac | string | MAC；注：按機器分組時有效 |
| shop_id | integer | 門市ID |
| shop_name | string | 門市名稱 |
| product_code | string | 機器類型編碼，詳見【枚舉】； 注：按機器分組時有效 |
| sn | string | 機器SN；注：按機器分組時有效 |
| begin_time | string | 任務開始時間（Y-m-d H:i:s格式） |
| destination | string | 任務目的地 |
| arrival_time | string | 到達目的地時間（Y-m-d H:i:s格式） |
| stay_duration | double | 目的地逗留時長（s） |
| cur_duration | double | 當前目的地運行時長（min） |
| cur_mileage | double | 當前目的地運行里程（m） |
| robot_name | string | 機器人暱稱 |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/task/lifting?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=331300000&time_unit=day&group_by=robot

### 回傳範例

json

{

"data": {

"limit": 10,

"list": [

{

"arrival_time": "",

"begin_time": "2024-09-12 14:10:08",

"cur_duration": 0,

"cur_mileage": 0,

"destination": "26樓抵達點",

"mac": "08:E9:F6:B1:93:34",

"sn": "OPA202311030123",

"product_code": "68",

"robot_name": "08:E9:F6:B1:93:34",

"shop_id": 415100008,

"shop_name": "jaden的門市",

"stay_duration": 0,

"task_time": "2024-09-12"

},

{

"arrival_time": "",

"begin_time": "2024-09-12 11:02:33",

"cur_duration": 0,

"cur_mileage": 0,

"destination": "25樓出餐",

"mac": "08:E9:F6:B1:93:34",

"sn": "OPA202311030123",

"product_code": "68",

"robot_name": "08:E9:F6:B1:93:34",

"shop_id": 415100008,

"shop_name": "jaden的門市",

"stay_duration": 0,

"task_time": "2024-09-12"

}

],

"offset": 0,

# 回盤-目的地執行明細

更新時間:2025-11-28 18:46:26

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/task/recovery |
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
| offset | integer | N | 偏移量，從0開始 |
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
| task_time | string | 任務結束時歸屬時段（hour時用Y-m-d H:i:s時間，day時用Y-m-d日期） |
| product_code | string | 機器類型編碼，詳見【枚舉】； 注：按機器分組時有效 |
| mac | string | MAC；注：按機器分組時有效 |
| sn | string | 機器SN |
| shop_id | integer | 門市ID |
| shop_name | string | 門市名稱 |
| begin_time | string | 任務開始時間（Y-m-d H:i:s格式） |
| destination | string | 任務目的地 |
| arrival_time | string | 到達目的地時間（Y-m-d H:i:s格式） |
| stay_duration | double | 目的地逗留時長（s） |
| cur_duration | double | 當前目的地運行時長（min） |
| cur_mileage | double | 當前目的地運行里程（m） |
| robot_name | string | 機器人暱稱；注：按機器分組時有效 |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/task/recovery?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=331300000&time_unit=day&group_by=robot

### 回傳範例

json

{

"data": {

"limit": 10,

"list": [

{

"arrival_time": "",

"begin_time": "2024-09-12 14:10:08",

"cur_duration": 0,

"cur_mileage": 0,

"destination": "26樓抵達點",

"mac": "08:E9:F6:B1:93:34",

"sn": "OPA202311030123",

"product_code": "68",

"robot_name": "08:E9:F6:B1:93:34",

"shop_id": 415100008,

"shop_name": "jaden的門市",

"stay_duration": 0,

"task_time": "2024-09-12"

},

{

"arrival_time": "",

"begin_time": "2024-09-12 11:02:33",

"cur_duration": 0,

"cur_mileage": 0,

"destination": "25樓出餐",

"mac": "08:E9:F6:B1:93:34",

"sn": "OPA202311030123",

"product_code": "68",

"robot_name": "08:E9:F6:B1:93:34",

"shop_id": 415100008,

"shop_name": "jaden的門市",

"stay_duration": 0,

"task_time": "2024-09-12"

}

],

"offset": 0,

# 清潔報告-列表

更新時間:2025-12-04 17:06:08

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/log/clean_task/query_list |
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
| offset | integer | N | 偏移量，從0開始 |
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
| task_name | string | 任務名稱 |
| report_id | string | 報告ID |
| mode | integer | 清掃模式：1洗地 2掃地 |
| start_time | integer | 任務開始時間(s) |
| end_time | integer | 任務結束時間(s) |
| clean_time | integer | 清潔時間(s) |
| clean_area | double | 清潔面積(m²) |
| create_time | string | 上報雲端時間(Y-m-d H:i:s) |
| mac | string | MAC |
| sn | string | 機器SN |
| status | integer | 狀態 0未開始/預設 1清掃中 2任務暫停 3任務中斷 4任務結束 5任務異常 6任務取消 |
| sub_mode | integer | 子模式: 掃地[0自定義 1地毯吸塵 3靜音塵推]; 洗地[0自定義 1吸力模式 11刷洗吸 12刷吸 13刷洗 14幹刷] |
| task_area | double | 任務計劃清潔面積(m²) |

### 

## 5.呼叫範例

### 請求範例

http

/data-board/v1/log/clean_task/query_list?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=2085&offset=0&limit=10

### 回傳範例

json

{

"message": "ok",

"data": {

"total": 100,

"offset": 0,

"limit": 10,

"list": [

{

"task_name": "任務6",

"report_id": "894770283318874112",

"mode": 2,

"start_time": 1693496325,

"end_time": 1693497125,

"clean_time": 529,

"clean_area": 82.33702850341797,

"create_time": "2023-08-31 23:52:08",

"mac": "B4:ED:D5:75:6E:EB",

"sn": "OPB4EDD5756EEB",

"status": 4,

"sub_mode": 0,

"task_area": 104.087494

},

{

"task_name": "任務6",

"report_id": "894766973299986432",

"mode": 2,

"start_time": 1693495536,

"end_time": 1693496319,

"clean_time": 511,

"clean_area": 80.64002990722656,

"create_time": "2023-08-31 23:38:43",

"mac": "B4:ED:D5:75:6E:EB",

"sn": "OPB4EDD5756EEB",

"status": 4,

"sub_mode": 0,

"task_area": 104.087494

# 清潔報告-詳情

更新時間:2025-12-04 17:06:00

## 1. 介面說明

### 功能描述

無

### 適用範圍

* **支援機型**：ALL

* **前置準備**：無

## 2. 基本資訊

| 請求路徑（Path） | /data-board/v1/log/clean_task/query |
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
| sn | string | Y | SN序列號 |
| report_id | string | Y | 報告ID (sn+報告ID才能唯一) |
| timezone_offset | integer | N | 時區偏移小時, 範圍 -12 ~ 14，表示 (UTC-12 ~ UTC+14）；預設UTC+0 |

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
| task_name | string | 任務名稱 |
| report_id | string | 報告ID |
| mode | integer | 清掃模式：1洗地 2掃地 |
| start_time | integer | 任務開始時間(s) |
| end_time | integer | 任務結束時間(s) |
| clean_time | integer | 清潔時間(s) |
| clean_area | double | 清潔面積(m²) |
| create_time | string | 上報雲端時間(Y-m-d H:i:s) |
| mac | string | MAC |
| sn | string | 機器SN |
| task_id | string | 任務ID |
| task_version | string | 任務的版本號 |
| battery | double | 任務結束時電量 |
| elevator_count | integer | 乘梯次數 |
| status | integer | 狀態 0未開始/預設 1清掃中 2任務暫停 3任務中斷 4任務結束 5任務異常 6任務取消 |
| config | string | 清掃設定 |
| floor_list | string | 樓層列表 |
| floor_count | integer | 清掃的樓層個數 |
| break_count | integer | 清掃中斷次數 |
| task_area | double | 任務計劃清潔面積(m²) |
| average_area | double | 實際平均清潔面積(m²) |
| percentage | integer | 進度百分比 |
| remaining_time | integer | 剩餘時間(s) |
| cost_water | integer | 消耗水量(ml） |
| cost_battery | integer | 消耗電量，百分比 |
| charge_count | integer | 充電次數 |
| sub_mode | integer | 子模式: 掃地[0自定義 1地毯吸塵 3靜音塵推]; 洗地[0自定義 1吸力模式 11刷洗吸 12刷吸 13刷洗 14幹刷] |

## 5.呼叫範例

### 請求範例

http

/data-board/v1/log/clean_task/query?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=2085&sn=OPB4EDD5756EEB&report_id=894770283318874112

### 回傳範例

json

{

"message": "ok",

"data": {

"task_name": "任務6",

"report_id": "894770283318874112",

"mode": 2,

"start_time": 1693496325,

"end_time": 1693497125,

"clean_time": 529,

"clean_area": 82.33702850341797,

"create_time": "2023-08-31 23:52:08",

"mac": "B4:ED:D5:75:6E:EB",

"sn": "OPB4EDD5756EEB",

"task_id": "894281823013060608",

"task_version": "1693379867190",

"battery": 15,

"elevator_count": 0,

"status": 4,

"config": "{\"mode\":2,\"type\":0,\"vacuum_speed\":2,\"vacuum_suction\":2,\"wash_speed\":0,\"wash_suction\":0,\"wash_wash\":0}",

"floor_list": "[{\"map_floor\":\"4\",\"map_name\":\"4#119#service\",\"map_version\":5,\"result\":{\"area\":82.33702744040733,\"break_point\":{\"start\":{},\"vector\":{}},\"status\":4,\"time\":529},\"task_local_url\":\"/sdcard/pudu/report/894770283318874112NCMxMTkjc2VydmljZQ==1693497126427.png\",\"task_result_url\":\"http://pudu-file-host.oss-cn-beijing.aliyuncs.com/pudu_cloud_platform/map/B4EDD5756EEB/9b9f22e7eb10d50586f44fe344b2c474.png\"}]",

"floor_count": 1,

"break_count": 0,

"task_area": 104.087494,

"average_area": 0,

"percentage": 100,

"remaining_time": 0,

"cost_water": 0,

"cost_battery": 4,

"charge_count": 0,

"sub_mode": 0

}

}

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

http

/data-board/v1/log/boot/query_list?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=325100001&offset=0&limit=10

### 回傳範例

json

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

http

/data-board/v1/log/charge/query_list?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=201200012&offset=0&limit=10

### 回傳範例

json

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

http

/data-board/v1/log/error/query_list?timezone_offset=8&start_time=1693324800&end_time=1693497599&shop_id=323400005&offset=0&limit=10&error_levels=Fatal,Error,Warning,Event&error_types=LostLocalization,LostRGBD

### 回傳範例

json

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



---

# 附錄A：PYTHON API/使用說明書.md（完整併入）

# Pudu 控制檯使用說明書（給不懂程式碼的使用者）

本文件是給「不需要看程式」也能上手的人。
只要照步驟做，就可以完成：

1. 在 API 測試頁找到可用 API
2. 填參數送出請求
3. 把成功請求內容做成動作範本
4. 把動作範本組成按鈕
5. 在操作頁一鍵執行

---

## 1. 這個系統在做什麼

這個網頁是 Pudu 機器人控制檯，主要分成三個工作區：

- 設定：管理門市、機器人、動作範本、按鈕、地圖分頁
- 操作：看到機器人狀態、地圖位置，並執行按鈕
- API 測試：測試 API，確認參數正確，再轉成範本

你可以把它想成三步：

- 先在 API 測試頁驗證「API 怎麼打才會成功」
- 再去設定頁把成功內容存成「動作範本」
- 最後在設定頁建立「按鈕」並綁定範本，回操作頁按按鈕執行

---

## 2. 進入系統

### 2.1 第一次使用：先安裝（Windows PowerShell）

請在 PowerShell 依序貼上執行：

```powershell
Set-Location "d:\SynologyDrive\桌面\PYTHON API"
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

若看到 PowerShell 阻擋啟用虛擬環境，先執行一次：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

然後關掉 PowerShell 重開，再執行上面 4 行安裝指令。

### 2.2 啟動網頁服務（Windows PowerShell）

啟動方法 A（建議）：

```powershell
Set-Location "d:\SynologyDrive\桌面\PYTHON API"
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py --server.port 8501 --server.address 127.0.0.1
```

啟動方法 B（不啟用環境，直接指定 python）：

```powershell
Set-Location "d:\SynologyDrive\桌面\PYTHON API"
& ".\.venv\Scripts\python.exe" -m streamlit run app.py --server.port 8501 --server.address 127.0.0.1
```

看到 `You can now view your Streamlit app in your browser.` 代表啟動成功。
這個終端機視窗要保持開著，關掉就會停止服務。

### 2.3 開啟網址

1. 啟動後進入 `http://localhost:8501/`
2. 看到「展間系統登入」畫面
3. 輸入 PIN（若管理員有設定 `SHOWROOM_ACCESS_PIN`）
4. 登入後從左側側欄切換頁面

### 2.4 如果打不開網頁，請照這組排查指令

先檢查 8501 埠是否真的有服務在跑：

```powershell
Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue
```

若查不到任何資料，代表服務沒起來，請回到「2.2 啟動網頁服務」重新跑。

若有資料但網頁還是打不開：

1. 改開 `http://127.0.0.1:8501/`
2. 確認你是同一臺電腦開啟瀏覽器
3. 檢查終端機是否已出現紅色錯誤訊息

若出現 `ModuleNotFoundError` 類錯誤，回「2.1 第一次使用：先安裝」重跑安裝指令。

若 8501 被其他程式佔用，改用 8502 啟動：

```powershell
Set-Location "d:\SynologyDrive\桌面\PYTHON API"
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py --server.port 8502 --server.address 127.0.0.1
```

然後開 `http://127.0.0.1:8502/`。

### 2.5 首頁（app 首頁）

首頁只做兩件事：

- 告訴你左側有「設定 / 操作 / API」三頁
- 提供「登出」按鈕

---

## 3. 設定頁（最重要的後臺）

設定頁有 6 個分頁：

1. 商店
2. 機器人
3. 群組
4. 動作範本
5. 按鈕
6. 地圖分頁

建議第一次使用時，照這個順序設定。

### 3.1 商店

用途：設定整體系統參數。

主要欄位：

- 商店名稱：畫面顯示用
- Pudu Shop ID：很多 API 會用到的門市 ID
- 時區：通常用 `Asia/Taipei`
- 機器人並發：同時處理機器人的數量上限
- API 並發：同時打 API 的數量上限
- 狀態輪詢秒數 / 位置輪詢秒數：更新頻率

常見操作：

- 按「儲存」更新設定
- 按「讀取商店」從 Pudu 拉商店清單確認 shop_id

### 3.2 機器人

用途：管理要控制哪些機器人。

可做的事：

- 重建預設分組（清潔機器人 / 運送機器人）
- 手動新增機器人（填 SN、暱稱）
- 從 Pudu 匯入機器人（選 SN 批次匯入）
- 編輯每臺機器人（改暱稱、啟用/停用、刪除）

提醒：

- 沒有啟用的機器人，不會在操作頁執行
- SN 一定要正確，錯 SN 會導致 API 打失敗

### 3.3 群組

用途：把多臺機器人整理成一組，方便查詢群組狀態或後續管理。

可做的事：

- 新增群組
- 修改群組名稱
- 勾選或取消群組成員
- 儲存群組內容
- 刪除群組
- 一鍵重建「清潔機器人 / 運送機器人」預設群組

提醒：

- API 測試頁查群組狀態時，可直接輸入群組名稱，例如「清潔機器人」或「運送機器人」
- 若系統找不到 Pudu 雲端 group_id，會自動改用本地群組成員 SN 查詢
- 群組沒有成員時，查群組狀態一定會失敗或回空資料

### 3.4 動作範本

用途：把「成功的 API 請求格式」存成可重複使用的模板。

新增時要填：

- 名稱：例如「切換到 A 地圖」
- Method：GET / POST / PUT / DELETE / PATCH
- Path：例如 `/open-platform-service/v1/switch_map`
- Query Template JSON：GET 常用
- Body Template JSON：POST 常用
- Timeout(ms)

重點觀念：

- 如果是 GET，通常重點放在 Query Template JSON
- 如果是 POST，通常重點放在 Body Template JSON
- 建議先從 API 測試頁測成功，再複製過來

### 3.5 按鈕

用途：把多個動作範本組成一顆可執行按鈕。

新增按鈕時：

- 填按鈕名稱（例如「開店前巡檢」）
- 可填描述
- 設排序（數字小的通常排前面）
- 至少綁定 1 個動作範本（可多選）

執行時效果：

- 在操作頁按下按鈕後，系統會依綁定順序執行範本
- 每個機器人的成功/失敗都會顯示

### 3.6 地圖分頁

用途：管理操作頁下拉選單中的地圖項目與顯示名稱。

可做的事：

- 手動新增 map_name
- 設定顯示名稱（比較好懂）
- 設定排序與啟用
- 從 Pudu 讀取地圖作為參考

提醒：

- map_name 要與實際 API 使用名稱一致
- map_name 不一致時，地圖載入與位置顯示會異常

---

## 4. 操作頁（現場執行頁）

操作頁主要分三塊：

1. 按鈕執行
2. 機器人狀態
3. 地圖資訊 + 事件紀錄

### 4.1 按鈕執行

使用方式：

1. 先勾選本次要作用的機器人（可全選/全不選）
2. 按任一功能按鈕
3. 看展開結果：每臺機器人、每個動作 API 的成功/失敗

結果會顯示：

- HTTP 狀態碼
- 請求 URL / 路徑
- Query 與 Body
- 回應 JSON

### 4.2 機器人狀態

可查看：

- 在線/離線
- 執行狀態
- 即時位置資訊（搭配地圖）

可用功能：

- 「更新機器人狀態」手動刷新
- 「每 10 秒自動更新機器人位置」自動刷新

### 4.3 地圖資訊

操作步驟：

1. 從下拉選地圖
2. 按「載入地圖資料」
3. 在預覽圖看到機器人點位
4. 需要時展開「地圖原始回應 JSON」或「地圖 API 除錯紀錄」

常見狀況：

- 有位置但不在圖上：可能機器人回傳的 map_name 跟你選的地圖不同
- 地圖空白：可能 shop_id/map_name 錯誤

### 4.4 事件紀錄

按「讀取事件紀錄」後可看最近操作事件，包含：

- 時間
- 狀態
- 事件類型
- 來源
- 機器人

---

## 5. API 測試頁（開發與驗證入口）

這頁用來「先測到成功，再標準化成範本」。

### 5.1 你會看到的區塊

- 快速搜尋 API（名稱/路徑/ID）
- Method（GET/POST）
- 常用 API（分類清單）或自訂輸入
- 參數總覽（哪些必填）
- Query Params(JSON)
- Request Body(JSON)
- 送出請求與結果 JSON

### 5.2 GET 與 POST 的填寫原則

- GET：主要填 Query Params（JSON）
- POST：主要填 Request Body（JSON）

兩者都可能會用到：

- 地圖名稱（map_name）
- SN 碼（sn）
- 門市 ID（shop_id）
- 時間欄位（start_time/end_time，支援日期字串，會自動轉時間戳）

補充：

- 「取得機器列表」與「取得地圖列表」若要填 shop_id，請先到設定頁查看商店的 Pudu Shop ID。
- 「取得組狀態（按 Group ID）」回傳的 sn 常是 MAC 格式（例如 00:9C:17:25:7F:ED），不是一般機器序列號字串。
- 「取得地圖詳情 V2」的 map_name，請到設定頁的地圖分頁複製（或用 API 測試頁快速帶入），避免手打錯字。
- 切換地圖前，機器人要先停在地圖對位點（同一固定參考點）再切換，不然切圖後機器人點位會偏移。

### 5.3 推薦做法

1. 先用「常用 API」選一支接近的
2. 看參數總覽補齊必填欄位
3. 用「快速帶入」把 shop_id/sn/map_name 帶進去
4. 送出請求
5. 直到回應成功（HTTP 2xx 且回應內容正確）

### 5.4 常用特殊規則速查

以下是這個系統裡最常用、也最容易搞混的規則。

#### A. 取得組狀態 V1 / V2

- 取得組狀態 V1：比較常拿來看多臺機器人的位置資訊
- 取得組狀態 V2：除了狀態外，通常會多看到充電相關類型資訊
- V1 的設備名稱回傳常只看到 MAC 值
- V2 通常可看到 MAC 與 SN
- 在這個網站裡，查組狀態時可以直接輸入群組名稱，不一定要自己找 group_id
- 若輸入的是本地群組名稱，例如「清潔機器人」或「運送機器人」，系統會自動找出群組內機器人再查詢

#### B. 取得機器狀態 V1 / V2

- 取得機器狀態 V1：比較常拿來看位置與基本狀態
- 取得機器狀態 V2：通常會比 V1 多一些充電類型或充電狀態相關資訊
- 若你只想先確認機器在線、位置是否正常，通常先測 V1 就夠用
- 若你要看更完整狀態，尤其是充電相關欄位，再看 V2

#### C. start_time / end_time 規則

- 很多 API 的 `start_time` / `end_time` 最終都要送成 integer 秒級時間戳
- 這個網站支援你直接輸入日期字串，例如 `2026/03/01`、`2026-03-01`、`2026/03/01 10:30:00`
- 系統送出前會自動轉成秒級時間戳
- `start_time` 會自動轉成當天 `00:00:00`
- `end_time` 會自動轉成當天 `23:59:59`
- 若 API 文件明確要求 integer，看到畫面是日期字串不用緊張，送出時系統會幫你轉

#### D. map_name 規則

- `map_name` 不要手打猜測，最好從設定頁的地圖分頁複製
- `map_name` 只要差一個字、井字號 `#`、大小寫或特殊符號，就可能查不到資料
- 切換地圖前，機器人最好先停在地圖對位點，不然切圖後位置可能偏掉

#### E. 群組名稱與 group_id 規則

- 在本網站中，很多群組查詢可以直接填群組名稱
- 若 Pudu 雲端 group API 查不到，但你本地群組存在，系統會自動 fallback 成「用群組成員 SN 一臺一臺查」
- 如果畫面出現本地群組查詢提示，代表系統是用你設定頁的群組成員在查，不是壞掉
- 如果群組裡沒有任何成員，fallback 也查不到資料

#### F. 取得語音列表規則

- 取得語音列表只支援 Kettybot
- 若回應 `CLOUD_OPEN_TIMEOUT`，通常不是你欄位填錯，而是雲端暫時連不到機器
- 此時請先查該 SN 的機器狀態，確認是否在線
- 若機器離線、關機，語音列表通常一定失敗

#### G. 地圖相關 API 規則

- 取得地圖點位列表目前以 `sn` 為主，並可搭配 `limit`、`offset`
- 取得點位分組目前使用 `sn` 與 `map_name`
- 若地圖 API 有資料但地圖預覽沒有看到機器人，常見原因是機器人回報的 `map_name` 跟你目前選的地圖不同

---

## 6. 你的標準操作流程（API 測試 → 範本 → 按鈕）

以下就是你指定的完整流程，照做即可。

### 步驟 A：在 API 測試找出可用 API

1. 到「API 測試」頁
2. 搜尋或選擇你要的 API
3. 根據 Method 填參數：
   - GET 填 Query Params（JSON）
   - POST 填 Request Body（JSON）
4. 常見欄位要填正確：地圖名稱、SN、門市 ID、時間
5. 按「送出請求」直到成功

### 步驟 B：複製成功請求內容

成功後，從畫面保留以下內容：

- Method
- Path
- Query Params JSON（若為 GET）
- Request Body JSON（若為 POST）

建議：先把這些內容暫存到記事本，避免切頁後忘記。

### 步驟 C：到設定頁新增動作範本

1. 到「設定」頁 →「動作範本」
2. 按「新增動作範本」
3. 填寫：
   - 名稱（好辨識）
   - Method（跟測試成功的一致）
   - Path（貼上成功 Path）
   - Query Template JSON 或 Body Template JSON（貼上成功 JSON）
4. 按「新增」

### 步驟 D：到設定頁按鈕綁定範本

1. 到「設定」頁 →「按鈕」
2. 新增按鈕，輸入名稱
3. 在「綁定動作範本」選你剛建的範本（可多選）
4. 按「新增」

### 步驟 E：到操作頁執行

1. 到「操作」頁
2. 勾選這次要執行的機器人
3. 按你剛建立的按鈕
4. 確認回應結果（HTTP 與 JSON）

完成後，這顆按鈕就可以重複使用。

---

## 7. 範例：一個 GET 和一個 POST

### 7.1 GET 範例（查狀態）

- Method: `GET`
- Path: `/open-platform-service/v2/status/get_by_sn`
- Query Params(JSON) 例如：

```json
{
  "sn": "PDxxxxxxxx"
}
```

- Body：留空 `{}`（GET 通常不用）

### 7.2 POST 範例（切換地圖）

- Method: `POST`
- Path: `/open-platform-service/v1/switch_map`
- Query Params(JSON)：通常 `{}`
- Body(JSON) 例如：

```json
{
  "sn": "PDxxxxxxxx",
  "map_info": {
    "map_name": "1#1#內湖展間v20"
  }
}
```

切換地圖注意事項：

- map_name 請從設定頁地圖分頁取得，不要自行猜測名稱。
- 送切換前，請讓機器人先在地圖的對位點再切換，避免切換後點位跑掉。

---

## 8. 常見錯誤與排除

### 8.1 API 回應失敗

優先檢查：

- shop_id 是否正確
- sn 是否正確
- map_name 是否完全一致（含符號）
- GET/POST 是否選錯

### 8.2 JSON 解析失敗

常見原因：

- 少逗號或多逗號
- 單引號寫成 JSON（請用雙引號）
- 大括號不成對

### 8.3 按鈕按了沒效果

檢查：

- 該按鈕是否有綁動作範本
- 動作範本是否啟用
- 目標機器人是否勾選且啟用

### 8.4 地圖載不出來

檢查：

- 設定頁的 Pudu Shop ID
- 地圖名稱 map_name 是否匹配
- 操作頁「地圖 API 除錯紀錄」是否有錯誤訊息

---

## 9. 新人上手最短路徑（5 分鐘）

1. 登入系統
2. 設定頁確認商店的 shop_id
3. 機器人分頁確認 SN 已匯入且啟用
4. API 測試頁測一支成功 API
5. 把成功請求存成動作範本
6. 建立按鈕並綁範本
7. 到操作頁按按鈕測一次

提醒：若你在「取得組狀態」看到 sn 長得像 00:9C:17:25:7F:ED，屬於正常格式。

做到這裡，就完成一個可重複執行的工作按鈕。


---

# 附錄B：PYTHON API/API_特殊需求說明.md（完整併入）

# API 特殊需求說明（網站內與官方直打差異）

本文件只講 API 相關的特殊規則，避免和一般操作手冊混在一起。

## 1. 先看這句話

在本網站的 API 測試頁，部分 API 有「本地兼容」邏輯。
離開網站（例如 Postman、curl、你自己的程式）直接打 Pudu 官方 API 時，這些本地兼容不會存在。

## 2. 群組相關最重要規則

### 2.1 在網站內打 API（本專案的 API 測試頁）

1. 查組狀態時可直接輸入群組名稱，例如「清潔機器人」、「運送機器人」。
2. 若 Pudu 雲端 group_id 查不到，系統會自動 fallback 成本地群組成員 SN 逐臺查詢。
3. `取得機器人組列表` 會顯示官方群組，也會補上本地群組（本地資料會標記 `source=local_showroom`）。
4. `按組或設備類型列表機器` 可接受本地群組名稱或本地群組 ID，並回傳本地成員清單。

### 2.2 不用網站，直接打官方 API（Postman/curl/自寫程式）

1. 不能直接用本地群組名稱。
2. 不能保證本地群組 ID 可用。
3. 必須先查官方群組，拿到官方 group_id。

標準流程：

1. 打 `GET /open-platform-service/v1/robot/group/list`（帶 `shop_id`）
2. 從回應 `data` 找到目標群組的 `group_id`
3. 再打組狀態 API（V1/V2）或按組查機器 API，使用該官方 `group_id`

## 3. 組狀態 V1 / V2 差異

1. V1 常用來看多機器位置資訊。
2. V2 通常會多充電相關類型資訊。
3. V1 的設備名稱常只看到 MAC 值。
4. V2 通常可看到 MAC 與 SN。

## 4. 機器狀態 V1 / V2 差異

1. V1 比較偏基本狀態與位置。
2. V2 通常有較完整狀態欄位（含充電類型相關）。

## 5. 機器回充 V1 / V2 規則

1. 回充 V1 路徑是 `GET /open-platform-service/v1/recharge`，參數是 `sn`。
2. 回充 V2 路徑是 `GET /open-platform-service/v2/recharge`，參數也是 `sn`。
3. 本專案目前定義：
	1. `recharge_v1` 主要給 `PuduBot2`
	2. `recharge_v2` 主要給 `FlashBot 2025 / FlashBot Pro / FlashBot Max / FlashBot Ultra / PuduT300`
4. 若是 PuduBot2，優先使用 V1；V2 可能不適用。
5. 若回充失敗，先查 `取得機器狀態 V1/V2`，確認機器是否在線、是否已在充電中、或是否處於不可接收命令的任務狀態。

## 6. 時間欄位規則（start_time / end_time）

1. 最終都要送 integer 秒級時間戳。
2. 本網站支援輸入日期字串，送出前會自動轉秒級時間戳。
3. `start_time` 會轉當天 `00:00:00`。
4. `end_time` 會轉當天 `23:59:59`。
5. 離開網站自行打 API 時，你要自己處理時間戳轉換。

## 7. 地圖欄位規則（map_name）

1. `map_name` 必須完全一致，包含 `#`、大小寫與特殊字元。
2. 最好從地圖分頁複製，不要手打猜。

## 8. 語音列表規則

1. `取得語音列表` 僅支援 Kettybot。
2. 若回 `CLOUD_OPEN_TIMEOUT`，通常是雲端連機器逾時，不是參數語法錯。
3. 先查該 SN 的機器狀態（在線/離線/關機）再判斷。

## 9. 常見誤解對照

1. 「我在網站輸入群組名稱可以成功，所以官方 API 也支援群組名稱」：不一定。
2. 「本地有 3 組，官方只回 1 組，是 API 壞掉」：不是，資料來源不同。
3. 「本地群組新增後，官方一定看得到」：不會自動同步，需在官方端建立或做同步機制。

## 10. 建議你固定用的做法

1. 在網站內操作時：可用群組名稱，速度快。
2. 對外部系統串接時：一律先拿官方 `group_id` 再打組 API。
3. 文件與實作分開維護：網站兼容規則寫在本文件，避免和官方文件混淆。
