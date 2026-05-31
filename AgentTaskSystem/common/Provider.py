"""
Provider - 服务提供者
"""

from typing import Dict, Optional, Any
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class Provider:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._services: Dict[str, Any] = {}
            self._initialized = True

    def register(self, key: str, service: Any):
        self._services[key] = service

    def get(self, key: str) -> Optional[Any]:
        return self._services.get(key)

    def has(self, key: str) -> bool:
        return key in self._services

    def clear(self):
        self._services.clear()


def initialize_services() -> Provider:
    """
    初始化所有服务并注册到Provider
    """
    provider = Provider()
    
    from AgentTaskSystem.task_core.task_define.impl.TaskDefineImpl import TaskDefineImpl
    from AgentTaskSystem.task_core.task_state.impl.TaskStateImpl import TaskStateImpl
    from AgentTaskSystem.agent_runtime.task_schedule.impl.TaskScheduleImpl import TaskScheduleImpl
    from AgentTaskSystem.agent_runtime.task_runner.impl.TaskRunnerImpl import TaskRunnerImpl
    from AgentTaskSystem.agent_runtime.impl.AgentRuntimeImpl import AgentRuntimeImpl
    from AgentTaskSystem.common.impl.SnapshotImpl import SnapshotImpl
    
    provider.register("task_define", TaskDefineImpl())
    provider.register("task_state", TaskStateImpl())
    provider.register("task_schedule", TaskScheduleImpl())
    provider.register("task_runner", TaskRunnerImpl())
    provider.register("agent_runtime", AgentRuntimeImpl())
    provider.register("snapshot", SnapshotImpl())
    
    return provider
