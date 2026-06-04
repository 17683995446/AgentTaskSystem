"""
ITaskDefine - 任务定义接口

职责：负责任务的创建、验证和基本信息管理
"""

from abc import ABC, abstractmethod
from typing import Optional
from .TaskResultDto import TaskResultDto


class ITaskDefine(ABC):
    """任务定义接口，提供任务生命周期入口"""

    @abstractmethod
    def create_task(self, task_data: dict) -> TaskResultDto:
        """
        创建新任务

        Args:
            task_data: 任务数据字典，必须包含:
                - name: str, 任务名称，长度不超过 MAX_TASK_NAME_LENGTH
                - params: tuple, 任务参数，长度不超过 MAX_TASK_PARAMS

        Returns:
            TaskResultDto: 包含 success(bool), task_id(str), message(str)

        Raises:
            ValueError: 当 task_data 为 None 或类型不正确时
        """
        pass

    @abstractmethod
    def validate_task(self, task_id: str) -> bool:
        """
        验证任务是否存在

        Args:
            task_id: 任务唯一标识符

        Returns:
            bool: 任务存在返回 True，否则返回 False
        """
        pass

    @abstractmethod
    def get_task(self, task_id: str) -> Optional[dict]:
        """
        获取任务详细信息

        Args:
            task_id: 任务唯一标识符

        Returns:
            dict: 任务信息字典，不存在返回 None
        """
        pass

    @abstractmethod
    def get_all_tasks(self) -> dict:
        """
        获取所有任务

        Returns:
            dict: 以 task_id 为键的任务字典
        """
        pass
