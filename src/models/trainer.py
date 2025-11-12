import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from typing import Dict, Any, Tuple

# 為了簡化，這裡不直接使用 Keras Tuner，而是模擬其功能
# 實際專案中會整合 Keras Tuner 進行自動超參數調整

class ModelTrainer:
    def __init__(self):
        self.model: keras.Model = None

    def build_model(self, input_shape: Tuple[int, ...], output_units: int, hyperparameters: Dict[str, Any]) -> keras.Model:
        """
        根據給定的超參數建構機器學習模型。
        :param input_shape: 輸入數據的形狀 (例如 (look_back, num_features))。
        :param output_units: 輸出層的單元數 (例如 1 用於預測單一值)。
        :param hyperparameters: 包含學習率、層數、單元數等超參數的字典。
        :return: 編譯後的 Keras 模型。
        """
        model = keras.Sequential([
            layers.Input(shape=input_shape),
            layers.LSTM(hyperparameters.get('lstm_units', 50), return_sequences=False),
            layers.Dropout(hyperparameters.get('dropout_rate', 0.2)),
            layers.Dense(output_units, activation='linear') # 預測數值，使用 linear 激活
        ])

        optimizer = keras.optimizers.Adam(learning_rate=hyperparameters.get('learning_rate', 0.001))
        model.compile(optimizer=optimizer, loss='mse', metrics=['mae']) # 迴歸問題使用 mse 和 mae

        self.model = model
        return model

    def train_model(self, X_train: np.ndarray, y_train: np.ndarray,
                    X_val: np.ndarray, y_val: np.ndarray,
                    hyperparameters: Dict[str, Any]) -> keras.callbacks.History:
        """
        訓練模型。
        :param X_train: 訓練數據的輸入特徵。
        :param y_train: 訓練數據的目標值。
        :param X_val: 驗證數據的輸入特徵。
        :param y_val: 驗證數據的目標值。
        :param hyperparameters: 包含 epochs, batch_size 等訓練參數的字典。
        :return: 訓練歷史對象。
        """
        if self.model is None:
            raise ValueError("模型尚未建構。請先調用 build_model。")

        history = self.model.fit(
            X_train, y_train,
            epochs=hyperparameters.get('epochs', 50),
            batch_size=hyperparameters.get('batch_size', 32),
            validation_data=(X_val, y_val),
            verbose=1
        )
        return history

    def auto_tune_hyperparameters(self, X_train: np.ndarray, y_train: np.ndarray,
                                  X_val: np.ndarray, y_val: np.ndarray,
                                  input_shape: Tuple[int, ...], output_units: int) -> Dict[str, Any]:
        """
        模擬自動超參數調整，返回最佳超參數。
        在實際應用中，這裡會整合 Keras Tuner 或其他超參數優化庫。
        :return: 最佳超參數字典。
        """
        print("正在執行自動超參數調整 (模擬)...")
        best_hyperparameters = {
            'learning_rate': 0.001,
            'lstm_units': 64,
            'dropout_rate': 0.3,
            'epochs': 30,
            'batch_size': 32
        }
        # 這裡可以加入更複雜的搜索邏輯，例如隨機搜索或網格搜索
        # 為了簡化，直接返回預設的最佳參數
        print(f"模擬超參數調整完成，最佳參數: {best_hyperparameters}")
        return best_hyperparameters

    def evaluate_model(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """
        評估模型在測試集上的表現。
        :param X_test: 測試數據的輸入特徵。
        :param y_test: 測試數據的目標值。
        :return: 包含損失和評估指標的字典。
        """
        if self.model is None:
            raise ValueError("模型尚未建構或訓練。")

        loss, mae = self.model.evaluate(X_test, y_test, verbose=0)
        return {"loss": loss, "mae": mae}

    def get_model(self) -> keras.Model:
        """
        獲取當前訓練好的模型實例。
        """
        return self.model

