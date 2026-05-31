from enum import IntEnum


class ErrorCode(IntEnum):
    SUCCESS = 0
    TASK_NOT_FOUND = 1001
    TASK_ALREADY_EXISTS = 1002
    INVALID_TASK_PARAMS = 1003
    INVALID_STATE_TRANSITION = 2001
    SCHEDULE_QUEUE_FULL = 3001
    SCHEDULE_QUEUE_EMPTY = 3002
    RUNNER_EXECUTION_FAILED = 4001
    RUNNER_TIMEOUT = 4002
    SYSTEM_NOT_INITIALIZED = 5001
    SYSTEM_ALREADY_RUNNING = 5002
    UNKNOWN_ERROR = 9999


class AgentTaskException(Exception):

    def __init__(self, code: ErrorCode, message: str):
        self._code = code
        self._message = message
        super().__init__(f"[{code.value}] {message}")

    @property
    def code(self) -> ErrorCode:
        return self._code

    @property
    def message(self) -> str:
        return self._message
