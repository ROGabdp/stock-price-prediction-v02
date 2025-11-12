@echo off
echo ========================================
echo 股價漲跌機率預測系統 - 全部啟動
echo ========================================
echo.

call venv\Scripts\activate

echo 啟動 Flask 後端 API (背景執行)...
start "Flask API" cmd /k "venv\Scripts\activate && python src\app.py"

timeout /t 3 /nobreak > nul

echo 啟動 Dash 前端介面 (背景執行)...
start "Dash UI" cmd /k "venv\Scripts\activate && python src\ui\dashboard.py"

timeout /t 3 /nobreak > nul

echo.
echo ========================================
echo 系統已啟動！
echo ========================================
echo Flask 後端: http://localhost:5000
echo Dash 前端: http://localhost:8050
echo ========================================
echo.
echo 請在瀏覽器中開啟: http://localhost:8050
echo.
echo 按任意鍵開啟瀏覽器...
pause > nul

start http://localhost:8050
