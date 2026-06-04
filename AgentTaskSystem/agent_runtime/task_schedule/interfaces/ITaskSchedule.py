"""
ITaskSchedule - 任务调度接口

职责：管理任务调度队列，支持优先级排序
"""

from abc import ABC, abstractmethod
from .ScheduleRequestDto import ScheduleRequestDto
from .ScheduleResultDto import ScheduleResultDto


class ITaskSchedule(ABC):
    """任务调度接口，提供优先级队列管理能力"""

    @abstractmethod
    def add_task(self, request: ScheduleRequestDto) -> ScheduleResultDto:
        """
        添加任务到调度队列

        Args:
            request: 调度请求，包含 task_id, priority, scheduled_at

        Returns:
            ScheduleResultDto: 包含 success, task_id, position, message

        Raises:
            ValueError: request 为 None 或 task_id 为空
        """
        pass

    @abstractmethod
    def get_next_task(self) -> ScheduleRequestDto:
        """
        获取下一个待执行的任务（按优先级）

        Returns:
            ScheduleRequestDto: 下一个任务，队列为空返回 None
        """
        pass

    @abstractmethod
    def get_queue_size(self) -> int:
        """
        获取当前队列大小

        Returns:
            int: 队列中的任务数量
        """
        pass

    @abstractmethod
    def has_task(self, task_id: str) -> bool:
        """
        检查任务是否在队列中

        Args:
            task_id: 任务唯一标识符

        Returns:
            bool: 任务在队列中返回 True
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        清空调度队列

        注意：此操作不可恢复，所有待调度任务将被移除
        """
        pass
