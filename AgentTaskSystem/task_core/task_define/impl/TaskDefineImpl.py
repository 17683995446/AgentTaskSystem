"""
TaskDefineImpl - 任务定义实现
"""

from ..interfaces.ITaskDefine import ITaskDefine
from ..interfaces.TaskParamDto import TaskParamDto
from ..interfaces.TaskResultDto import TaskResultDto
from AgentTaskSystem.common.utils import generate_task_id


class TaskDefineImpl(ITaskDefine):
    def __init__(self):
        self._tasks = {}

    def create_task(self, task_data: dict):
        task_id = generate_task_id()
        name = task_data.get("name", "default")
        params = task_data.get("params", ())
        self._tasks[task_id] = TaskParamDto(name=name, params=params)
        return TaskResultDto(success=True, task_id=task_id, message="Task created")

    def validate_task(self, task_id: str) -> bool:
        return task_id in self._tasks
