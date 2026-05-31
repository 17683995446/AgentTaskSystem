"""
IdUtil - ID生成工具
"""

import uuid


def generate_task_id() -> str:
    return str(uuid.uuid4())


def generate_session_id() -> str:
    return str(uuid.uuid4())
