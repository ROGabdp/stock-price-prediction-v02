import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
import sys
import os

# 為了讓測試能夠找到 src/data/preprocessor.py，需要將 src/ 加入 Python 路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

# 由於 preprocessor.py 尚未實作，這裡先假設其存在並嘗試導入
# 實際執行時，如果 preprocessor.py 不存在，這裡會報 ImportError
try:
    from data.preprocessor import DataPreprocessor
except ImportError:
    # 如果 DataPreprocessor 尚未實作，則跳過測試
    DataPreprocessor = None

@unittest.skipUnless(DataPreprocessor, "DataPreprocessor 尚未實作")
class TestDataPreprocessor(unittest.TestCase):

    def setUp(self):
        # 建立一個模擬的 DataFrame 作為測試數據
        self.raw_data = pd.DataFrame({
            'Date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']),
            'Open': [100, 101, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [99, 100, 101, 102, 103],
            'Close': [103, 105, 106, 107, 108],
            'Volume': [1000, 1100, 1200, 1300, 1400],
            'SMA': [None, None, 102, 104, 106], # 模擬技術指標，包含 NaN
            'MACD': [0.1, 0.2, 0.3, None, 0.5] # 模擬技術指標，包含 NaN
        })
        self.preprocessor = DataPreprocessor()

    def test_feature_engineering(self):
        """
        測試特徵工程是否正確添加了新的特徵。
        """
        processed_df = self.preprocessor.feature_engineering(self.raw_data.copy())
        self.assertIn('Daily_Return', processed_df.columns)
        self.assertIn('Volatility', processed_df.columns)
        self.assertGreater(len(processed_df.columns), len(self.raw_data.columns))

    def test_normalize_data(self):
        """
        測試數據正規化是否將數據縮放到指定範圍。
        """
        df_with_features = self.preprocessor.feature_engineering(self.raw_data.copy())
        normalized_df, scaler = self.preprocessor.normalize_data(df_with_features)

        # 檢查數據是否在 0 到 1 之間 (或接近)
        self.assertTrue((normalized_df.min() >= -0.01).all()) # 允許微小浮點誤差
        self.assertTrue((normalized_df.max() <= 1.01).all())

        # 檢查 scaler 是否被返回
        self.assertIsNotNone(scaler)

    def test_create_sequences(self):
        """
        測試序列創建是否正確生成了輸入序列和目標值。
        """
        df_with_features = self.preprocessor.feature_engineering(self.raw_data.copy())
        normalized_df, _ = self.preprocessor.normalize_data(df_with_features)

        # 假設我們預測 'Close' 的漲跌
        X, y = self.preprocessor.create_sequences(normalized_df, look_back=3, forecast_horizon=1, target_column='Close')

        self.assertIsNotNone(X)
        self.assertIsNotNone(y)
        self.assertEqual(X.shape[0], y.shape[0]) # 序列數量應相同
        self.assertEqual(X.shape[1], 3) # look_back 應為 3
        self.assertEqual(y.shape[1], 1) # forecast_horizon 應為 1

        # 檢查序列內容是否合理
        # 例如，第一個序列的最後一個 Close 值應該是第二個目標值
        # 由於數據正規化和特徵工程，直接比較原始值會很複雜，這裡只檢查形狀和非空
        self.assertFalse(pd.isna(X).any())
        self.assertFalse(pd.isna(y).any())

    def test_full_preprocessing_pipeline(self):
        """
        測試完整的預處理流程。
        """
        look_back = 2
        forecast_horizon = 1
        target_column = 'Close'

        X, y, scaler = self.preprocessor.preprocess(self.raw_data.copy(), look_back, forecast_horizon, target_column)

        self.assertIsNotNone(X)
        self.assertIsNotNone(y)
        self.assertIsNotNone(scaler)
        self.assertEqual(X.shape[0], y.shape[0])
        self.assertEqual(X.shape[1], look_back)
        self.assertEqual(y.shape[1], forecast_horizon)

if __name__ == '__main__':
    unittest.main()
