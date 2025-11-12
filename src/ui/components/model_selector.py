"""
模型選擇器元件
提供已訓練模型選擇的介面邏輯
"""

import os
import json
from typing import List, Dict, Optional


class ModelSelector:
    """
    模型選擇器，負責管理和提供可用模型的選項
    """

    def __init__(self, metadata_dir: str = None):
        """
        初始化模型選擇器
        :param metadata_dir: 模型元資料目錄路徑
        """
        if metadata_dir is None:
            metadata_dir = os.path.join(os.getcwd(), 'models', 'metadata')

        self.metadata_dir = metadata_dir

        # 確保元資料目錄存在
        if not os.path.exists(self.metadata_dir):
            os.makedirs(self.metadata_dir, exist_ok=True)

    def get_model_list(self) -> List[Dict[str, any]]:
        """
        取得所有已訓練模型的列表
        :return: 模型元資料列表
        """
        models = []

        try:
            # 讀取所有 JSON 元資料檔案
            files = os.listdir(self.metadata_dir)
            json_files = [f for f in files if f.endswith('.json')]

            for json_file in json_files:
                metadata_path = os.path.join(self.metadata_dir, json_file)
                try:
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)

                        # 如果 metadata 是列表（舊格式），取出所有模型
                        if isinstance(metadata, list):
                            models.extend(metadata)
                        # 如果是單一物件（新格式），直接添加
                        else:
                            models.append(metadata)
                except Exception as e:
                    print(f"讀取模型元資料 {json_file} 時發生錯誤: {e}")
                    continue

            # 依訓練日期排序（最新的在前）
            models.sort(key=lambda x: x.get('training_date', ''), reverse=True)

        except Exception as e:
            print(f"取得模型列表時發生錯誤: {e}")

        return models

    def get_dropdown_options(self) -> List[Dict[str, str]]:
        """
        取得下拉選單格式的選項
        :return: Dash Dropdown 元件所需的選項列表
        """
        models = self.get_model_list()

        options = []
        for model in models:
            # 跳過非字典類型的項目
            if not isinstance(model, dict):
                continue

            model_id = model.get('model_id', 'unknown')
            model_name = model.get('model_name', 'Unknown Model')

            # 添加訓練日期和效能資訊到標籤
            training_date = model.get('training_date', '')[:10] if model.get('training_date') else 'N/A'
            performance = model.get('performance_metrics', {})
            loss = performance.get('loss', 'N/A')

            # 格式化 loss 值
            if isinstance(loss, float):
                loss = f"{loss:.6f}"

            display_label = f"{model_name} (訓練日期: {training_date}, Loss: {loss})"

            options.append({
                'label': display_label,
                'value': model_id
            })

        return options

    def get_model_metadata(self, model_id: str) -> Optional[Dict[str, any]]:
        """
        根據模型 ID 取得模型元資料
        :param model_id: 模型 ID
        :return: 模型元資料字典，如果找不到則返回 None
        """
        # 先嘗試找獨立的模型 JSON 檔案
        metadata_path = os.path.join(self.metadata_dir, f"{model_id}.json")

        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    return metadata
            except Exception as e:
                print(f"讀取模型元資料時發生錯誤: {e}")

        # 如果找不到獨立檔案，從所有模型列表中查找
        all_models = self.get_model_list()
        for model in all_models:
            if model.get('model_id') == model_id:
                return model

        return None

    def format_model_info(self, metadata: Dict[str, any]) -> str:
        """
        格式化模型資訊為可讀的字串
        :param metadata: 模型元資料
        :return: 格式化的模型資訊字串
        """
        if not metadata:
            return "無模型資訊"

        info_parts = []

        # 基本資訊
        info_parts.append(f"模型名稱: {metadata.get('model_name', 'N/A')}")
        info_parts.append(f"模型 ID: {metadata.get('model_id', 'N/A')}")
        info_parts.append(f"訓練日期: {metadata.get('training_date', 'N/A')}")

        # 訓練資料集
        info_parts.append(f"訓練資料集: {metadata.get('dataset_name', 'N/A')}")
        info_parts.append(f"預測天數: {metadata.get('n_days', 'N/A')}")

        # 效能指標
        performance = metadata.get('performance_metrics', {})
        if performance:
            info_parts.append("效能指標:")
            for key, value in performance.items():
                info_parts.append(f"  - {key}: {value}")

        # 超參數
        hyperparams = metadata.get('hyperparameters', {})
        if hyperparams:
            info_parts.append("超參數:")
            for key, value in hyperparams.items():
                info_parts.append(f"  - {key}: {value}")

        return "\n".join(info_parts)

    def get_model_count(self) -> int:
        """
        取得已訓練模型的數量
        :return: 模型數量
        """
        return len(self.get_model_list())

    def filter_models_by_dataset(self, dataset_name: str) -> List[Dict[str, any]]:
        """
        根據訓練資料集過濾模型
        :param dataset_name: 資料集名稱
        :return: 使用指定資料集訓練的模型列表
        """
        all_models = self.get_model_list()
        filtered_models = [m for m in all_models if m.get('dataset_name') == dataset_name]
        return filtered_models
