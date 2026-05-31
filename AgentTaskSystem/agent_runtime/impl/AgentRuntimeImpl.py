"""
AgentRuntimeImpl - 代理运行时实现
"""

from typing import Optional
from ..interfaces.IAgentRuntime import IAgentRuntime
from ..task_schedule.impl.TaskScheduleImpl import TaskScheduleImpl
from ..task_runner.impl.TaskRunnerImpl import TaskRunnerImpl
from ...task_core.task_define.impl.TaskDefineImpl import TaskDefineImpl
from ...task_core.task_state.impl.TaskStateImpl import TaskStateImpl
from ...task_core.task_state.interfaces.TaskStateEnum import TaskStateEnum
from ...task_core.task_state.interfaces.TaskStateDto import TaskStateDto
from ..task_schedule.interfaces.SchedulePriority import SchedulePriority
from ..task_schedule.interfaces.ScheduleRequestDto import ScheduleRequestDto
from ..task_runner.interfaces.ExecuteRequestDto import ExecuteRequestDto
from AgentTaskSystem.common.utils import get_current_timestamp


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
        params = task_data.get("params", ())
        result = self._task_define.create_task(task_data)
        if not result.success:
            return None
        self._task_state.set_state(result.task_id, TaskStateEnum.PENDING)
        schedule_request = ScheduleRequestDto(
            task_id=result.task_id,
            priority=SchedulePriority.NORMAL,
            scheduled_at=get_current_timestamp()
        )
        self._task_schedule.add_task(schedule_request)
        return result.task_id

    def get_task_status(self, task_id: str) -> Optional[str]:
        state = self._task_state.get_state(task_id)
        return state.value if state else None

    def shutdown(self) -> None:
        self._is_running = False

    def is_running(self) -> bool:
        return self._is_running
