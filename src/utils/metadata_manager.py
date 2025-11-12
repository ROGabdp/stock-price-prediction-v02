import json
import os
from typing import List, Dict, Any

class MetadataManager:
    def __init__(self, metadata_file='metadata.json', metadata_dir='models'):
        self.metadata_dir = metadata_dir
        os.makedirs(self.metadata_dir, exist_ok=True)
        self.metadata_file_path = os.path.join(self.metadata_dir, metadata_file)
        self.metadata: List[Dict[str, Any]] = self._load_metadata()

    def _load_metadata(self) -> List[Dict[str, Any]]:
        """
        從 JSON 檔案載入所有模型元資料。
        """
        if os.path.exists(self.metadata_file_path):
            with open(self.metadata_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def _save_metadata(self):
        """
        將所有模型元資料儲存到 JSON 檔案。
        """
        with open(self.metadata_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=4)

    def add_metadata(self, new_metadata: Dict[str, Any]):
        """
        添加新的模型元資料。
        :param new_metadata: 包含模型元資料的字典。
        """
        self.metadata.append(new_metadata)
        self._save_metadata()
        print(f"已添加模型元資料: {new_metadata.get('model_id', '未知ID')}")

    def get_all_metadata(self) -> List[Dict[str, Any]]:
        """
        獲取所有模型元資料。
        """
        return self.metadata

    def get_metadata_by_id(self, model_id: str) -> Dict[str, Any] | None:
        """
        根據模型 ID 獲取單個模型元資料。
        """
        for meta in self.metadata:
            if meta.get('model_id') == model_id:
                return meta
        return None

    def update_metadata(self, model_id: str, updates: Dict[str, Any]):
        """
        更新指定模型 ID 的元資料。
        """
        for i, meta in enumerate(self.metadata):
            if meta.get('model_id') == model_id:
                self.metadata[i].update(updates)
                self._save_metadata()
                print(f"已更新模型元資料: {model_id}")
                return True
        print(f"未找到模型 ID 為 '{model_id}' 的元資料進行更新。")
        return False

    def delete_metadata(self, model_id: str):
        """
        刪除指定模型 ID 的元資料。
        """
        initial_len = len(self.metadata)
        self.metadata = [meta for meta in self.metadata if meta.get('model_id') != model_id]
        if len(self.metadata) < initial_len:
            self._save_metadata()
            print(f"已刪除模型元資料: {model_id}")
            return True
        print(f"未找到模型 ID 為 '{model_id}' 的元資料進行刪除。")
        return False

