"""
ITaskState - 任务状态接口

职责：管理任务状态的生命周期和状态转换
"""

from abc import ABC, abstractmethod
from typing import List
from .TaskStateEnum import TaskStateEnum
from .TaskStateDto import TaskStateDto
from .StateTransitionDto import StateTransitionDto


class ITaskState(ABC):
    """任务状态接口，提供状态查询和转换能力"""

    @abstractmethod
    def set_state(self, task_id: str, state: TaskStateEnum) -> StateTransitionDto:
        """
        设置任务状态

        Args:
            task_id: 任务唯一标识符，非空字符串
            state: 目标状态，必须是 TaskStateEnum 枚举值

        Returns:
            StateTransitionDto: 状态转换记录，包含 from_state, to_state, transitioned_at

        Raises:
            ValueError: task_id 为空或 state 类型不正确
        """
        pass

    @abstractmethod
    def get_state(self, task_id: str) -> TaskStateEnum:
        """
        获取任务当前状态

        Args:
            task_id: 任务唯一标识符

        Returns:
            TaskStateEnum: 任务当前状态，未记录的任务返回 PENDING
        """
        pass

    @abstractmethod
    def get_state_dto(self, task_id: str) -> TaskStateDto:
        """
        获取任务状态DTO

        Args:
            task_id: 任务唯一标识符

        Returns:
            TaskStateDto: 包含 task_id, state, updated_at
        """
        pass

    @abstractmethod
    def get_transitions(self, task_id: str) -> List[StateTransitionDto]:
        """
        获取任务的所有状态转换历史

        Args:
            task_id: 任务唯一标识符

        Returns:
            List[StateTransitionDto]: 状态转换记录列表
        """
        pass
