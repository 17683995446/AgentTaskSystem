"""
TaskDefine interfaces - 任务定义接口模块
"""

from .ITaskDefine import ITaskDefine
from .ITaskValidator import ITaskValidator
from .TaskParamDto import TaskParamDto
from .TaskResultDto import TaskResultDto
from .TaskInfoDto import TaskInfoDto

__all__ = [
    "ITaskDefine",
    "ITaskValidator",
    "TaskParamDto",
    "TaskResultDto",
    "TaskInfoDto"
]
