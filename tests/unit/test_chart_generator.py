import unittest
import sys
import os
from unittest.mock import MagicMock, patch
import pandas as pd
import numpy as np

# 將 src/ 加入 Python 路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

try:
    from ui.components.chart_generator import ChartGenerator
except ImportError:
    ChartGenerator = None


@unittest.skipUnless(ChartGenerator, "ChartGenerator 尚未實作")
class TestChartGenerator(unittest.TestCase):
    """
    測試 ChartGenerator 類別的圖表生成功能
    """

    def setUp(self):
        """設定測試資料"""
        if ChartGenerator:
            self.chart_gen = ChartGenerator()

        # 建立模擬的歷史資料
        self.historical_data = pd.DataFrame({
            'date': pd.date_range(start='2025-01-01', periods=10),
            'close': [100, 102, 101, 105, 107, 106, 108, 110, 109, 111]
        })

        # 建立模擬的預測資料
        self.prediction_data = pd.DataFrame({
            'target_date': pd.date_range(start='2025-01-11', periods=5),
            'up_down_probability': [0.65, 0.70, 0.55, 0.60, 0.68],
            'change_magnitude': [0.015, 0.020, -0.010, 0.012, 0.018]
        })

    def test_generate_historical_chart(self):
        """
        測試生成歷史股價圖表
        """
        fig = self.chart_gen.generate_historical_chart(self.historical_data)

        self.assertIsNotNone(fig)
        # 檢查圖表是否包含數據
        self.assertTrue(len(fig.data) > 0)
        # 檢查圖表標題
        self.assertIsNotNone(fig.layout.title)

    def test_generate_prediction_chart(self):
        """
        測試生成預測結果圖表
        """
        fig = self.chart_gen.generate_prediction_chart(self.prediction_data)

        self.assertIsNotNone(fig)
        self.assertTrue(len(fig.data) > 0)

    def test_generate_combined_chart(self):
        """
        測試生成結合歷史與預測的圖表
        """
        fig = self.chart_gen.generate_combined_chart(
            self.historical_data,
            self.prediction_data
        )

        self.assertIsNotNone(fig)
        # 應該包含至少兩條線：歷史和預測
        self.assertGreaterEqual(len(fig.data), 2)

    def test_generate_chart_with_empty_data(self):
        """
        測試處理空資料的情況
        """
        empty_df = pd.DataFrame()

        with self.assertRaises(ValueError):
            self.chart_gen.generate_historical_chart(empty_df)

    def test_generate_chart_with_missing_columns(self):
        """
        測試處理缺少必要欄位的情況
        """
        invalid_df = pd.DataFrame({
            'date': pd.date_range(start='2025-01-01', periods=5)
            # 缺少 'close' 欄位
        })

        with self.assertRaises(KeyError):
            self.chart_gen.generate_historical_chart(invalid_df)

    @patch('ui.components.chart_generator.go.Figure')
    def test_chart_styling(self, mock_figure):
        """
        測試圖表樣式設定
        """
        mock_fig = MagicMock()
        mock_figure.return_value = mock_fig

        self.chart_gen.generate_historical_chart(self.historical_data)

        # 驗證圖表物件被創建
        mock_figure.assert_called()


if __name__ == '__main__':
    unittest.main()
