"""
TaskCore - 任务核心模块
"""

from .task_define import (
    ITaskDefine,
    ITaskValidator,
    TaskParamDto,
    TaskResultDto,
    TaskInfoDto
)
from .task_state import (
    ITaskState,
    TaskStateEnum,
    TaskStateDto,
    StateTransitionDto
)

__all__ = [
    "ITaskDefine",
    "ITaskValidator",
    "TaskParamDto",
    "TaskResultDto",
    "TaskInfoDto",
    "ITaskState",
    "TaskStateEnum",
    "TaskStateDto",
    "StateTransitionDto"
]
