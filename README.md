# PYTHON API

Python 版 Pudu API 網頁控制檯，分成三個功能區：
- 設定
- 操作
- API

## 使用說明書（推薦先看）

- 完整新手手冊：`使用說明書.md`

## 1) 安裝

在 Windows PowerShell 於專案目錄執行：

```powershell
Set-Location "d:\SynologyDrive\桌面\PYTHON API"
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2) 啟動

```powershell
Set-Location "d:\SynologyDrive\桌面\PYTHON API"
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py --server.port 8501 --server.address 127.0.0.1
```

開啟網址：`http://127.0.0.1:8501/`

若打不開，請先看完整排查流程：`使用說明書.md` 的「2.4 如果打不開網頁，請照這組排查指令」。

## 3) 功能說明

- 設定：填寫 Base URL、ApiAppKey、ApiAppSecret、shop_id、map_name。
- 操作：內建「取得地圖詳情V2」與「健康檢查」。
- API：可自訂 Method、Path、Query、Body，使用同一套 HMAC 簽名送出。

## 4) 注意事項

- map_name 若有中文或 # 等特殊字元，程式會自動 URL encode。
- GET 請求不帶 body；POST/PUT/PATCH/DELETE 會自動處理 JSON body 與 Content-MD5。
- 若回應為 MAP_ROBOT_ERROR，通常是 shop_id / map_name 與機器實際資料不一致。
