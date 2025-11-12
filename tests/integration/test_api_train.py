import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# 為了讓測試能夠找到 src/app.py，需要將 src/ 加入 Python 路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

# 由於 app.py 已經實作，這裡直接導入
from app import create_app

class TestApiTrain(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    @patch('services.model_service.ModelService.train_and_save_model')
    def test_train_model_endpoint_success(self, mock_train_and_save_model):
        """
        測試 /api/model/train 端點成功啟動模型訓練。
        """
        mock_train_and_save_model.return_value = "mock_model_id_123"

        payload = {
            "dataset_name": "test_data_set",
            "n_days": 5
        }
        response = self.client.post('/api/model/train',
                                    data=json.dumps(payload),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 202)
        data = json.loads(response.data)
        self.assertIn("message", data)
        self.assertIn("task_id", data)
        self.assertEqual(data["message"], "Model training started")
        self.assertEqual(data["task_id"], "mock_model_id_123")
        mock_train_and_save_model.assert_called_once()

    def test_train_model_endpoint_missing_dataset_name(self):
        """
        測試 /api/model/train 端點缺少 dataset_name 參數。
        """
        payload = {
            "n_days": 5
        }
        response = self.client.post('/api/model/train',
                                    data=json.dumps(payload),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Missing 'dataset_name' or 'n_days' in request body.")

    def test_train_model_endpoint_invalid_n_days(self):
        """
        測試 /api/model/train 端點 n_days 參數無效。
        """
        payload = {
            "dataset_name": "test_data_set",
            "n_days": 0 # 無效的 n_days
        }
        response = self.client.post('/api/model/train',
                                    data=json.dumps(payload),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Invalid 'n_days' value. Must be between 1 and 30.")

    @patch('services.model_service.ModelService.train_and_save_model')
    def test_train_model_endpoint_training_failure(self, mock_train_and_save_model):
        """
        測試 /api/model/train 端點模型訓練失敗。
        """
        mock_train_and_save_model.side_effect = Exception("模擬訓練失敗")

        payload = {
            "dataset_name": "test_data_set",
            "n_days": 5
        }
        response = self.client.post('/api/model/train',
                                    data=json.dumps(payload),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "模型訓練失敗: 模擬訓練失敗")
        mock_train_and_save_model.assert_called_once()

if __name__ == '__main__':
    unittest.main()
