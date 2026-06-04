"""
ISnapshot - 快照接口

职责：提供数据持久化能力，支持状态保存和恢复
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class ISnapshot(ABC):
    """快照接口，提供键值对持久化存储"""

    @abstractmethod
    def save(self, key: str, data: Dict[str, Any]) -> bool:
        """
        保存数据到快照

        Args:
            key: 快照键名，非空字符串
            data: 要保存的字典数据

        Returns:
            bool: 保存成功返回 True

        Raises:
            ValueError: key 为空或 data 为 None
        """
        pass

    @abstractmethod
    def load(self, key: str) -> Dict[str, Any]:
        """
        从快照加载数据

        Args:
            key: 快照键名

        Returns:
            dict: 加载的数据，不存在或失败返回空字典
        """
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """
        检查快照是否存在

        Args:
            key: 快照键名

        Returns:
            bool: 存在返回 True
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """
        删除快照

        Args:
            key: 快照键名

        Returns:
            bool: 删除成功返回 True
        """
        pass
