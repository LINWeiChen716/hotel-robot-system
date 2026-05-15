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

## 1.5) 部署到 Streamlit Cloud

這個專案可以直接部署到 Streamlit Cloud，最適合目前這種 Streamlit 網頁。

1. 確認 GitHub repo 是公開的，或已授權 Streamlit Cloud 存取。
2. 到 https://share.streamlit.io/ 登入。
3. 點 `New app`，選你的 GitHub repo：`LINWeiChen716/hotel-robot-system`。
4. Main file path 填 `app.py`。
5. Deploy。
6. 在 Streamlit Cloud 的 `Settings` / `Secrets` 貼上：
	```toml
	SHOWROOM_ACCESS_PIN="你的 PIN"
	SUPABASE_URL="你的 Supabase URL"
	SUPABASE_SERVICE_ROLE_KEY="你的 Supabase service role key"
	PUDU_BASE_URL="你的 Pudu API base URL"
	PUDU_APP_KEY="你的 App Key"
	PUDU_APP_SECRET="你的 App Secret"
	```

本機開發時，你可以把 `.env.example` 複製成 `.env`；上線時則用 Streamlit Cloud 的 Secrets，不要把真實金鑰提交進 Git。

如果你想先測試，本機啟動指令維持不變。

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
- 上線後請務必把 `.env`、`.streamlit/secrets.toml` 這類敏感檔排除在 Git 之外。

## 5) Streamlit Cloud Secrets 範本

可參考 [\.streamlit/secrets.toml.example](.streamlit/secrets.toml.example) 的格式建立自己的 Secrets。
