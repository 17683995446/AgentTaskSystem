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
from ...task_core.task_define.impl.TaskValidatorImpl import TaskValidatorImpl
from ..task_schedule.interfaces.SchedulePriority import SchedulePriority
from ..task_schedule.interfaces.ScheduleRequestDto import ScheduleRequestDto
from AgentTaskSystem.common.utils import get_current_timestamp
from AgentTaskSystem.common.Logger import get_logger


class AgentRuntimeImpl(IAgentRuntime):
    def __init__(self):
        self._is_running = False
        self._is_initialized = False
        self._task_define = TaskDefineImpl()
        self._task_state = TaskStateImpl()
        self._task_schedule = TaskScheduleImpl()
        self._task_runner = TaskRunnerImpl()
        self._validator = TaskValidatorImpl()
        self._logger = get_logger()
        self._logger.info("AgentRuntime", "AgentRuntimeImpl initialized")

    def initialize(self) -> bool:
        self._logger.info("AgentRuntime", "initialize() called")
        if self._is_initialized and self._is_running:
            self._logger.warn("AgentRuntime", "Already initialized and running, returning True")
            return True
        self._is_running = True
        self._is_initialized = True
        self._logger.info("AgentRuntime", f"System started, is_running={self._is_running}")
        return True

    def submit_task(self, task_data: dict) -> Optional[str]:
        self._logger.info("AgentRuntime", f"submit_task() called with data={task_data}")
        if not self._is_running:
            self._logger.error("AgentRuntime", "Runtime not running, cannot submit task")
            return None
        if task_data is None:
            self._logger.error("AgentRuntime", "task_data is None")
            return None
        if not isinstance(task_data, dict):
            self._logger.error("AgentRuntime", f"task_data is not dict, got {type(task_data)}")
            return None

        task_name = task_data.get("name", "default")
        params = task_data.get("params", ())
        self._logger.debug("AgentRuntime", f"Extracted name={task_name}, params={params}")

        if not self._validator.validate_name(task_name):
            self._logger.error("AgentRuntime", f"Task name validation failed: {task_name}")
            return None
        if not self._validator.validate_params(params):
            self._logger.error("AgentRuntime", f"Task params validation failed: {params}")
            return None

        result = self._task_define.create_task(task_data)
        self._logger.debug("AgentRuntime", f"create_task result: success={result.success}, task_id={result.task_id}")
        if not result.success:
            self._logger.error("AgentRuntime", "create_task failed")
            return None

        transition = self._task_state.set_state(result.task_id, TaskStateEnum.PENDING)
        self._logger.debug("AgentRuntime", f"State set to PENDING: {transition}")

        schedule_request = ScheduleRequestDto(
            task_id=result.task_id,
            priority=SchedulePriority.NORMAL,
            scheduled_at=get_current_timestamp()
        )
        schedule_result = self._task_schedule.add_task(schedule_request)
        self._logger.debug("AgentRuntime", f"Schedule result: {schedule_result}")

        if not schedule_result.success:
            self._logger.error("AgentRuntime", f"Schedule failed: {schedule_result.message}")
            self._task_state.set_state(result.task_id, TaskStateEnum.FAILED)
            return None

        self._logger.info("AgentRuntime", f"Task submitted successfully: {result.task_id}")
        return result.task_id

    def get_task_status(self, task_id: str) -> Optional[str]:
        self._logger.debug("AgentRuntime", f"get_task_status() called for {task_id}")
        if not task_id or not isinstance(task_id, str):
            self._logger.error("AgentRuntime", f"Invalid task_id: {task_id}")
            return None
        state = self._task_state.get_state(task_id)
        status = state.value if state else None
        self._logger.debug("AgentRuntime", f"Task {task_id} status: {status}")
        return status

    def shutdown(self) -> None:
        self._logger.info("AgentRuntime", "shutdown() called")
        if not self._is_running:
            self._logger.warn("AgentRuntime", "Already shutdown")
            return
        self._is_running = False
        self._logger.info("AgentRuntime", "System shutdown complete")

    def is_running(self) -> bool:
        return self._is_running
