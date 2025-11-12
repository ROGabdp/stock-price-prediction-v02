import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# 為了讓測試能夠找到 src/models/trainer.py，需要將 src/ 加入 Python 路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

# 由於 trainer.py 尚未實作，這裡先假設其存在並嘗試導入
try:
    from models.trainer import ModelTrainer
except ImportError:
    ModelTrainer = None

@unittest.skipUnless(ModelTrainer, "ModelTrainer 尚未實作")
class TestModelTrainer(unittest.TestCase):

    def setUp(self):
        # 模擬一個簡單的 Keras 模型
        self.mock_model = MagicMock()
        self.mock_model.fit.return_value = MagicMock(history={'loss': [0.1, 0.05], 'accuracy': [0.9, 0.95]})
        self.mock_model.evaluate.return_value = [0.05, 0.95] # loss, accuracy

        # 模擬訓練數據
        self.mock_X_train = MagicMock()
        self.mock_y_train = MagicMock()
        self.mock_X_val = MagicMock()
        self.mock_y_val = MagicMock()

        # 模擬超參數調整的結果
        self.mock_best_hyperparameters = {'learning_rate': 0.001, 'epochs': 10}

        # 模擬 ModelTrainer 實例
        self.trainer = ModelTrainer()

    @patch('models.trainer.tf.keras.Sequential') # 假設 ModelTrainer 內部會創建 Keras 模型
    @patch('models.trainer.tf.keras.optimizers.Adam') # 假設使用 Adam 優化器
    def test_build_model(self, mock_adam, mock_sequential):
        """
        測試模型建構方法是否正確。
        """
        mock_sequential.return_value = self.mock_model
        model = self.trainer.build_model(input_shape=(10,), output_units=1, hyperparameters={'learning_rate': 0.001})
        self.assertIsNotNone(model)
        mock_sequential.assert_called_once()
        self.mock_model.compile.assert_called_once()
        mock_adam.assert_called_once_with(learning_rate=0.001)

    @patch('models.trainer.tf.keras.Sequential')
    def test_train_model(self, mock_sequential):
        """
        測試模型訓練流程。
        """
        mock_sequential.return_value = self.mock_model
        # 假設 build_model 已經被調用並返回了 self.mock_model
        self.trainer.model = self.mock_model

        history = self.trainer.train_model(
            self.mock_X_train, self.mock_y_train,
            self.mock_X_val, self.mock_y_val,
            hyperparameters={'epochs': 2, 'batch_size': 32}
        )
        self.assertIsNotNone(history)
        self.mock_model.fit.assert_called_once()
        self.assertEqual(self.mock_model.fit.call_args[1]['epochs'], 2)

    @patch('models.trainer.tf.keras.Sequential')
    @patch('models.trainer.Hyperband') # 假設使用 Keras Tuner 的 Hyperband
    def test_auto_tune_hyperparameters(self, mock_hyperband, mock_sequential):
        """
        測試自動參數調整流程。
        """
        mock_sequential.return_value = self.mock_model
        mock_tuner_instance = MagicMock()
        mock_tuner_instance.search.return_value = None
        mock_tuner_instance.get_best_hyperparameters.return_value = [MagicMock(values=self.mock_best_hyperparameters)]
        mock_hyperband.return_value = mock_tuner_instance

        best_hp = self.trainer.auto_tune_hyperparameters(
            self.mock_X_train, self.mock_y_train,
            self.mock_X_val, self.mock_y_val,
            input_shape=(10,), output_units=1
        )
        self.assertIsNotNone(best_hp)
        self.assertEqual(best_hp, self.mock_best_hyperparameters)
        mock_hyperband.assert_called_once()
        mock_tuner_instance.search.assert_called_once()
        mock_tuner_instance.get_best_hyperparameters.assert_called_once()

    @patch('models.trainer.tf.keras.Sequential')
    def test_evaluate_model(self, mock_sequential):
        """
        測試模型評估流程。
        """
        mock_sequential.return_value = self.mock_model
        self.trainer.model = self.mock_model

        metrics = self.trainer.evaluate_model(self.mock_X_val, self.mock_y_val)
        self.assertIsNotNone(metrics)
        self.mock_model.evaluate.assert_called_once_with(self.mock_X_val, self.mock_y_val, verbose=0)
        self.assertEqual(metrics['loss'], 0.05)
        self.assertEqual(metrics['accuracy'], 0.95)

if __name__ == '__main__':
    unittest.main()
