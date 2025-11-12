from flask import Flask, jsonify, request
import os
import sys
import json

# 將專案根目錄加入 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.data_loader import DataLoader
from src.utils.model_manager import ModelManager
from src.utils.metadata_manager import MetadataManager
from src.services.data_service import DataService
from src.services.model_service import ModelService
from src.data.preprocessor import DataPreprocessor

def create_app():
    app = Flask(__name__)

    # 配置
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_very_secret_key')
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'data', 'uploads') # 假設上傳資料夾
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # 初始化服務
    data_loader = DataLoader(data_dir=os.path.join(os.getcwd(), 'data', 'processed_data')) # 處理後的資料儲存路徑
    model_manager = ModelManager(model_dir=os.path.join(os.getcwd(), 'models', 'saved_models')) # 模型檔案儲存路徑
    metadata_manager = MetadataManager(metadata_dir=os.path.join(os.getcwd(), 'models', 'metadata')) # 模型元資料儲存路徑
    data_service = DataService(data_loader)
    model_service = ModelService(model_manager, metadata_manager)
    data_preprocessor = DataPreprocessor() # 初始化資料預處理器

    # 範例路由
    @app.route('/')
    def index():
        return "歡迎來到股價預測系統後端！"

    @app.route('/api/status')
    def status():
        return jsonify({"status": "running", "version": "1.0"})

    @app.route('/api/model/train', methods=['POST'])
    def train_model():
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        dataset_name = data.get('dataset_name')
        n_days = data.get('n_days')

        if not dataset_name or not n_days:
            return jsonify({"error": "Missing 'dataset_name' or 'n_days' in request body."}), 400

        try:
            n_days = int(n_days)
            if not (1 <= n_days <= 30):
                return jsonify({"error": "Invalid 'n_days' value. Must be between 1 and 30."}), 400
        except ValueError:
            return jsonify({"error": "'n_days' must be an integer."}), 400

        try:
            # 載入原始數據
            raw_df = data_service.get_dataset(dataset_name)
            
            # 預處理數據
            # 這裡需要定義 look_back 和 target_column
            # 為了範例，我們假設 look_back=5, target_column='Close'
            look_back = 5 
            target_column = 'Close'
            X, y, scaler = data_preprocessor.preprocess(raw_df, look_back, n_days, target_column)

            # 這裡需要將 X, y 分割為訓練集和驗證集
            # 為了簡化，這裡直接使用全部數據作為訓練數據
            # 實際應用中應進行適當的分割
            X_train, y_train = X, y
            X_val, y_val = X, y # 暫時使用相同數據作為驗證集

            # 模擬模型配置
            model_config = {
                'look_back': look_back,
                'n_days': n_days,
                'target_column': target_column,
                'input_shape': X_train.shape[1:], # 傳遞給 build_model
                'output_units': y_train.shape[1] # 傳遞給 build_model
            }

            # 啟動模型訓練 (這裡需要將 ModelService 的 train_and_save_model 調整為非同步)
            # 為了簡化，這裡直接同步執行
            model_id = model_service.train_and_save_model(
                dataset_name=dataset_name,
                n_days=n_days,
                model_config=model_config,
                training_data=(X_train, y_train, X_val, y_val, scaler) # 傳遞所有必要數據
            )
            return jsonify({"message": "Model training started", "task_id": model_id}), 202
        except FileNotFoundError as e:
            return jsonify({"error": str(e)}), 404
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            app.logger.error(f"模型訓練失敗: {e}")
            return jsonify({"error": f"模型訓練失敗: {e}"}), 500

    @app.route('/api/model/train/status/<task_id>', methods=['GET'])
    def get_train_status(task_id):
        metadata = model_service.get_model_metadata(task_id)
        if metadata:
            # 這裡可以根據元資料中的某些標誌來判斷狀態
            # 為了簡化，我們假設只要有元資料就表示已完成
            # 實際應用中，可以添加 'status' 欄位到元資料中
            return jsonify({
                "task_id": task_id,
                "status": "completed", # 這裡簡化為 completed，實際應根據訓練進度更新
                "progress": 1.0,
                "message": "Model training completed",
                "model_id": task_id
            }), 200
        else:
            # 這裡可以模擬 pending 或 running 狀態
            # 為了簡化，如果沒有元資料就認為任務不存在或失敗
            return jsonify({"error": "Task not found or failed"}), 404

    @app.route('/api/data/history', methods=['GET'])
    def get_history():
        """
        取得歷史股價資料
        查詢參數: dataset_name (必要)
        """
        dataset_name = request.args.get('dataset_name')

        if not dataset_name:
            return jsonify({"error": "Missing 'dataset_name' parameter"}), 400

        try:
            # 載入歷史資料
            df = data_service.get_dataset(dataset_name)

            # 轉換為 JSON 格式
            # 確保日期格式正確
            df_copy = df.copy()
            if 'date' in df_copy.columns or 'Date' in df_copy.columns:
                date_col = 'date' if 'date' in df_copy.columns else 'Date'
                df_copy[date_col] = df_copy[date_col].astype(str)

            # 標準化欄位名稱為小寫
            df_copy.columns = df_copy.columns.str.lower()

            # 返回 JSON
            result = df_copy.to_dict(orient='records')
            return jsonify(result), 200

        except FileNotFoundError as e:
            return jsonify({"error": f"Dataset not found: {str(e)}"}), 404
        except Exception as e:
            app.logger.error(f"取得歷史資料失敗: {e}")
            return jsonify({"error": f"Failed to get historical data: {str(e)}"}), 500

    @app.route('/api/model/predict', methods=['GET'])
    def get_prediction():
        """
        取得模型預測結果
        查詢參數: model_id (必要), n_days (必要)
        """
        model_id = request.args.get('model_id')
        n_days = request.args.get('n_days')

        if not model_id or not n_days:
            return jsonify({"error": "Missing 'model_id' or 'n_days' parameter"}), 400

        try:
            n_days = int(n_days)
            if not (1 <= n_days <= 30):
                return jsonify({"error": "Invalid 'n_days' value. Must be between 1 and 30."}), 400
        except ValueError:
            return jsonify({"error": "'n_days' must be an integer."}), 400

        try:
            # 取得模型元資料
            metadata = model_service.get_model_metadata(model_id)
            if not metadata:
                return jsonify({"error": "Model not found"}), 404

            # 載入訓練資料集以取得最新資料點
            dataset_name = metadata['dataset_name']
            df = data_service.get_dataset(dataset_name)

            # 在預處理前先保存最後的日期
            import pandas as pd
            from datetime import timedelta
            last_date = pd.to_datetime(df.iloc[-1]['date'] if 'date' in df.columns else df.iloc[-1]['Date'])

            # 預處理資料以取得輸入特徵
            look_back = metadata['model_config']['look_back']
            target_column = metadata['model_config']['target_column']

            # 只需要最後 look_back 個資料點進行預測
            X, _, scaler = data_preprocessor.preprocess(df, look_back, n_days, target_column)

            # 取得最後一組輸入資料
            last_X = X[-1:] if len(X) > 0 else X

            # 使用模型服務進行預測
            predictions = model_service.predict(model_id, last_X)

            # 格式化預測結果

            prediction_results = []
            for i in range(n_days):
                target_date = last_date + timedelta(days=i+1)

                # 假設預測輸出為價格變化
                # 計算漲跌機率和幅度（這裡需要根據實際模型輸出調整）
                pred_value = float(predictions[0][i]) if len(predictions.shape) > 1 else float(predictions[i])

                # 簡化處理：將預測值轉換為漲跌機率和幅度
                up_down_probability = 0.5 + (pred_value * 0.1)  # 示例計算
                up_down_probability = max(0.0, min(1.0, up_down_probability))

                change_magnitude = pred_value * 0.01  # 示例：轉換為百分比

                prediction_results.append({
                    "target_date": target_date.strftime('%Y-%m-%d'),
                    "up_down_probability": up_down_probability,
                    "change_magnitude": change_magnitude
                })

            return jsonify(prediction_results), 200

        except FileNotFoundError as e:
            return jsonify({"error": f"Dataset not found: {str(e)}"}), 404
        except Exception as e:
            app.logger.error(f"預測失敗: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

    @app.route('/api/model/list', methods=['GET'])
    def list_models():
        """
        取得已訓練模型列表
        """
        try:
            models = model_service.get_all_model_metadata()
            return jsonify(models), 200
        except Exception as e:
            app.logger.error(f"取得模型列表失敗: {e}")
            return jsonify({"error": f"Failed to get model list: {str(e)}"}), 500

    @app.route('/api/data/upload', methods=['POST'])
    def upload_data():
        """
        上傳新的歷史資料
        請求參數:
        - file: CSV 檔案 (multipart/form-data)
        - dataset_name: 資料集名稱
        """
        # 檢查是否有檔案
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        dataset_name = request.form.get('dataset_name')

        if not dataset_name:
            # 如果沒有提供資料集名稱，使用檔案名稱
            dataset_name = file.filename

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # 檢查檔案格式
        if not file.filename.endswith('.csv'):
            return jsonify({"error": "Invalid file format. Only CSV files are allowed"}), 400

        try:
            # 確保上傳目錄存在
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

            # 儲存檔案
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], dataset_name)

            # 檢查檔案是否已存在
            if os.path.exists(file_path):
                return jsonify({"error": "Dataset name already exists"}), 400

            file.save(file_path)

            # 驗證 CSV 格式
            import pandas as pd
            try:
                df = pd.read_csv(file_path)

                # 檢查必要欄位（支援中英文）
                # 英文欄位對應
                date_columns = ['date', '時間', '日期', 'Date', 'TIME']
                close_columns = ['close', '收盤價', '收盘价', 'Close', 'CLOSE']

                # 檢查是否有日期欄位
                has_date = any(col in df.columns for col in date_columns)
                # 檢查是否有收盤價欄位
                has_close = any(col in df.columns for col in close_columns)

                if not has_date or not has_close:
                    missing = []
                    if not has_date:
                        missing.append('date/時間')
                    if not has_close:
                        missing.append('close/收盤價')

                    os.remove(file_path)  # 刪除無效檔案
                    return jsonify({
                        "error": f"CSV file is missing required columns: {', '.join(missing)}. Your columns: {', '.join(df.columns[:5])}..."
                    }), 400

                # 標準化欄位名稱
                column_mapping = {}

                # 對應日期欄位
                for col in date_columns:
                    if col in df.columns:
                        column_mapping[col] = 'date'
                        break

                # 對應收盤價欄位
                for col in close_columns:
                    if col in df.columns:
                        column_mapping[col] = 'close'
                        break

                # 對應其他可能的欄位
                price_mapping = {
                    '開盤價': 'open',
                    '最高價': 'high',
                    '最低價': 'low',
                    '成交量': 'volume',
                    'Open': 'open',
                    'High': 'high',
                    'Low': 'low',
                    'Volume': 'volume'
                }

                for chinese_col, english_col in price_mapping.items():
                    if chinese_col in df.columns:
                        column_mapping[chinese_col] = english_col

                # 重新命名欄位
                if column_mapping:
                    df.rename(columns=column_mapping, inplace=True)
                    # 保存標準化後的檔案
                    df.to_csv(file_path, index=False)

                # 將檔案移動到處理後的資料目錄
                processed_dir = os.path.join(os.getcwd(), 'data', 'processed_data')
                os.makedirs(processed_dir, exist_ok=True)

                final_path = os.path.join(processed_dir, dataset_name)

                # 如果檔案已存在，先刪除
                if os.path.exists(final_path):
                    os.remove(final_path)

                os.rename(file_path, final_path)

                return jsonify({
                    "message": "Dataset uploaded successfully",
                    "dataset_name": dataset_name,
                    "rows": len(df),
                    "columns": list(df.columns)
                }), 200

            except Exception as e:
                # 清理檔案
                if os.path.exists(file_path):
                    os.remove(file_path)
                return jsonify({"error": f"Invalid CSV file: {str(e)}"}), 400

        except Exception as e:
            app.logger.error(f"上傳資料失敗: {e}")
            return jsonify({"error": f"Failed to upload data: {str(e)}"}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
