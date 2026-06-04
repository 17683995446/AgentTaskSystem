"""
Logger - 系统日志模块
"""

import sys
from datetime import datetime
from enum import IntEnum


class LogLevel(IntEnum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3


class Logger:
    _instance = None
    _level = LogLevel.DEBUG

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def set_level(self, level: LogLevel):
        self._level = level

    def _log(self, level: LogLevel, module: str, message: str):
        if level < self._level:
            return
        timestamp = datetime.now().isoformat()
        level_name = level.name
        print(f"[{timestamp}] [{level_name}] [{module}] {message}", file=sys.stderr)

    def debug(self, module: str, message: str):
        self._log(LogLevel.DEBUG, module, message)

    def info(self, module: str, message: str):
        self._log(LogLevel.INFO, module, message)

    def warn(self, module: str, message: str):
        self._log(LogLevel.WARN, module, message)

    def error(self, module: str, message: str):
        self._log(LogLevel.ERROR, module, message)


def get_logger() -> Logger:
    return Logger()
