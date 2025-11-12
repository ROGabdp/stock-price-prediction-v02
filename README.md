# 股價漲跌機率預測系統

一個基於機器學習的股價預測系統，使用 LSTM 神經網路模型從歷史資料中學習，並預測未來 1-30 天的股價漲跌機率與幅度。

## 專案特色

- 🤖 **自動超參數調整**: 系統會自動尋找最佳的模型參數
- 📊 **視覺化圖表**: 使用 Plotly 提供互動式的歷史與預測圖表
- 🎯 **多模型管理**: 可儲存和比較多個訓練好的模型
- 📁 **彈性資料管理**: 支援上傳和選擇多個歷史資料集
- 🔄 **即時預測**: 模型切換後在 3 秒內更新預測結果

## 技術架構

### 後端
- **語言**: Python 3.12
- **框架**: Flask (Web API)
- **機器學習**: TensorFlow/Keras
- **資料處理**: Pandas, NumPy

### 前端
- **框架**: Dash (基於 Flask 和 React)
- **視覺化**: Plotly
- **樣式**: Bootstrap (dash-bootstrap-components)

### 儲存
- **模型檔案**: HDF5 格式 (.h5)
- **歷史資料**: CSV 檔案
- **模型元資料**: JSON 檔案

## 系統需求

- Python 3.12 或以上
- 4GB RAM 以上（建議 8GB）
- 2GB 可用磁碟空間

## 安裝步驟

### 1. 複製專案

```bash
git clone <repository-url>
cd stock-price-prediction-v02
```

### 2. 建立虛擬環境

#### Windows
```bash
python -m venv venv
.\venv\Scripts\activate
```

#### macOS/Linux
```bash
python -m venv venv
source venv/bin/activate
```

### 3. 安裝依賴套件

```bash
pip install -r requirements.txt
```

## 使用方法

### 啟動後端服務

```bash
python src/app.py
```

後端服務將在 `http://localhost:5000` 啟動。

### 啟動前端介面

開啟另一個終端視窗：

```bash
python src/ui/dashboard.py
```

前端介面將在 `http://localhost:8050` 啟動。

在瀏覽器中開啟 `http://localhost:8050` 即可使用系統。

## 使用流程

### 1. 上傳或選擇資料集

- 點擊「拖曳或選擇檔案」區域上傳 CSV 格式的歷史股價資料
- 或從下拉選單中選擇已上傳的資料集

**CSV 檔案格式要求**:
- 必須包含 `date` 和 `close` 欄位
- 支援額外的技術指標欄位（如 SMA, MACD 等）
- 缺失值（N/A）的資料行將被自動刪除

範例 CSV 格式:
```csv
date,open,high,low,close,volume
2025-01-01,100.0,105.0,98.0,103.0,1000000
2025-01-02,103.0,107.0,101.0,106.0,1200000
```

### 2. 訓練模型

1. 選擇資料集
2. 設定預測天數 N（1-30 天）
3. 點擊「開始訓練模型」按鈕
4. 系統將自動調整參數並訓練模型（可能需要數分鐘）

### 3. 查看預測結果

1. 從模型下拉選單選擇已訓練的模型
2. 點擊「顯示預測」按鈕
3. 系統將顯示:
   - 歷史股價圖表
   - 結合歷史與預測的綜合圖表
   - 預測結果圖表（漲跌機率和幅度）

### 4. 比較不同模型

可以選擇不同的模型來比較預測結果，系統會保留所有訓練過的模型記錄。

## API 端點

### 資料管理
- `POST /api/data/upload` - 上傳新的歷史資料
- `GET /api/data/history?dataset_name=<name>` - 取得歷史資料

### 模型訓練
- `POST /api/model/train` - 啟動模型訓練
- `GET /api/model/train/status/<task_id>` - 查詢訓練狀態

### 模型管理與預測
- `GET /api/model/list` - 取得已訓練模型列表
- `GET /api/model/predict?model_id=<id>&n_days=<n>` - 取得預測結果

