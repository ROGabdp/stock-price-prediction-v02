import uuid
import datetime
from typing import Dict, Any, List, Tuple
import numpy as np

from src.utils.model_manager import ModelManager
from src.utils.metadata_manager import MetadataManager
from src.models.trainer import ModelTrainer

class ModelService:
    def __init__(self, model_manager: ModelManager, metadata_manager: MetadataManager):
        self.model_manager = model_manager
        self.metadata_manager = metadata_manager

    def train_and_save_model(self, dataset_name: str, n_days: int,
                             model_config: Dict[str, Any],
                             training_data: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, Any]) -> str:
        """
        訓練模型並儲存，同時記錄元資料。
        整合自動超參數調整功能。
        :param dataset_name: 用於訓練的資料集名稱。
        :param n_days: 預測天數。
        :param model_config: 模型配置（包含 input_shape, output_units, look_back, target_column 等）。
        :param training_data: 訓練數據 (X_train, y_train, X_val, y_val, scaler)。
        :return: 訓練後模型的 ID。
        """
        model_id = str(uuid.uuid4())
        model_name = f"Model_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

        X_train, y_train, X_val, y_val, scaler = training_data

        # 初始化模型訓練器
        trainer = ModelTrainer()

        # 執行自動超參數調整
        print(f"開始為模型 {model_id} 執行自動超參數調整...")
        best_hyperparameters = trainer.auto_tune_hyperparameters(
            X_train, y_train, X_val, y_val,
            input_shape=model_config['input_shape'],
            output_units=model_config['output_units']
        )

        # 使用最佳超參數建構模型
        print(f"使用最佳超參數建構模型: {best_hyperparameters}")
        model = trainer.build_model(
            input_shape=model_config['input_shape'],
            output_units=model_config['output_units'],
            hyperparameters=best_hyperparameters
        )

        # 訓練模型
        print(f"開始訓練模型 {model_id}...")
        history = trainer.train_model(X_train, y_train, X_val, y_val, best_hyperparameters)

        # 評估模型
        print(f"評估模型 {model_id}...")
        performance_metrics = trainer.evaluate_model(X_val, y_val)
        print(f"模型效能: {performance_metrics}")

        # 儲存模型
        trained_model = trainer.get_model()
        model_path = self.model_manager.save_model(trained_model, model_id)
        print(f"模型已儲存至: {model_path}")

        # 記錄完整的元資料
        metadata = {
            "model_id": model_id,
            "model_name": model_name,
            "file_path": model_path,
            "training_date": datetime.datetime.now().isoformat(),
            "performance_metrics": performance_metrics,
            "hyperparameters": best_hyperparameters,
            "model_config": {
                "look_back": model_config.get('look_back'),
                "n_days": n_days,
                "target_column": model_config.get('target_column'),
                "input_shape": list(model_config['input_shape']),
                "output_units": model_config['output_units']
            },
            "dataset_name": dataset_name,
            "n_days": n_days,
            "training_history": {
                "final_loss": float(history.history['loss'][-1]) if 'loss' in history.history else None,
                "final_val_loss": float(history.history['val_loss'][-1]) if 'val_loss' in history.history else None,
                "final_mae": float(history.history['mae'][-1]) if 'mae' in history.history else None,
                "final_val_mae": float(history.history['val_mae'][-1]) if 'val_mae' in history.history else None
            }
        }
        self.metadata_manager.add_metadata(metadata)
        print(f"模型元資料已記錄: {model_id}")

        return model_id

    def get_model_metadata(self, model_id: str) -> Dict[str, Any] | None:
        """
        根據模型 ID 獲取模型元資料。
        """
        return self.metadata_manager.get_metadata_by_id(model_id)

    def get_all_model_metadata(self) -> List[Dict[str, Any]]:
        """
        獲取所有模型的元資料列表。
        """
        return self.metadata_manager.get_all_metadata()

    def predict(self, model_id: str, input_data: Any) -> Any:
        """
        使用指定模型進行預測。
        :param model_id: 要使用的模型 ID。
        :param input_data: 預測輸入數據。
        :return: 預測結果。
        """
        model = self.model_manager.load_model(model_id)
        predictions = model.predict(input_data)
        return predictions

    def update_model_performance(self, model_id: str, metrics: Dict[str, Any]):
        """
        更新模型的效能指標。
        """
        self.metadata_manager.update_metadata(model_id, {"performance_metrics": metrics})

