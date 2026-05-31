from typing import Any, Dict


class SystemConfig:
    _instance = None
    _config: Dict[str, Any] = {}

    def __init__(self):
        self._config = {
            "max_task_params": 10,
            "max_task_name_length": 64,
            "max_queue_size": 1000,
            "default_timeout": 300,
            "snapshot_enabled": True,
            "log_level": "INFO"
        }

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get(self, key: str) -> Any:
        return self._config.get(key)

    def set(self, key: str, value: Any) -> None:
        self._config[key] = value

    def get_all(self) -> Dict[str, Any]:
        return self._config.copy()
