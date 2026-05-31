"""
ExecuteRequestDto - 执行请求DTO
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecuteRequestDto:
    task_id: str
    params: tuple
