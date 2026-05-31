"""
TaskStateEnum - 任务状态枚举
"""

from enum import Enum


class TaskStateEnum(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
