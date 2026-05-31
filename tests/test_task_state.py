"""
Tests for TaskState module
"""

import pytest
from AgentTaskSystem.task_core.task_state.impl.TaskStateImpl import TaskStateImpl
from AgentTaskSystem.task_core.task_state.interfaces.TaskStateEnum import TaskStateEnum


def test_set_and_get_state():
    """Test setting and getting task state"""
    task_state = TaskStateImpl()
    task_id = "test_task_1"
    
    # Initial state should be PENDING
    state = task_state.get_state(task_id)
    assert state == TaskStateEnum.PENDING
    
    # Set to RUNNING
    transition = task_state.set_state(task_id, TaskStateEnum.RUNNING)
    assert transition.task_id == task_id
    assert transition.from_state == TaskStateEnum.PENDING
    assert transition.to_state == TaskStateEnum.RUNNING
    
    # Verify state
    state = task_state.get_state(task_id)
    assert state == TaskStateEnum.RUNNING


def test_get_state_dto():
    """Test getting state DTO"""
    task_state = TaskStateImpl()
    task_id = "test_task_2"
    
    task_state.set_state(task_id, TaskStateEnum.COMPLETED)
    dto = task_state.get_state_dto(task_id)
    
    assert dto.task_id == task_id
    assert dto.state == TaskStateEnum.COMPLETED
    assert dto.updated_at is not None


def test_multiple_state_transitions():
    """Test multiple state transitions"""
    task_state = TaskStateImpl()
    task_id = "test_task_3"
    
    # Transition 1: PENDING -> RUNNING
    transition1 = task_state.set_state(task_id, TaskStateEnum.RUNNING)
    assert transition1.from_state == TaskStateEnum.PENDING
    assert transition1.to_state == TaskStateEnum.RUNNING
    
    # Transition 2: RUNNING -> COMPLETED
    transition2 = task_state.set_state(task_id, TaskStateEnum.COMPLETED)
    assert transition2.from_state == TaskStateEnum.RUNNING
    assert transition2.to_state == TaskStateEnum.COMPLETED


def test_task_failed_state():
    """Test setting failed state"""
    task_state = TaskStateImpl()
    task_id = "test_task_4"
    
    transition = task_state.set_state(task_id, TaskStateEnum.FAILED)
    assert transition.to_state == TaskStateEnum.FAILED
    assert task_state.get_state(task_id) == TaskStateEnum.FAILED
