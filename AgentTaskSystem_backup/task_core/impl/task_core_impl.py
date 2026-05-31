from AgentTaskSystem.task_core.task_define.impl.task_define_impl import TaskDefineImpl
from AgentTaskSystem.task_core.task_state.impl.task_state_impl import TaskStateImpl


class TaskCoreImpl:

    def __init__(self):
        self._task_define = TaskDefineImpl()
        self._task_state = TaskStateImpl()

    @property
    def task_define(self):
        return self._task_define

    @property
    def task_state(self):
        return self._task_state
