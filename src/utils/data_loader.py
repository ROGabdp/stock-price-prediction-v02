import pandas as pd
import os

class DataLoader:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def load_csv(self, file_path: str) -> pd.DataFrame:
        """
        載入 CSV 檔案，處理中文欄位名稱、額外技術指標和缺失值。
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"檔案不存在: {file_path}")

        df = pd.read_csv(file_path)

        # 處理缺失值：刪除包含 N/A 值的整行數據
        df.dropna(inplace=True)

        # 假設 CSV 包含中文欄位，這裡需要一個映射來轉換為英文或標準名稱
        # 這裡只是一個範例映射，實際應根據具體 CSV 檔案的欄位來定義
        column_mapping = {
            '日期': 'Date',
            '開盤價': 'Open',
            '最高價': 'High',
            '最低價': 'Low',
            '收盤價': 'Close',
            '成交量': 'Volume',
            # 根據實際 CSV 檔案添加更多技術指標的映射
            # 例如：
            # 'SMA': 'SMA',
            # 'MACD': 'MACD',
            # ...
        }

        # 轉換欄位名稱
        df.rename(columns=column_mapping, inplace=True)

        # 確保必要的欄位存在
        required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in df.columns for col in required_columns):
            missing = [col for col in required_columns if col not in df.columns]
            raise ValueError(f"CSV 檔案缺少必要的欄位: {missing}")

        # 將 'Date' 欄位轉換為日期時間格式並設定為索引
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)

        # 包含額外技術指標：如果 CSV 中有其他欄位，它們將被保留
        # 這裡不需要額外處理，因為 rename 之後，未映射的欄位會保留原名

        return df

    def save_dataframe(self, df: pd.DataFrame, dataset_name: str):
        """
        將處理後的 DataFrame 儲存為內部格式 (例如 Parquet 或另一個 CSV)。
        """
        save_path = os.path.join(self.data_dir, f"{dataset_name}.parquet")
        df.to_parquet(save_path)
        print(f"資料集 '{dataset_name}' 已儲存至 {save_path}")

    def load_dataframe(self, dataset_name: str) -> pd.DataFrame:
        """
        載入已儲存的 DataFrame。
        支援 .csv 和 .parquet 格式。
        """
        # 先嘗試找 CSV 檔案（因為上傳的檔案是 CSV）
        csv_path = os.path.join(self.data_dir, dataset_name)
        parquet_path = os.path.join(self.data_dir, f"{dataset_name}.parquet")

        # 如果 dataset_name 本身就包含 .csv，直接使用
        if dataset_name.endswith('.csv') and os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            return df

        # 嘗試 parquet 格式
        if os.path.exists(parquet_path):
            return pd.read_parquet(parquet_path)

        # 嘗試添加 .csv
        csv_with_ext = os.path.join(self.data_dir, f"{dataset_name}.csv")
        if os.path.exists(csv_with_ext):
            df = pd.read_csv(csv_with_ext)
            return df

        # 都找不到就報錯
        raise FileNotFoundError(f"資料集 '{dataset_name}' 不存在。已嘗試: {csv_path}, {parquet_path}, {csv_with_ext}")

