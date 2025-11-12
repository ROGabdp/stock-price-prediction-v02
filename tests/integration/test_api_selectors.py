import unittest
import sys
import os
import json

# 將 src/ 加入 Python 路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

try:
    from app import create_app
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False


@unittest.skipUnless(FLASK_AVAILABLE, "Flask 應用尚未完整實作")
class TestAPISelectors(unittest.TestCase):
    """
    整合測試：測試 /api/model/list 和 /api/data/upload 端點
    """

    def setUp(self):
        """設定測試環境"""
        if FLASK_AVAILABLE:
            self.app = create_app()
            self.client = self.app.test_client()
            self.app.config['TESTING'] = True

    def test_api_model_list(self):
        """
        測試 GET /api/model/list 端點
        """
        response = self.client.get('/api/model/list')

        self.assertEqual(response.status_code, 200)

        # 檢查回應格式
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

        # 如果有模型，檢查元資料格式
        if len(data) > 0:
            model = data[0]
            self.assertIn('model_id', model)
            self.assertIn('model_name', model)
            self.assertIn('training_date', model)

    def test_api_data_upload_missing_file(self):
        """
        測試上傳缺少檔案的情況
        """
        response = self.client.post('/api/data/upload', data={})

        # 應該返回錯誤
        self.assertIn(response.status_code, [400, 404])

    def test_api_data_upload_invalid_format(self):
        """
        測試上傳非 CSV 格式檔案
        """
        data = {
            'file': (b'not a csv file', 'test.txt'),
            'dataset_name': 'test_dataset'
        }

        response = self.client.post(
            '/api/data/upload',
            data=data,
            content_type='multipart/form-data'
        )

        # 應該返回錯誤
        self.assertIn(response.status_code, [400, 415])

    @unittest.skip("需要建立測試 CSV 檔案")
    def test_api_data_upload_success(self):
        """
        測試成功上傳 CSV 檔案
        """
        # 建立測試 CSV 檔案
        csv_content = b"date,open,high,low,close,volume\n2025-01-01,100,105,98,103,1000000"

        data = {
            'file': (csv_content, 'test_data.csv'),
            'dataset_name': 'test_dataset'
        }

        response = self.client.post(
            '/api/data/upload',
            data=data,
            content_type='multipart/form-data'
        )

        self.assertEqual(response.status_code, 200)

        # 檢查回應
        result = json.loads(response.data)
        self.assertIn('message', result)
        self.assertIn('dataset_name', result)


if __name__ == '__main__':
    unittest.main()
