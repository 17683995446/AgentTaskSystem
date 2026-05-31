"""
SchedulePriority - 调度优先级枚举
"""

from enum import IntEnum


class SchedulePriority(IntEnum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4
