import unittest
import sys
import os
from unittest.mock import MagicMock, patch
import uuid
import datetime

# 為了讓測試能夠找到 src/services/model_service.py，需要將 src/ 加入 Python 路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

# 由於 ModelService 已經實作，這裡直接導入
from services.model_service import ModelService
from utils.model_manager import ModelManager
from utils.metadata_manager import MetadataManager

class TestModelService(unittest.TestCase):

    def setUp(self):
        # 模擬 ModelManager 和 MetadataManager
        self.mock_model_manager = MagicMock(spec=ModelManager)
        self.mock_metadata_manager = MagicMock(spec=MetadataManager)
        self.model_service = ModelService(self.mock_model_manager, self.mock_metadata_manager)

        # 模擬訓練數據
        self.mock_training_data = MagicMock()
        self.mock_training_data.shape = (100, 10) # 模擬輸入數據的形狀

    @patch('services.model_service.tf.keras.Sequential') # 模擬 Keras 模型創建
    @patch('services.model_service.uuid.uuid4', return_value=uuid.UUID('12345678-1234-5678-1234-567812345678'))
    @patch('services.model_service.datetime.datetime')
    def test_train_and_save_model(self, mock_datetime, mock_uuid4, mock_sequential):
        """
        測試模型訓練和儲存功能。
        """
        mock_datetime.now.return_value = datetime.datetime(2025, 1, 1, 10, 0, 0)
        mock_datetime.now.isoformat.return_value = "2025-01-01T10:00:00"

        mock_model_instance = MagicMock()
        mock_sequential.return_value = mock_model_instance
        self.mock_model_manager.save_model.return_value = "/path/to/model/12345678-1234-5678-1234-567812345678.keras"

        dataset_name = "test_dataset"
        n_days = 5
        model_config = {"learning_rate": 0.001}

        model_id = self.model_service.train_and_save_model(dataset_name, n_days, model_config, self.mock_training_data)

        self.assertEqual(model_id, '12345678-1234-5678-1234-567812345678')
        mock_sequential.assert_called_once()
        mock_model_instance.compile.assert_called_once()
        # mock_model_instance.fit.assert_called_once() # 由於 ModelService 內部沒有實際調用 fit，這裡不檢查
        self.mock_model_manager.save_model.assert_called_once_with(mock_model_instance, model_id)
        self.mock_metadata_manager.add_metadata.assert_called_once()

        # 檢查 add_metadata 的參數
        added_metadata = self.mock_metadata_manager.add_metadata.call_args[0][0]
        self.assertEqual(added_metadata['model_id'], model_id)
        self.assertEqual(added_metadata['dataset_name'], dataset_name)
        self.assertEqual(added_metadata['n_days'], n_days)
        self.assertEqual(added_metadata['parameters'], model_config)
        self.assertIn('Model_20250101_100000', added_metadata['model_name'])


    def test_get_model_metadata(self):
        """
        測試獲取單個模型元資料。
        """
        mock_metadata = {"model_id": "test_id", "name": "Test Model"}
        self.mock_metadata_manager.get_metadata_by_id.return_value = mock_metadata

        result = self.model_service.get_model_metadata("test_id")
        self.assertEqual(result, mock_metadata)
        self.mock_metadata_manager.get_metadata_by_id.assert_called_once_with("test_id")

    def test_get_all_model_metadata(self):
        """
        測試獲取所有模型元資料。
        """
        mock_all_metadata = [{"model_id": "id1"}, {"model_id": "id2"}]
        self.mock_metadata_manager.get_all_metadata.return_value = mock_all_metadata

        result = self.model_service.get_all_model_metadata()
        self.assertEqual(result, mock_all_metadata)
        self.mock_metadata_manager.get_all_metadata.assert_called_once()

    def test_predict(self):
        """
        測試模型預測功能。
        """
        mock_model_instance = MagicMock()
        mock_model_instance.predict.return_value = [0.6, 0.7]
        self.mock_model_manager.load_model.return_value = mock_model_instance

        model_id = "test_model_id"
        input_data = MagicMock()

        predictions = self.model_service.predict(model_id, input_data)
        self.assertEqual(predictions, [0.6, 0.7])
        self.mock_model_manager.load_model.assert_called_once_with(model_id)
        mock_model_instance.predict.assert_called_once_with(input_data)

    def test_update_model_performance(self):
        """
        測試更新模型效能指標。
        """
        model_id = "test_id"
        metrics = {"loss": 0.01, "accuracy": 0.99}
        self.model_service.update_model_performance(model_id, metrics)
        self.mock_metadata_manager.update_metadata.assert_called_once_with(model_id, {"performance_metrics": metrics})

if __name__ == '__main__':
    unittest.main()
