"""
TaskParamDto - 任务参数DTO
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TaskParamDto:
    name: str
    params: tuple
