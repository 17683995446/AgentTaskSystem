"""
SnapshotImpl - 快照实现
"""

import json
import os
from typing import Dict, Any
from ..interfaces.ISnapshot import ISnapshot


class SnapshotImpl(ISnapshot):
    def __init__(self, storage_dir: str = "./snapshots"):
        self._storage_dir = storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir, exist_ok=True)

    def _get_file_path(self, key: str) -> str:
        safe_key = key.replace("/", "_").replace("\\", "_")
        return os.path.join(self._storage_dir, f"{safe_key}.json")

    def save(self, key: str, data: Dict[str, Any]) -> bool:
        try:
            file_path = self._get_file_path(key)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def load(self, key: str) -> Dict[str, Any]:
        try:
            file_path = self._get_file_path(key)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def exists(self, key: str) -> bool:
        return os.path.exists(self._get_file_path(key))

    def delete(self, key: str) -> bool:
        try:
            file_path = self._get_file_path(key)
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except Exception:
            return False
