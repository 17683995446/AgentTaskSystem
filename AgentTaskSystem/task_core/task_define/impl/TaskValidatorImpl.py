"""
TaskValidatorImpl - 任务校验实现
"""

from ..interfaces.ITaskValidator import ITaskValidator
from AgentTaskSystem.common import MAX_TASK_PARAMS, MAX_TASK_NAME_LENGTH


class TaskValidatorImpl(ITaskValidator):
    def validate_name(self, name: str) -> bool:
        if not name or not isinstance(name, str):
            return False
        if len(name) > MAX_TASK_NAME_LENGTH:
            return False
        return True

    def validate_params(self, params: tuple) -> bool:
        if not isinstance(params, tuple):
            return False
        if len(params) > MAX_TASK_PARAMS:
            return False
        return True
