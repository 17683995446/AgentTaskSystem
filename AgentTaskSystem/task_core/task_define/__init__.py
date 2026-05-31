"""
TaskDefine - 任务定义模块
"""

from .interfaces import (
    ITaskDefine,
    ITaskValidator,
    TaskParamDto,
    TaskResultDto,
    TaskInfoDto
)

__all__ = [
    "ITaskDefine",
    "ITaskValidator",
    "TaskParamDto",
    "TaskResultDto",
    "TaskInfoDto"
]
