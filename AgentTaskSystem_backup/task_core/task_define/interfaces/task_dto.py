from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TaskParamDto:
    name: str
    type_hint: str
    required: bool
    default_value: Optional[str] = None


@dataclass(frozen=True)
class TaskResultDto:
    success: bool
    task_id: str
    message: Optional[str] = None


@dataclass(frozen=True)
class TaskInfoDto:
    task_id: str
    name: str
    params: list[TaskParamDto]
    created_at: int
