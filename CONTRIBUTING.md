# 貢獻指南

感謝您對股價漲跌機率預測系統的興趣！本文件提供貢獻本專案的指引。

## 開發流程

### 1. Fork 和 Clone

```bash
# Fork 這個專案到您的 GitHub 帳號
# 然後 clone 您的 fork
git clone https://github.com/YOUR_USERNAME/stock-price-prediction-v02.git
cd stock-price-prediction-v02
```

### 2. 設定開發環境

```bash
# 建立虛擬環境
python -m venv venv

# 啟用虛擬環境
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt
```

### 3. 建立功能分支

```bash
git checkout -b feature/your-feature-name
```

### 4. 進行開發

- 遵循專案的程式碼風格
- 撰寫清晰的註解（使用正體中文）
- 確保所有測試通過
- 為新功能撰寫測試

### 5. 提交變更

```bash
git add .
git commit -m "描述您的變更"
git push origin feature/your-feature-name
```

### 6. 建立 Pull Request

在 GitHub 上建立 Pull Request，並描述您的變更。

## 程式碼風格

### Python 風格指南

- 遵循 PEP 8 風格指南
- 使用 4 個空格進行縮排
- 行長度限制為 100 字元
- 使用有意義的變數名稱

### 註解規範

- 所有公開的類別、函數和方法都應該有 docstring
- 使用正體中文撰寫註解
- docstring 格式：

```python
def function_name(param1: type1, param2: type2) -> return_type:
    """
    函數的簡短描述
    :param param1: 參數1的說明
    :param param2: 參數2的說明
    :return: 返回值的說明
    """
    pass
```

### 程式碼檢查

在提交前執行以下檢查：

```bash
# 格式檢查
flake8 src/ tests/

# 格式化
black src/ tests/

# 執行測試
pytest tests/
```

## 測試規範

### 撰寫測試

- 所有新功能都必須有對應的測試
- 測試檔案放在 `tests/` 目錄下
- 測試檔案命名格式：`test_<module_name>.py`
- 測試函數命名格式：`test_<function_description>`

### 測試類型

1. **單元測試** (`tests/unit/`): 測試單一函數或類別
2. **整合測試** (`tests/integration/`): 測試多個元件的互動
3. **端對端測試** (`tests/e2e/`): 測試完整的使用者流程

### 執行測試

```bash
# 執行所有測試
pytest tests/

# 執行特定測試
pytest tests/unit/test_trainer.py

# 執行測試並顯示覆蓋率
pytest tests/ --cov=src
```

## 提交訊息規範

使用清晰且有意義的提交訊息：

```
<類型>: <簡短描述>

<詳細描述（可選）>

<相關 issue 編號（可選）>
```

### 類型

- `feat`: 新功能
- `fix`: 錯誤修復
- `docs`: 文件變更
- `style`: 程式碼格式調整（不影響功能）
- `refactor`: 重構
- `test`: 測試相關
- `chore`: 其他維護工作

### 範例

```
feat: 新增模型自動保存功能

- 在訓練完成後自動保存模型
- 記錄訓練時間和效能指標

Closes #123
```

## 專案章程

本專案遵循以下核心原則，請確保您的貢獻符合這些原則：

1. **高品質**: 程式碼清晰、高效且易於維護
2. **可被測試**: 所有功能都有對應的測試案例
3. **最小可行產品**: 專注於核心功能
4. **避免過度設計**: 遵循 YAGNI 原則
5. **使用正體中文**: 所有使用者介面和文件使用正體中文

## 問題回報

### 回報錯誤

如果您發現錯誤，請在 GitHub Issues 中建立新的 issue，並包含：

1. 錯誤描述
2. 重現步驟
3. 預期行為
4. 實際行為
5. 環境資訊（作業系統、Python 版本等）
6. 錯誤訊息或截圖

### 功能請求

如果您有新功能建議，請在 GitHub Issues 中建立新的 issue，並包含：

1. 功能描述
2. 使用案例
3. 預期效益
4. 可能的實作方式（可選）

## 程式碼審查

所有 Pull Request 都會經過程式碼審查。審查者會檢查：

- 程式碼品質和風格
- 測試覆蓋率
- 文件完整性
- 是否符合專案章程
- 效能影響

請耐心等待審查，並根據回饋進行必要的調整。

## 資源

- [專案 README](README.md)
- [專案章程](.specify/memory/constitution.md)
- [API 規格](specs/1-stock-price-prediction/contracts/api_contracts.md)
- [資料模型](specs/1-stock-price-prediction/data-model.md)

## 聯絡方式

如有任何問題，歡迎：

- 在 GitHub Issues 中提問
- [在此添加其他聯絡方式]

感謝您的貢獻！
