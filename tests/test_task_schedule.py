"""
Tests for TaskSchedule module
"""

import pytest
from AgentTaskSystem.agent_runtime.task_schedule.impl.TaskScheduleImpl import TaskScheduleImpl
from AgentTaskSystem.agent_runtime.task_schedule.interfaces.SchedulePriority import SchedulePriority
from AgentTaskSystem.agent_runtime.task_schedule.interfaces.ScheduleRequestDto import ScheduleRequestDto


def test_add_task():
    """Test adding a task to schedule"""
    task_schedule = TaskScheduleImpl()
    request = ScheduleRequestDto(
        task_id="test_task_1",
        priority=SchedulePriority.NORMAL,
        scheduled_at=1234567890
    )
    result = task_schedule.add_task(request)
    assert result.success is True


def test_get_next_task():
    """Test getting next task from schedule"""
    task_schedule = TaskScheduleImpl()
    
    # Add tasks
    request1 = ScheduleRequestDto(
        task_id="low_priority",
        priority=SchedulePriority.LOW,
        scheduled_at=1234567890
    )
    request2 = ScheduleRequestDto(
        task_id="high_priority",
        priority=SchedulePriority.HIGH,
        scheduled_at=1234567890
    )
    
    task_schedule.add_task(request1)
    task_schedule.add_task(request2)
    
    # High priority should come first
    next_task = task_schedule.get_next_task()
    assert next_task is not None
    assert next_task.task_id == "high_priority"


def test_get_queue_size():
    """Test getting queue size"""
    task_schedule = TaskScheduleImpl()
    
    assert task_schedule.get_queue_size() == 0
    
    request = ScheduleRequestDto(
        task_id="test_task",
        priority=SchedulePriority.NORMAL,
        scheduled_at=1234567890
    )
    task_schedule.add_task(request)
    
    assert task_schedule.get_queue_size() == 1


def test_priority_order():
    """Test that tasks are ordered by priority"""
    task_schedule = TaskScheduleImpl()
    
    # Add tasks in reverse priority order
    request1 = ScheduleRequestDto(
        task_id="task_low",
        priority=SchedulePriority.LOW,
        scheduled_at=1
    )
    request2 = ScheduleRequestDto(
        task_id="task_normal",
        priority=SchedulePriority.NORMAL,
        scheduled_at=2
    )
    request3 = ScheduleRequestDto(
        task_id="task_high",
        priority=SchedulePriority.HIGH,
        scheduled_at=3
    )
    
    task_schedule.add_task(request1)
    task_schedule.add_task(request2)
    task_schedule.add_task(request3)
    
    # Should get high first, then normal, then low
    task1 = task_schedule.get_next_task()
    assert task1.task_id == "task_high"
    
    task2 = task_schedule.get_next_task()
    assert task2.task_id == "task_normal"
    
    task3 = task_schedule.get_next_task()
    assert task3.task_id == "task_low"


def test_empty_queue_returns_none():
    """Test that empty queue returns None"""
    task_schedule = TaskScheduleImpl()
    assert task_schedule.get_next_task() is None
