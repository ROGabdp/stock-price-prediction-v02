@echo off
echo ========================================
echo 股價漲跌機率預測系統 - 啟動腳本
echo ========================================
echo.

echo [1/4] 檢查虛擬環境...
if not exist "venv\" (
    echo 虛擬環境不存在，正在建立...
    python -m venv venv
    call venv\Scripts\activate
    echo 安裝依賴套件...
    pip install -r requirements.txt
) else (
    echo 虛擬環境已存在
    call venv\Scripts\activate
)

echo.
echo [2/4] 建立必要目錄...
if not exist "data\processed_data\" mkdir data\processed_data
if not exist "data\uploads\" mkdir data\uploads
if not exist "models\saved_models\" mkdir models\saved_models
if not exist "models\metadata\" mkdir models\metadata
if not exist "logs\" mkdir logs

echo.
echo [3/4] 複製測試資料...
if exist "19940513-20251111.csv" (
    if not exist "data\processed_data\19940513-20251111.csv" (
        copy "19940513-20251111.csv" "data\processed_data\" > nul
        echo 測試資料已複製
    ) else (
        echo 測試資料已存在
    )
)

echo.
echo [4/4] 啟動服務...
echo.
echo ========================================
echo 請選擇要啟動的服務：
echo ========================================
echo 1. 啟動 Flask 後端 API
echo 2. 啟動 Dash 前端介面
echo 3. 執行測試
echo 4. 退出
echo ========================================
echo.

set /p choice="請輸入選項 (1-4): "

if "%choice%"=="1" (
    echo.
    echo 正在啟動 Flask 後端 API...
    echo 訪問地址: http://localhost:5000
    echo 按 Ctrl+C 停止服務
    echo.
    python src\app.py
) else if "%choice%"=="2" (
    echo.
    echo 正在啟動 Dash 前端介面...
    echo 訪問地址: http://localhost:8050
    echo 按 Ctrl+C 停止服務
    echo.
    python src\ui\dashboard.py
) else if "%choice%"=="3" (
    echo.
    echo 正在執行測試...
    pytest tests\ -v
    echo.
    pause
) else if "%choice%"=="4" (
    echo 退出
) else (
    echo 無效的選項
    pause
)
