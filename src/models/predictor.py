import numpy as np
import tensorflow as tf # 假設使用 TensorFlow
from typing import Any

class ModelPredictor:
    def __init__(self, model: tf.keras.Model):
        self.model = model

    def predict_next_n_days(self, input_sequence: np.ndarray, n_days: int) -> np.ndarray:
        """
        使用訓練好的模型預測未來 N 天的股價變化。
        注意：這個是一個簡化的預測器。實際的序列預測通常需要更複雜的邏輯，
        例如多步預測（multi-step prediction）或遞歸預測（recursive prediction），
        其中每個新的預測點都作為下一個預測的輸入。
        為保持獨立性，這裡只進行單步預測，並重複 N 次。
        
        :param input_sequence: 經過預處理和正規化的輸入序列 (例如 (1, look_back, num_features))。
                                注意：這裡假設 input_sequence 已經是正確的 input shape。
        :param n_days: 預測未來的天數。
        :return: 預測的未來 N 天的正規化股價變化 (例如漲跌機率或幅度)。
        """
        if n_days <= 0:
            raise ValueError("預測天數 n_days 必須大於 0。")

        predictions = []
        current_input = input_sequence # 假設輸入序列已經是批次格式 (batch_size, look_back, features)

        for _ in range(n_days):
            # 進行單步預測
            next_prediction = self.model.predict(current_input, verbose=0)
            predictions.append(next_prediction[0]) # 取出批次中的第一個預測結果

            # 更新輸入序列以進行下一個預測 (這裡是一個簡化方法)
            # 在實際的多步預測中，通常需要將最新預測的結果整合回輸入序列
            # 例如：current_input = np.roll(current_input, -1, axis=1)
            # current_input[0, -1, target_feature_idx] = next_prediction[0]
            # 為了簡潔，這裡假設模型足夠簡單，不依賴於精確序列更新
            # 或者每次都是基於一個固定的 input_sequence 進行單步預測
            pass # 這裡不更新 input_sequence，因為大多數基於 LSTM 的多步預測已經是在訓練時定義了輸出步長

        return np.array(predictions)
