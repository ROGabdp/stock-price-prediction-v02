import pandas as pd
from src.utils.data_loader import DataLoader
import uuid
import os
from typing import List

class DataService:
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader
        self.data_storage_dir = data_loader.data_dir # 儲存處理後資料的目錄

    def upload_and_process_data(self, file_path: str, dataset_name: str) -> str:
        """
        上傳並處理 CSV 資料，然後儲存為內部格式。
        返回處理後資料集的名稱。
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"上傳檔案不存在: {file_path}")

        # 檢查資料集名稱是否已存在
        if self.get_all_datasets() and dataset_name in self.get_all_datasets():
            raise ValueError(f"資料集名稱 '{dataset_name}' 已存在。")

        df = self.data_loader.load_csv(file_path)
        self.data_loader.save_dataframe(df, dataset_name)
        return dataset_name

    def get_dataset(self, dataset_name: str) -> pd.DataFrame:
        """
        根據資料集名稱獲取處理後的資料。
        """
        return self.data_loader.load_dataframe(dataset_name)

    def get_all_datasets(self) -> List[str]:
        """
        獲取所有已儲存的資料集名稱。
        """
        # 假設內部儲存格式為 .parquet
        return [f.replace('.parquet', '') for f in os.listdir(self.data_storage_dir) if f.endswith('.parquet')]

