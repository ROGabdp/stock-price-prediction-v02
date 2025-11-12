# API 合約：股價漲跌機率預測系統

**功能分支**: `1-stock-price-prediction`  
**日期**: 2025-11-12
**規格書**: [../../spec.md](../../spec.md)
**計畫**: [../../plan.md](../../plan.md)

## API 端點定義

本文件定義了 Flask 後端將提供的 API 端點，供 Dash 前端應用程式使用。

### 1. 取得歷史股價資料

- **端點**: `/api/data/history`
- **方法**: `GET`
- **描述**: 根據指定的資料集名稱，取得歷史股價資料。
- **查詢參數**:
    - `dataset_name` (string, **必要**): 要取得的資料集名稱。
- **回應 (成功: 200 OK)**:
    ```json
    [
        {
            "date": "YYYY-MM-DD",
            "open": 100.0,
            "high": 105.0,
            "low": 98.0,
            "close": 103.0,
            "volume": 1000000
        },
        // ... 更多歷史數據
    ]
    ```
- **回應 (錯誤: 404 Not Found)**:
    ```json
    {"error": "Dataset not found"}
    ```

### 2. 啟動模型訓練

- **端點**: `/api/model/train`
- **方法**: `POST`
- **描述**: 使用指定的資料集和預測天數 N 啟動模型訓練，並自動進行參數調整。
- **請求主體**:
    ```json
    {
        "dataset_name": "string",  // 必要，用於訓練的資料集名稱
        "n_days": 5                // 必要，預測未來的天數 (1-30)
    }
    ```
- **回應 (成功: 202 Accepted)**:
    ```json
    {"message": "Model training started", "task_id": "uuid-of-training-task"}
    ```
- **回應 (錯誤: 400 Bad Request)**:
    ```json
    {"error": "Invalid input or training already in progress"}
    ```

### 3. 取得訓練任務狀態

- **端點**: `/api/model/train/status/<task_id>`
- **方法**: `GET`
- **描述**: 取得指定訓練任務的當前狀態。
- **路徑參數**:
    - `task_id` (string, **必要**): 訓練任務的唯一識別符。
- **回應 (成功: 200 OK)**:
    ```json
    {
        "task_id": "uuid-of-training-task",
        "status": "pending" | "running" | "completed" | "failed",
        "progress": 0.75, // 0.0 - 1.0
        "message": "Training model X with parameters Y...",
        "model_id": "uuid-of-trained-model" // 僅在 completed 時存在
    }
    ```
- **回應 (錯誤: 404 Not Found)**:
    ```json
    {"error": "Task not found"}
    ```

### 4. 取得已訓練模型列表

- **端點**: `/api/model/list`
- **方法**: `GET`
- **描述**: 取得所有已訓練模型的元資料列表。
- **回應 (成功: 200 OK)**:
    ```json
    [
        {
            "model_id": "uuid-of-model-1",
            "model_name": "Model_20251112_01",
            "training_date": "2025-11-12",
            "performance_metrics": {"loss": 0.01, "accuracy": 0.95},
            "dataset_name": "stock_data_a.csv"
        },
        // ... 更多模型元資料
    ]
    ```

### 5. 取得模型預測結果

- **端點**: `/api/model/predict`
- **方法**: `GET`
- **描述**: 使用指定的模型 ID 取得未來 N 天的預測結果。
- **查詢參數**:
    - `model_id` (string, **必要**): 要使用的模型 ID。
    - `n_days` (integer, **必要**): 預測未來的天數 (1-30)。
- **回應 (成功: 200 OK)**:
    ```json
    [
        {
            "target_date": "YYYY-MM-DD",
            "up_down_probability": 0.6, // 漲跌機率
            "change_magnitude": 0.015   // 漲跌幅度 (例如 0.015 代表 +1.5%)
        },
        // ... 更多預測結果
    ]
    ```
- **回應 (錯誤: 404 Not Found)**:
    ```json
    {"error": "Model not found"}
    ```

### 6. 上傳新的歷史資料

- **端點**: `/api/data/upload`
- **方法**: `POST`
- **描述**: 上傳新的歷史股價資料檔案。
- **請求主體**: `multipart/form-data`
    - `file` (file, **必要**): CSV 格式的股價資料檔案。
    - `dataset_name` (string, **必要**): 為此資料集指定一個名稱。
- **回應 (成功: 200 OK)**:
    ```json
    {"message": "Dataset uploaded successfully", "dataset_name": "new_stock_data.csv"}
    ```
- **回應 (錯誤: 400 Bad Request)**:
    ```json
    {"error": "Invalid file format or dataset name already exists"}
    ```
