import os
import tensorflow as tf # 假設使用 TensorFlow

class ModelManager:
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)

    def save_model(self, model: tf.keras.Model, model_id: str):
        """
        儲存機器學習模型。
        :param model: 要儲存的 TensorFlow Keras 模型。
        :param model_id: 模型的唯一識別符。
        """
        model_path = os.path.join(self.model_dir, f"{model_id}.keras") # TensorFlow 3.x 推薦的格式
        model.save(model_path)
        print(f"模型 '{model_id}' 已儲存至 {model_path}")
        return model_path

    def load_model(self, model_id: str) -> tf.keras.Model:
        """
        載入機器學習模型。
        :param model_id: 模型的唯一識別符。
        :return: 載入的 TensorFlow Keras 模型。
        """
        model_path = os.path.join(self.model_dir, f"{model_id}.keras")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型 '{model_id}' 不存在於 {model_path}")
        model = tf.keras.models.load_model(model_path)
        print(f"模型 '{model_id}' 已從 {model_path} 載入")
        return model

    def get_model_path(self, model_id: str) -> str:
        """
        獲取指定模型的儲存路徑。
        """
        return os.path.join(self.model_dir, f"{model_id}.keras")

