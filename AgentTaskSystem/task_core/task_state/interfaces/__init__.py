"""
TaskState interfaces - 任务状态接口模块
"""

from .ITaskState import ITaskState
from .TaskStateEnum import TaskStateEnum
from .TaskStateDto import TaskStateDto
from .StateTransitionDto import StateTransitionDto

__all__ = [
    "ITaskState",
    "TaskStateEnum",
    "TaskStateDto",
    "StateTransitionDto"
]
