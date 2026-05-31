from abc import ABC, abstractmethod
from typing import Optional


class IAgentRuntime(ABC):

    @abstractmethod
    def initialize(self) -> bool:
        pass

    @abstractmethod
    def submit_task(self, task_data: dict) -> Optional[str]:
        pass

    @abstractmethod
    def get_task_status(self, task_id: str) -> Optional[str]:
        pass

    @abstractmethod
    def shutdown(self) -> None:
        pass

    @abstractmethod
    def is_running(self) -> bool:
        pass
