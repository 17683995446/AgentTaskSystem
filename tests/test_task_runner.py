"""
Tests for TaskRunner module
"""

import pytest
from AgentTaskSystem.agent_runtime.task_runner.impl.TaskRunnerImpl import TaskRunnerImpl
from AgentTaskSystem.agent_runtime.task_runner.interfaces.ExecuteRequestDto import ExecuteRequestDto


def test_execute_task():
    """Test executing a task"""
    task_runner = TaskRunnerImpl()
    request = ExecuteRequestDto(
        task_id="test_task_1",
        params=(1, 2, 3)
    )
    result = task_runner.execute_task(request)
    assert result.success is True
    assert result.task_id == "test_task_1"
    assert "Executed with params" in str(result.result)


def test_cancel_task():
    """Test cancelling a task"""
    task_runner = TaskRunnerImpl()
    task_id = "test_task_2"
    
    # Cancel the task
    cancelled = task_runner.cancel_task(task_id)
    assert cancelled is True
    
    # Try to execute the cancelled task
    request = ExecuteRequestDto(
        task_id=task_id,
        params=(1, 2, 3)
    )
    result = task_runner.execute_task(request)
    assert result.success is False
    assert "Task cancelled" in result.error


def test_get_progress():
    """Test getting task progress"""
    task_runner = TaskRunnerImpl()
    task_id = "test_task_3"
    
    # Initial progress should be 0
    progress = task_runner.get_progress(task_id)
    assert progress.task_id == task_id
    assert progress.progress == 0
    
    # Execute task
    request = ExecuteRequestDto(
        task_id=task_id,
        params=(1, 2, 3)
    )
    task_runner.execute_task(request)
    
    # Progress should be 100 after execution
    progress = task_runner.get_progress(task_id)
    assert progress.progress == 100


def test_execute_multiple_tasks():
    """Test executing multiple tasks"""
    task_runner = TaskRunnerImpl()
    
    request1 = ExecuteRequestDto(
        task_id="task1",
        params=("a", "b")
    )
    request2 = ExecuteRequestDto(
        task_id="task2",
        params=(10, 20)
    )
    
    result1 = task_runner.execute_task(request1)
    result2 = task_runner.execute_task(request2)
    
    assert result1.success is True
    assert result2.success is True
    
    progress1 = task_runner.get_progress("task1")
    progress2 = task_runner.get_progress("task2")
    
    assert progress1.progress == 100
    assert progress2.progress == 100


def test_progress_during_execution():
    """Test progress during execution"""
    task_runner = TaskRunnerImpl()
    task_id = "test_task_4"
    
    # Execute task - progress should go to 50 first, then 100
    request = ExecuteRequestDto(
        task_id=task_id,
        params=(1, 2, 3)
    )
    
    # When execute_task is called, it sets progress to 50 first
    result = task_runner.execute_task(request)
    assert result.success is True
    
    # After completion, progress is 100
    progress = task_runner.get_progress(task_id)
    assert progress.progress == 100
