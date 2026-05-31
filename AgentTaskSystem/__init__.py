"""
AgentTaskSystem - 标准化 AI Agent 任务系统
"""

__version__ = "2.1.0"

from .common import (
    Provider,
    initialize_services,
    generate_task_id,
    get_current_timestamp
)
from .task_core import (
    ITaskDefine,
    ITaskState,
    TaskStateEnum
)
from .agent_runtime import (
    IAgentRuntime,
    ITaskSchedule,
    ITaskRunner,
    SchedulePriority
)

__all__ = [
    "Provider",
    "initialize_services",
    "generate_task_id",
    "get_current_timestamp",
    "ITaskDefine",
    "ITaskState",
    "TaskStateEnum",
    "IAgentRuntime",
    "ITaskSchedule",
    "ITaskRunner",
    "SchedulePriority"
]
