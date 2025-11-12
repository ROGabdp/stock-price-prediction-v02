# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概述

這是一個股價漲跌機率預測系統，使用機器學習模型從歷史資料中學習，並預測未來 N 天（1-30天）的股價漲跌機率與幅度。系統採用 Python 技術棧，提供 Web 介面進行模型訓練、管理和預測結果視覺化。

**技術棧**: Python 3.12, TensorFlow/Keras, Flask, Dash, Plotly, Pandas

## 專案章程 (Constitution)

本專案遵循以下核心原則（詳見 `.specify/memory/constitution.md`）：

1. **高品質 (High Quality)**: 程式碼須遵循專案慣例，清晰、高效且易於維護
2. **可被測試 (Testable)**: 所有功能變更或錯誤修復都必須伴隨測試案例
3. **最小可行產品 (MVP)**: 專注於核心功能，快速交付可用產品
4. **避免過度設計 (Avoid Over-design)**: 遵循 YAGNI 原則，設計應恰如其分
5. **使用正體中文**: 所有使用者溝通內容、註解及文件必須使用正體中文

## 常用指令

### 環境設定

```bash
# 建立並啟用虛擬環境 (Windows)
python -m venv venv
.\venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt
```

### 開發與執行

```bash
# 啟動 Flask 後端應用
python src/app.py

# 執行所有測試
pytest tests/

# 執行單元測試
pytest tests/unit/

# 執行整合測試
pytest tests/integration/

# 執行特定測試檔案
pytest tests/unit/test_trainer.py

# 執行特定測試並顯示詳細輸出
pytest tests/unit/test_trainer.py -v

# 程式碼格式檢查
flake8 src/ tests/

# 程式碼格式化
black src/ tests/
```

## 專案架構

### 目錄結構

```
src/
├── data/                # 資料處理模組（載入、預處理）
│   └── preprocessor.py  # 資料預處理邏輯
├── models/              # 機器學習模型定義與訓練
│   ├── trainer.py       # 模型訓練邏輯（含超參數調整）
│   └── predictor.py     # 模型預測邏輯
├── services/            # 業務邏輯層
│   ├── data_service.py  # 資料管理服務
│   └── model_service.py # 模型管理與預測服務
├── ui/                  # 使用者介面
│   └── dashboard.py     # Dash 介面
├── utils/               # 通用工具
│   ├── data_loader.py       # 資料載入工具
│   ├── model_manager.py     # 模型檔案管理
│   └── metadata_manager.py  # 模型元資料管理
└── app.py               # Flask 應用程式入口

tests/
├── unit/                # 單元測試
├── integration/         # 整合測試
└── e2e/                 # 端到端測試

specs/1-stock-price-prediction/  # 功能規格文件
├── plan.md              # 實作計畫
├── data-model.md        # 資料模型定義
├── quickstart.md        # 快速入門指南
└── contracts/
    └── api_contracts.md # API 端點定義
```

### 核心元件說明

#### 1. 資料流程
- **DataLoader**: 從檔案系統載入 CSV 格式的歷史股價資料
- **DataPreprocessor**: 處理 CSV 中文欄位名稱、技術指標、缺失值（刪除整行）
- **DataService**: 提供資料管理的業務邏輯介面

#### 2. 模型訓練流程
- **ModelTrainer**:
  - 建構 LSTM 神經網路模型
  - 執行自動超參數調整（目前為模擬實作，實際專案應整合 Keras Tuner）
  - 訓練並評估模型
- **ModelService**: 協調訓練流程、儲存模型和元資料

#### 3. 儲存機制
- **模型檔案**: 儲存在檔案系統（.h5 格式）
- **模型元資料**: JSON 檔案，包含訓練日期、效能指標、超參數設定等
- **歷史資料**: CSV 檔案

#### 4. API 架構
Flask 後端提供以下主要端點（詳見 `specs/1-stock-price-prediction/contracts/api_contracts.md`）：
- `GET /api/data/history`: 取得歷史股價資料
- `POST /api/model/train`: 啟動模型訓練
- `GET /api/model/train/status/<task_id>`: 取得訓練狀態
- `GET /api/model/list`: 取得已訓練模型列表
- `GET /api/model/predict`: 取得模型預測結果
- `POST /api/data/upload`: 上傳新的歷史資料

## 資料模型

### 歷史資料 (Historical Data)
- 日期、開盤價、最高價、最低價、收盤價、成交量
- 可包含額外技術指標（SMA, MACD 等）
- CSV 格式，支援中文欄位名稱

### 預測模型 (Prediction Model)
- 模型 ID (UUID)、檔案路徑、訓練日期
- 訓練資料集名稱、效能指標（loss, mae 等）
- 超參數設定（learning_rate, lstm_units, dropout_rate, epochs, batch_size）

### 預測結果 (Prediction Result)
- 預測日期、目標日期
- 漲跌機率（0-1 範圍）
- 漲跌幅度（百分比）

## 開發注意事項

### 模型訓練
- 預測天數範圍: 1-30 天
- 使用 LSTM 網路進行時間序列預測
- look_back 參數: 使用過去 N 天的資料作為輸入特徵
- 輸出: 未來 n_days 的收盤價或漲跌機率

### 測試策略
- 使用 pytest 作為測試框架
- 使用 unittest.mock 模擬外部依賴（如 Keras 模型）
- 所有測試檔案需加入 `sys.path.insert(0, ...)` 以正確導入 src/ 模組
- 整合測試應覆蓋完整的 API 端點

### 效能目標
- 上傳資料到顯示預測結果: < 5 分鐘（不含模型訓練）
- 切換已訓練模型更新預測: < 3 秒
- 自動參數調整與訓練: < 30 分鐘

### Git 分支策略
- 主要開發分支: `1-stock-price-prediction`
- 遵循功能分支工作流程

## 相關文件

- **專案章程**: `.specify/memory/constitution.md`
- **實作計畫**: `specs/1-stock-price-prediction/plan.md`
- **資料模型**: `specs/1-stock-price-prediction/data-model.md`
- **API 規格**: `specs/1-stock-price-prediction/contracts/api_contracts.md`
- **快速入門**: `specs/1-stock-price-prediction/quickstart.md`
