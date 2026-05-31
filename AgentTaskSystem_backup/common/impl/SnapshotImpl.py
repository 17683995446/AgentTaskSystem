import json
from typing import Any, Optional
from AgentTaskSystem.common.interfaces.i_snapshot import ISnapshot


class SnapshotImpl(ISnapshot):

    def __init__(self, storage_path: str = "/tmp/snapshots"):
        self._storage_path = storage_path
        self._cache = {}

    def save(self, key: str, data: Any) -> bool:
        try:
            self._cache[key] = data
            return True
        except Exception:
            return False

    def load(self, key: str) -> Optional[Any]:
        return self._cache.get(key)

    def delete(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def exists(self, key: str) -> bool:
        return key in self._cache
