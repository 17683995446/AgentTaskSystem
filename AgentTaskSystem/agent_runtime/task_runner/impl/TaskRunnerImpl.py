"""
TaskRunnerImpl - 任务执行实现
"""

from ..interfaces.ITaskRunner import ITaskRunner
from ..interfaces.ExecuteRequestDto import ExecuteRequestDto
from ..interfaces.ExecuteResultDto import ExecuteResultDto
from ..interfaces.TaskProgressDto import TaskProgressDto
from AgentTaskSystem.common.Provider import Provider


class TaskRunnerImpl(ITaskRunner):
    def __init__(self):
        self._progress = {}
        self._cancelled = set()
        self._snapshot = None
        self._load_from_snapshot()

    def _get_snapshot(self):
        if not self._snapshot:
            provider = Provider()
            self._snapshot = provider.get("snapshot")
        return self._snapshot

    def _load_from_snapshot(self):
        snapshot = self._get_snapshot()
        if snapshot and snapshot.exists("task_runner"):
            data = snapshot.load("task_runner")
            self._progress = data.get("progress", {})
            self._cancelled = set(data.get("cancelled", []))

    def _save_to_snapshot(self):
        snapshot = self._get_snapshot()
        if snapshot:
            data = {
                "progress": self._progress,
                "cancelled": list(self._cancelled)
            }
            snapshot.save("task_runner", data)

    def execute_task(self, request: ExecuteRequestDto) -> ExecuteResultDto:
        if request.task_id in self._cancelled:
            return ExecuteResultDto(
                success=False,
                task_id=request.task_id,
                result=None,
                error="Task cancelled"
            )
        self._progress[request.task_id] = 50
        self._save_to_snapshot()
        try:
            result = self._execute(request.params)
            self._progress[request.task_id] = 100
            self._save_to_snapshot()
            return ExecuteResultDto(
                success=True,
                task_id=request.task_id,
                result=result,
                error=""
            )
        except Exception as e:
            return ExecuteResultDto(
                success=False,
                task_id=request.task_id,
                result=None,
                error=str(e)
            )

    def _execute(self, params: tuple) -> object:
        return f"Executed with params: {params}"

    def cancel_task(self, task_id: str) -> bool:
        self._cancelled.add(task_id)
        self._save_to_snapshot()
        return True

    def get_progress(self, task_id: str) -> TaskProgressDto:
        return TaskProgressDto(
            task_id=task_id,
            progress=self._progress.get(task_id, 0),
            message="In progress"
        )