詳細的 API 規格請參考 `specs/1-stock-price-prediction/contracts/api_contracts.md`

## 測試

### 執行所有測試

```bash
pytest tests/
```

### 執行特定類型的測試

```bash
# 單元測試
pytest tests/unit/

# 整合測試
pytest tests/integration/

# 端對端測試
pytest tests/e2e/
```

### 執行特定測試檔案

```bash
pytest tests/unit/test_trainer.py -v
```

## 開發工具

### 程式碼格式檢查

```bash
flake8 src/ tests/
```

### 程式碼格式化

```bash
black src/ tests/
```

## 專案結構

```
stock-price-prediction-v02/
├── src/                    # 原始碼
│   ├── app.py             # Flask 應用程式入口
│   ├── data/              # 資料處理模組
│   ├── models/            # 機器學習模型
│   ├── services/          # 業務邏輯層
│   ├── ui/                # 使用者介面
│   └── utils/             # 通用工具
├── tests/                 # 測試
│   ├── unit/             # 單元測試
│   ├── integration/      # 整合測試
│   └── e2e/              # 端對端測試
├── specs/                # 功能規格文件
├── data/                 # 資料目錄
│   ├── uploads/         # 上傳的原始資料
│   └── processed_data/  # 處理後的資料
├── models/              # 模型儲存目錄
│   ├── saved_models/   # 訓練好的模型檔案
│   └── metadata/       # 模型元資料
├── logs/                # 日誌檔案
├── requirements.txt     # Python 依賴套件
├── CLAUDE.md           # Claude Code 指引文件
└── README.md           # 本檔案
```

## 效能指標

- **資料上傳到顯示預測**: < 5 分鐘（不含模型訓練時間）
- **模型切換更新時間**: < 3 秒
- **自動參數調整與訓練**: < 30 分鐘

## 注意事項

### 資料品質
- 建議使用至少 100 個資料點進行訓練
- 資料應按日期順序排列
- 確保資料中沒有異常值或錯誤

### 模型訓練
- 訓練時間取決於資料量和硬體效能
- 建議在訓練期間不要關閉瀏覽器
- 模型檔案可能較大，請確保有足夠的磁碟空間

### 預測準確性
- 機器學習模型的預測結果僅供參考
- 股市具有高度不確定性，預測結果不保證準確
- 建議結合其他分析方法進行決策

## 疑難排解

### 問題：pip install 失敗
- 嘗試更新 pip: `python -m pip install --upgrade pip`
- 確認 Python 版本為 3.12 或以上

### 問題：TensorFlow 安裝錯誤
- Windows 使用者可能需要安裝 Visual C++ 可轉散發套件
- 參考 TensorFlow 官方安裝指南

### 問題：模型訓練失敗
- 檢查資料格式是否正確
- 確認資料量是否足夠（建議 > 100 筆）
- 查看日誌檔案以了解詳細錯誤資訊

### 問題：圖表無法顯示
- 清除瀏覽器快取
- 確認 Flask 後端服務正在執行
- 檢查瀏覽器控制台是否有錯誤訊息

## 專案章程

本專案遵循以下核心原則：

1. **高品質**: 程式碼清晰、高效且易於維護
2. **可被測試**: 所有功能都有對應的測試案例
3. **最小可行產品**: 專注於核心功能
4. **避免過度設計**: 遵循 YAGNI 原則
5. **使用正體中文**: 所有使用者介面和文件使用正體中文

詳見 `.specify/memory/constitution.md`

## 授權

[在此添加授權資訊]

## 聯絡方式

如有問題或建議，請聯繫 [在此添加聯絡資訊]

## 更新日誌

### v1.0.0 (2025-11-12)
- 初始版本發布
- 實作基本的模型訓練與預測功能
- 實作視覺化圖表
- 實作模型與資料選擇功能
