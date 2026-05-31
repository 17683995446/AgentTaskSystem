"""
TaskCoreImpl - 任务核心实现
"""

from ..task_define.impl.TaskDefineImpl import TaskDefineImpl
from ..task_state.impl.TaskStateImpl import TaskStateImpl


class TaskCoreImpl:
    def __init__(self):
        self._task_define = TaskDefineImpl()
        self._task_state = TaskStateImpl()

    @property
    def task_define(self) -> TaskDefineImpl:
        return self._task_define

    @property
    def task_state(self) -> TaskStateImpl:
        return self._task_state
