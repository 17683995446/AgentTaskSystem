from typing import Optional
from ..interfaces.i_agent_runtime import IAgentRuntime
from ..task_schedule.impl.task_schedule_impl import TaskScheduleImpl
from ..task_runner.impl.task_runner_impl import TaskRunnerImpl
from AgentTaskSystem.task_core.task_define.impl.task_define_impl import TaskDefineImpl
from AgentTaskSystem.task_core.task_state.impl.task_state_impl import TaskStateImpl


class AgentRuntimeImpl(IAgentRuntime):

    def __init__(self):
        self._is_running = False
        self._task_define = TaskDefineImpl()
        self._task_state = TaskStateImpl()
        self._task_schedule = TaskScheduleImpl()
        self._task_runner = TaskRunnerImpl()

    def initialize(self) -> bool:
        self._is_running = True
        return True

    def submit_task(self, task_data: dict) -> Optional[str]:
        if not self._is_running:
            return None
        task_name = task_data.get("name", "default")
        params = task_data.get("params", [])
        result = self._task_define.create_task(task_name, params)
        if result.success:
            self._task_state.set_state(result.task_id, self._task_state.get_state(result.task_id))
        return result.task_id if result.success else None

    def get_task_status(self, task_id: str) -> Optional[str]:
        state = self._task_state.get_state(task_id)
        return state.value if state else None

    def shutdown(self) -> None:
        self._is_running = False

    def is_running(self) -> bool:
        return self._is_running
