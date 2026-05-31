"""
Tests for TaskDefine module
"""

import pytest
from AgentTaskSystem.task_core.task_define.impl.TaskDefineImpl import TaskDefineImpl
from AgentTaskSystem.task_core.task_define.interfaces.TaskParamDto import TaskParamDto


def test_create_task():
    """Test creating a task"""
    task_define = TaskDefineImpl()
    result = task_define.create_task({"name": "test_task", "params": (1, 2, 3)})
    assert result.success is True
    assert result.task_id is not None
    assert len(result.task_id) > 0


def test_validate_task():
    """Test validating a task"""
    task_define = TaskDefineImpl()
    result = task_define.create_task({"name": "test_task", "params": (1, 2, 3)})
    is_valid = task_define.validate_task(result.task_id)
    assert is_valid is True


def test_validate_nonexistent_task():
    """Test validating a non-existent task"""
    task_define = TaskDefineImpl()
    is_valid = task_define.validate_task("nonexistent_task_id")
    assert is_valid is False


def test_create_task_without_name():
    """Test creating a task without name"""
    task_define = TaskDefineImpl()
    result = task_define.create_task({"params": (1, 2, 3)})
    assert result.success is True
