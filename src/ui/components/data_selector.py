"""
資料集選擇器元件
提供資料集選擇的介面邏輯
"""

import os
from typing import List, Dict


class DataSelector:
    """
    資料集選擇器，負責管理和提供可用資料集的選項
    """

    def __init__(self, data_dir: str = None):
        """
        初始化資料選擇器
        :param data_dir: 資料目錄路徑
        """
        if data_dir is None:
            data_dir = os.path.join(os.getcwd(), 'data', 'processed_data')

        self.data_dir = data_dir

        # 確保資料目錄存在
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)

    def scan_datasets(self) -> List[str]:
        """
        掃描資料目錄，取得所有可用的 CSV 資料集
        :return: 資料集檔案名稱列表
        """
        try:
            files = os.listdir(self.data_dir)
            # 只返回 CSV 檔案
            csv_files = [f for f in files if f.endswith('.csv')]
            return csv_files
        except Exception as e:
            print(f"掃描資料集時發生錯誤: {e}")
            return []

    def get_dataset_list(self) -> List[str]:
        """
        取得資料集列表
        :return: 資料集名稱列表
        """
        return self.scan_datasets()

    def get_dropdown_options(self) -> List[Dict[str, str]]:
        """
        取得下拉選單格式的選項
        :return: Dash Dropdown 元件所需的選項列表
        """
        datasets = self.get_dataset_list()

        options = []
        for dataset in datasets:
            # 移除 .csv 副檔名作為顯示名稱
            display_name = dataset.replace('.csv', '')
            options.append({
                'label': display_name,
                'value': dataset
            })

        return options

    def get_dataset_info(self, dataset_name: str) -> Dict[str, any]:
        """
        取得資料集的基本資訊
        :param dataset_name: 資料集名稱
        :return: 資料集資訊字典
        """
        dataset_path = os.path.join(self.data_dir, dataset_name)

        if not os.path.exists(dataset_path):
            return {"error": "資料集不存在"}

        try:
            # 取得檔案大小
            file_size = os.path.getsize(dataset_path)

            # 取得修改時間
            import datetime
            mod_time = os.path.getmtime(dataset_path)
            mod_datetime = datetime.datetime.fromtimestamp(mod_time)

            return {
                "name": dataset_name,
                "size": file_size,
                "size_mb": round(file_size / (1024 * 1024), 2),
                "modified_date": mod_datetime.strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            return {"error": str(e)}

    def validate_dataset(self, dataset_name: str) -> bool:
        """
        驗證資料集是否有效
        :param dataset_name: 資料集名稱
        :return: True 如果有效，否則 False
        """
        dataset_path = os.path.join(self.data_dir, dataset_name)
        return os.path.exists(dataset_path) and dataset_name.endswith('.csv')
