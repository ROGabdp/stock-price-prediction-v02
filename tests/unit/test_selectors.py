import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# 將 src/ 加入 Python 路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

try:
    from ui.components.data_selector import DataSelector
    from ui.components.model_selector import ModelSelector
    DATA_SELECTOR_AVAILABLE = True
except ImportError:
    DATA_SELECTOR_AVAILABLE = False
    DataSelector = None
    ModelSelector = None


@unittest.skipUnless(DATA_SELECTOR_AVAILABLE, "Selector 元件尚未實作")
class TestDataSelector(unittest.TestCase):
    """
    測試資料集選擇器元件
    """

    def setUp(self):
        """設定測試環境"""
        if DataSelector:
            self.data_selector = DataSelector()

    def test_get_dataset_list(self):
        """
        測試取得資料集列表
        """
        datasets = self.data_selector.get_dataset_list()
        self.assertIsInstance(datasets, list)

    def test_dataset_options_format(self):
        """
        測試資料集選項格式正確
        """
        options = self.data_selector.get_dropdown_options()
        self.assertIsInstance(options, list)

        if len(options) > 0:
            # 檢查選項格式
            for option in options:
                self.assertIn('label', option)
                self.assertIn('value', option)

    @patch('ui.components.data_selector.os.listdir')
    def test_scan_data_directory(self, mock_listdir):
        """
        測試掃描資料目錄
        """
        mock_listdir.return_value = ['data1.csv', 'data2.csv', 'readme.txt']

        datasets = self.data_selector.scan_datasets()

        # 應該只返回 CSV 檔案
        self.assertEqual(len(datasets), 2)
        self.assertIn('data1.csv', datasets)
        self.assertIn('data2.csv', datasets)


@unittest.skipUnless(DATA_SELECTOR_AVAILABLE, "Selector 元件尚未實作")
class TestModelSelector(unittest.TestCase):
    """
    測試模型選擇器元件
    """

    def setUp(self):
        """設定測試環境"""
        if ModelSelector:
            self.model_selector = ModelSelector()

    def test_get_model_list(self):
        """
        測試取得模型列表
        """
        models = self.model_selector.get_model_list()
        self.assertIsInstance(models, list)

    def test_model_options_format(self):
        """
        測試模型選項格式正確
        """
        options = self.model_selector.get_dropdown_options()
        self.assertIsInstance(options, list)

        if len(options) > 0:
            # 檢查選項格式
            for option in options:
                self.assertIn('label', option)
                self.assertIn('value', option)

    def test_model_metadata_display(self):
        """
        測試顯示模型元資料
        """
        mock_metadata = {
            'model_id': 'test-123',
            'model_name': 'Test Model',
            'training_date': '2025-11-12',
            'performance_metrics': {'loss': 0.01, 'mae': 0.02}
        }

        display_info = self.model_selector.format_model_info(mock_metadata)
        self.assertIsNotNone(display_info)
        self.assertIn('Test Model', display_info)


if __name__ == '__main__':
    unittest.main()
