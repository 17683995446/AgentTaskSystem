"""
Integration tests for AgentTaskSystem
"""

import pytest
from AgentTaskSystem.agent_runtime.impl.AgentRuntimeImpl import AgentRuntimeImpl
from AgentTaskSystem.common import initialize_services
from AgentTaskSystem.common.Provider import Provider
from AgentTaskSystem.task_core.task_state.interfaces.TaskStateEnum import TaskStateEnum


def test_agent_runtime_full_workflow():
    """Test full workflow of AgentRuntime
    """
    # Initialize services
    provider = initialize_services()
    
    # Get runtime
    runtime = provider.get("agent_runtime")
    
    # Initialize
    assert runtime.is_running() is False
    initialized = runtime.initialize()
    assert initialized is True
    assert runtime.is_running() is True
    
    # Submit a task
    task_id = runtime.submit_task({
        "name": "test_integration_task",
        "params": (1, 2, 3)
    })
    
    assert task_id is not None
    assert len(task_id) > 0
    
    # Get task status
    status = runtime.get_task_status(task_id)
    assert status is not None
    
    # Shutdown
    runtime.shutdown()
    assert runtime.is_running() is False


def test_submit_multiple_tasks():
    """Test submitting multiple tasks
    """
    runtime = AgentRuntimeImpl()
    runtime.initialize()
    
    task_ids = []
    for i in range(5):
        task_id = runtime.submit_task({
            "name": f"task_{i}",
            "params": (i,)
        })
        task_ids.append(task_id)
    
    # Check that all task IDs are unique
    assert len(set(task_ids)) == 5
    
    runtime.shutdown()


def test_service_provider():
    """Test that ServiceProvider functionality
    """
    provider = Provider()
    
    # Clear any existing services
    provider.clear()
    
    # Register a test service
    test_service = {"test": "value"}
    provider.register("test_service", test_service)
    
    # Check that service exists and can be retrieved
    assert provider.has("test_service") is True
    retrieved = provider.get("test_service")
    assert retrieved == test_service
    
    # Check that non-existent service returns None
    assert provider.get("nonexistent") is None


def test_task_state_integration():
    """Test TaskState with AgentRuntime
    """
    runtime = AgentRuntimeImpl()
    runtime.initialize()
    
    task_id = runtime.submit_task({
        "name": "integration_test",
        "params": (1, 2, 3)
    })
    
    # Should be in PENDING state
    status = runtime.get_task_status(task_id)
    assert status is not None
    
    runtime.shutdown()


def test_multiple_runtimes():
    """Test that multiple runtimes work independently
    """
    runtime1 = AgentRuntimeImpl()
    runtime2 = AgentRuntimeImpl()
    
    runtime1.initialize()
    runtime2.initialize()
    
    task_id1 = runtime1.submit_task({"name": "task1", "params": (1,)})
    task_id2 = runtime2.submit_task({"name": "task2", "params": (2,)})
    
    assert task_id1 != task_id2
    
    runtime1.shutdown()
    runtime2.shutdown()
