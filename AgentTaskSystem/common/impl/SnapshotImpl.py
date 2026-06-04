"""
SnapshotImpl - 快照实现
"""

import json
import os
import threading
from typing import Dict, Any
from ..interfaces.ISnapshot import ISnapshot
from ..Logger import get_logger


class SnapshotImpl(ISnapshot):
    def __init__(self, storage_dir: str = "./snapshots"):
        self._storage_dir = storage_dir
        self._lock = threading.Lock()
        self._logger = get_logger()
        self._logger.info("Snapshot", f"SnapshotImpl initialized, dir={storage_dir}")
        if not os.path.exists(storage_dir):
            try:
                os.makedirs(storage_dir, exist_ok=True)
                self._logger.info("Snapshot", f"Created snapshot directory: {storage_dir}")
            except Exception as e:
                self._logger.error("Snapshot", f"Failed to create directory: {e}")

    def _get_file_path(self, key: str) -> str:
        if not key or not isinstance(key, str):
            raise ValueError(f"Invalid key: {key}")
        safe_key = key.replace("/", "_").replace("\\", "_").replace("..", "_")
        return os.path.join(self._storage_dir, f"{safe_key}.json")

    def save(self, key: str, data: Dict[str, Any]) -> bool:
        self._logger.debug("Snapshot", f"save() called: key={key}")
        if data is None:
            self._logger.error("Snapshot", "data is None")
            return False
        try:
            file_path = self._get_file_path(key)
            with self._lock:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            self._logger.debug("Snapshot", f"Saved: {file_path}")
            return True
        except Exception as e:
            self._logger.error("Snapshot", f"Save failed: {e}")
            return False

    def load(self, key: str) -> Dict[str, Any]:
        self._logger.debug("Snapshot", f"load() called: key={key}")
        try:
            file_path = self._get_file_path(key)
            if not os.path.exists(file_path):
                self._logger.debug("Snapshot", f"File not found: {file_path}")
                return {}
            with self._lock:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            self._logger.debug("Snapshot", f"Loaded: {file_path}")
            return data
        except json.JSONDecodeError as e:
            self._logger.error("Snapshot", f"JSON decode error: {e}")
            return {}
        except Exception as e:
            self._logger.error("Snapshot", f"Load failed: {e}")
            return {}

    def exists(self, key: str) -> bool:
        try:
            exists = os.path.exists(self._get_file_path(key))
            self._logger.debug("Snapshot", f"exists({key}) = {exists}")
            return exists
        except Exception as e:
            self._logger.error("Snapshot", f"exists() failed: {e}")
            return False

    def delete(self, key: str) -> bool:
        self._logger.info("Snapshot", f"delete() called: key={key}")
        try:
            file_path = self._get_file_path(key)
            with self._lock:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self._logger.info("Snapshot", f"Deleted: {file_path}")
            return True
        except Exception as e:
            self._logger.error("Snapshot", f"Delete failed: {e}")
            return False
