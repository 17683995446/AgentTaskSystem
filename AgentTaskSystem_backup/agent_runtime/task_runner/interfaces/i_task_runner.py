from abc import ABC, abstractmethod
from typing import Optional, Any, Dict


class ITaskRunner(ABC):

    @abstractmethod
    def execute(self, task_id: str, params: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def get_result(self, task_id: str) -> Optional[Any]:
        pass

    @abstractmethod
    def is_running(self, task_id: str) -> bool:
        pass

    @abstractmethod
    def cancel(self, task_id: str) -> bool:
        pass

    @abstractmethod
    def get_progress(self, task_id: str) -> float:
        pass
