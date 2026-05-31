from AgentTaskSystem.task_core.task_define.impl.task_define_impl import TaskDefineImpl
from AgentTaskSystem.task_core.task_define.impl.task_validator_impl import TaskValidatorImpl
from AgentTaskSystem.task_core.task_state.impl.task_state_impl import TaskStateImpl
from AgentTaskSystem.agent_runtime.task_schedule.impl.task_schedule_impl import TaskScheduleImpl
from AgentTaskSystem.agent_runtime.task_runner.impl.task_runner_impl import TaskRunnerImpl
from AgentTaskSystem.agent_runtime.impl.agent_runtime_impl import AgentRuntimeImpl


class ServiceProvider:

    _instance = None

    def __init__(self):
        self._services = {}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register(self, key: str, service: object) -> None:
        self._services[key] = service

    def get(self, key: str) -> object:
        return self._services.get(key)

    def initialize(self) -> None:
        self.register("ITaskDefine", TaskDefineImpl())
        self.register("ITaskValidator", TaskValidatorImpl())
        self.register("ITaskState", TaskStateImpl())
        self.register("ITaskSchedule", TaskScheduleImpl())
        self.register("ITaskRunner", TaskRunnerImpl())
        self.register("IAgentRuntime", AgentRuntimeImpl())
