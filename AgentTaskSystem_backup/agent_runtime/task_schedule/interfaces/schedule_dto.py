from dataclasses import dataclass
from typing import Optional
from AgentTaskSystem.agent_runtime.task_schedule.interfaces.schedule_priority import SchedulePriority


@dataclass(frozen=True)
class ScheduleRequestDto:
    task_id: str
    priority: SchedulePriority
    enqueued_at: int


@dataclass(frozen=True)
class ScheduleResultDto:
    success: bool
    task_id: str
    message: Optional[str] = None
