from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class ExecuteRequestDto:
    task_id: str
    params: dict[str, Any]
    timeout_seconds: int = 300


@dataclass(frozen=True)
class ExecuteResultDto:
    task_id: str
    success: bool
    result: Optional[Any] = None
    error_message: Optional[str] = None
    execution_time_ms: int = 0


@dataclass(frozen=True)
class TaskProgressDto:
    task_id: str
    progress: float
    current_step: str
    estimated_remaining_ms: int = 0
