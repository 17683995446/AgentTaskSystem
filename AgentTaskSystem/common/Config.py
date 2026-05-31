"""
Config - 系统配置类
"""


class Config:
    def __init__(self):
        self._task_timeout = 300
        self._max_retries = 3
        self._enable_snapshot = True

    @property
    def task_timeout(self) -> int:
        return self._task_timeout

    @task_timeout.setter
    def task_timeout(self, value: int):
        self._task_timeout = value

    @property
    def max_retries(self) -> int:
        return self._max_retries

    @max_retries.setter
    def max_retries(self, value: int):
        self._max_retries = value

    @property
    def enable_snapshot(self) -> bool:
        return self._enable_snapshot

    @enable_snapshot.setter
    def enable_snapshot(self, value: bool):
        self._enable_snapshot = value
