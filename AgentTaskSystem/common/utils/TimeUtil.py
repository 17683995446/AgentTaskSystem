"""
TimeUtil - 时间工具
"""

from datetime import datetime


def get_current_timestamp() -> int:
    return int(datetime.now().timestamp())


def get_current_datetime() -> str:
    return datetime.now().isoformat()
