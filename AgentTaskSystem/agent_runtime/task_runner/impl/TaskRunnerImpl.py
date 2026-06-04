"""
TaskRunnerImpl - 任务执行实现
"""

from ..interfaces.ITaskRunner import ITaskRunner
from ..interfaces.ExecuteRequestDto import ExecuteRequestDto
from ..interfaces.ExecuteResultDto import ExecuteResultDto
from ..interfaces.TaskProgressDto import TaskProgressDto
from AgentTaskSystem.common.Provider import Provider
from AgentTaskSystem.common.Logger import get_logger


class TaskRunnerImpl(ITaskRunner):
    def __init__(self):
        self._progress = {}
        self._cancelled = set()
        self._snapshot = None
        self._logger = get_logger()
        self._logger.info("TaskRunner", "TaskRunnerImpl initialized")
        self._load_from_snapshot()

    def _get_snapshot(self):
        if not self._snapshot:
            provider = Provider()
            self._snapshot = provider.get("snapshot")
        return self._snapshot

    def _load_from_snapshot(self):
        self._logger.debug("TaskRunner", "_load_from_snapshot() called")
        snapshot = self._get_snapshot()
        if snapshot and snapshot.exists("task_runner"):
            try:
                data = snapshot.load("task_runner")
                self._progress = data.get("progress", {})
                self._cancelled = set(data.get("cancelled", []))
                self._logger.info("TaskRunner", f"Loaded {len(self._progress)} progress entries")
            except Exception as e:
                self._logger.error("TaskRunner", f"Failed to load snapshot: {e}")
                self._progress = {}
                self._cancelled = set()

    def _save_to_snapshot(self):
        self._logger.debug("TaskRunner", "_save_to_snapshot() called")
        snapshot = self._get_snapshot()
        if snapshot:
            try:
                data = {
                    "progress": self._progress,
                    "cancelled": list(self._cancelled)
                }
                snapshot.save("task_runner", data)
                self._logger.debug("TaskRunner", "Snapshot saved successfully")
            except Exception as e:
                self._logger.error("TaskRunner", f"Failed to save snapshot: {e}")

    def execute_task(self, request: ExecuteRequestDto) -> ExecuteResultDto:
        self._logger.info("TaskRunner", f"execute_task() called: request={request}")
        if request is None:
            self._logger.error("TaskRunner", "request is None")
            return ExecuteResultDto(success=False, task_id="", result=None, error="request is None")
        if not isinstance(request, ExecuteRequestDto):
            self._logger.error("TaskRunner", f"Invalid request type: {type(request)}")
            return ExecuteResultDto(success=False, task_id="", result=None, error="Invalid request type")
        if not request.task_id:
            self._logger.error("TaskRunner", "task_id is empty")
            return ExecuteResultDto(success=False, task_id="", result=None, error="task_id is empty")

        if request.task_id in self._cancelled:
            self._logger.warn("TaskRunner", f"Task {request.task_id} was cancelled")
            return ExecuteResultDto(
                success=False,
                task_id=request.task_id,
                result=None,
                error="Task cancelled"
            )

        self._progress[request.task_id] = 50
        self._save_to_snapshot()
        self._logger.info("TaskRunner", f"Task {request.task_id} progress: 50%")

        try:
            result = self._execute(request.params)
            self._progress[request.task_id] = 100
            self._save_to_snapshot()
            self._logger.info("TaskRunner", f"Task {request.task_id} completed successfully")
            return ExecuteResultDto(
                success=True,
                task_id=request.task_id,
                result=result,
                error=""
            )
        except Exception as e:
            self._logger.error("TaskRunner", f"Task {request.task_id} failed: {e}")
            return ExecuteResultDto(
                success=False,
                task_id=request.task_id,
                result=None,
                error=str(e)
            )

    def _execute(self, params: tuple) -> object:
        self._logger.debug("TaskRunner", f"_execute() called with params={params}")
        return f"Executed with params: {params}"

    def cancel_task(self, task_id: str) -> bool:
        self._logger.info("TaskRunner", f"cancel_task() called: {task_id}")
        if not task_id or not isinstance(task_id, str):
            self._logger.error("TaskRunner", f"Invalid task_id: {task_id}")
            return False
        self._cancelled.add(task_id)
        self._save_to_snapshot()
        self._logger.info("TaskRunner", f"Task {task_id} cancelled")
        return True

    def get_progress(self, task_id: str) -> TaskProgressDto:
        self._logger.debug("TaskRunner", f"get_progress() called: {task_id}")
        if not task_id or not isinstance(task_id, str):
            self._logger.error("TaskRunner", f"Invalid task_id: {task_id}")
            return TaskProgressDto(task_id="", progress=0, message="Invalid task_id")
        progress = self._progress.get(task_id, 0)
        is_cancelled = task_id in self._cancelled
        message = "Cancelled" if is_cancelled else ("Completed" if progress == 100 else "In progress")
        self._logger.debug("TaskRunner", f"Task {task_id} progress: {progress}%, message={message}")
        return TaskProgressDto(
            task_id=task_id,
            progress=progress,
            message=message
        )

    def reset_task(self, task_id: str) -> bool:
        self._logger.info("TaskRunner", f"reset_task() called: {task_id}")
        if not task_id or not isinstance(task_id, str):
            return False
        self._cancelled.discard(task_id)
        self._progress.pop(task_id, None)
        self._save_to_snapshot()
        self._logger.info("TaskRunner", f"Task {task_id} reset")
        return True
