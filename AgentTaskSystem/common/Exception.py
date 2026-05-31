"""
Exception - 基础异常类
"""

from .Errors import ErrorCode


class AgentTaskException(Exception):
    def __init__(self, message: str, code: ErrorCode = ErrorCode.INTERNAL_ERROR):
        super().__init__(message)
        self._code = code

    @property
    def code(self) -> ErrorCode:
        return self._code
