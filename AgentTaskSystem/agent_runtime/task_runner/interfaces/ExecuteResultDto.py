"""
ExecuteResultDto - 执行结果DTO
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecuteResultDto:
    success: bool
    task_id: str
    result: object
    error: str
