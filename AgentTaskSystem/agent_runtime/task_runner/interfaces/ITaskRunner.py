"""
ITaskRunner - 任务执行接口

职责：负责任务的实际执行、取消和进度跟踪
"""

from abc import ABC, abstractmethod
from .ExecuteRequestDto import ExecuteRequestDto
from .ExecuteResultDto import ExecuteResultDto
from .TaskProgressDto import TaskProgressDto


class ITaskRunner(ABC):
    """任务执行接口，提供任务执行控制能力"""

    @abstractmethod
    def execute_task(self, request: ExecuteRequestDto) -> ExecuteResultDto:
        """
        执行任务

        Args:
            request: 执行请求，包含 task_id, params

        Returns:
            ExecuteResultDto: 包含 success, task_id, result, error

        Raises:
            ValueError: request 为 None 或 task_id 为空
        """
        pass

    @abstractmethod
    def cancel_task(self, task_id: str) -> bool:
        """
        取消任务

        Args:
            task_id: 任务唯一标识符

        Returns:
            bool: 取消成功返回 True
        """
        pass

    @abstractmethod
    def get_progress(self, task_id: str) -> TaskProgressDto:
        """
        获取任务执行进度

        Args:
            task_id: 任务唯一标识符

        Returns:
            TaskProgressDto: 包含 task_id, progress(0-100), message
        """
        pass

    @abstractmethod
    def reset_task(self, task_id: str) -> bool:
        """
        重置任务状态（清除取消标记和进度）

        Args:
            task_id: 任务唯一标识符

        Returns:
            bool: 重置成功返回 True
        """
        pass
