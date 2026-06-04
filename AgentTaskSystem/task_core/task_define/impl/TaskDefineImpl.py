"""
TaskDefineImpl - 任务定义实现
"""

from ..interfaces.ITaskDefine import ITaskDefine
from ..interfaces.TaskParamDto import TaskParamDto
from ..interfaces.TaskResultDto import TaskResultDto
from AgentTaskSystem.common.utils import generate_task_id
from AgentTaskSystem.common.Logger import get_logger


class TaskDefineImpl(ITaskDefine):
    def __init__(self):
        self._tasks = {}
        self._logger = get_logger()
        self._logger.info("TaskDefine", "TaskDefineImpl initialized")

    def create_task(self, task_data: dict):
        self._logger.info("TaskDefine", f"create_task() called with data={task_data}")
        if task_data is None:
            self._logger.error("TaskDefine", "task_data is None")
            return TaskResultDto(success=False, task_id="", message="task_data is None")
        if not isinstance(task_data, dict):
            self._logger.error("TaskDefine", f"task_data is not dict, got {type(task_data)}")
            return TaskResultDto(success=False, task_id="", message="task_data must be dict")

        task_id = generate_task_id()
        name = task_data.get("name", "default")
        params = task_data.get("params", ())
        self._logger.debug("TaskDefine", f"Generated task_id={task_id}, name={name}, params={params}")

        if not isinstance(name, str):
            self._logger.error("TaskDefine", f"name is not str, got {type(name)}")
            return TaskResultDto(success=False, task_id="", message="name must be str")
        if not isinstance(params, tuple):
            self._logger.error("TaskDefine", f"params is not tuple, got {type(params)}")
            return TaskResultDto(success=False, task_id="", message="params must be tuple")

        self._tasks[task_id] = TaskParamDto(name=name, params=params)
        self._logger.info("TaskDefine", f"Task created: {task_id}")
        return TaskResultDto(success=True, task_id=task_id, message="Task created")

    def validate_task(self, task_id: str) -> bool:
        self._logger.debug("TaskDefine", f"validate_task() called for {task_id}")
        if not task_id or not isinstance(task_id, str):
            self._logger.error("TaskDefine", f"Invalid task_id: {task_id}")
            return False
        exists = task_id in self._tasks
        self._logger.debug("TaskDefine", f"Task {task_id} exists: {exists}")
        return exists

    def get_task(self, task_id: str):
        self._logger.debug("TaskDefine", f"get_task() called for {task_id}")
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> dict:
        self._logger.debug("TaskDefine", f"get_all_tasks() called, count={len(self._tasks)}")
        return self._tasks.copy()
