import uuid
from typing import Optional
from ..interfaces.i_task_define import (
    ITaskDefine,
    TaskParam,
    TaskResult
)


class TaskDefineImpl(ITaskDefine):

    def __init__(self):
        self._tasks = {}

    def create_task(self, name: str, params: list[TaskParam]) -> TaskResult:
        task_id = str(uuid.uuid4())
        self._tasks[task_id] = {
            "name": name,
            "params": params
        }
        return TaskResult(success=True, task_id=task_id)

    def validate_task(self, task_id: str) -> bool:
        return task_id in self._tasks

    def get_task_info(self, task_id: str) -> Optional[dict]:
        return self._tasks.get(task_id)
