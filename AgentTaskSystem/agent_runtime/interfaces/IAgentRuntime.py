"""
IAgentRuntime - 代理运行时接口

职责：系统主入口，负责任务提交、状态查询和生命周期管理
"""

from abc import ABC, abstractmethod
from typing import Optional


class IAgentRuntime(ABC):
    """Agent运行时接口，提供一站式任务管理能力"""

    @abstractmethod
    def initialize(self) -> bool:
        """
        初始化运行时

        Returns:
            bool: 初始化成功返回 True

        Note:
            幂等操作，多次调用不会重复初始化
        """
        pass

    @abstractmethod
    def submit_task(self, task_data: dict) -> Optional[str]:
        """
        提交任务到系统

        Args:
            task_data: 任务数据字典，格式:
                {
                    "name": str,      # 任务名称
                    "params": tuple   # 任务参数
                }

        Returns:
            str: 任务ID，提交失败返回 None

        Raises:
            无异常，所有错误内部处理并返回 None
        """
        pass

    @abstractmethod
    def get_task_status(self, task_id: str) -> Optional[str]:
        """
        获取任务状态

        Args:
            task_id: 任务唯一标识符

        Returns:
            str: 状态字符串 (pending/running/completed/failed)，未找到返回 None
        """
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """
        关闭运行时

        Note:
            幂等操作，多次调用不会报错
        """
        pass

    @abstractmethod
    def is_running(self) -> bool:
        """
        检查运行时是否正在运行

        Returns:
            bool: 运行中返回 True
        """
        pass
