"""
TaskRunner interfaces - 任务执行接口模块
"""

from .ITaskRunner import ITaskRunner
from .ExecuteRequestDto import ExecuteRequestDto
from .ExecuteResultDto import ExecuteResultDto
from .TaskProgressDto import TaskProgressDto

__all__ = [
    "ITaskRunner",
    "ExecuteRequestDto",
    "ExecuteResultDto",
    "TaskProgressDto"
]
