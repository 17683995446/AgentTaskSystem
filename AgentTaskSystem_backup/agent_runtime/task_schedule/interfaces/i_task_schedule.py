from abc import ABC, abstractmethod
from typing import Optional
from AgentTaskSystem.agent_runtime.task_schedule.interfaces.schedule_priority import SchedulePriority


class ITaskSchedule(ABC):

    @abstractmethod
    def enqueue(self, task_id: str, priority: SchedulePriority) -> bool:
        pass

    @abstractmethod
    def dequeue(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_queue_size(self) -> int:
        pass

    @abstractmethod
    def is_full(self) -> bool:
        pass

    @abstractmethod
    def clear_queue(self) -> None:
        pass
