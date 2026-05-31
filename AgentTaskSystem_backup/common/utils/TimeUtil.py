import time
from typing import Optional


class TimeUtil:

    @staticmethod
    def get_timestamp() -> int:
        return int(time.time())

    @staticmethod
    def get_timestamp_ms() -> int:
        return int(time.time() * 1000)

    @staticmethod
    def format_timestamp(ts: int) -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))

    @staticmethod
    def is_expired(timestamp: int, ttl_seconds: int) -> bool:
        return (TimeUtil.get_timestamp() - timestamp) >= ttl_seconds
